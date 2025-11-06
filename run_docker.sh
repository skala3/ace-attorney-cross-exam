#!/bin/bash
# Script to run Ace Attorney game in Docker with GPU support

# Build the image
echo "Building Docker image..."
docker build -t ace_attorney_llm .

# Run with GPU support
echo "Starting game with GPU support..."
docker run --rm -it \
    --gpus all \
    -v $(pwd)/outputs:/app/outputs \
    ace_attorney_llm "$@"
