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
from nltk import word_tokenize, pos_tag

def getContentWords(list_of_str):
    tag_set = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS",\
               "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    selected_word_list = []
    for s in list_of_str:
        text = word_tokenize(s)
        word_pos_list = pos_tag(text)
        words = [item[0] for item in word_pos_list if item[1] in tag_set]
        selected_word_list.append(words)
    return selected_word_list




def modify_key_words(sentence, Words_List)
