FROM python:3.8

# Additional/nice-to-have software:
#
# - git for cloning in source code
# - iproute2 for network emulation ability
RUN apt-get update && \
    apt-get install -y \
    git \
    iproute2

# Install apt dependencies for running network-stats
RUN apt-get update && \
    apt-get install -y \
    libpcap-dev

# Install python dependencies for running network-stats
RUN pip install \
    impacket \
    pcapy

# Install apt dependencies for web browsing
RUN apt-get update && \
    apt-get install -y \
    firefox-esr

# We'll need geckodriver in order to use selenium
#
# Here we're just finding the download url to the latest pre-compiled release
# for linux64, then downloading and extracting to a location that's part of PATH
RUN export org=mozilla && export repo=geckodriver && \
    export tag=$(curl -s "https://api.github.com/repos/$org/$repo/releases/latest" \
          | grep tag_name \
          | cut -d'"' -f4) && \
    wget -O- "https://github.com/$org/$repo/releases/download/$tag/$repo-$tag-linux64.tar.gz" \
    | tar -xz -C /usr/local/bin

# Install python dependencies for automated web browsing
RUN pip install \
    selenium

# Dependencies for connecting to a VPN
# See: https://www.infradead.org/openconnect/index.html
RUN apt-get install -y openconnect && \
    curl -O https://gitlab.com/openconnect/vpnc-scripts/-/raw/master/vpnc-script && \
    chmod +x ./vpnc-script

# We'll use a pre-build C++ binary from Ookla in order to run a speedtest from
# the command line.
# See: https://www.speedtest.net/apps/cli
RUN apt-get install gnupg1 apt-transport-https dirmngr && \
    export INSTALL_KEY=379CE192D401AB61 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $INSTALL_KEY && \
    echo "deb https://ookla.bintray.com/debian generic main" | tee  /etc/apt/sources.list.d/speedtest.list && \
    apt-get update && \
    apt-get install speedtest

CMD ["sleep", "infinity"]

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.opencontainers.image.created=${BUILD_DATE}
