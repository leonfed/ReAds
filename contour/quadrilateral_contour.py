import torch
import numpy as np
import matplotlib.pylab as plt
import cv2
import os


# Основной код для вписывания контура в четырехугольник
# Частично взят с https://github.com/Dogiko/Quadrilateral_contour
class QContour():
    def __init__(self, data_points):
        self.data = data_points
        centerlize = self.data - self.data.mean(axis=0)
        self.var, self.pc = np.linalg.eigh(np.dot(centerlize.T, centerlize))
        self.pc_std = np.sqrt(self.var / len(self.data))
        self.normal_data = torch.tensor(np.dot(centerlize, self.pc) / self.pc_std, dtype=torch.float32)

        self.region_bound = torch.nn.Linear(2, 4, bias=True)
        self.region_bound.weight.data = torch.tensor([[1., 0.], [0., 1.], [-1., 0.], [0., -1.]])
        self.region_bound.bias.data = torch.ones(4)

        self.totally_score = torch.nn.Linear(4, 1, bias=True)
        self.totally_score.weight.data = torch.ones(1, 4)
        self.totally_score.bias.data = torch.tensor([-2.])

    def compute(self):
        def forward(x0):
            x1 = torch.sigmoid(self.region_bound(x0))
            x2 = torch.sigmoid(self.totally_score(x1))
            return x2

        params = [self.region_bound.weight, self.region_bound.bias, self.totally_score.bias]
        self.optimizer = torch.optim.Adam(params, lr=1e-2, betas=(0.9, 0.999), weight_decay=0)
        self.criterion = torch.nn.MSELoss()
        for e in range(1000):
            self.optimizer.zero_grad()
            datums = len(self.normal_data)
            extend_input = torch.cat((self.normal_data, 8 * torch.rand((int(0.2 * datums), 2)) - 4), 0)
            extend_label = torch.ones(int(1.2 * datums), 1)
            extend_label[datums:] *= 0
            loss = self.criterion(forward(extend_input), extend_label)
            loss.backward()
            self.optimizer.step()

    def get_vertexes(self):
        output = torch.zeros(4, 2)
        for i in range(-4, 0):
            raw_b = self.region_bound.bias.data[[i, i + 1]]
            b = torch.tensor([[t] for t in raw_b])
            a = -self.region_bound.weight.data[[i, i + 1]]
            x, _ = torch.solve(b, a)

            output[i] = x[:, 0]

        output = output.numpy()
        output = np.dot(output * self.pc_std, self.pc.T) + self.data.mean(axis=0)
        return output


# Вписывание может быть неудачно. В этом случае quad_find возвратит False в ответе
def quad_find(mask_path, result_path):
    print(filename)
    mask = np.load(mask_path)
    result = []

    arr = []
    for i in range(len(mask)):
        for j in range(len(mask[0])):
            if mask[i][j] == True:
                arr.append([j, i])

    sample = np.array(arr)

    foo = QContour(sample)
    foo.compute()
    fooo = foo.get_vertexes()
    result.append(fooo)
    plt.figure(figsize=(8, 8))
    plt.plot(sample[:, 0], sample[:, 1], "bp")
    plt.plot(fooo[[0, 1, 2, 3, 0], 0], fooo[[0, 1, 2, 3, 0], 1])
    plt.show()

    contour = np.array(result[0])

    contour_for_cv2 = contour.copy()
    contour_for_cv2 = np.append(contour_for_cv2, [contour_for_cv2[0]], axis=0)
    contour_for_cv2 = np.vectorize(lambda x: int(x))(contour_for_cv2)

    all_mask_count = 0
    in_counter_count = 0

    for i in range(len(mask)):
        for j in range(len(mask[0])):
            if mask[i][j] == True:
                all_mask_count += 1
            dist = cv2.pointPolygonTest(contour_for_cv2, (j, i), False)
            if dist >= 0.0:
                in_counter_count += 1

    print('All mask count: ' + str(all_mask_count) + "  In counter: " + str(in_counter_count))

    np.save(result_path, contour)

    return all_mask_count > in_counter_count * 0.9


# Определяет рамки баннеров - вписывает маски в четырехугольник
if __name__ == "__main__":
    torch.set_default_tensor_type(torch.FloatTensor)

    mask_path = 'input/'
    result_path = 'output/'

    filenames = os.listdir(mask_path)
    print(filenames)

    for filename in filenames:
        quad_find(mask_path + filename, result_path + filename)