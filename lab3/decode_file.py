import argparse

from lab3.constants import CIPHERS


def main():
    '''Decodes file and stores result in specified one'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k', required=True)
    parser.add_argument('--input', '-i', required=True, type=argparse.FileType('r'))
    parser.add_argument('--output', '-o', required=True, type=argparse.FileType('w+'))
    parser.add_argument('--type', '-t', required=True)

    arguments = parser.parse_args()

    CIPHERS.get(arguments.type)(arguments.key).decipher_file(arguments.input, arguments.output)
    print(f'Your file was successfully decoded.')


if __name__ == '__main__':
    main()
