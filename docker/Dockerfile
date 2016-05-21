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
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/django

ENV SOCKFILE=/srv/run/gunicorn.sock

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade

# install needed software
RUN apt-get install -y python python-pip python-dev python-pandas nginx sqlite3
# install libblas-dev
RUN apt-get install -y libatlas-base-dev

#Getting key for Postgres
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
#RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list


#Install or Update PostgresSQL 9.3
#RUN apt-get update && apt-get -y -q install python-software-properties software-properties-common \
#    && apt-get -y -q install postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs run DataProcessing
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Copy nginx configuration
COPY ./nginx.conf /etc/nginx/
#Copy Client to src/static
COPY ./Client /srv/static/
#Copy DataProcessing to srv/DataProcessing
COPY ./DataProcessing /srv/DataProcessing
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

# TODO: CREATE DB-PASSWORD IN TRAVIS-CI AND USE THIS ONE BELOW INSTEAD OF pguser PWD

# Setup Postgres
# Switching to User Postgres
#USER postgres
# Start Postgres
#RUN /etc/init.d/postgresql start \
#    && psql --command "CREATE USER pguser WITH SUPERUSER PASSWORD 'pguser';" \
#    && createdb -O pguser pgdb

# Switching to root and finish configuration of Postgres
# TODO: Change Configuration: Not every application should be able to access the db
##USER root
#RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
#RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# Port Postgres is listening
#EXPOSE 5432

# Creating folders for postgres
#RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql
#VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

#Switching back to postgres and Define the Start
#USER postgres
#CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]


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
