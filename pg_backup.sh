set -e

POSTGRES_DSN="${POSTGRES_DSN:-postgresql://recallme:recallme@127.0.0.1:5432/recallme}"

pg_dump --column-inserts --data-only ${POSTGRES_DSN} > backup_$(date +'%d_%m_%Y').sql
