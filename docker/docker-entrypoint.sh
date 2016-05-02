#!/bin/bash

set -ue

SOCKFILE=/srv/run/gunicorn.sock



python manage.py migrate                  # Apply database migrations
#python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
touch /srv/logs/nginx-access.log
touch /srv/logs/nginx-error.log
touch $SOCKFILE
tail -n 0 -f /srv/logs/*.log &

#Start Nginx

#echo Starting nginx.

# inject the CONTEXT_PATH variable


# for some reason piping output to the original nginx.conf file does not work
envsubst '$CONTEXT_PATH' </etc/nginx/nginx.conf> /etc/nginx/nginx2.conf
cp /etc/nginx/nginx2.conf /etc/nginx/nginx.conf
cp /etc/nginx/nginx.conf /srv/logs/
cp /etc/nginx/nginx2.conf /srv/logs/

exec nginx &

# Start Gunicorn processes
echo Starting Gunicorn.

#exec /sbin/setuser www-data \

exec gunicorn amos.wsgi:application \
    --name amos-6 \
    --bind=0.0.0.0:8000  \
    --workers 3


#     authbind --deep \


