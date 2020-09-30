import argparse

from labsrc.constants import CIPHERS


def main():
    '''Decodes string and prints result'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k', required=True)
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--type', '-t', required=True)

    arguments = parser.parse_args()

    decoded = CIPHERS.get(arguments.type)(arguments.key).decipher(arguments.input)
    print(f'Decoded string: {decoded}')


if __name__ == '__main__':
    main()
