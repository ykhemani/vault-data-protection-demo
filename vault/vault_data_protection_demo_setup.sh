#!/bin/bash

export VAULT=${VAULT:-/bin/vault}

if [ -f "/vault/vaultrc" ]
then
  . /vault/vaultrc
else
  echo "ERROR: File /vault/vaultrc not found. Cannot proceed."
  exit 1
fi

########################################################################
# Enable secrets engines and roles for demo
########################################################################
# Transit
echo "Configuring Transit Convergent Encryption"
export TRANSIT_MOUNT=${TRANSIT_MOUNT:-transit-demo}
export TRANSIT_KEY=${TRANSIT_KEY:-vault-demo-key}
${VAULT} secrets disable ${TRANSIT_MOUNT}
${VAULT} secrets enable -path=${TRANSIT_MOUNT} transit
${VAULT} write ${TRANSIT_MOUNT}/keys/${TRANSIT_KEY} \
  type=aes256-gcm96 \
  convergent_encryption=true \
  derived=true

########################################################################
# Transform FPE
echo "Configuring Transform FPE"
export TRANSFORM_MOUNT=${TRANSFORM_MOUNT:-transform-demo}
export TRANSFORM_ROLE=${TRANSFORM_ROLE:-vault-fpe-role}
export TRANSFORM_ENCODE_POLICY=${TRANSFORM_ENCODE_POLICY:-vault-demo-transform-encode}
export TRANSFORM_DECODE_POLICY=${TRANSFORM_DECODE_POLICY:-vault-demo-transform-decode}

${VAULT} secrets disable ${TRANSFORM_MOUNT}
${VAULT} secrets enable -path=${TRANSFORM_MOUNT} transform
${VAULT} write ${TRANSFORM_MOUNT}/role/${TRANSFORM_ROLE} transformations=card-number
${VAULT} list ${TRANSFORM_MOUNT}/role

${VAULT} write ${TRANSFORM_MOUNT}/transformations/fpe/card-number \
  template="builtin/creditcardnumber" \
  tweak_source=internal \
  allowed_roles=${TRANSFORM_ROLE}

#${VAULT} list ${TRANSFORM_MOUNT}/transformations/fpe

#${VAULT} read ${TRANSFORM_MOUNT}/transformations/fpe/card-number

${VAULT} policy write ${TRANSFORM_ENCODE_POLICY} -<<EOF
# To request data encoding using any of the roles
# Specify the role name in the path to narrow down the scope
path "${TRANSFORM_MOUNT}/encode/${TRANSFORM_ROLE}" {
   capabilities = [ "update" ]
}
EOF

${VAULT} policy write ${TRANSFORM_DECODE_POLICY} -<<EOF
# To request data decoding using any of the roles
# Specify the role name in the path to narrow down the scope
path "${TRANSFORM_MOUNT}/decode/${TRANSFORM_ROLE}" {
   capabilities = [ "update" ]
}
EOF

########################################################################
# Tokenization
echo "Configuring Transform Tokenization"
export TOKENIZATION_MOUNT=${TOKENIZATION_MOUNT:-tokenization-demo}
export TOKENIZATION_ROLE=${TOKENIZATION_ROLE:-vault-tokenize-role}
export TOKENIZATION_CC_TRANSFORMATION=${TOKENIZATION_CC_TRANSFORMATION:-credit-card}
export TOKENIZATION_ENCODE_POLICY=${TOKENIZATION_ENCODE_POLICY:-vault-demo-tokenize-encode}
export TOKENIZATION_DECODE_POLICY=${TOKENIZATION_DECODE_POLICY:-vault-demo-tokenize-decode}

${VAULT} secrets disable ${TOKENIZATION_MOUNT}
${VAULT} secrets enable -path=${TOKENIZATION_MOUNT} transform

${VAULT} write ${TOKENIZATION_MOUNT}/role/${TOKENIZATION_ROLE} \
  transformations=${TOKENIZATION_CC_TRANSFORMATION}

${VAULT} write \
  ${TOKENIZATION_MOUNT}/transformations/tokenization/${TOKENIZATION_CC_TRANSFORMATION} \
  allowed_roles=${TOKENIZATION_ROLE}

echo "All done."

exit 0

