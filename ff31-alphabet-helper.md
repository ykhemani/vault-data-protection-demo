# ff31-alphabet-helper

The [ff31-alphabet-helper.py](ff31-alphabet-helper.py) script:
* generates an alphabet starting with character `c1` and ending with character `c2`
* determines whether the sample plain text value that would be encoded using FF3-1 Format Preserving Encryption and the alphabet that is generated is valid.

## Usage

```
$ ./ff31-alphabet-helper.py -h
usage: ff31-alphabet-helper.py [-h] --c1 C1 --c2 C2 [--other OTHER]
                               [--plaintext PLAINTEXT] [--version]

Generate an alphabet and indicates whether the plain text sample provided could be
encoded using the FF3-1 Format Preserving Encryption algorithm.

optional arguments:
  -h, --help            show this help message and exit
  --c1 C1               First character of alphabet.
  --c2 C2               Last character of alphabet.
  --other OTHER         Other characters to include in alphabet.
  --plaintext PLAINTEXT
                        A sample of the plaintext to be encoded.
  --version             Version
```

## Examples

```
$ ./ff31-alphabet-helper.py --c1 0 --c2 z --other " " --plaintext "Yash Khemani"
Alphabet has 76 characters:
------------------------------------------------------------------------
0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz 
------------------------------------------------------------------------
Maximum length of plain text to encode is 30
Plain text sample length is 12
Plain text sample provided is "Yash Khemani"
Plain text sample contains valid characters: True
Plain text sample length is valid: True
```

```
$ ./ff31-alphabet-helper.py --c1 0 --c2 9 --plaintext "4000005267038413"
Alphabet has 10 characters:
------------------------------------------------------------------------
0123456789
------------------------------------------------------------------------
Maximum length of plain text to encode is 56
Plain text sample length is 16
Plain text sample provided is "4000005267038413"
Plain text sample contains valid characters: True
Plain text sample length is valid: True
```

```
$ ./ff31-alphabet-helper.py --c1 0 --c2 9 --other " -" --plaintext "5643 1147 8018 7280"
Alphabet has 12 characters:
------------------------------------------------------------------------
0123456789 -
------------------------------------------------------------------------
Maximum length of plain text to encode is 52
Plain text sample length is 19
Plain text sample provided is "5643 1147 8018 7280"
Plain text sample contains valid characters: True
Plain text sample length is valid: True
```

```
$ ./ff31-alphabet-helper.py --c1 0 --c2 z --other "åß" --plaintext "Yash Khemœni"
Alphabet has 77 characters:
------------------------------------------------------------------------
0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyzåß
------------------------------------------------------------------------
Maximum length of plain text to encode is 30
" " in plaintext value not found in list.
"œ" in plaintext value not found in list.
Plain text sample length is 12
Plain text sample provided is "Yash Khemœni"
Plain text sample contains valid characters: False
Plain text sample length is valid: True
```

```
$ ./ff31-alphabet-helper.py --c1 a --c2 z --other "åßœ "
Alphabet has 30 characters:
------------------------------------------------------------------------
abcdefghijklmnopqrstuvwxyzåßœ 
------------------------------------------------------------------------
Maximum length of plain text to encode is 38
```
