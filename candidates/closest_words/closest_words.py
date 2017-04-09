# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20, 2017

This program 
(1) for each given input word, find a list of closest words
"""



import difflib
from nltk.corpus import words



'''
Helper Functions
'''

'''
Find a list of closest words for each input word
input:
    word - input word
    n0 - (optional, default: 3) the max number of closest matches that is found 
        for each incorrect word
    cutoff0 - (optional, default: 0.6) the cutoff above which closest matches 
             are found for each incorrect word           
output:
    Closest_Words - a list of closest matches to the input word
'''
def close_matches(word, n0=3, cutoff0=0.6):
    word_list = words.words()
    Closest_Words = difflib.get_close_matches(word, word_list, n=n0, cutoff=cutoff0)    
    return Closest_Words   
        
        
        
'''
Main
'''
'''
a = close_matches('idiiotr')
print(a)
'''