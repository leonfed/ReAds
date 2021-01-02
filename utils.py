def rgb2hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def hex2rgb(rgb):
    h = rgb.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))