###########################################################
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

# install needed software
RUN apt-get install -y python python-pip python-dev python-pandas nginx sqlite3 gettext
# install libblas-dev
RUN apt-get install -y libatlas-base-dev


# the following packages will be needed for postgresql
# postgresql-9.3 postgresql-contrib-9.3 postgres-xc libpq-dev  


# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs run DataProcessig
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Copy nginx configuration
COPY ./nginx.conf /etc/nginx/
#Copy Client to src/static
COPY ./Client /srv/static/
#Copy DataProcessing Scripts to srv/DataProcessing
RUN cp -r ./DataProcessing/Scripts /srv/DataProcessing
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

# setup postgres
# removed until problems are solved, uncomment later
# TODO: CREATE DB-PASSWORD IN TRAVIS-CI AND USE THIS ONE BELOW INSTEAD OF DOCKER PWD

# USER postgres
# RUN    /etc/init.d/postgresql start &&\
#    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
#    createdb -O docker docker

# RUN echo "host all  all    127.0.0.1/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
# COPY ./pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
# RUN echo "listen_addresses= 'localhost'" >> /etc/postgresql/9.3/main/postgresql.conf

# COPY ./postgresql.conf /etc/postgresql/9.3/main/postgresql.conf

# Expose the PostgreSQL port
# EXPOSE 5432

# Set the default command to run when starting the container
# CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

USER root