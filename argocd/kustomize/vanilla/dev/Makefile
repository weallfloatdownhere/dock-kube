TENV=$(shell basename -- `pwd`)

install:
	kubectl apply -k .
	echo $(TENV)

remove:
	kubectl delete -k ./cluster/$(TENV) --force