#!/bin/bash

# Define the name of the process or script to check
PROCESS_NAME="status_update.py"

# Define the full path to your script
SCRIPT_PATH="/home/ubuntu/spot-finder/main/status_update.py"

LOG_FILE="/home/ubuntu/spot-finder/logs/upload_status.log"

source /home/ubuntu/spot-finder/venv/bin/activate

python3 "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1 &

deactivate
