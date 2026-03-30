FROM mediawiki:1.41

# Install Postgres PHP client and psql CLI for the entrypoint
RUN apt-get update && apt-get install -y \
    postgresql-client \
    php-pgsql \
    && docker-php-ext-enable pgsql \
    && rm -rf /var/lib/apt/lists/*

# Copy our env-driven LocalSettings and entrypoint
COPY LocalSettings.php /mediawiki-config/LocalSettings.php
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
