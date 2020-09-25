from binascii import hexlify

from lab3.cipher.Cipher import Cipher

class XOR(Cipher):

    def __init__(self, key='fortification'):
        self.key = [k.upper() for k in key]

    def encipher(self, string):
        """ Enciphers string:
            :param string: String to encipher.
        """
        result = []
        i = 0
        j = 0
        for line in string:
            cline = ""
            for char in line:
                if i == len(self.key[j]):
                    j = j + 1 if j < len(self.key) else 0
                    i = 0
                cline += hex(ord(char) ^ ord(self.key[j][i])).lstrip("0x").rstrip("L")
            result.append(cline)
        return ''.join(result)

    def decipher(self, string):
        """ Deciphers string:
            :param string: String to decipher.
        """
        encoded = string
        import binascii
        nums = binascii.unhexlify(encoded)
        strings = (''.join(chr(num ^ key) for num in nums) for key in range(256))
        return max(strings, key=lambda s: s.count(' '))

    def xor_strings(self, xs, ys):
        ascii_string = "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))
        hex_string = hexlify(ascii_string.encode())
        print("Hex Cipher key:" + hex_string.decode())
        return ascii_string