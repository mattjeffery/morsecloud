#!/usr/bin/env python
# encoding: utf-8
"""
morseCodec.py

a codec class for morse code.
encoder is based on http://svn.python.org/projects/python/trunk/Demo/scripts/morse.py


Created by Benjamin Fields on 2012-03-24.
Copyright (c) 2012 .
"""

import sys, math
import os
import audiodev, aifc
import unittest


class morseCodec(object):
    """class for encoding and decoding morse.
    Inputs supported:
    Text
    Outputs
    Morsetab, aiff
    """
    morsetab = {
            'A': '.-',
            'B': '-...',
            'C': '-.-.',
            'D': '-..',
            'E': '.',
            'F': '..-.',
            'G': '--.',
            'H': '....',
            'I': '..',
            'J': '.---',
            'K': '-.-',
            'L': '.-..',
            'M': '--',
            'N': '-.',
            'O': '---',
            'P': '.--.',
            'Q': '--.-',
            'R': '.-.',
            'S': '...',
            'T': '-',
            'U': '..-',
            'V': '...-',
            'W': '.--',
            'X': '-..-',
            'Y': '-.--',
            'Z': '--..',
            '0': '-----',           ',': '--..--',
            '1': '.----',           '.': '.-.-.-',
            '2': '..---',           '?': '..--..',
            '3': '...--',           ';': '-.-.-.',
            '4': '....-',           ':': '---...',
            '5': '.....',           "'": '.----.',
            '6': '-....',           '-': '-....-',
            '7': '--...',           '/': '-..-.',
            '8': '---..',           '(': '-.--.-',
            '9': '----.',           ')': '-.--.-',
            ' ': ' ',               '_': '..--.-',
    }
    def __init__(self, dot_width=None, audioWriter = aifc):
        self.dot_width = dot_width
        self.morsetab = morseCodec.morsetab
        self.tab2ascii = dict([(v, k) for k, v in self.morsetab.iteritems()])
        
    def text2tab(self, text):
        return ''.join([self.morsetab[c.upper()]+'\001' for c in text])
        
    def tab2text(self, text):
        """assumes '\001' is used as a char break, as in text2tab"""
        return ''.join([self.tab2ascii[t] for t in text.split('\001') if t != ''])
        
    # # to audio.
    # nowave = '\0' * 200
    # # If we play at 44.1 kHz (which we do), then if we produce one sine
    # # wave in 100 samples, we get a tone of 441 Hz.  If we produce two
    # # sine waves in these 100 samples, we get a tone of 882 Hz.  882 Hz
    # # appears to be a nice one for playing morse code.
    # def mkwave(self, octave):
    #     sinewave = ''
    #     for i in range(100):
    #         val = int(math.sin(math.pi * i * octave / 50.0) * 30000)
    #         sinewave += chr((val >> 8) & 255) + chr(val & 255)
    #     return sinewave
    # 
    # defaultwave = mkwave(OCTAVE)
    # 
    # def play(line, dev, wave):
    #     for c in line:
    #         if c == '.':
    #             sine(dev, DOT, wave)
    #         elif c == '-':
    #             sine(dev, DAH, wave)
    #         else:                   # space
    #             pause(dev, DAH + DOT)
    #         pause(dev, DOT)
    # 
    # def sine(dev, length, wave):
    #     for i in range(length):
    #         dev.writeframesraw(wave)
    # 
    # def pause(dev, length):
    #     for i in range(length):
    #         dev.writeframesraw(nowave)
    
    
class morseCodecTests(unittest.TestCase):
    def setUp(self):
        self.c = morseCodec()
    def test_basic_op(self):
        tab = self.c.text2tab('I like Cheese.')
        text = self.c.tab2text('..\x01 \x01.-..\x01..\x01-.-\x01.\x01 \x01-.-.\x01....\x01.\x01.\x01...\x01.\x01.-.-.-\x01')
    def test_identity_text(self, testText = "I like Cheese."):
        assert self.c.tab2text(self.c.text2tab(testText)) == testText.upper()
    def test_identity_tab(self, testTab='..\x01 \x01.-..\x01..\x01-.-\x01.\x01 \x01-.-.\x01....\x01.\x01.\x01...\x01.\x01.-.-.-\x01'):
        assert self.c.text2tab(self.c.tab2text(testTab)) == testTab

if __name__ == '__main__':
    unittest.main()