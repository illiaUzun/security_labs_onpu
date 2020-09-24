import argparse

from lab3.constants import CIPHERS


def main():
    '''Encodes string and prints result'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k', required=True)
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--type', '-t', required=True)

    arguments = parser.parse_args()

    encoded = CIPHERS.get(arguments.type)(arguments.key).encipher(arguments.input)
    print(f'Encoded string: {encoded}')


if __name__ == '__main__':
    main()
