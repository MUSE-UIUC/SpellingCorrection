# -*- coding: utf-8 -*-
"""
Created on Mon May 29 15:10:53 2017

@author: liyuchen
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 14:58:27 2017

@author: liyuchen

This file contrains functions that can be used to deliberately add mis-spellings
to sentences.
"""

import pickle
from add_spelling_errors import change_a_word_5_ways_invalid_v2
from spam_util import preprocess
from corpus_util import loadDict

'''
- renamed on 2017.5.23
A function that loads pickle files.
'''
def load_pickle(fn):
    with open(fn, "rb") as handle:
        Content = pickle.load(handle)
    return Content    

'''
- added on 2017.5.29
Difference from the above:
(1) only add errors to words that have length > 3

Add spelling errors to the toxic words in input lists, and store the modified content, 
as well as the way in which each word is modified, in an output file.
input:
    Toxic_Words - a list of toxic words
    fn - the name of the input file
    out_fn - the name of the output file
output:
    original_and_modified_content - a string containing the original and the modified content in the file
    Correct_and_Wrong_Words - a list of (correct_word, wrong_word) tuples
effect:
    every toxic word is revised using one of the following methods: 
    0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate
    
    output file format:
    
    original sentence
    revised sentence
    correct word, wrong word; correct word, wrong word; ……
'''
def modify_toxic_words_in_file_v3(Toxic_Words, fn, out_fn):
    
    with open(fn) as f:
        content = f.read()    
    
    Words_In_Sentence, lemma_list = preprocess(content)
    if (len(Words_In_Sentence) != len(lemma_list)):
        print('bug: len(word_list) != len(lemma_list)')
        print(content)
        print(len(Words_In_Sentence), Words_In_Sentence)        
        print(len(lemma_list), lemma_list)
    
    New_Words_In_Sentence = []
    Correct_and_Wrong_Words = []
    for i in range(len(Words_In_Sentence)):
        if (len(Words_In_Sentence[i])>3 and (lemma_list[i] in Toxic_Words)):
            wrong_word = change_a_word_5_ways_invalid_v2(Words_In_Sentence[i])[0]
            New_Words_In_Sentence.append(wrong_word)
            Correct_and_Wrong_Words.append((Words_In_Sentence[i], wrong_word))
        else:
            New_Words_In_Sentence.append(Words_In_Sentence[i])
    
    sentence = ''
    for i in range(len(Words_In_Sentence)):
        try:
            sentence = sentence + Words_In_Sentence[i] + ' '
        except:
            print(Words_In_Sentence[i])
            print(Words_In_Sentence)
        
    modified_content = ''
    for i in range(len(New_Words_In_Sentence)):
        try:
            modified_content = modified_content + New_Words_In_Sentence[i] + ' '
        except:
            print(New_Words_In_Sentence[i])
            print(Words_In_Sentence[i])
            print(Words_In_Sentence)
            
    original_and_modified_content = (sentence, modified_content)

    with open(out_fn, "w") as f:
        try:
            f.write(sentence+'\n')
            f.write(modified_content+'\n')
            for j in range(len(Correct_and_Wrong_Words)):
                f.write(Correct_and_Wrong_Words[j][0]+', '+Correct_and_Wrong_Words[j][1]+'; ')
        except:
            print('modify_toxic_words_in_file: around line 600: write to file bug for sentence:')
            print('sentence:',sentence)
            print('modified_content:',modified_content)
            print('Correct_and_Wrong_Words:',Correct_and_Wrong_Words)

    return original_and_modified_content, Correct_and_Wrong_Words

'''
Process a file for the spam data.
(1) record whether the file is missing.
(2) try to add spelling errors to the toxic words and store the output file, 
calling other functions and record whether this step is successful.
input:
    fn - input file name
    out_fn - output file name
    Toxic_Words - a list of words that are likely to be recognized as typical in spams
output:
    file_missing - boolean
    original_and_modified_content - a string containing the original and the modified content in the file
    Correct_and_Wrong_Words - a list of (correct_word, wrong_word) tuples
    op_successful - boolean, whether adding errors is successful.
effect:
    store the output file at out_fn, calling other functions.
'''
def process_spam_file(fn, out_fn, Toxic_Words):
    
    # check whether the input file is missing.
#    f = open(fn)
#    f.close()
#    file_missing = False
    try:
        f = open(fn)
        f.close()
        file_missing = False
    except:
        file_missing = True
        
    # try to add spelling errors to the toxic words and store the output file, 
    # calling other functions and record whether this step is successful.
#    original_and_modified_content, Correct_and_Wrong_Words = modify_toxic_words_in_file_v2(Toxic_Words, fn, out_fn)
#    op_successful = True
    try:
        original_and_modified_content, Correct_and_Wrong_Words = modify_toxic_words_in_file_v3(Toxic_Words, fn, out_fn)
        op_successful = True
    except:
        original_and_modified_content = None
        Correct_and_Wrong_Words = None
        op_successful = False
    
    return file_missing, original_and_modified_content, Correct_and_Wrong_Words, op_successful
    
    

'''
Main
'''

# 2017.5.29 version

# load the list of words that are likely to be toxic
# filter the top 500 frequent words
fn = 'preprocess/toxic_words.pickle'
Toxic_Words_All = load_pickle(fn)
Toxic_Words = []
dictionary = loadDict()

count = 0
idx = 0
while (count < 1000):
    if (dictionary[Toxic_Words_All[idx]] >= 1000):
        Toxic_Words.append(Toxic_Words_All[idx])
        count = count + 1
    idx = idx + 1
print('Chose the top %d frequent words from %d the most toxic words' % (len(Toxic_Words),idx+1))



# add spelling errors to the toxic words in spam test data
Original_and_Modified_Content_List = []
Correct_and_Wrong_Words_List = []
Missing_Filenames = []
Except_Filenames = []
        
for i in range(74,145):
    fn = 'spam_data/'+'orig-test/'+'spmsgc'+str(i)+'.txt'
    out_fn = 'spam_data/'+'spam-test-w-errors/c'+str(i)+'.txt'
    file_missing, original_and_modified_content, Correct_and_Wrong_Words, op_successful = process_spam_file(fn, out_fn, Toxic_Words)
    
    if (file_missing):
        Missing_Filenames.append(i)
    
    if (op_successful):
        Original_and_Modified_Content_List.append(original_and_modified_content)
        Correct_and_Wrong_Words_List.append(Correct_and_Wrong_Words)
        print('processed file a', i)
    else:
        Except_Filenames.append(i)
        print('file c', i, 'has bug')
        
pickle_output_file_path_prefix = 'spam_data/spam-test-w-errors-pickle/'
with open(pickle_output_file_path_prefix+'Original_and_Modified_Content_List6.pickle', "wb") as handle:
    pickle.dump(Original_and_Modified_Content_List, handle)
with open(pickle_output_file_path_prefix+'Correct_and_Wrong_Words_List6.pickle', "wb") as handle:
    pickle.dump(Correct_and_Wrong_Words_List, handle)

print(Missing_Filenames)
print('length:',len(Missing_Filenames))
print(Except_Filenames)
print('length:',len(Except_Filenames))

