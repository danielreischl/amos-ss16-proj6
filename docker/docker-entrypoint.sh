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
chmod u+x /srv/DataProcessing/initSimulation.sh
# open sub-shell, change the directory, and execute - needed since the called python scripts use relative paths
( cd /srv/DataProcessing/; sh ./initSimulation.sh )

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
touch /srv/logs/nginx-access.log
touch /srv/logs/nginx-error.log

touch $SOCKFILE
tail -n 0 -f /srv/logs/*.log &



#echo Starting nginx.

# inject the $CONTEXT_PATH variable into nginx - configfile
# $CONTEXT_PATH is injected by the OSR-servers and is either /ss16/proj6-test or /ss16/proj6

sed -i s:\$CONTEXT_PATH:$CONTEXT_PATH: /etc/nginx/nginx.conf

# for debugging
#cp /etc/nginx/nginx.conf /srv/logs/


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


