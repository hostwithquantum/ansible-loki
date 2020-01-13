# ansible-loki

An Ansible role to install loki and promtail.

Requirements
------------

 - `unzip` on the manager host

Role Variables
--------------

See `defaults/main.yml` to customize this role.

In addition, please set "roles" in your inventory:

```
all:
  hosts:
    server
  children:
    loki:
      hosts:
        server
    promtail:
      hosts:
        server
```

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

    - hosts: all
      roles:
         - { role: ansible-loki }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
