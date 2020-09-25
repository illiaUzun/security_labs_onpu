import argparse

from lab3.constants import CIPHERS


def main():
    '''Finds a key by encoded and opend text'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--open', '-o', required=True)
    parser.add_argument('--ciphered', '-c', required=True)
    parser.add_argument('--type', '-t', required=True)

    arguments = parser.parse_args()

    key = CIPHERS.get(arguments.type)('').xor_strings(arguments.ciphered, arguments.open)
    print(f'Cipher key: {key}')


if __name__ == '__main__':
    main()
