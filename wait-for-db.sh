#!/bin/sh

echo "Waiting for MySQL to be ready..."

until nc -z "$MYSQL_HOST" 3306; do
  echo "MySQL is unavailable - sleeping"
  sleep 1
done

echo "MySQL is up - executing tests"
exec "$@"
