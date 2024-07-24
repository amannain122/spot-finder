#!/bin/bash

# Define the name of the process or script to check
PROCESS_NAME="parking_fares.py"

# Define the full path to your script
SCRIPT_PATH="/home/ubuntu/spot-finder/experimental/pipeline/model-related/parking_fares.py"

LOG_FILE="/home/ubuntu/spot-finder/experimental/pipeline/model-related/logs/parking_fares_status.log"

source /home/ubuntu/spot-finder/venv/bin/activate

python3 "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1 &

deactivate