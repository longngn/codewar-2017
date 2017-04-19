# pylint: disable=all

import hashlib

B = '_WHATEVER_'
possibleCs = ['BRETT', 'UWANT', 'MARIA', 'AEE09']
expectedSHA256 = '753053aeae0d1a3fe33bd2cb31a901069873b8c37127b0d3757dd3a90313b526'

def tohop(i, A):
    if i > 6:
        for C in possibleCs:
            wholeString = A + B + C
            hash = hashlib.sha256(wholeString).hexdigest()
            if hash == expectedSHA256:
                print wholeString
        return
    for charCode in range(ord('A'), ord('Z')):
        char = chr(charCode)
        tohop(i+1, A + char)

tohop(1, '')