#!/bin/bash

set -ue

SOCKFILE=/srv/run/gunicorn.sock


# Postgresql startup: temporarily removed
# echo Starting postgresq

# touch /srv/logs/postgresql.log
# exec su postgres -c 'pg_ctl start -D /var/lib/postgresql/9.3/main -l /srv/logs/postgresql.log'
# exec sudo su - postgres && /usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf


echo apply django migrations

python manage.py makemigrations helloWorld
python manage.py migrate --noinput                 # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# run init script
chmod u+x /srv/DataProcessing/Scripts/initSimulation.sh
# open sub-shell, change the directory, and execute - needed since the called python scripts use relative paths
( cd /srv/DataProcessing/Scripts; sh ./initSimulation.sh )

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
touch /srv/logs/nginx-access.log
touch /srv/logs/nginx-error.log

touch $SOCKFILE
tail -n 0 -f /srv/logs/*.log &



#echo Starting nginx.

# inject the CONTEXT_PATH variable


# for some reason piping output to the original nginx.conf file does not work
envsubst '$CONTEXT_PATH' </etc/nginx/nginx.conf> /etc/nginx/nginx2.conf
cp /etc/nginx/nginx2.conf /etc/nginx/nginx.conf
#cp /etc/nginx/nginx.conf /srv/logs/
#cp /etc/nginx/nginx2.conf /srv/logs/

#Start Nginx

exec nginx &



# Start Gunicorn processes
echo Starting Gunicorn.

#exec /sbin/setuser www-data \

exec gunicorn amos.wsgi:application \
    --name amos-6 \
    --bind=0.0.0.0:8000  \
    --workers 3 


#     authbind --deep \


