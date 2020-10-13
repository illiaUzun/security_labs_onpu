from labsrc.cipher import cryptocommon
from labsrc.cipher.Cipher import Cipher

# ---- Numerical constants/tables ----

_NUM_ROUNDS = 8

class IDEA(Cipher):

    def __init__(self, key):
        self.__key = key

    def encipher(self, block):
        print(f"block = {block}, key = {self.__key}")
        return "".join([chr(int(b)) for b in self._crypt([ord(char) for char in block], [ord(kchar) for kchar in self.__key], "encrypt", True)])

    def decipher(self, block):
        print(f"block = {block}, \nkey = {self.__key}")
        return "".join([chr(int(b)) for b in self._crypt([ord(char) for char in block], [ord(kchar) for kchar in self.__key], "decrypt", True)])

    def _crypt(self, block, key, direction, printdebug):
        # Check input arguments
        assert isinstance(block, list) and len(block) == 8
        assert isinstance(key, list) and len(key) == 16
        assert direction in ("encrypt", "decrypt")
        if printdebug: print(
            f"ideacipher.{direction}(block = {cryptocommon.bytelist_to_debugstr(block)}, key = {cryptocommon.bytelist_to_debugstr(key)})")

        # Compute and handle the key schedule
        keyschedule = self._expand_key_schedule(key)
        if direction == "decrypt":
            keyschedule = self._invert_key_schedule(keyschedule)

        # Pack block bytes into variables as uint16 in big endian
        w = block[0] << 8 | block[1]
        x = block[2] << 8 | block[3]
        y = block[4] << 8 | block[5]
        z = block[6] << 8 | block[7]

        # Perform 8 rounds of encryption/decryption
        for i in range(_NUM_ROUNDS):
            if printdebug: print(f"    Round {i}: block = [{w:04X} {x:04X} {y:04X} {z:04X}]")
            j = i * 6
            w = self._multiply(w, keyschedule[j + 0])
            x = self._add(x, keyschedule[j + 1])
            y = self._add(y, keyschedule[j + 2])
            z = self._multiply(z, keyschedule[j + 3])
            u = self._multiply(w ^ y, keyschedule[j + 4])
            v = self._multiply(self._add(x ^ z, u), keyschedule[j + 5])
            u = self._add(u, v)
            w ^= v
            x ^= u
            y ^= v
            z ^= u
            x, y = y, x

        # Perform final half-round
        if printdebug: print(f"    Round {_NUM_ROUNDS}: block = [{w:04X} {x:04X} {y:04X} {z:04X}]")
        x, y = y, x
        w = self._multiply(w, keyschedule[-4])
        x = self._add(x, keyschedule[-3])
        y = self._add(y, keyschedule[-2])
        z = self._multiply(z, keyschedule[-1])

        # Serialize the final block as a bytelist in big endian
        return [
            w >> 8, w & 0xFF,
            x >> 8, x & 0xFF,
            y >> 8, y & 0xFF,
            z >> 8, z & 0xFF]

    # Given a 16-element bytelist, this computes and returns a tuple containing 52 elements of uint16.
    def _expand_key_schedule(self, key):
        # Pack all key bytes into a single uint128
        bigkey = 0
        for b in key:
            assert 0 <= b <= 0xFF
            bigkey = (bigkey << 8) | b
        assert 0 <= bigkey < (1 << 128)

        # Append the 16-bit prefix onto the suffix to yield a uint144
        bigkey = (bigkey << 16) | (bigkey >> 112)

        # Extract consecutive 16 bits at different offsets to form the key schedule
        result = []
        for i in range(_NUM_ROUNDS * 6 + 4):
            offset = (i * 16 + i // 8 * 25) % 128
            result.append((bigkey >> (128 - offset)) & 0xFFFF)
        return tuple(result)

    # Given an encryption key schedule, this computes and returns the
    # decryption key schedule as a tuple containing 52 elements of uint16.
    def _invert_key_schedule(self, keysch):
        assert isinstance(keysch, tuple) and len(keysch) % 6 == 4
        result = []
        result.append(self._reciprocal(keysch[-4]))
        result.append(self._negate(keysch[-3]))
        result.append(self._negate(keysch[-2]))
        result.append(self._reciprocal(keysch[-1]))
        result.append(keysch[-6])
        result.append(keysch[-5])

        for i in range(1, _NUM_ROUNDS):
            j = i * 6
            result.append(self._reciprocal(keysch[-j - 4]))
            result.append(self._negate(keysch[-j - 2]))
            result.append(self._negate(keysch[-j - 3]))
            result.append(self._reciprocal(keysch[-j - 1]))
            result.append(keysch[-j - 6])
            result.append(keysch[-j - 5])

        result.append(self._reciprocal(keysch[0]))
        result.append(self._negate(keysch[1]))
        result.append(self._negate(keysch[2]))
        result.append(self._reciprocal(keysch[3]))
        return tuple(result)

    # ---- Private arithmetic functions ----

    # Returns x + y modulo 2^16. Inputs and output are uint16. Only used by _crypt().
    def _add(self, x, y):
        assert 0 <= x <= 0xFFFF
        assert 0 <= y <= 0xFFFF
        return (x + y) & 0xFFFF

    # Returns x * y modulo (2^16 + 1), where 0x0000 is treated as 0x10000.
    # Inputs and output are uint16. Note that 2^16 + 1 is prime. Only used by _crypt().
    def _multiply(self, x, y):
        assert 0 <= x <= 0xFFFF
        assert 0 <= y <= 0xFFFF
        if x == 0x0000:
            x = 0x10000
        if y == 0x0000:
            y = 0x10000
        z = (x * y) % 0x10001
        if z == 0x10000:
            z = 0x0000
        assert 0 <= z <= 0xFFFF
        return z

    # Returns the additive inverse of x modulo 2^16.
    # Input and output are uint16. Only used by _invert_key_schedule().
    def _negate(self, x):
        assert 0 <= x <= 0xFFFF
        return (-x) & 0xFFFF

    # Returns the multiplicative inverse of x modulo (2^16 + 1), where 0x0000 is
    # treated as 0x10000. Input and output are uint16. Only used by _invert_key_schedule().
    def _reciprocal(self, x):
        assert 0 <= x <= 0xFFFF
        if x == 0:
            return 0
        else:
            return pow(x, 0xFFFF, 0x10001)  # By Fermat's little theorem
