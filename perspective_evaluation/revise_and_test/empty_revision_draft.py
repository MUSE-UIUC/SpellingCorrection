# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:57:17 2017

re-generate the data file whose new_word is an empty string.

@author: liyuchen
"""

import codecs
import string
from find_toxic_word import most_toxic_word
from add_spelling_errors import modify_key_words_5_ways_readTag_invalid_v2_force_method

'''
Helper Functions
'''

'''
Read a file containing groups separated by newline characters, in which
k lines form a group. each patter contains the k lines and an additional empty line.
'''
def read_k_tuples(in_file_name, k):
    with codecs.open(in_file_name,'r',encoding='utf8') as f:
        content = f.read()
    List_Of_List = []
    if (content != ''):
        Content_List = content.split('\n')
        for i in range(int((len(Content_List)-1)/(k+1))):
            List = []
            for j in range(i*(k+1),i*(k+1)+k):
                List.append(Content_List[j])
            List_Of_List.append(List)
    f.close()
    return List_Of_List

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
    
# re-generate the data file whose new_word is an empty string.
for fn in Empty_Revision_File_Names:
    print('processing file:', fn)
    
    # parse for method: 0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate
    if (fn[33]=='a'):
        method = 0
    elif (fn[33]=='d'):
        method = 1
    elif (fn[33]=='r'):
        method = 2
    elif (fn[33]=='p'):
        method = 3
        
    List_Of_List = read_k_tuples(fn, 5)    
    
    Modified_Sentences_And_Words_List = []    
    
    for group in List_Of_List:
        # [original_sentence, original_score, new_sentence, new_score, correct word and wrong word pairs, empty line]
        original_sentence = group[0]
        correct_word = group[4].split(',')[0]
        
        s_wo_punctuation = original_sentence
        for p in list(string.punctuation):
            s_wo_punctuation = s_wo_punctuation.replace(p,'')
        Words_In_Sentence = s_wo_punctuation.split()
        indices = [count for count, elem in enumerate(Words_In_Sentence) if elem==correct_word]
        
        Modified_Sentences_And_Words = modify_key_words_5_ways_readTag_invalid_v2_force_method(indices, original_sentence, method)
        Modified_Sentences_And_Words_List.append(Modified_Sentences_And_Words)
        
THIS PROGRAM IS NOT FINISHED
        