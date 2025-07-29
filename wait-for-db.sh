#!/bin/sh
set -e

HOST="${DB_HOST:-db}"
PORT="${DB_PORT:-3306}"

echo "Waiting for MySQL at $HOST:$PORT..."

while ! nc -z "$HOST" "$PORT"; do
  echo "MySQL is unavailable - sleeping"
  sleep 1
done

echo "MySQL is up!"
