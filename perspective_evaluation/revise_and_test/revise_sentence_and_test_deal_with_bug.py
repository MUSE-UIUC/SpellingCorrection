# -*- coding: utf-8 -*-
"""
Created on Thu May 18 09:02:24 2017

@author: liyuchen
"""

from add_spelling_errors import load_toxic_word
import string
from revise_sentence_and_test import revise_sentence_and_test_list_5_ways_invalid_v2
from find_toxic_word import most_toxic_word
import pickle

'''
Main
'''

#selected_inds = []
#selected_words = []
#tok_sent = []
#
#
#All_Sentences_Scores_separate = load_toxic_word('All_Sentences_Scores_separate.pickle')
#print('len(All_Sentences_Scores_separate)', len(All_Sentences_Scores_separate))
#
#Sentence_And_Toxic_Word = []
#
#for i in range(len(All_Sentences_Scores_separate)):
#    
#    sentence = All_Sentences_Scores_separate[i][0]
#    
#    s_wo_punctuation = sentence = sentence
#    for p in list(string.punctuation):
#        s_wo_punctuation = s_wo_punctuation.replace(p,'')
#    Words_In_Sentence = s_wo_punctuation.split()
#    selected_inds.append(range(len(Words_In_Sentence)))
#    
#    selected_words.append(Words_In_Sentence)
#    
#    tok_sent.append(sentence)
#    
#Sentence_And_Toxic_Word = most_toxic_word(selected_inds, selected_words, tok_sent)
#with open('Sentence_And_Toxic_Word_separate.pickle', "wb") as handle:
#    pickle.dump(Sentence_And_Toxic_Word, handle)
    

Sentence_And_Toxic_Word = load_toxic_word('Sentence_And_Toxic_Word_separate.pickle')
print('len(Sentence_And_Toxic_Word): ',len(Sentence_And_Toxic_Word))

# 10 sentences per batch
folder_prefix = 'output/separated_by_revised_type/separate_redo/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for i in range(0,int(len(Sentence_And_Toxic_Word)/10)+1):
    print('Processing the %d-th batch of 10 sentences\n' % i)
    if (i*10+10 <= len(Sentence_And_Toxic_Word)):
        All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word[i*10:i*10+10], Folder_List, str(i)+'_')
    else:
        All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word[i*10:len(Sentence_And_Toxic_Word)], Folder_List, str(i)+'_')
    #print(len(All_Sentences_Scores))
    out_file_name = 'All_Sentences_Scores_separate/All_Sentences_Scores'+str(i)+'.pickle'
    with open(out_file_name, "wb") as handle:
        pickle.dump(All_Sentences_Scores, handle)