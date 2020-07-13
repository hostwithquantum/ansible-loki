SHELL=/bin/bash

IMAGE:=quay.io/ansible/molecule:3.0.4
ANSIBLE_ROLE:=ansible-loki
OPTS?=--all

.PHONY: test-local
test-local:
	docker run --rm -it \
		-v "$(CURDIR)":/tmp/$(ANSIBLE_ROLE):ro \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-w /tmp/$(ANSIBLE_ROLE) \
		--env MOLECULE_NO_LOG=no \
		$(IMAGE) \
		molecule test $(OPTS)
