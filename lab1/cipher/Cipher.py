import re
from typing import TextIO


class Cipher(object):
    """ Base class for all Ciphers. Can be extended.
    """

    def encipher(self, string):
        """ Enciphers string:
            :param string: String to encipher.
        """
        return string

    def decipher(self, string):
        """ Deciphers string:
            :param string: String to decipher.
        """
        return string

    def encipher_file(self, source_file: TextIO, destination_file: TextIO):
        """ Enciphers file line by line:
            :param source_file: File to encipher.
            :param destination_file: File to store enciphered output in.
        """
        for line in source_file:
            destination_file.write(self.encipher(line))

    def decipher_file(self, source_file: TextIO, destination_file: TextIO):
        """ Deciphers file line by line:
            :param source_file: File to decipher.
            :param destination_file: File to store deciphered output in.
        """
        for line in source_file:
            destination_file.write(self.decipher(line))

    def a2i(self, ch):
        """ Returns index of character in alphabet.
            :param ch: Character to get index of.
        """
        ch = ch.upper()
        arr = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
               'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
               'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
        return arr[ch]

    def i2a(self, i):
        """ Returns character by it's index.
            :param i: Index of character to return
        """
        i = i % 26
        arr = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        return arr[i]

    def remove_punctuation(self, text, filter='[^A-Z]'):
        return re.sub(filter, '', text.upper())
