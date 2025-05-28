#!/bin/bash
mkdir -p static
docker-compose exec web poetry run python manage.py collectstatic --noinput 