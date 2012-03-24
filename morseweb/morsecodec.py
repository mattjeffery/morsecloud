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
import audioop
import wave, aifc
import audioread
import unittest

def replace(a_list, item, new_item):
    '''generic replace method in a list.'''
    if item == new_item:
        return a_list
    while item in a_list:
        a_list[a_list.index(item)] = new_item
    return a_list
    
def hard_norm(a_list, midpoint):
    ret_list = []
    for uniq_val in set(a_list):
        if uniq_val > midpoint:
            if uniq_val != 1:
                a_list = replace(a_list, uniq_val, 1)
        else:
            if uniq_val != 0:
                a_list = replace(a_list, uniq_val, 0)
    return a_list

def rreplaced(a_str, find, replace, **kwargs):
    """does a find and replace, but from right to left rather than left to right, 
     returns the resulting string
     passes any additional kwargs to replaced"""
    return ''.join(reversed(''.join(reversed(a_str)).replace(find,replace, **kwargs)))
    

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
    def mkwave(self, octave=1):
        sinewave = ''
        for i in range(100):
            val = int(math.sin(math.pi * i * octave / 50.0) * 30000)
            sinewave += chr((val >> 8) & 255) + chr(val & 255)
        return sinewave
        
    def setaudiowriter(self, filename, writer=wave):
        self.audioWriterClass = writer
        self.audioWriter = self.audioWriterClass.open(filename, 'w')
        self.audioWriter.setframerate(44100)
        self.audioWriter.setsampwidth(2)
        self.audioWriter.setnchannels(1)
    
    def setaudioreader(self, filename, reader=audioread):
        self.audioReaderClass = reader
        try:
            self.audioReader = self.audioReaderClass.audio_open(filename)
        except AttributeError:
            self.audioReader = self.audioReaderClass.open(filename)
    
    def tabs2bitlength(self, line):
        length = 0
        for c in line:
            if c == '.':
                 length += len(self.wave)*self.dot
            elif c == '-':
                 length += len(self.wave)*self.dah
            elif c == '\x01': #char break
                 length += len(self.nowave)*self.dot*2
            else:   # space, don't add anything 
                 continue
            length += len(self.nowave) * self.dot
        return length
        
    def tabs2audio(self, line, filename, customWriter=None, closeWriter=True):
        if customWriter:
            self.setaudiowriter(filename, customWriter)
        else:
            self.setaudiowriter(filename)
        if not closeWriter:
            #if we aren't closing, we'll gues what the number of frames will be a priori
            self.audioWriter.setnframes(self.tabs2bitlength(line))
        for c in line:
            if c == '.':
                self.sine(self.dot)
            elif c == '-':
                self.sine(self.dah)
            elif c == '\x01': #char break
                self.pause(self.dot*2)
            else:   # space, don't add anything 
                continue
            self.pause(self.dot)
        if closeWriter:
            self.audioWriter.close()
        
    def text2audio(self, text, filename, customWriter=None, closeWriter=True):
        self.tabs2audio(self.text2tab(text), filename, customWriter, closeWriter)
        
    def sine(self,length):
        for i in range(length):
            self.audioWriter.writeframesraw(self.wave)
    
    def pause(self, length):
        for i in range(length):
            self.audioWriter.writeframesraw(self.nowave)
            
    #decode bits are here, currently only fixed width (window)
    def audio2tabs(self, filename, customReader=None):
        if customReader:
            self.setaudioreader(filename, customReader)
        else:
            self.setaudioreader(filename)
        
        rms_stream = []
        start = 0
        data =''.join([block for block in self.audioReader])
        for end_idx in xrange(len(self.mkwave())*self.dot, 
                              len(data)+len(self.mkwave())*self.dot, 
                              len(self.mkwave())*self.dot):
            rms_stream.append(audioop.rms(data[start:end_idx], 2))
            start = end_idx
        midpoint = (max(rms_stream) - min(rms_stream))/2
        normed_power = hard_norm(rms_stream, midpoint)
        str_seq = ''.join([str(i) for i in normed_power])
        return self.str2tab(str_seq)
        
    def audio2text(self, filename, customReader=None):
        tab = self.audio2tabs(filename, customReader=customReader)
        return self.tab2text(tab)
        
    def str2tab(self, str_seq):
        #spaces
        str_seq = rreplaced(str_seq, '000000', '\x01 \x01')
        #char breaks
        str_seq = rreplaced(str_seq, '000', '\x01')
        #dashes
        str_seq = str_seq.replace('1110', '-')
        #dots
        str_seq = str_seq.replace('10', '.')
        return str_seq
    
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