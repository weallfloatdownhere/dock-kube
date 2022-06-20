TAGS=1.0.5
DOCKERIMAGE=dock-kube

DOCKUSERNAME=${DOCKERUSERNAME}
DOCKPASSWD=${DOCKERPASSWORD}
IMAGE_NAME=$(DOCKUSERNAME)/$(DOCKERIMAGE)

push:
	docker login --username="$(DOCKUSERNAME)" --password="$(DOCKPASSWD)"
	DOCKER_BUILDKIT=1 docker build -t $(IMAGE_NAME):$(TAGS) .
	docker push $(IMAGE_NAME):$(TAGS)
	docker tag $(IMAGE_NAME):$(TAGS) $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):latest
