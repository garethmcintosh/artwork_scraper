#!/bin/bash

# Set the path to the artwork folder (modify if needed)
ARTWORK_FOLDER="$(cd "$(dirname "$0")" && pwd)/artwork"
echo $ARTWORK_FOLDER
# Check if the artwork folder exists
if [ ! -d "$ARTWORK_FOLDER" ]; then
    echo "Artwork folder not found: $ARTWORK_FOLDER"
    exit 1
fi

# Get a random image from the artwork folder
RANDOM_IMAGE=$(find "$ARTWORK_FOLDER" -type f | shuf -n 1)

# Check if a random image was found
if [ -z "$RANDOM_IMAGE" ]; then
    echo "No images found in the artwork folder."
    exit 1
fi

SCREEN_RESOLUTION="1920x1080"

# Generate a unique filename for the resized image
RESIZED_IMAGE="/tmp/resized_image_$(date +%s).png"

# Resize image to fit screen
convert "$RANDOM_IMAGE" -resize "$SCREEN_RESOLUTION>" "$RESIZED_IMAGE" 

# Get the color of first pixel in the image
BG_COLOR=$(convert "$RESIZED_IMAGE"  -format "%[pixel:p{0,0}]" info:)

# Set background color of tmp image
convert -size "$SCREEN_RESOLUTION" "xc:$BG_COLOR" /tmp/bg_color.png

convert /tmp/bg_color.png "$RESIZED_IMAGE" -gravity center -composite "$RESIZED_IMAGE"

# Set the desktop background for kde plasma
plasma-apply-wallpaperimage "$RESIZED_IMAGE"

rm /tmp/bg_color.png

exit 0
