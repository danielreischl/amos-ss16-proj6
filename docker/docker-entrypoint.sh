#!/bin/bash

set -ue

SOCKFILE=/srv/run/gunicorn.sock

# Sets up Django
echo apply django migrations

# Migrates app dataInterface
python manage.py makemigrations dataInterface
# Applies database migrations
python manage.py migrate --noinput
# Collects static files
python manage.py collectstatic --noinput

# Copy files that are not on GitHub from persistent directory to directory where the initScript is looking for them
# deactivated until issues are resolved
# cp /persistent/*.csv /srv/DataProcessing/InitialData/
# copy to /srv/static for testing instead
cp /persistent/*.csv /srv/static/

# Runs init script
chmod u+x /srv/DataProcessing/initDataProcessingSimulation.sh
# Opens sub-shell, change the directory, and execute - needed since the called python scripts use relative paths
( cd /srv/DataProcessing/; sh ./initDataProcessingSimulation.sh )

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
touch /srv/logs/nginx-access.log
touch /srv/logs/nginx-error.log

touch $SOCKFILE
tail -n 0 -f /srv/logs/*.log &

# echo Starting nginx.
# inject the $CONTEXT_PATH variable into nginx - configfile
# $CONTEXT_PATH is injected by the OSR-servers and is either /ss16/proj6-test or /ss16/proj6

sed -i s:\$CONTEXT_PATH:$CONTEXT_PATH: /etc/nginx/nginx.conf

# for debugging
#cp /etc/nginx/nginx.conf /srv/logs/

#Start Nginx
exec nginx &

# Starts Gunicorn
echo Starting Gunicorn.

#exec /sbin/setuser www-data \

exec gunicorn amos.wsgi:application \
    --name amos-6 \
    --bind=0.0.0.0:8000  \
    --workers 3 

#     authbind --deep \
