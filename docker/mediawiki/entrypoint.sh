#!/bin/bash
# mediawiki-entrypoint.sh
# Waits for Postgres, creates the mediawiki DB if needed, installs MediaWiki,
# then hands off to the standard Apache entrypoint.

set -e

POSTGRES_HOST="${POSTGRES_HOST:-postgres}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
POSTGRES_USER="${POSTGRES_USER:-galdr}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-CHANGE_ME_postgres}"
MEDIAWIKI_DB_NAME="${MEDIAWIKI_DB_NAME:-mediawiki}"
MEDIAWIKI_DB_PREFIX="${MEDIAWIKI_DB_PREFIX:-mw_}"

MEDIAWIKI_SITE_NAME="${MEDIAWIKI_SITE_NAME:-galdr Knowledge Base}"
MEDIAWIKI_SERVER="${MEDIAWIKI_SERVER:-http://localhost:8880}"
MEDIAWIKI_ADMIN_USER="${MEDIAWIKI_ADMIN_USER:-WikiAdmin}"
MEDIAWIKI_ADMIN_PASSWORD="${MEDIAWIKI_ADMIN_PASSWORD:-CHANGE_ME}"
MEDIAWIKI_ADMIN_EMAIL="${MEDIAWIKI_ADMIN_EMAIL:-admin@localhost}"

echo "[mediawiki-entrypoint] Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" \
      -U "$POSTGRES_USER" -c '\q' 2>/dev/null; do
  sleep 2
done
echo "[mediawiki-entrypoint] Postgres is ready."

# Create the mediawiki database if it doesn't exist
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" \
  -U "$POSTGRES_USER" -tc \
  "SELECT 1 FROM pg_database WHERE datname='${MEDIAWIKI_DB_NAME}'" \
  | grep -q 1 || \
  PGPASSWORD="$POSTGRES_PASSWORD" createdb -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" \
    -U "$POSTGRES_USER" "${MEDIAWIKI_DB_NAME}"
echo "[mediawiki-entrypoint] Database '${MEDIAWIKI_DB_NAME}' ready."

# Copy LocalSettings.php into place
cp /mediawiki-config/LocalSettings.php /var/www/html/LocalSettings.php

# Run installer if not already installed (check for a core table)
INSTALLED=$(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" \
  -U "$POSTGRES_USER" -d "$MEDIAWIKI_DB_NAME" -tc \
  "SELECT to_regclass('${MEDIAWIKI_DB_PREFIX}user')" 2>/dev/null | tr -d '[:space:]')

if [ "$INSTALLED" = "${MEDIAWIKI_DB_PREFIX}user" ]; then
  echo "[mediawiki-entrypoint] Already installed, skipping install script."
else
  echo "[mediawiki-entrypoint] Running MediaWiki installer (non-interactive)..."
  php /var/www/html/maintenance/install.php \
    --dbtype=postgres \
    --dbserver="${POSTGRES_HOST}:${POSTGRES_PORT}" \
    --dbname="${MEDIAWIKI_DB_NAME}" \
    --dbuser="${POSTGRES_USER}" \
    --dbpass="${POSTGRES_PASSWORD}" \
    --dbprefix="${MEDIAWIKI_DB_PREFIX}" \
    --server="${MEDIAWIKI_SERVER}" \
    --scriptpath="" \
    --lang=en \
    --pass="${MEDIAWIKI_ADMIN_PASSWORD}" \
    "${MEDIAWIKI_SITE_NAME}" \
    "${MEDIAWIKI_ADMIN_USER}"
  echo "[mediawiki-entrypoint] Install complete."
fi

# Hand off to the official MediaWiki entrypoint
exec docker-php-entrypoint apache2-foreground "$@"
