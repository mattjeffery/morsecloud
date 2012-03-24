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
import wave, aifc
import unittest


class morseCodec(object):
    """class for encoding and decoding morse.
    Inputs supported:
    Text, morsetab
    Outputs
    morsetab, aiff
    When the writer writes audio, it does so using self.audioWriter (to the file given at call time)
    by default this is the aifc writer, but it can be anything that behaves the same to the expected calls
    self.wave is the waveform that will be writen (by default a 882Hz sine tone) 
        for DOT 20 times (~22ms) (a baseunit)
        for DAH 3*DOT (~66ms)
        intercharacter pause is equal to a DOT
        interword pause is equal to DAH-DAH-DOT (7 base units, ~155,ms)
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
    DOT = 20
    DAH = 3 * DOT
    def __init__(self, dot_width=20, audioWriter = aifc):
        self.morsetab = morseCodec.morsetab
        self.dot = dot_width
        self.dah = 3 * self.dot
        self.tab2ascii = dict([(v, k) for k, v in self.morsetab.iteritems()])
        self.wave = self.mkwave()
        self.nowave = '\0' * len(self.mkwave())
        
    def text2tab(self, text):
        return ''.join([self.morsetab[c.upper()]+'\001' for c in text])
        
    def tab2text(self, text, charsep='\001' ):
        """assumes '\001' is used as a char break, as in text2tab"""
        return ''.join([self.tab2ascii[t] for t in text.split(charsep) if t != ''])
        
    # to audio.
    
    # If we play at 44.1 kHz (which we do), then if we produce one sine
    # wave in 100 samples, we get a tone of 441 Hz.  If we produce two
    # sine waves in these 100 samples, we get a tone of 882 Hz.  882 Hz
    # appears to be a nice one for playing morse code.
    def mkwave(self, octave=2):
        sinewave = ''
        for i in range(100):
            val = int(math.sin(math.pi * i * octave / 50.0) * 30000)
            sinewave += chr((val >> 8) & 255) + chr(val & 255)
        return sinewave
        
    def setaudiowriter(self, writer=aifc):
        self.audioWriterClass = writer
        
    def setupwriter(self, filename):
        self.audioWriter = self.audioWriterClass.open(filename, 'w')
        self.audioWriter.setframerate(44100)
        self.audioWriter.setsampwidth(2)
        self.audioWriter.setnchannels(1)
    
    def tab2audio(self, line, filename, customWriter=None):
        if customWriter:
            self.setaudiowriter(customWriter)
        else:
            self.setaudiowriter()
        self.setupwriter(filename)
        for c in line:
            if c == '.':
                self.sine(self.dot)
            elif c == '-':
                self.sine(self.dah)
            else:   # space
                self.pause(self.dah*2+self.dot)
            self.pause(self.dot)
        self.audioWriter.close()
        
    def sine(self,length):
        for i in range(length):
            self.audioWriter.writeframesraw(self.wave)
    
    def pause(self, length):
        for i in range(length):
            self.audioWriter.writeframesraw(self.nowave)
    
    
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