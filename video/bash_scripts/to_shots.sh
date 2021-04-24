#!/bin/bash

ffmpeg -i full.mp4 -vf fps=24 result/%d.jpg
