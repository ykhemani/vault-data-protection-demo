#!/usr/local/bin/python3

import random
import hvac
import base64
from os import environ
import sys

# to handle self-signed or otherwise unverifiable certs
import urllib3
urllib3.disable_warnings()
vault_ssl_verify=False

card_types = { 'visa' : 400000 } # IIN
card_delimiter = ' '
ccs = {}

vault_client = hvac.Client(
  url = environ['VAULT_ADDR'],
  token = environ['VAULT_TOKEN'],
  verify=vault_ssl_verify
)

def base64ify(bytes_or_str):
  """Helper method to perform base64 encoding across Python 2.7 and Python 3.X"""
  if sys.version_info[0] >= 3 and isinstance(bytes_or_str, str):
    input_bytes = bytes_or_str.encode('utf8')
  else:
    input_bytes = bytes_or_str

  output_bytes = base64.urlsafe_b64encode(input_bytes)
  if sys.version_info[0] >= 3:
    return output_bytes.decode('ascii')
  else:
    return output_bytes

# transit mount, key and context
vault_transit_mount   = 'transit-demo'
vault_transit_key     = 'vault-demo-key'
vault_transit_context = base64ify('CZHDam4tkahEGekHKNZ0HNTla7heoJDmRy')
print ("context is " + vault_transit_context)

# transform fpe mount, role and transformation
vault_fpe_mount          = 'transform-demo'
vault_fpe_role           = 'vault-fpe-role'
vault_fpe_transformation = 'card-number'

# transform tokenization mount, role and transformation
vault_tokenize_mount          = 'tokenization-demo'
vault_tokenize_role           = 'vault-tokenize-role'
vault_tokenize_transformation = 'credit-card'

def transit_encrypt(plaintext):
  global vault_client
  global vault_transit_context
  global vault_transit_key
  global vault_transit_mount
  encrypt_data_response = vault_client.secrets.transit.encrypt_data(
      mount_point = vault_transit_mount,
      name = vault_transit_key,
      context = vault_transit_context,
      plaintext = base64ify(plaintext.encode())
  )
  return encrypt_data_response['data']['ciphertext']

def transit_decrypt(ciphertext):
  global vault_client
  global vault_transit_context
  global vault_transit_key
  global vault_transit_mount
  decrypt_data_response = vault_client.secrets.transit.decrypt_data(
      mount_point = vault_transit_mount,
      name = vault_transit_key,
      context = vault_transit_context,
      ciphertext = ciphertext
  )
  return str(base64.b64decode(decrypt_data_response['data']['plaintext']), "utf-8")

def transform_encode(
  plaintext, 
  vault_transform_mount, 
  vault_transform_role, 
  vault_transformation_name
):
  global vault_client
  encode_response = vault_client.secrets.transform.encode(
    mount_point    = vault_transform_mount,
    role_name      = vault_transform_role,
    value          = plaintext,
    transformation = vault_transformation_name,
  )
  return encode_response['data']['encoded_value'] # fpe or token

def transform_decode(
  fpe, 
  vault_transform_mount, 
  vault_transform_role, 
  vault_transformation_name
):
  global vault_client
  
  decode_response = vault_client.secrets.transform.decode(
    mount_point = vault_transform_mount,
    role_name = vault_transform_role,
    value = fpe,
    transformation = vault_transformation_name,
  )
  return decode_response['data']['decoded_value']

def luhn(first_6):
  global card_delimiter
  card_no = [int(i) for i in str(first_6)]  # To find the checksum digit on
  card_num = [int(i) for i in str(first_6)]  # Actual account number
  seventh_15 = random.sample(range(9), 9)  # Acc no (9 digits)
  for i in seventh_15:
    card_no.append(i)
    card_num.append(i)
  for t in range(0, 15, 2):  # odd position digits
    card_no[t] = card_no[t] * 2
  for i in range(len(card_no)):
    if card_no[i] > 9:  # deduct 9 from numbers greater than 9
      card_no[i] -= 9
  s = sum(card_no)
  mod = s % 10
  check_sum = 0 if mod == 0 else (10 - mod)
  card_num.append(check_sum)
  card_num = [str(i) for i in card_num]

  formatted_card_num = ''.join(card_num)
  if card_delimiter != '':
    formatted_card_num = card_delimiter.join(formatted_card_num[i: i + 4] for i in range(0, len(formatted_card_num), 4) )
  #return ''.join(card_num)
  return formatted_card_num

def generate_card():
  card = luhn(card_types["visa"])
  content = {'card': card, 'ciphertext': 'None', 'fpe': 'None', 'token': 'None'}
  return card, content

def test():
  global vault_fpe_mount
  global vault_fpe_role
  global vault_fpe_transformation
  
  global vault_tokenize_mount
  global vault_tokenize_role
  global vault_tokenize_transformation
  
  test_card = luhn(card_types["visa"])

  test_ciphertext = transit_encrypt(test_card)

  test_decrypt = transit_decrypt(test_ciphertext)

  test_fpe_encode = transform_encode(
    test_card, 
    vault_fpe_mount, 
    vault_fpe_role,
    vault_fpe_transformation,
  )

  test_token_encode = transform_encode(
    test_card,
    vault_tokenize_mount, 
    vault_tokenize_role, 
    vault_tokenize_transformation,
  )

  test_fpe_decode = transform_decode(
    test_fpe_encode,
    vault_fpe_mount, 
    vault_fpe_role,
    vault_fpe_transformation,
  )

  test_token_decode = transform_decode(
    test_token_encode,
    vault_tokenize_mount, 
    vault_tokenize_role, 
    vault_tokenize_transformation,
  )
  
  print ("Test results:")
  print ("  test card:                   " + test_card         + "\n")
  print ("  test transform fpe encode:   " + test_fpe_encode         )
  print ("  test transform fpe decode:   " + test_fpe_decode   + "\n")
  print ("  test transform token encode: " + test_token_encode       )
  print ("  test transform token decode: " + test_token_decode + "\n")
  print ("  test transit encrypt:        " + test_ciphertext         )
  print ("  test transit decrypt:        " + test_decrypt      + "\n")

test()
