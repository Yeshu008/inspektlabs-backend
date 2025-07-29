#!/bin/sh

host="db"
port=3306

echo "Waiting for MySQL at $host:$port..."

while ! nc -z "$host" "$port"; do
  echo "MySQL is unavailable - sleeping"
  sleep 2
done

echo "MySQL is up!"
