import argparse

from labsrc.constants import CIPHERS


def main():
    '''Encodes file and stores result in specified one'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k')
    parser.add_argument('--keyfile', '-kf')
    parser.add_argument('--input', '-i', required=True, type=argparse.FileType('r'))
    parser.add_argument('--output', '-o', required=True, type=argparse.FileType('w+'))
    parser.add_argument('--type', '-t', required=True)

    arguments = parser.parse_args()

    key = arguments.key
    if key is None:
        for line in arguments.keyfile:
            key += line

    CIPHERS.get(arguments.type)(key).encipher_file(arguments.input, arguments.output)
    print(f'Your file was successfully encoded.')


if __name__ == '__main__':
    main()
