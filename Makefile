SHELL := /bin/bash
PROJECT_NAME := $(shell basename $$(pwd))
LISTEN_PORT := $(shell sed -nr 's/ARG SERVICE_PORT=([0-9]+)/\1/p' Dockerfile)

.PHONY: clean-pycache
clean-pycache:
	find . -name "__pycache__" -exec rm -r {} \;

# Targets to test/format code - these should be run from inside the dev container
.PHONY: format
format:
	black .

.PHONY: lint
lint:
	pylint -j0 app

.PHONY: test
test:
	pytest -v --showlocals

.PHONY: presubmit
presubmit: format lint test

# Targets to build/run containers - these must be run from the host, outside the container
.PHONY: image
image:
	docker image build --pull --target service-container  --tag $(PROJECT_NAME) .

.PHONY: dev-image
dev-image:
	docker image build --pull --target dev-container  --tag $(PROJECT_NAME)-dev .

.PHONY: run
run: image
	docker container run --rm -it --privileged --pid=host \
		--name $(PROJECT_NAME) \
		-p $(LISTEN_PORT):$(LISTEN_PORT) \
		-v $$(pwd):/work \
		-w /work/app \
		$(PROJECT_NAME) \
		--app-dir /work --log-config /work/app/logconfig.json --reload
