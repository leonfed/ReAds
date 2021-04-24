from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

path = 'data/full.mp4'
start_time_seconds = 5
end_time_seconds = 12

# для ускорения
# ffmpeg -y -i full.mp4 -vf "setpts=0.75*PTS" -r 24 speeded.mp4

# обрезать
# ffmpeg -ss <начало> -t <продолжительность> -i in1.avi out1.avi

# для разбития про фреймам
# ffmpeg -i file.mp4 -vf fps=1 %d.jpg

# для зацикливания
# ffmpeg -f concat -i for_merge.txt -c copy final_loop.mp4

ffmpeg_extract_subclip(path, start_time_seconds, end_time_seconds, targetname="data/original.mp4")

