#!/bin/bash

# Navigate to the project directory
cd ~/berry-weather || exit

# Pull the latest changes
git pull origin main

# Install any new dependencies
poetry install --no-root

# Restart the application (ensure the systemd service is configured)
#sudo systemctl restart berry-weather.service
