#!/bin/bash

#соединить несколько видео в одно
ffmpeg -f concat -i for_merge.txt -c copy final_loop.mp4
