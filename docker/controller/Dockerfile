FROM alpine:latest

# the iproute2 package lets us use `tc` for network emulation
RUN apk add --update iproute2

CMD ["sleep", "infinity"]

# Metadata
ARG BUILD_DATE
LABEL maintainer="pgaddiso@ucsd.edu"
LABEL org.opencontainers.image.created=${BUILD_DATE}
