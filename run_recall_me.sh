#!/bin/bash
set -e
POETRY="/home/bot/.local/bin/poetry"
RECALL_PATH="/home/bot/recall_me"
${POETRY} --directory ${RECALL_PATH} run alembic upgrade head
${POETRY} --directory ${RECALL_PATH} run python3 -m recall_me
