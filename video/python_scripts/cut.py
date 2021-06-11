from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# обрезать видео
if __name__ == "__main__":
    path = '../data/full.mp4'
    start_time_seconds = 5
    end_time_seconds = 12

    ffmpeg_extract_subclip(path, start_time_seconds, end_time_seconds, targetname="../data/original.mp4")
