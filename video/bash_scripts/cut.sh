#!/bin/bash

# ffmpeg -ss <начало> -t <продолжительность> -i in1.avi out1.avi
ffmpeg -ss 0 -t 100 -i input.mp4 output.mp4
