from labsrc.cipher.Feistel import Feistel
from labsrc.cipher.IDEA import IDEA
from labsrc.cipher.Polybius import PolybiusSquare
from labsrc.cipher.Vigenere import Vigenere
from labsrc.cipher.XOR import XOR

CIPHERS = \
    {'vigenere': Vigenere,
     'polybius': PolybiusSquare,
     'xor': XOR,
     'feistel': Feistel,
     'idea': IDEA}
