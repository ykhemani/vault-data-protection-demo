storage "raft" {
  path    = "/vault/raft"
  node_id = "vault"
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = "false"
  tls_key_file    = "/vault/certs/privkey.pem"
  tls_cert_file   = "/vault/certs/fullchain.pem"
  tls_min_version = "tls12"
}

cluster_addr          = "https://127.0.0.1:8201"
api_addr              = "https://127.0.0.1:8200"

disable_mlock         = "false"
disable_cache         = "false"
ui                    = "true"

max_lease_ttl         = "24h"
default_lease_ttl     = "1h"

#raw_storage_endpoint = true

cluster_name          = "mac-vault"

insecure_tls          = "false"

plugin_directory      = "/vault/plugins"
