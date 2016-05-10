############################################################
# Dockerfile to run a Django-based web application
# Based on an Amos Web Service Base Image
############################################################

# Set the base image to use to Ubuntu
FROM osrgroup/amos-web-service-base-image:1.0 

MAINTAINER AMOS-TEAM-6


# Set env variables used in this Dockerfile
# Local directory with project source
ENV DOCKYARD_SRC=django
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/django

ENV SOCKFILE=/srv/run/gunicorn.sock

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip nginx gettext

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs run
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

COPY ./nginx.conf /etc/nginx/
COPY ./Client/* /srv/static
# COPY ./index.html /srv/static/index.html

# turn daemon mode off, otherwise nginx quits and docker container also
RUN echo "daemon off;" >> /etc/nginx/nginx.conf


RUN touch /srv/logs/nginx-access.log
RUN touch /srv/logs/nginx-error.log
RUN touch $SOCKFILE

# Install Python dependencies
RUN pip install -r $DOCKYARD_SRVPROJ/requirements.txt

# Port to expose
EXPOSE 80


# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
