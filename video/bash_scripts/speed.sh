#!/bin/bash

ffmpeg -y -i full.mp4 -vf "setpts=0.75*PTS" -r 24 speeded.mp4
