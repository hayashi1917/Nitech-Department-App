#!/bin/sh
set -e

echo "=== Checking database state ==="
if [ ! -d "/code/migrations" ]; then
    echo "=== Initializing database ==="
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
else
    echo "=== Recreating migrations ==="
    rm -rf /code/migrations/*
    flask db init
    flask db migrate -m "Reset migration"
    flask db upgrade
fi

echo "=== Starting Flask application ==="
exec "$@"


