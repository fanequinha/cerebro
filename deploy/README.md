# Deploy commander, datamgr and mastermind

**You must add your public key to the host**

## Provision in production:

Add system dependencies for compiling Python 3 as well as some packages for
Ansible deployment.

```
$ ansible-playbook -i inventories/production/hosts provision.yml
```

## Deploy in production:

```
$ ansible-playbook -i inventories/production/hosts deploy.yml
```