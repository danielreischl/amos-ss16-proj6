###########################################################
# Dockerfile to run a Django-based web application
# Based on an Amos Web Service Base Image
############################################################

# Set the base image to use to Ubuntu
FROM osrgroup/amos-web-service-base-image:1.0 

#Define the Maintainer of the Image
MAINTAINER AMOS-TEAM-6

# Set env variables used in this Dockerfile
# Local directory with project source
ENV DOCKYARD_SRC=django
# Directory in docker container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in docker container for django related files
ENV DOCKYARD_SRVPROJ=/srv/django

ENV SOCKFILE=/srv/run/gunicorn.sock

# Updates the default application repository sources list
RUN apt-get update && apt-get -y upgrade

# Installs needed software:
# python, python-pip, python-pandas, nginx, sqlite3 libatlas-base-dev nodejs
RUN apt-get install -y python python-pip python-pandas nginx sqlite3 libatlas-base-dev nodejs

# Creates application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static Tests logs run DataProcessing DataProcessing/InitialData DataProcessing/CarrierData DataProcessing/CarrierDataArchive DataProcessing/InitialDataArchive
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Copies nginx configuration
COPY ./nginx.conf /etc/nginx/
# Copies Client to src/static
COPY ./Client /srv/static/
# Copies DataProcessing to srv/DataProcessing
COPY ./DataProcessing /srv/DataProcessing
# Copies Tests to /srv/Tests
COPY ./Tests /srv/Tests

# Turns daemon mode off, otherwise nginx quits and docker container also
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# TODO: Comment what it does
RUN touch /srv/logs/nginx-access.log
RUN touch /srv/logs/nginx-error.log
RUN touch $SOCKFILE

# Installs Bower
RUN npm install -g bower

# Installs Python dependencies
# Django 1.9.5, Gunicorn 19.3.0, SQL Alchemy, django-bower
RUN pip install Django==1.9.5 gunicorn==19.3.0 SQLAlchemy django-bower

# Exposes port 80
EXPOSE 80

# Copies entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./docker-entrypoint.sh /

# Sets up Django
# Migrates app dataInterface
RUN python manage.py makemigrations dataInterface
# Applies database migrations
RUN python manage.py migrate --noinput
# Installs bower libraries
RUN python manage.py bower_install -- --allow-root  --no-input
# Collects static files
RUN python manage.py collectstatic --noinput

# Runs UnitTests
RUN python /srv/DataProcessing/test_dataProcessing.py -v
RUN python /srv/Tests/test_JavaScriptLibraries.py -v

ENTRYPOINT ["/docker-entrypoint.sh"]

# Switches User to root
USER root