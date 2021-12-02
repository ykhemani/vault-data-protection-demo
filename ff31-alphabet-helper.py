#!/usr/local/bin/python3

import math
import argparse
from EnvDefault import env_default

version = '0.0.1'

parser = argparse.ArgumentParser(
  description = 'Generate an alphabet and indicates whether the plain text sample provided could be encoded using the FF3-1 Format Preserving Encryption algorithm.'
)

parser.add_argument(
  '--c1',
  action=env_default('C1'),
  help='First character of alphabet.',
  required=True
)

parser.add_argument(
  '--c2',
  action=env_default('C2'),
  help='Last character of alphabet.',
  required=True
)

parser.add_argument(
  '--other',
  action=env_default('OTHER'),
  help='Other characters to include in alphabet.',
  required=False
)

parser.add_argument(
  '--plaintext',
  action=env_default('PLAINTEXT'),
  help='A sample of the plaintext to be encoded.',
  required=False
)

parser.add_argument(
  '--version',
  help='Version',
  action='version',
  version=f"{version}"
)

args = parser.parse_args()

def generate_alphabet(c1, c2):
  """Generates an alphabet from `c1` to `c2`, inclusive."""
  alphabet = str()
  for c in range(ord(c1), ord(c2)+1):
    yield chr(c)


alphabet_as_list = list(generate_alphabet(args.c1, args.c2))
#alphabet = ''.join(generate_alphabet(args.c1, args.c2))

if args.other:
  for c in args.other:
    if c not in alphabet_as_list:
      alphabet_as_list.append(c)

alphabet = ''.join(alphabet_as_list)
length_alphabet = len(alphabet)
length_input_max = 2 * math.floor(math.log(math.pow(2,96),length_alphabet))

print ("Alphabet has {} characters:".format(length_alphabet))
print ("------------------------------------------------------------------------")
print (alphabet)
print ("------------------------------------------------------------------------")
print ("Maximum length of plain text to encode is {}".format(length_input_max))

if args.plaintext:
  plaintext_chunks = []
  plaintext_is_valid = True
  for c in args.plaintext:
    if c not in alphabet_as_list:
      print("\"{}\" in plaintext value not found in list.".format(c))
      plaintext_is_valid = False
  length_plaintext = len(args.plaintext)
  if length_plaintext >= 2 and math.pow(length_alphabet,length_plaintext) >= 1000000 and length_plaintext <= length_input_max:
    plaintext_length_is_valid = True
  else:
    plaintext_length_is_valid = False
  if length_plaintext > length_input_max:
    for i in range(0, length_plaintext, length_input_max):
      plaintext_chunks.append(args.plaintext[i : i + length_input_max])

  print ("Plain text sample length is {}".format(length_plaintext))
  print ("Plain text sample provided is \"{}\"".format(args.plaintext))
  print ("Plain text sample contains valid characters: {}".format(plaintext_is_valid))
  print ("Plain text sample length is valid: {}".format(plaintext_length_is_valid))
  if len(plaintext_chunks):
    print ("Split the plain text sample for encoding as follows:")
    for chunk in plaintext_chunks:
      print ("  \"{}\"".format(chunk))
