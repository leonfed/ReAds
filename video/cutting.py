from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

path = '/home/fedleonid/Study/diploma/video/20210314_152822.mp4'
path = '/home/fedleonid/Study/diploma/video/road.mp4'

start_time_seconds = 7 * 60 + 12
end_time_seconds = 7 * 60 + 18

ffmpeg_extract_subclip(path, start_time_seconds, end_time_seconds, targetname="data/test.mp4")
