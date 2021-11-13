#!/bin/bash

export VAULT_ADDR=${VAULT_ADDR:-https://127.0.0.1:8200}
export VAULT_INIT_KEYS=${VAULT_INIT_KEYS:-/vault/vault_init_keys}
export VAULTRC=${VAULTRC:-/vault/vaultrc}
export VAULT=${VAULT:-/bin/vault}

echo "Waiting for $VAULT_ADDR/v1/sys/health to return 501 (not initialized)."
vault_http_return_code=0
while [ "$vault_http_return_code" != "501" ]
do
  vault_http_return_code=$(curl --insecure -s -o /dev/null -w "%{http_code}" $VAULT_ADDR/v1/sys/health)
  sleep 1
done

echo "Initializing Vault"
curl \
  --insecure \
  -s \
  --header "X-Vault-Request: true" \
  --request PUT \
  --data '{"secret_shares":1,"secret_threshold":1}' $VAULT_ADDR/v1/sys/init \
  > ${VAULT_INIT_KEYS}

export VAULT_TOKEN=$(cat ${VAULT_INIT_KEYS} | jq -r '.root_token')
export UNSEAL_KEY=$(cat ${VAULT_INIT_KEYS} | jq -r .keys[])

echo "Writing vaultrc ${VAULTRC}"
cat << EOF > ${VAULTRC}
#!/bin/bash

export VAULT_TOKEN=${VAULT_TOKEN}
export VAULT_ADDR=${VAULT_ADDR}
export VAULT_SKIP_VERIFY=true
export UNSEAL_KEY=${UNSEAL_KEY}
EOF

# unseal
echo "Waiting for ${VAULT_ADDR}/v1/sys/health to return 503 (sealed)."
vault_http_return_code=0
while [ "$vault_http_return_code" != "503" ]
do
  vault_http_return_code=$(curl --insecure -s -o /dev/null -w "%{http_code}" $VAULT_ADDR/v1/sys/health)
  sleep 1
done

echo "Unsealing Vault"
curl \
  -s \
  --insecure \
  --request PUT \
  --data "{\"key\": \"${UNSEAL_KEY}\"}" \
  ${VAULT_ADDR}/v1/sys/unseal | jq -r .

echo "Waiting for ${VAULT_ADDR}/v1/sys/health to return 200 (initialized, unsealed, active)."
vault_http_return_code=0
while [ "$vault_http_return_code" != "200" ]
do
  vault_http_return_code=$(curl --insecure -s -o /dev/null -w "%{http_code}" $VAULT_ADDR/v1/sys/health)
  sleep 1
done

echo "Vault is now initialized, unsealed and active."

curl --insecure -s $VAULT_ADDR/v1/sys/health | jq

echo "All done."

exit 0
