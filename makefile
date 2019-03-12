DOCKER_REGISTRY := mathematiguy
IMAGE_NAME := $(shell basename `git rev-parse --show-toplevel`)
IMAGE := $(DOCKER_REGISTRY)/$(IMAGE_NAME)
GIT_TAG ?= $(shell git log --oneline | head -n1 | awk '{print $$1}')
RUN ?= docker run $(INTERACT) --rm -v $$(pwd):/work -w /work -u $(UID):$(GID) $(IMAGE)
UID ?= $(shell id -u)
GID ?= $(shell id -g)

crawl: 
	cd papakilo && $(RUN) scrapy crawl nupepa

.PHONY: docker
docker:
	docker build --tag $(IMAGE):$(GIT_TAG) .
	docker tag $(IMAGE):$(GIT_TAG) $(IMAGE):latest
	docker push $(IMAGE):$(GIT_TAG)

.PHONY: docker-push
docker-push:
	docker push $(IMAGE):$(GIT_TAG)

.PHONY: enter
enter: INTERACT=-it
enter:
	$(RUN) bash

clean_slides:
	rm -f *.html

clean_babynames:
	rm -f babynames/babynames.csv
