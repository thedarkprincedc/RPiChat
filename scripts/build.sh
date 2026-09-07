#!/bin/bash

set -e

IMAGE_NAME="pychat"
TAG="latest"

echo "Building $IMAGE_NAME:$TAG..."

docker build \
    -t "$IMAGE_NAME:$TAG" \
    .

echo "Build complete."