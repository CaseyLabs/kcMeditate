.PHONY: build test run stop clean serve serve-sw

IMAGE_NAME ?= kcmeditate
CONTAINER_NAME ?= kcmeditate-app
PORT ?= 8000
HOST_PORT ?= $(PORT)
DOCKER_RUN = docker run --rm --user $(shell id -u):$(shell id -g) -v "$(CURDIR)":/app -w /app

build:
	docker build -t $(IMAGE_NAME) .

test:
	$(DOCKER_RUN) python:3.14.3-slim python scripts/validate_assets.py

run: build stop
	docker run -d --name $(CONTAINER_NAME) --user $(shell id -u):$(shell id -g) -p $(HOST_PORT):8000 -v "$(CURDIR)":/app -w /app $(IMAGE_NAME)
	@printf 'App URL: http://127.0.0.1:%s\n' '$(HOST_PORT)'

stop:
	-docker rm -f $(CONTAINER_NAME)

clean: stop
	-docker rmi $(IMAGE_NAME)

serve: run

serve-sw: run
