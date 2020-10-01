from labsrc.cipher.Cipher import Cipher

from struct import pack
from binascii import unhexlify
import matplotlib.pyplot as plt


class Feistel(Cipher):

    def __init__(self, keys):
        self.__avalanche_metrics = []

        if keys is None:
            self.__keys = (12, 44, 52, 77, 20, 4, 200, 250, 102, 237, 3, 111, 13, 77, 22, 17)
        else:
            self.__keys = keys

    def encipher(self, string):
        while len(string) % 8 != 0:
            string += " "

        result = ""
        for i in range(int(len(string) / 8)):
            formated = string[8 * i:8 * (i + 1)]
            byte_str = formated.encode("utf-8")

            print("Hex representation      | Text     | Stage")
            print("------------------------+----------+----------")
            print("{hex} | {plain} | INPUT".format(plain=formated, hex=self.__str2hex(formated)))

            cipher_bytes = self.__encrypt_bstr(byte_str, self.__keys)
            cipher_hex = self.__bstr2hex(cipher_bytes)
            print("\r{hex} | {printable} | ENCRYPTED\n".format(hex=cipher_hex,
                                                               printable=self.__to_printable(cipher_bytes)))

            result += cipher_bytes.decode()

            print("\n\n Avalanche metrics:", self.__avalanche_metrics)
            self.__plot_avalanche_metrics(self.__avalanche_metrics)

        return result

    def decipher(self, string):
        result = ""
        cipher_bytes = str.encode(string)

        for i in range(int(len(cipher_bytes) / 8)):
            formated = cipher_bytes[8 * i:8 * (i + 1)]
            decrypted_bytes = self.__encrypt_bstr(formated, self.__keys[::-1])
            decrypted_hex = self.__bstr2hex(decrypted_bytes)
            print("\r{hex} | {printable} | DECRYPTED\n".format(hex=decrypted_hex,
                                                               printable=self.__to_printable(decrypted_bytes)))

            result += self.__to_printable(decrypted_bytes) + "\n"
        return result

    def __rotate_bytes_byte(self, right_end, k):
        """Function that rotates the bytes k places"""
        return right_end[k:] + right_end[:k]

    def __append_to_each_byte(self, right_end, k):
        """Function that adds itself to each byte"""
        return [byte + k for byte in right_end]

    def __append_to_one_byte(self, right_end, k):
        """Function that adds itself to 1 byte"""
        i = k % len(right_end)
        result = right_end[:]
        result[i] = (k + right_end[i]) % 256
        return result

    def __xor_list(self, left_end, rotated_right_end):
        result = []
        for index, c in enumerate(left_end):
            result.append(c ^ rotated_right_end[index])
        return result

    def __plot_avalanche_metrics(self, metrics):
        plt.suptitle('Avalanche effect')
        plt.xlabel('rounds')
        plt.ylabel('amount of changed bytes in initial text')
        plt.plot([round for round in range(len(self.__keys))], metrics)
        plt.show()

    def __find_avalanche_metrics(self, initial, ciphered):
        byte_changes_cnt = 0
        for i, c in zip(initial, ciphered):
            if i != c:
                byte_changes_cnt += 1

        self.__avalanche_metrics.append(byte_changes_cnt)

    def __execute_round(self, byte_string, keys, round, initial):
        left_end = byte_string[:4]
        right_end = byte_string[4:]
        rotated_right_end = self.__rotate_bytes_byte(right_end, keys[round])
        round_result = right_end + self.__xor_list(left_end, rotated_right_end)

        self.__find_avalanche_metrics(initial, round_result)
        return round_result

    def __encrypt_bstr(self, bstr, keys):
        """Takes a byte string and outputs a byte string"""
        last = list(bstr)
        initial = list(bstr)
        for round in range(len(keys)):
            last = self.__execute_round(last, keys, round, initial)
            print("\r{hex} | {printable} | ROUND {round}".format(hex=self.__bstr2hex(last),
                                                                 printable=self.__to_printable(last), round=round + 1))

        # Swap both sides
        swapped = last[4:] + last[:4]

        return b''.join(map(lambda x: pack("B", x), swapped))

    def __bstr2hex(self, string):
        return " ".join("{:02x}".format(char) for char in string)

    def __str2hex(self, string):
        return " ".join("{:02x}".format(ord(char)) for char in string)

    def __hex2bstr(self, hex):
        return unhexlify(hex.replace(' ', ''))

    def __hex2str(self, hex):
        return unhexlify(hex.replace(' ', '')).decode('utf-8')

    def __to_printable(self, byte_string):
        result = ''
        for byte in list(byte_string):
            result += chr(byte)
        return result
