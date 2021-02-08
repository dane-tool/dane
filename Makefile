
.PHONY: start run up
d ?= 
start run up: init raw
# Start up all of the containers defined in our docker compose yaml. If Linux or
# MacOS is being used then the unix override will be applied so that the traffic
# control is able to work!
#
# The if filter expression is simply a way to check if the client os (as seen by
# docker) is linux or darwin

.PHONY: raw
raw:
# Start up all containers using an already created compose file.
	docker-compose \
	-p netem -f built/docker-compose.yml \
	$(if \
		$(filter $(shell docker version -f {{.Client.Os}}),linux darwin),\
		-f docker/compose/docker-compose.unix.yml,\
		\
	) \
	up \
	$(if $(d),-d,)

.PHONY: stop interrupt
name ?= netem_daemon_1
stop interrupt:
# Send a SIGINT signal to a container, defaulting to the daemon.
	docker kill --signal SIGINT $(name)

.PHONY: down
down:
	docker-compose \
	-p netem -f built/docker-compose.yml \
	down \
	--remove-orphans

.PHONY: init
tool_dir ?= 
config_file ?= 
init:
# Build the compose file from given configuration in config.py
	docker run \
	--rm \
	-v "$(PWD):/home" \
	netem-init \
	python setup/build_compose.py \
	$(if $(tool_dir),--src $(tool_dir),) \
	$(if $(config_file),-config $(config_file),)

.PHONY: build
tag ?= latest
only ?= all
build:
# Build all (or only some) images.
ifeq ($(only),all)
	docker build \
	-f docker/controller/Dockerfile \
	--build-arg BUILD_DATE="$(shell date --rfc-3339 seconds)" \
	-t netem-controller:$(tag) .

	docker build \
	-f docker/client/Dockerfile \
	--build-arg BUILD_DATE="$(shell date --rfc-3339 seconds)" \
	-t netem-client:$(tag) .

	docker build \
	-f docker/daemon/Dockerfile \
	--build-arg BUILD_DATE="$(shell date --rfc-3339 seconds)" \
	-t netem-daemon:$(tag) .

	docker build \
	-f docker/router/Dockerfile \
	--build-arg BUILD_DATE="$(shell date --rfc-3339 seconds)" \
	-t netem-router:$(tag) .

	docker build \
	-f Dockerfile \
	--build-arg BUILD_DATE="$(shell date --rfc-3339 seconds)" \
	-t netem-init:$(tag) .

else ifeq ($(only),init)
	docker build \
	-f Dockerfile \
	--build-arg BUILD_DATE="$(shell date --rfc-3339 seconds)" \
	-t netem-init:$(tag) .
else
	docker build \
	-f docker/$(only)/Dockerfile \
	--build-arg BUILD_DATE="$(shell date --rfc-3339 seconds)" \
	-t netem-$(only):$(tag) .
endif

.PHONY: clean
clean: stop
# Make sure everything is stopped and remove all built images
	docker rmi netem-controller
	docker rmi netem-client
	docker rmi netem-daemon
	docker rmi netem-router
	docker rmi netem-init

.PHONY: exec
service ?= daemon
command ?= sh
exec:
# Exec into a shell for a given service.
	docker-compose \
	-p netem -f built/docker-compose.yml \
	exec $(service) $(command)

.PHONY: sh
sh:
# Run a daemon shell mounted to the project directory
	docker run -it --rm \
	-v $(CURDIR):/network-data-generation \
	-e DOCKER_HOST=tcp://host.docker.internal:2375 \
	netem-daemon sh

.PHONY: delay
delay:
#! TEMPORARY -- just for demonstration purposes
	docker exec -it netem_daemon_1 \
		docker run -it -d --rm --cap-add NET_ADMIN --net container:netem_client_1 \
		netem-controller \
		tc qdisc add dev eth0 root netem delay 300ms

.PHONY: daemon-delay
daemon-delay:
#! TEMPORARY -- acts like the daemon spawning a traffic controller for client_1
	docker run -i --rm \
	-e DOCKER_HOST=tcp://host.docker.internal:2375 \
	-v $(CURDIR)/scripts:/scripts \
	netem-daemon \
	sh < scripts/daemon.sh
