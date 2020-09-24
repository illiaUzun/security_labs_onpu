# Lab1. Vigenere Cipher and Letter Frequency Analysis:
Before commands execution please ensure you exported your PYTHONPATH:

export PYTHONPATH='{root-project-dir}'

## Encode:
#### String:
python3 encode.py --key {key-pass} --input {string-to-encode}
#### File:
python3 encode_file.py --key {key-pass} --input {path-to-file} --output {path-to-file}

## Decode:
#### String:
python3 decode.py --key {key-pass} --input {string-to-encode}
#### File:
python3 decode_file.py --key {key-pass} --input {path-to-file} --output {path-to-file}


## Analysis:
python3 analyse_file.py --input {path-to-file}
