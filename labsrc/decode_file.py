import argparse

from labsrc.constants import CIPHERS


def main():
    '''Decodes file and stores result in specified one'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k')
    parser.add_argument('--keyfile', '-kf', type=argparse.FileType('r'))
    parser.add_argument('--input', '-i', required=True, type=argparse.FileType('r'))
    parser.add_argument('--output', '-o', required=True, type=argparse.FileType('w+'))
    parser.add_argument('--type', '-t', required=True)

    arguments = parser.parse_args()

    key = arguments.key
    key_file = arguments.keyfile
    if key is None and key_file is not None:
        for line in key_file:
            key = line

    CIPHERS.get(arguments.type)(key).decipher_file(arguments.input, arguments.output)
    print(f'Your file was successfully decoded.')


if __name__ == '__main__':
    main()
