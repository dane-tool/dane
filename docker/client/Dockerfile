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

# Install python dependencies for running network-stats, and include speedtest
# capability for labeling the file
RUN pip install \
    impacket \
    pcapy \
    speedtest-cli

RUN git clone https://github.com/viasat/network-stats

# Install apt dependencies for web browsing
RUN apt-get update && \
    apt-get install -y \
    firefox-esr

# We'll need geckodriver in order to use selenium
#
# Here we're just finding the download url to the latest pre-compiled release
# for linux64, then downloading and extracting to a location that's part of PATH
RUN curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep browser_download_url \
    | grep 'linux64.tar.gz"' \
    | cut -d '"' -f 4 \
    | wget -i - -O /dev/stdout \
    | tar -xz -C /usr/local/bin/

# Install python dependencies for automated web browsing
RUN pip install \
    selenium

#* VPN-RELATED SOFTWARE
RUN apt-get install -y openconnect && \
    curl -O https://git.infradead.org/users/dwmw2/vpnc-scripts.git/blob_plain/HEAD:/vpnc-script

# ADD scripts/init/client.sh /
# RUN chmod +x /client.sh
# ENTRYPOINT ["/client.sh"]
CMD ["sleep", "infinity"]

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.opencontainers.image.created=${BUILD_DATE}
