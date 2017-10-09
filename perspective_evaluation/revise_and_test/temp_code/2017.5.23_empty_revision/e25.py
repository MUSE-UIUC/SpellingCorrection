# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:02:21 2017

re-generate the data file whose new_word is an empty string.

@author: liyuchen
"""

import pickle
print('done import pickle')
from add_spelling_errors import load_toxic_word
print('done from add_spelling_errors import load_toxic_word')
from revise_sentence_and_test import revise_sentence_and_test_list_5_ways_invalid_v2
print('done from revise_sentence_and_test import revise_sentence_and_test_list_5_ways_invalid_v2')


'''
Main
'''

# the indices of all data files whose new_word is an empty string.
empty_inds = [27, 45, 76, 84, 89, 126, 134, 134, 135, 151, 170, 174, 184, 190, 201, 234, 241, 256, 336, 26, 112, 120, 131, 175, 178, 197, 217, 250, 255, 257, 273, 293, 329, 341, 35, 43, 105, 192, 225, 257, 280, 320, 323]
empty_inds = list(set(empty_inds)) # unique
print('empty_inds:', empty_inds)
print('len(empty_inds)', len(empty_inds)) # 41

# re-generate the data file whose new_word is an empty string.

Sentence_And_Toxic_Word = load_toxic_word('Sentence_And_Toxic_Word.pickle')

# 10 sentences per batch
folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for j in range( 24, 25):
    i = empty_inds[j]
    print('Processing the %d-th batch of 10 sentences\n' % i)
    if (i*10 < len(Sentence_And_Toxic_Word)):
        if (i*10+10 < len(Sentence_And_Toxic_Word)):
            All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word[i*10:i*10+10], Folder_List, str(i)+'_')
        else:
            All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word[i*10:len(Sentence_And_Toxic_Word)], Folder_List, str(i)+'_')
        out_file_name = 'All_Sentences_Scores/All_Sentences_Scores'+str(i)+'.pickle'
        with open(out_file_name, "wb") as handle:
            pickle.dump(All_Sentences_Scores, handle)