# DANE Composer
# =================
#
# This container will be responsible for creating the Docker Compose file which
# will set up all containers needed to run the data collection tool.
#
# Will run `build_compose.py`:
# > This script builds the Docker Compose file used to launch all containers
#   needed by the tool, with proper volume mounts, environment variables, and
#   labels for behaviors and network conditions as specified in the config.
#
# Since Compose files are written with a YAML file format, PyYAML is required.
#
# NOTE: It is assumed that this container will be mounted to the root directory
# from which it is being run.
#

FROM python:3.8-alpine

RUN pip install pyyaml

WORKDIR /home

CMD ["sleep", "infinity"]

# Metadata
ARG BUILD_DATE
LABEL maintainer="https://github.com/parkeraddison"
LABEL org.opencontainers.image.created=${BUILD_DATE}
