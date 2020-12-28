tag ?= latest
service ?= daemon

start:
	docker-compose \
	-p netem -f docker/docker-compose.yml \
	up

build:
# Build all required images.
	docker build \
	-f docker/controller/Dockerfile \
	--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
	-t netem-controller:$(tag) .

	docker build \
	-f docker/client/Dockerfile \
	--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
	-t netem-client:$(tag) .

	docker build \
	-f docker/daemon/Dockerfile \
	--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
	-t netem-daemon:$(tag) .

exec:
# Exec into a shell for a given service.
	docker-compose \
	-p netem -f docker/docker-compose.yml \
	exec $(service) sh

delay:
#! TEMPORARY -- just for demonstration purposes
	docker exec -it netem_daemon_1 \
		docker run -it -d --rm --cap-add NET_ADMIN --net container:netem_client_1 \
		netem-controller \
		tc qdisc add dev eth0 root netem delay 300ms
