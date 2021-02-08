# Router
# ======
#
# The router serves as the connection between the client containers and the
# external internet. We'll run network emulation inside of the router (iproute2)
# and the router needs to be able to re-route packets (iptables).
#
# This must be run with cap-add NET_ADMIN or neither iptables nor tc will be
# permitted.
# 

# FROM alpine:latest
FROM python:3.8-alpine

RUN apk add --update iproute2 iptables
RUN pip install \
    tcconfig

CMD ["sleep", "infinity"]

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.opencontainers.image.created=${BUILD_DATE}
