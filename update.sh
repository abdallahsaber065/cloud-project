#!/bin/bash

# --- Configuration ---
APP_DIR="/home/ubuntu/app"         # Directory where your application code resides
GIT_BRANCH="master"                # The branch you want to pull updates from
SERVICE_NAME="waitress.service"    # The name of your systemd service file

# --- Script Logic ---

# Exit immediately if a command exits with a non-zero status.
set -e

echo ">>> Navigating to application directory: ${APP_DIR}"
cd "${APP_DIR}" || { echo "Error: Could not change directory to ${APP_DIR}"; exit 1; }

echo ">>> Fetching latest changes from remote 'origin'..."
git fetch origin

echo ">>> WARNING: Discarding any local changes and resetting to latest ${GIT_BRANCH} from origin..."
git reset --hard "origin/${GIT_BRANCH}"

echo ">>> Cleaning up untracked files and directories..."
git clean -fd

# Install/update dependencies if requirements change
echo "Checking/installing Python dependencies..."
if [ -f "requirements.txt" ]; then
  ./venv/bin/pip install -r requirements.txt
else
  echo "No requirements.txt found, skipping dependency installation."
fi

# Restart the application service using systemctl
echo "Restarting service '$SERVICE_NAME'..."
sudo systemctl restart "$SERVICE_NAME"

echo ">>> Checking service status..."
sleep 2
sudo systemctl status "$SERVICE_NAME" --no-pager

echo "--- Application Update Finished ---"

exit 0