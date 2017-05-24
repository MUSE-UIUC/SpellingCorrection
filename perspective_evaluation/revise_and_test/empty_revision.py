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

# read the file reporting all data files whose new_word is an empty string.
fname = 'empty_file'
with open(fname) as f:
    content = f.readlines()    
    
Empty_Revision_File_Names = []
for i in range(len(content)):
    Empty_Revision_File_Names.append(content[i][54::])
    
empty_inds = []
for fn in Empty_Revision_File_Names:
    # extract 13 from 'output/separated_by_revised_type/add/13_method0.txt'
    ind = int(fn.split('/')[3].split('_')[0])
    empty_inds.append(ind)
empty_inds = list(set(empty_inds)) # unique
print('empty_inds:', empty_inds)
print('len(empty_inds)', len(empty_inds)) # 14

# re-generate the data file whose new_word is an empty string.

Sentence_And_Toxic_Word = load_toxic_word('Sentence_And_Toxic_Word.pickle')

# 10 sentences per batch
folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for j in range(0,len(empty_inds)):
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