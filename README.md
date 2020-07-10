![ansible-lint](https://github.com/hostwithquantum/ansible-loki/workflows/ansible-lint/badge.svg) ![flake8](https://github.com/hostwithquantum/ansible-loki/workflows/flake8/badge.svg) ![yaml-lint](https://github.com/hostwithquantum/ansible-loki/workflows/yaml-lint/badge.svg) ![molecule](https://github.com/hostwithquantum/ansible-loki/workflows/molecule/badge.svg)

# ansible-loki

An Ansible role to install loki and promtail.

Requirements
------------

 - `unzip` on the manager host

Role Variables
--------------

See `defaults/main.yml` to customize this role.

Dependencies
------------

_None._

Example Playbook
----------------

This role is driven by inventory groups:

```
all:
  hosts:
    monitoring.host.example.org:
  children:
    loki:
      monitoring.host.example.org:
    promtail:
      monitoring.host.example.org:
```

And the playbook:

```
- hosts: all
  roles:
    - { role: hostwithquantum.loki }
```

License
-------

BSD-2-Clause

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
