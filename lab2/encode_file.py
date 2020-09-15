import argparse

from lab2.cipher.Vigenere import Vigenere


def main():
    '''Encodes file and stores result in specified one'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k', required=True)
    parser.add_argument('--input', '-i', required=True, type=argparse.FileType('r'))
    parser.add_argument('--output', '-o', required=True, type=argparse.FileType('w+'))

    arguments = parser.parse_args()

    Vigenere(arguments.key).encipher_file(arguments.input, arguments.output)
    print(f'Your file was successfully encoded.')


if __name__ == '__main__':
    main()
