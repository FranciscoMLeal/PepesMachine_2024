#!/bin/zsh

# Start the first Python program in the background
python twin_drawer.py &

# Start the second Python program in the background
python twincloud_window.py &

# Start the third Python program in the background
python Color_Slider.py &

# Optional: Wait for all background processes to finish
wait
