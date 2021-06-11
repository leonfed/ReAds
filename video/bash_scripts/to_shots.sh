#!/bin/bash

#разбить видео на кадры
ffmpeg -i full.mp4 -vf fps=24 result/%d.jpg
