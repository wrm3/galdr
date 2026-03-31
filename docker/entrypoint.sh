#!/bin/bash
set -e

DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_USER="${POSTGRES_USER:-knowledge_base}"
DB_NAME="${POSTGRES_DB:-knowledge_base}"

export PGPASSWORD="${POSTGRES_PASSWORD:-knowledge_base}"

table_count=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tAc \
  "SELECT count(*) FROM pg_tables WHERE schemaname='public';" 2>/dev/null || echo "0")

if [ "$table_count" -lt 5 ]; then
  echo "galdr: DB schema missing or incomplete ($table_count tables). Running init scripts..."
  for f in /app/init_db/*.sql; do
    echo "  Running $(basename "$f")..."
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$f" 2>&1 | tail -1
  done
  echo "galdr: DB init complete."
else
  echo "galdr: DB schema OK ($table_count tables)."
fi

unset PGPASSWORD

exec python -m galdr.server
