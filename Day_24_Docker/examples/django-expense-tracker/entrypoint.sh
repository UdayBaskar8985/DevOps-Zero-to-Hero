#!/bin/sh

echo "Waiting for postgres database..."

# Use inline python to poll psycopg2 connection
python << END
import sys
import time
import psycopg2
import os

db_name = os.environ.get("DB_NAME", "expense_tracker")
db_user = os.environ.get("DB_USER", "postgres")
db_password = os.environ.get("DB_PASSWORD", "postgres")
db_host = os.environ.get("DB_HOST", "db")
db_port = os.environ.get("DB_PORT", "5432")

while True:
    try:
        psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        break
    except psycopg2.OperationalError as e:
        print("Database not ready yet, waiting 1s...")
        time.sleep(1)
END

echo "PostgreSQL database is online!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute command passed to entrypoint (e.g. gunicorn or runserver)
exec "$@"
