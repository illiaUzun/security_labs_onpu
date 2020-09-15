import argparse

from lab2.cipher.Vigenere import Vigenere


def main():
    '''Encodes string and prints result'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k', required=True)
    parser.add_argument('--input', '-i', required=True)

    arguments = parser.parse_args()

    encoded = Vigenere(arguments.key).encipher(arguments.input)
    print(f'Encoded string: {encoded}')


if __name__ == '__main__':
    main()
