#!/bin/bash

while ! python manage.py flush --no-input 2>&1; do
  echo "Flusing django manage command"
  sleep 3
done

echo "Migrating database..."

python manage.py makemigrations api

while ! python manage.py migrate  2>&1; do
   echo "Migration is in progress..."
   sleep 3
done

echo "Ingesting data in database..."

python setup.py

echo "Data Ingestion Completed"

echo "Django docker is fully configured successfully."

exec "$@"