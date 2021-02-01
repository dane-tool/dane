# FROM alpine:latest
FROM python:3.8-alpine

# The main purpose of this daemon is to launch containers connected to the
# network of other containers in order to alter their network conditions.
RUN apk add docker
RUN pip install docker

# We also utilize this container during setup (building the compose file), so it
# helps to have the PyYAML package installed
RUN pip install pyyaml

CMD ["sleep", "infinity"]

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.opencontainers.image.created=${BUILD_DATE}
