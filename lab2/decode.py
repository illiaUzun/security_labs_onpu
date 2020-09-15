import argparse

from lab2.cipher.Vigenere import Vigenere


def main():
    '''Decodes string and prints result'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k', required=True)
    parser.add_argument('--input', '-i', required=True)

    arguments = parser.parse_args()

    decoded = Vigenere(arguments.key).decipher(arguments.input)
    print(f'Decoded string: {decoded}')


if __name__ == '__main__':
    main()
