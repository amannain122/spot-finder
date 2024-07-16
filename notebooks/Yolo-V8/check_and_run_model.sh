#!/bin/bash

# Define the name of the process or script to check
PROCESS_NAME="6.0-CSV_coords.py"

# Define the full path to your script
SCRIPT_PATH="/home/ubuntu/spot-finder/notebooks/Yolo-V8/6.0-CSV_coords.py"

# Check if the process is running
if ! pgrep -f "$PROCESS_NAME" > /dev/null
then
    echo "$(date): $PROCESS_NAME not running, starting it now..." >> /home/ubuntu/spot-finder/notebooks/Yolo-V8/logs/script_running.log
    nohup $SCRIPT_PATH &
else
    echo "$(date): $PROCESS_NAME is already running." >> /home/ubuntu/spot-finder/notebooks/Yolo-V8/logs/script_running.log
fi
