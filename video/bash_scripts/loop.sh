#!/bin/bash

ffmpeg -f concat -i for_merge.txt -c copy final_loop.mp4
