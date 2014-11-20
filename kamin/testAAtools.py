from random import randrange, getrandbits
from math import *
import os
from AAbasictools import *

for i in range(12):
    print MapIntToAlphabet(Zp(getrandbits(5)).n)

