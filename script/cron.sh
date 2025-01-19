#!/bin/bash

# This script will add a cron job to run the Python script periodically.

# Path to your Python script
SCRIPT_PATH="index.py"

# Path to the python executable (make sure it's correct for your environment)
PYTHON_PATH="/usr/bin/python3"

# Cron job schedule: every 6 hours
CRON_SCHEDULE="0 */6 * * *"

# Add the cron job (make sure the job does not already exist)
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $PYTHON_PATH $SCRIPT_PATH") | crontab -

# Verify the cron job has been added
crontab -l
