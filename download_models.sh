#!/bin/bash
# Script to download YOLOv4-Tiny model files (optional)

MODELS_DIR="models"
mkdir -p "$MODELS_DIR"

echo "Downloading YOLOv4-Tiny model files..."
echo "Note: These files are large (~20MB for weights file)"

# Download YOLOv4-Tiny configuration
echo "Downloading yolov4-tiny.cfg..."
curl -L -o "$MODELS_DIR/yolov4-tiny.cfg" \
  "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg"

# Download YOLOv4-Tiny weights
echo "Downloading yolov4-tiny.weights..."
curl -L -o "$MODELS_DIR/yolov4-tiny.weights" \
  "https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov4-tiny.weights"

# Download COCO class names
echo "Downloading coco.names..."
curl -L -o "$MODELS_DIR/coco.names" \
  "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"

echo "Download complete!"
echo "Model files are now in the $MODELS_DIR directory"

