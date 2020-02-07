SHELL=/bin/bash

.PHONY: test
test:
	drone exec --trusted

.PHONY: test-local
test-local:
	docker run --rm -it \
		-v "$(shell pwd)":/tmp/$(shell basename "$(shell pwd)"):ro \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-w /tmp/$(shell basename "$(shell PWD)") \
		--env MOLECULE_NO_LOG=no \
		quay.io/ansible/molecule:2.20 \
		molecule test
