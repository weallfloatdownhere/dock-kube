APP?=argo-demo
PORT?=8080

clean:
	rm -f ${APP}

build: clean
	go build -o ${APP}

run: build
	PORT=${PORT} ./${APP}

test:
	go test -v -race ./...

dockerbuild:
	docker build -t retersi/argo-demo:v$(VERSION) .

dockerpush: dockerbuild
	docker push retersi/argo-demo:v$(VERSION)


deploy: 
	kubectl apply -f ./manifests/config-secret.yaml 
	kubectl apply -f ./manifests/argo-demo.yaml 
	
secret:
	kubectl create secret generic config-data --from-file=$(CFGPATH) --dry-run=client -o yaml > ./manifests/config-secret.yaml