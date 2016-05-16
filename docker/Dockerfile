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

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]