#!/bin/bash

# Define the name of the process or script to check
PROCESS_NAME="spotfinder-aws.py"

# Define the full path to your script
SCRIPT_PATH="/home/ubuntu/spot-finder/notebooks/Yolo-V8/spotfinder-aws.py"

LOG_FILE="/home/ubuntu/spot-finder/notebooks/Yolo-V8/logs/script_running.log"

source /home/ubuntu/spot-finder/venv/bin/activate

if ! pgrep -f "$PROCESS_NAME" > /dev/null; then
       	echo "$(date): $PROCESS_NAME not running, starting it now..." >> "$LOG_FILE"
	  # Start the script in the background with nohup
   	 nohup python3 "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1 &
else
        echo "$(date): $PROCESS_NAME is already running." >> "$LOG_FILE"
fi

deactivate
