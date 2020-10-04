from labsrc.cipher.Cipher import Cipher

import numpy as np
import matplotlib.pyplot as plt


class Feistel(Cipher):

    def __init__(self, keys):
        self.__avalanche_metrics = []

        if keys is None:
            self.__keys = (bin(12).replace("0b", "").zfill(8),
                           bin(44).replace("0b", "").zfill(8),
                           bin(52).replace("0b", "").zfill(8),
                           bin(77).replace("0b", "").zfill(8),
                           bin(20).replace("0b", "").zfill(8),
                           bin(4).replace("0b", "").zfill(8),
                           bin(200).replace("0b", "").zfill(8),
                           bin(250).replace("0b", "").zfill(8),
                           bin(102).replace("0b", "").zfill(8),
                           bin(237).replace("0b", "").zfill(8),
                           bin(3).replace("0b", "").zfill(8),
                           bin(111).replace("0b", "").zfill(8),
                           bin(13).replace("0b", "").zfill(8),
                           bin(77).replace("0b", "").zfill(8),
                           bin(22).replace("0b", "").zfill(8),
                           bin(17).replace("0b", "").zfill(8))
        else:
            self.__keys = keys

    def encipher(self, string):
        while len(string) % 8 != 0:
            string += " "

        result = ""
        for i in range(int(len(string) / 8)):
            formatted = string[8 * i:8 * (i + 1)]
            binary_str = self.__str2binary(formatted)
            binary_strs = map(lambda string: string.zfill(8), binary_str.split())

            print("INPUT: {plain}, {binary}".format(plain=string, binary=binary_str))
            print(f"Binary representation {' ' * 74} | Stage")
            print(f"{'-' * 97}+{'-' * 9}")

            cipher_bineries = self.__encrypt_binary(binary_strs, self.__keys)
            print("\r{binary} | ENCRYPTED\n".format(binary=cipher_bineries))

            result += " ".join(cipher_bineries) + " "

        # PLOTTING AVALANCHE
        # print("\n\n Avalanche metrics:", self.__avalanche_metrics)
        #  self.__plot_avalanche_metrics(self.__avalanche_metrics)

        return result

    def decipher(self, string):
        result = ""
        cipher_blocks = np.array_split(string.split(), 2)

        for binary_blocks in cipher_blocks:
            decrypted_binaries = self.__encrypt_binary(binary_blocks, self.__keys[::-1])
            print("\r{binary} | {printable} | DECRYPTED\n".format(binary=decrypted_binaries, printable=self.__to_printable(decrypted_binaries)))

            result += self.__to_printable(decrypted_binaries)
        return result

    def __rotate_binaries(self, right_end):
        """Function that rotates the binray blocks"""
        import numpy as np
        return np.flip(right_end)

    def __xor_list(self, left_end, rotated_right_end):
        result = []
        for index, block in enumerate(left_end):
            local_res = ''
            for bin_idx, binary in enumerate(block):
                y = ord(binary) ^ ord(rotated_right_end[index][bin_idx])
                local_res += str(y)
            result.append(local_res)
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

    def __execute_round(self, binary_string, initial):
        left_end = binary_string[:4]
        right_end = binary_string[4:]
        round_result = right_end + self.__xor_list(left_end, right_end)

        self.__find_avalanche_metrics(initial, round_result)
        return round_result

    def __encrypt_binary(self, bstr, keys):
        """Takes a byte string and outputs a byte string"""
        last = list(bstr)
        initial = list(bstr)
        for round in range(len(keys)):
            last = self.__execute_round(last, initial)
            print("\r{binary} | ROUND {round}".format(binary=last, round=round + 1))

        # Swap both sides
        swapped = last[4:] + last[:4]

        return swapped

    def __bstr2binary(self, string):
        return " ".join("{0:08b}".format(char) for char in string)

    def __str2binary(self, string):
        return " ".join("{0:0b}".format(ord(char)) for char in string)

    def __to_printable(self, binary_strings):
        result = ''
        for binary_block in binary_strings:
            result += chr(int(binary_block, 2))
        return result
