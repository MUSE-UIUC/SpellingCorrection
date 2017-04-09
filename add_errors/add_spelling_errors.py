# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 18:41:01 2017

This file contrains functions that can be used to deliberately add mis-spellings
to sentences.

@author: liyuchen
"""

'''
Modify certain words in a sentence
input:
    sentence - a string representing the sentence
    Words_List - a list of words that should be modified
output:
    Modified_Sentences - a list of sentences, with each being the input sentence
                         with one word from Words_List modified.
'''
def modify_key_words(sentence, Words_List)