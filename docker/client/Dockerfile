FROM python:3.8

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.opencontainers.image.created=${BUILD_DATE}

# Install apt dependencies for running network-stats
RUN apt-get update && \
    apt-get install -y \
    libpcap-dev

# Install python dependencies for running network-stats
RUN pip install \
    impacket \
    pcapy

# Will probably add browsing related software here
#
# RUN ...

# Additional/nice-to-have software:
#
# - git for cloning in source code
# - iproute2 for network emulation ability
RUN apt-get install -y \
    git \
    iproute2

RUN git clone https://github.com/viasat/network-stats

CMD sleep infinity
