# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 20:47:55 2017

@author: liyuchen
"""

from corpus_util import loadDict
import editdistance

'''
Helper Functions
'''

'''
Find a list of closest words for each input word in terms of edit distance
input:
    word - input word
    vocab - the vocabulary that is used, in dictionary format
    cutoff - (optional, default: 1) the cutoff edit distance below which closest matches 
             are found     
output:
    Closest_Words - a list of closest matches to the input word
'''
def closest_words_edit_distance(word, vocab, cutoff=1):
    Closest_Words = []
    for key in vocab:
        if (editdistance.eval(key, word) <= cutoff):
            Closest_Words.append(key)
    return Closest_Words
    
'''
Find a list of closest words for each input word in terms of edit distance, 
using a "dict.pickle" file in the same folder as vocabulary
input:
    word - input word
    cutoff - (optional, default: 1) the cutoff edit distance below which closest matches 
             are found     
output:
    Closest_Words - a list of closest matches to the input word
'''
def closest_words_edit_distance_pickle(word, cutoff=1):
    cnt = loadDict()
    return closest_words_edit_distance(word, cnt, cutoff)
    


'''
Main
'''
'''
Closest_Words = closest_words_edit_distance_pickle('idiiot', cutoff=1)
print(Closest_Words)
'''