#!/bin/bash
# Launch script for Reachy Mini dance demo with proper GStreamer paths

# Set up library paths for GStreamer on macOS
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export GI_TYPELIB_PATH="/opt/homebrew/lib/girepository-1.0"
export GST_PLUGIN_PATH="/opt/homebrew/lib/gstreamer-1.0"

# Activate the virtual environment
source ~/Documents/Workspace/reachy_mini/reachy_mini_env/bin/activate

# Run the dance demo
python dance_demo.py
