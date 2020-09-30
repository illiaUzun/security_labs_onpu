from labsrc.cipher.Cipher import Cipher


class XOR(Cipher):

    def __init__(self, key='fortification'):
        self.key = [bin(ord(k))[2:].zfill(8) for k in key]

    def encipher(self, string):
        """ Enciphers string:
            :param string: String to encipher.
        """
        result = []
        i = 0
        for line in string:
            cline = ""
            for char in line:
                if i == len(self.key):
                    i = 0
                byteKey = self.key[i]
                byteOrigin = bin(ord(char))[2:].zfill(8)
                byteRes = bin(int(byteKey, 2) ^ int(byteOrigin, 2))[2:].zfill(8)
                cline += str(byteRes)
                i += 1
            result.append(cline)
        return ''.join(result)

    def decipher(self, string):
        """ Deciphers string:
            :param string: String to decipher.
        """
        decoded = []
        encoded = [string[i:i + 8] for i in range(0, len(string), 8)]
        i = 0

        for line in encoded:
            if i == len(self.key):
                i = 0

            byteKey = self.key[i]
            byteOrigin = line
            byteRes = chr(int(byteOrigin, 2) ^ int(byteKey, 2))
            i += 1
            decoded.append(byteRes)
        return ''.join(decoded)


    def xor_strings(self, ciphered, open):
        self.key = [bin(ord(o))[2:].zfill(8) for o in open]
        return self.decipher(ciphered)
