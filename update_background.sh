#!/bin/bash

ARTWORK_FOLDER="$(cd "$(dirname "$0")" && pwd)/artwork"
echo $ARTWORK_FOLDER

if [ ! -d "$ARTWORK_FOLDER" ]; then
    echo "Artwork folder not found: $ARTWORK_FOLDER"
    exit 1
fi

RANDOM_IMAGE=$(find "$ARTWORK_FOLDER" -type f | shuf -n 1)

if [ -z "$RANDOM_IMAGE" ]; then
    echo "No images found in the artwork folder."
    exit 1
fi

SCREEN_RESOLUTION="1920x1080"

RESIZED_IMAGE="/tmp/resized_image_$(date +%s).png"

convert "$RANDOM_IMAGE" -resize "$SCREEN_RESOLUTION>" "$RESIZED_IMAGE" 

BG_COLOR=$(convert "$RESIZED_IMAGE"  -format "%[pixel:p{0,0}]" info:)

convert -size "$SCREEN_RESOLUTION" "xc:$BG_COLOR" /tmp/bg_color.png

convert /tmp/bg_color.png "$RESIZED_IMAGE" -gravity center -composite "$RESIZED_IMAGE"

plasma-apply-wallpaperimage "$RESIZED_IMAGE"

rm /tmp/bg_color.png

exit 0
