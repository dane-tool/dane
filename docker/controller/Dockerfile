FROM alpine:latest

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=${BUILD_DATE}

# the iproute2 package lets us use `tc` for network emulation
RUN apk add --update iproute2

CMD sleep infinity
