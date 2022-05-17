IMAGENAME=dock-kube
TAGS=latest
DOCKUSER="${DOCKERUSERNAME}"
DOCKPASSWD="${DOCKERPASSWORD}"

define dockclean
	docker system prune -f || true 
	docker rm -vf $(docker ps -a -q) || true 
	docker rmi -f $(docker images -a -q) || true 
	docker system prune -f || true
endef

define dockbuild
	docker login --username=$(DOCKUSER) --password=$(DOCKPASSWD)
	DOCKER_BUILDKIT=1 docker build -t "$(DOCKUSER)/$(IMAGENAME):$(TAGS)" .
endef

define dockpush
	docker push "$(DOCKUSER)/$(IMAGENAME):$(TAGS)"
endef


build:
	$(call dockbuild)

push:
	$(call dockpush)

deploy:
	$(call dockclean)
	$(call dockbuild)
	$(call dockpush)