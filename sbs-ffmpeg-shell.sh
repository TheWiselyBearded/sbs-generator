#!/bin/bash

# hevc_nvenc

clipDelay=$3
factor3D=20
factorTimeOffset=$clipDelay
encoder=libx264 
bitRate=15M
minBitRate=15M
maxBitRate=15M
bufferSize=512K

# Extract the width and height of the video automatically.
# Comment this section and set videoW and videoH explicitly if needed.
dimensions=$(ffprobe -hide_banner -show_streams "$1" 2>/dev/null | grep "^width\|^height")
eval "$dimensions"

ResW=$((videoW + videoW / factor3D))
videoH=$((videoH + videoH / factor3D))
CropW=$((ResW - videoW))


ffmpeg -i "$1" -vf "scale=$ResW:$videoH,crop=$videoW:$videoH:0:0" -c:v "$encoder" -b:v "$bitRate" -minrate "$minBitRate" -maxrate "$maxBitRate" -bufsize "$bufferSize" -c:a aac -ss "$factorTimeOffset" right_eye.mp4


ffmpeg -i "$1" -vf "scale=$ResW:$videoH,crop=$videoW:$videoH:$CropW:0" -c:v "$encoder" -b:v "$bitRate" -minrate "$minBitRate" -maxrate "$maxBitRate" -bufsize "$bufferSize" -c:a aac left_eye.mp4


# ffmpeg -i left_eye.mp4 -vf "movie=right_eye.mp4 [in1]; [in]pad=iw*2:ih:iw:0[in0]; [in0][in1] overlay=0:0 [out]" -c:v %encoder% -b:v %bitRate% -minrate %minBitRate% -maxrate %maxBitRate% -bufsize %bufferSize% %2.SBS.mp4
# ffmpeg -i left_eye.mp4 -vf "movie=right_eye.mp4 [in1]; [in]pad=iw*2:ih:iw:0[in0]; [in0][in1] overlay=0:0 [out]" -c:v "$encoder" -b:v "$bitRate" -minrate "$minBitRate" -maxrate "$maxBitRate" -bufsize "$bufferSize" "./$2.SBS.mp4"
ffmpeg -i left_eye.mp4 -vf "movie=right_eye.mp4 [in1]; [in]pad=iw*2:ih:iw:0[in0]; [in0][in1] overlay=0:0 [out]" -c:v "$encoder" -b:v "$bitRate" -minrate "$minBitRate" -maxrate "$maxBitRate" -bufsize "$bufferSize" "output.SBS.mp4"

