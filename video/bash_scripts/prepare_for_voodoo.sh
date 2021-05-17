#!/bin/bash

file="$1"
output_dir="$2"

cat $file | grep -E "^([0-9.-]+\s+){3}$" > "$output_dir/3d_points.tsv"
cat $file | grep -E "^([0-9.-]+\s+){28}$" > "$output_dir/frames_params.tsv"
