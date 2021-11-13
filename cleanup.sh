#!/bin/bash

docker-compose down

rm -rfv \
  vault/raft/* \
  vault/file/* \
  vault/logs/* \
  postgres/data/* \
  openldap/etc/ldap/slap.d/* \
  openldap/var/lib/ldap/*

> vault/vaultrc
> vault/vault_init_keys
