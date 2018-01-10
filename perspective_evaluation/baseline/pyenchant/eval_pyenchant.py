#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 12:20:16 2017

@author: liyuchen
"""

import enchant
from enchant.checker import SpellChecker
import pickle
from fetch_toxic_score import fetch_toxic_score_online
import matplotlib.pyplot as plt

'''
2017.10.8
Try the enchant package
note:
    While looping through the errors using 'for err in chkr', only the first loop
    is non-empty
'''
'''
d = enchant.Dict("en_US")
chkr = SpellChecker("en_US")
chkr.set_text("This is sme sample txt with erors.")

err_words = []
for err in chkr:
    print (err.word)
    err_words.append(err.word)
    
suggestions = d.suggest("Heloe")

chkr.set_text("Thiis is anoother sample.")
#for err in chkr:
#    print (err.word)
correction_word_list = []
#for err in chkr:
#    err_word = err.word
#    suggestions = d.suggest(err_word)
#    if (len(suggestions) > 0):
#        correction_word_list.append((err_word, suggestions[0]))
#        err.replace(suggestions[0])
#for err in chkr:
#    suggestions = d.suggest(err.word)
#    if (len(suggestions) > 0):
#        correction_word_list.append((err.word, suggestions[0]))
#        err.replace(suggestions[0])
'''

'''
2017.10.8
Test the enchant package on 'All_Sentences_Scores_Filtered.pickle'
input:
    All_Sentences_Scores_Filtered: a list [0..4] of list of 
    (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, new_word_list)
    where filter means the following: 
    check the (sentence, most toxic word) list. 
    - If len(most toxic word) <= 2
    - If the most toxic word appears less than 100 times in the dictionary, then discard the sentence.
    - if the most toxic word is auxiliary verb, then discard the sentence.
output:
    Correction_All_Sentences_Scores: a list [0..3] of list of 
    (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, 
    new_word_list, correction_word_list, correction_score, corrected_sentence), where
    correction_word_list is a list of (wrong_word, suggested_word).
note: 
    While looping through the errors using 'for err in chkr', only the first loop
    is non-empty
'''
'''
fn = 'input/All_Sentences_Scores_Filtered.pickle'
with open(fn, "rb") as handle:
    All_Sentences_Scores_Filtered = pickle.load(handle)
print('Number of sentences: %d' % (len(All_Sentences_Scores_Filtered[0])+len(All_Sentences_Scores_Filtered[1])
+len(All_Sentences_Scores_Filtered[2])+len(All_Sentences_Scores_Filtered[3])+len(All_Sentences_Scores_Filtered[4])))

Correction_All_Sentences_Scores = []
count = 0
d = enchant.Dict("en_US")
chkr = SpellChecker("en_US")

for i in range(4):
    Correction_All_Sentences_Scores.append([])
    for j in range(len(All_Sentences_Scores_Filtered[i])):
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, new_word_list) = \
        All_Sentences_Scores_Filtered[i][j]   
        
        original_score = fetch_toxic_score_online(original_sentence)
        revised_toxic_score = fetch_toxic_score_online(revised_sentence)
        
        correction_word_list = []
        chkr.set_text(revised_sentence)
        err_words = []
        for err in chkr:
            suggestions = d.suggest(err.word)
            if (len(suggestions) > 0):
                correction_word_list.append((err.word, suggestions[0]))
                err.replace(suggestions[0])
        corrected_sentence = chkr.get_text()
        correction_score = fetch_toxic_score_online(corrected_sentence)
        
        Correction_All_Sentences_Scores[i].append((original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
                                       new_word_list, correction_word_list, correction_score, corrected_sentence))
        
        count += 1
        if (count%100==0):
            print('\tprocessed %d sentences' % count)
        #if (count>=10):
        #    raise ValueError("count>=10, time to stop for debug")

with open("output/Correction_All_Sentences_Scores.pickle", "wb") as handle:
    pickle.dump(Correction_All_Sentences_Scores, handle, protocol=2)
'''

'''
2017.10.8
Plot correction effects
'''
fn = "output/Correction_All_Sentences_Scores.pickle"
with open(fn, "rb") as handle:
    CASS = pickle.load(handle)

# X_Scores[0..3]: scores for method 0..3
# X_Scores[4]: scores for all methods
Original_Scores = [[],[],[],[],[]]
Revised_Scores = [[],[],[],[],[]]
Corrected_Scores = [[],[],[],[],[]]

for i in range(4):
    for j in range(len(CASS[i])):
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
        new_word_list, correction_word_list, correction_score, corrected_sentence) = CASS[i][j]
        Original_Scores[i].append(original_score)
        Revised_Scores[i].append(revised_toxic_score)
        Corrected_Scores[i].append(correction_score)
        Original_Scores[4].append(original_score)
        Revised_Scores[4].append(revised_toxic_score)
        Corrected_Scores[4].append(correction_score)
        
title_prefix = 'Original vs. Revised vs. Correction Scores - '
title_suffixes = ['add', 'delete', 'replace', 'permute', 'all']
for i in range(5):
    plt.figure(i)
    plt.plot(range(len(Original_Scores[i])),sorted(Original_Scores[i]), 'r',label='original')
    plt.plot(range(len(Revised_Scores[i])),sorted(Revised_Scores[i]), 'g', label='revised')
    plt.plot(range(len(Corrected_Scores[i])),sorted(Corrected_Scores[i]), 'b', label='corrected')
    plt.legend(loc=0)
    plt.xlabel('Data point')
    plt.ylabel('Score')
    plt.title(title_prefix+title_suffixes[i])
    plt.show()







