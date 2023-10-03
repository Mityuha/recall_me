#!/bin/bash
set -e
source ${HOME}/.bashrc
echo "Executing cron..."
poetry run python3 -m cron > last_notify.log
echo "Notifications were done."
