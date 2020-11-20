"""
SoundexEncoder: An implementation of the American Soundex algorithm,
as described in http://en.wikipedia.org/wiki/Soundex.
"""

import re


class SoundexEncoder(object):

    # _SOUNDDICT: Maps char to digit (1-6), vowels to 'v'
    #   digit =  1      2           3     4    5     6
    __GROUPS = ("BFPV", "CGJKQSXZ", "DT", "L", "MN", "R")
    _SOUNDDICT = dict((ch, str(idx+1)) for (idx, chars) in enumerate(__GROUPS) for ch in chars)
    for ch in 'AEIOUY':
        _SOUNDDICT[ch] = 'v'

    _RE_COLLAPSE = re.compile(r'([0-9])\1')

    def __init__(self):
        pass


    def soundex(self, word):
        """
        Return soundex code for word.

        @param word:	Word to encode.

        @return:		soundex code
        """
        word = word.upper().strip()
        if not word:
            return ""
        firstChar = word[0]
        enc = [self.__class__._SOUNDDICT.get(c) for c in word]
        while enc and enc[0] is None:
            del enc[0]
        out = enc[0]
        idx = 1
        while idx < len(enc):
            if enc[idx] is None or (word[-1] == enc[idx] and enc[idx] == enc[idx-1]):
                idx += 1
                continue
            out += enc[idx]
            idx += 1
        out = self.__class__._RE_COLLAPSE.sub(r'\1', out)
        if firstChar in 'HW':
            out = firstChar + out
        else:
            out = firstChar + out[1:]
        out = out.replace('v', '')[:4]
        if len(out) < 4:
            out += (4-len(out))*'0'
        return out


    def reverse_soundex(self, word):
        """
        Return reverse-soundex code for word.

        @param word:	Word to encode.

        @return:		reverse-soundex code
        """
        # Reverse word and return soundex code for reversed word.
        return self.soundex(word[::-1])


    def __call__(self, word):
        """
        As callable, perform (forward) soundex encoding.
        """
        return self.soundex(word)
