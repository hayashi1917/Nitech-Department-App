#!/bin/sh
set -e  # エラーがあれば即終了

echo "=== Checking migrations directory ==="
if [ ! -d "/code/migrations" ]; then
  echo "No migrations folder found. Initializing..."
  flask db init
  flask db migrate -m "Initial migration"
fi

echo "=== Upgrading database ==="
flask db upgrade

echo "=== Starting Flask application ==="
exec "$@"


