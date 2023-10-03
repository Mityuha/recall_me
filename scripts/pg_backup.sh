#!/bin/bash
set -e

POSTGRES_DSN="${POSTGRES_DSN:-postgresql://recallme:recallme@127.0.0.1:5432/recallme}"
PG_DUMP="/usr/bin/pg_dump"
BACKUP_PATH="/home/bot/recall_me/backups"

mkdir -p ${BACKUP_PATH}
${PG_DUMP} --column-inserts --data-only ${POSTGRES_DSN} > ${BACKUP_PATH}/backup_$(date +'%d_%m_%Y').sql
