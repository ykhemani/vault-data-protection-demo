#!/bin/bash

export VAULT=${VAULT:-/bin/vault}
export VAULT_AUDIT=${VAULT_AUDIT:-/vault/logs/vault_audit.log}
export VAULT_AUDIT_RAW=${VAULT_AUDIT_RAW:-/vault/logs/vault_audit_raw.log}

if [ -f "/vault/vaultrc" ]
then
  . /vault/vaultrc
else
  echo "ERROR: File /vault/vaultrc not found. Cannot proceed."
  exit 1
fi

########################################################################
# Enable audit log
echo "Enable audit device ${VAULT_AUDIT}."
${VAULT} audit enable \
  file \
  file_path=${VAULT_AUDIT}

echo "Enable raw audit device ${VAULT_AUDIT_RAW}."
${VAULT} audit enable \
  -path=raw file \
  file_path=${VAULT_AUDIT_RAW} \
  log_raw=true

echo ""

${VAULT} audit list -detailed

echo ""
echo "All done."

exit 0

