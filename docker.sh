#!/bin/bash
python manage.py migrate --noinput                # Apply database migrations
python manage.py collectstatic --clear --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
mkdir /src/
mkdir /src/logs/
touch /src/logs/gunicorn.log
touch /src/logs/access.log
touch /src/logs/celery.log
tail -n 0 -f /src/logs/*.log &

# Test if PORT is set or set it. Comment
if [ -z "${PORT:-}" ]; then export PORT="8000"; fi


# Start Gunicorn processes with workers
echo Starting Gunicorn.
exec gunicorn \
   --bind 0.0.0.0:$PORT \
   --workers 3 \
   --worker-class gevent \
   --log-level=info \
   --log-file=/src/logs/gunicorn.log \
   --access-logfile=/src/logs/access.log \
   --name feleexpress --reload feleexpress.wsgi:application \
   --chdir feleexpress/
