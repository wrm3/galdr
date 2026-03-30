#!/bin/bash
# Grant CREATEDB to POSTGRES_USER so MediaWiki (or manual createdb) can create the mediawiki DB.
# Uses container env POSTGRES_USER (from docker-compose / .env).
set -e
if [ -z "$POSTGRES_USER" ]; then
  echo "10_mediawiki_db: POSTGRES_USER not set, skipping."
  exit 0
fi
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -c "ALTER USER \"$POSTGRES_USER\" CREATEDB;"
