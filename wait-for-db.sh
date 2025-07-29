#!/bin/sh

echo "⏳ Waiting for MySQL to be ready..."

until mysql -h db -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1;" "$MYSQL_DATABASE"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 2
done

echo "✅ MySQL is up - continuing..."
