FROM alpine:latest

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=${BUILD_DATE}

# The main purpose of this daemon is to launch containers connected to the
# network of other containers in order to alter their network conditions.
RUN apk add docker

CMD sleep infinity
