#!/bin/bash

# Set the path to the artwork folder (modify if needed)
ARTWORK_FOLDER="/artwork"

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

# Set the desktop background using feh
feh --bg-fill "$RANDOM_IMAGE"

exit 0
