from labsrc.cipher.Cipher import Cipher

from struct import pack
from binascii import unhexlify

class Feistel(Cipher):

    def __init__(self, keys):
        if keys is None:
            self.__keys = (12, 44, 52, 77, 20, 4, 200, 250, 102, 237, 3, 111, 13, 77, 22, 17)
        else:
            self.__keys = keys

    def encipher(self, string):
        while len(string) % 8 != 0:
            string += " "

        result = ""
        for i in range(int(len(string) / 8)):
            str = string[8 * i:8 * (i + 1)]
            str_b = str.encode("utf-8")

            print("Hex representation      | Text     | Stage")
            print("------------------------+----------+----------")
            print("{hex} | {plain} | INPUT".format(plain=str, hex=self.__str2hex(str)))

            cipher_bytes = self.__encrypt_bstr(str_b, self.__keys)
            cipher_hex = self.__bstr2hex(cipher_bytes)
            print("\r{hex} | {printable} | ENCRYPTED\n".format(hex=cipher_hex, printable=self.__to_printable(cipher_bytes)))

            result += self.__to_printable(cipher_bytes)

            decrypted_bytes = self.__encrypt_bstr(cipher_bytes, self.__keys[::-1])
            decrypted_hex = self.__bstr2hex(decrypted_bytes)
            print("\r{hex} | {printable} | DECRYPTED\n".format(
                hex=decrypted_hex,
                printable=self.__to_printable(decrypted_bytes)
            ))

            result += " -> "
            result += self.__to_printable(decrypted_bytes) + "\n"

        return result

    def decipher(self, string):
        pass

    def __rotate_bytes_byte(self, RE, k):
        """Function that rotates the bytes k places"""
        lst = RE
        return lst[k:] + lst[:k]

    def __append_to_each_byte(self, RE, k):
        """Function that adds itself to each byte"""
        return [b + k for b in RE]

    def __append_to_one_byte(self, RE, k):
        """Function that adds itself to 1 byte"""
        i = k % len(RE)
        result = RE[:]
        result[i] = (k + RE[i]) % 256
        return result

    def __xor_list(self, LE, RE_f):
        result = []
        for index, c in enumerate(LE):
            result.append(c ^ RE_f[index])
        return result

    def __execute_round(self, b_string, keys, round):
        assert (len(b_string) == 8)
        LE = b_string[:4]
        RE = b_string[4:]
        RE_f = self.__rotate_bytes_byte(RE, keys[round])
        return RE + self.__xor_list(LE, RE_f)

    def __encrypt_bstr(self, bstr, keys):
        """Takes a byte string and outputs a byte string"""
        last = list(bstr)
        for round in range(len(keys)):
            last = self.__execute_round(last, keys, round)
            print("\r{hex} | {printable} | ROUND {round}".format(
                hex=self.__bstr2hex(last),
                printable=self.__to_printable(last),
                round=round + 1
            ))

        # Swap both sides
        swapped = last[4:] + last[:4]

        return b''.join(map(lambda x: pack("B", x), swapped))

    def __bstr2hex(self, s):
        return " ".join("{:02x}".format(c) for c in s)

    def __str2hex(self, s):
        return " ".join("{:02x}".format(ord(c)) for c in s)

    def __hex2bstr(self, h):
        return unhexlify(h.replace(' ', ''))

    def __hex2str(self, h):
        return unhexlify(h.replace(' ', '')).decode('utf-8')

    def __to_printable(self, b_str):
        result = ''
        printable_ascii = range(32, 127)
        for b in list(b_str):
            if b in printable_ascii:
                result += chr(b)
            else:
                result += '�'
        return result
