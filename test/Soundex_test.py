import unittest
import parameterized

from spinward.core.Soundex import SoundexEncoder


class SoundexTest(unittest.TestCase):

    TESTS = [
            ('fuzzy',		'F200',	'Y210'),
            ('Christine',	'C623',	'E532'),
            ('Christina',	'C623',	'A532'),
            ('Catherine',	'C365',	'E563'),
            ('Katherine',	'K365',	'E563'),
            ('Katarina',	'K365',	'A563'),
            ('Johnathan',	'J535',	'N352'),
            ('Jonathan',	'J535',	'N352'),
            ('John',		'J500',	'N200'),
            ('Teresa',		'T620',	'A263'),
            ('Theresa',		'T620',	'A263'),
            ('Smith',		'S530',	'H352'),
            ('Smyth',		'S530',	'H352'),
            ('Jessica',		'J220',	'A222'),
            ('Joshua',		'J200',	'A220'),
            ('Robert',		'R163',	'T616'),
            ('Rupert',		'R163',	'T616'),
            ('Rubin',		'R150',	'N160'),
            ('Ashcraft',	'A261',	'T162'),
            ('Ashcroft',	'A261',	'T162'),
            ('Tymczak',		'T522',	'K253'),
            ('Pfister',		'P236',	'R321'),
            ('Edward',		'E363',	'D630'),
            ('Edouard',		'E363',	'D630'),
            ('Howard',		'H630',	'D600'),
            ('Hewart',		'H630',	'T600'),
            ('Dandre',		'D536',	'E635'),
            ('Lawson',		'L250',	'N240'),
            ('Jones',		'J520',	'S520'),
            ('Reynolds',	'R543',	'S345'),
        ]

    def setUp(self):
        pass


    def test_call(self):
        encoder = SoundexEncoder()
        for word, sdx, rev_sdx in self.TESTS:
            encoded = encoder(word)
            if encoded != sdx:
                print("%4s  %-15r  %-6r -- expected %r" % ('FAIL', word, encoded, sdx))
            self.assertEqual(encoded, sdx)


    def test_encode(self):
        encoder = SoundexEncoder()
        for word, sdx, rev_sdx in self.TESTS:
            encoded = encoder.soundex(word)
            if encoded != sdx:
                print("%4s  %-15r  %-6r -- expected %r" % ('FAIL', word, encoded, sdx))
            self.assertEqual(encoded, sdx)


    def test_reverse_encode(self):
        encoder = SoundexEncoder()
        for word, sdx, rev_sdx in self.TESTS:
            encoded = encoder.reverse_soundex(word)
            if encoded != rev_sdx:
                print("%4s  %-15r  %-6r -- expected %r" % ('FAIL', word, encoded, rev_sdx))


if __name__ == '__main__':
    unittest.main()
