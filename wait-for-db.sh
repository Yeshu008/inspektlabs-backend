#!/bin/sh

MYSQL_HOST="${MYSQL_HOST:-db}"  # default to 'db' if not set
MYSQL_PORT="${MYSQL_PORT:-3306}"

echo "Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."

until nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
  echo "MySQL is unavailable - sleeping"
  sleep 1
done

echo "MySQL is up - continuing..."
exec "$@"
