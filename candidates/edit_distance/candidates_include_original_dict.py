# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:23:55 2017

@author: liyuchen
"""

import codecs
import matplotlib.pyplot as plt
import numpy as np
from closest_edit_distance import closest_words_edit_distance_pickle
import editdistance
from nltk.corpus import words
import corpus_util
import statistics

'''
Helper Functions
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

# read original vs. revised sentences
List_Of_List = read_k_tuples('output/separated_by_revised_type/add/sentences_and_revised_scores0_method0.txt', 5)
for i in range(1,100):
    in_file_name = 'output/separated_by_revised_type/add/sentences_and_revised_scores'+str(i)+'_method0.txt'
    List_Of_List = List_Of_List+read_k_tuples(in_file_name, 5)

# do not allow 'permute' or 'separate'
Folder_Names = ['add','delete','permute','replace','separate']
for j in range(1,5):
    if (j != 2 and j != 4):
        for i in range(100):
            in_file_name = 'output/separated_by_revised_type/'+Folder_Names[j]+'/sentences_and_revised_scores'+str(i)+'_method'+str(j)+'.txt'
            List_Of_List = List_Of_List+read_k_tuples(in_file_name, 5)

print('number of sentences:',len(List_Of_List))

Original_Sentences = []
Original_Scores = []
Revised_Sentences = []
Revised_Scores = []
for i in range(len(List_Of_List)):
    Original_Sentences.append(List_Of_List[i][1])
    Original_Scores.append(float(List_Of_List[i][2]))
    Revised_Sentences.append(List_Of_List[i][3])
    Revised_Scores.append(float(List_Of_List[i][4]))

# Find the words that are revised
# record original words and revised words
original_words = []
revised_words = []
multiple_revised_words = 0
multiple_original_words = 0
zero_revised_words = 0
zero_original_words = 0
for i in range(len(Revised_Sentences)):
    flag = 0
    original_sentence_split = Original_Sentences[i].split()
    revised_sentence_split = Revised_Sentences[i].split()
    revised_words_choices = []
    for j in revised_sentence_split:
        if j not in original_sentence_split:
            revised_words_choices.append(j.lower())
    revised_words_choices = np.unique(revised_words_choices)
    if len(revised_words_choices) > 1:
        multiple_revised_words = multiple_revised_words + 1
        #print('\tthe number of revised words:',len(revised_words_choices))
    elif len(revised_words_choices) == 0:
        zero_revised_words = zero_revised_words + 1
    else:
        flag = flag + 1
    original_words_choices = []
    for j in original_sentence_split:
        if j not in revised_sentence_split:
            original_words_choices.append(j.lower())
    original_words_choices = np.unique(original_words_choices)
    if len(original_words_choices) > 1:
        multiple_original_words = multiple_original_words + 1
    elif len(original_words_choices) == 0:
        zero_original_words = zero_original_words + 1
    else:
        flag = flag + 1
    if flag == 2:
        revised_words.append(revised_words_choices[0])
        original_words.append(original_words_choices[0])
        if (editdistance.eval(revised_words_choices[0], original_words_choices[0]) > 2):
            print('\tedit distance =',editdistance.eval(revised_words_choices[0], original_words_choices[0]))
#revised_words = np.unique(revised_words)
#original_words = np.unique(original_words)
print('number of revised words:',len(revised_words))
print('number of original words:',len(original_words)) 
print('multiple_revised_words',multiple_revised_words)
print('multiple_original_words',multiple_original_words)
print('zero_revised_words',zero_revised_words)
print('zero_original_words',zero_original_words)
print('single revised words',len(revised_words))
print('single original words',len(original_words))



# read candidates with the least edit distance
List_Of_List = read_k_tuples('closest_edit_distance_out/0.txt', 4)
for i in range(1,42):
    in_file_name = 'closest_edit_distance_out/'+str(i)+'.txt'
    List_Of_List = List_Of_List+read_k_tuples(in_file_name, 4)
print('number of valid data (no errors in file I/O):',len(List_Of_List))

# process data
Revised_Words = []
Distances = []
Num_Candidates = []
Candidates = [] # each entry is a string containing all candidates, comma separated
for i in range(len(List_Of_List)):
    Revised_Words.append(List_Of_List[i][0])
    Distances.append(List_Of_List[i][1])
    Num_Candidates.append(int(List_Of_List[i][2]))
    Candidates.append(List_Of_List[i][3])
print('number of valid revised words:',len(Revised_Words))
print('\n')



# check whether the original word is in the candidates

out_file_name1 = 'original_word_not_in_candidate.txt'
out_file_name2 = 'original_word_is_correct_but_not_in_candidate.txt'
out_file_name3 = 'original_word_in_candidate.txt'
number_of_candidates_if_include_original_word = []
d = corpus_util.loadDict()
temp1 = codecs.open(out_file_name1, "w", "utf-8-sig")
temp2 = codecs.open(out_file_name2, "w", "utf-8-sig")
temp3 = codecs.open(out_file_name3, "w", "utf-8-sig")
# index in the list of valid data (sentences with unique identifiable revised & original words)    
for i in range(len(revised_words)): 
    # index in the list of valid data (no I/O errors)
    for j in range(len(Revised_Words)): 
        if (Revised_Words[j] == revised_words[i]):
            if (original_words[i] not in Candidates[j]):
                print(original_words[i], 'not in candidates of ', revised_words[i])
                temp1.write(original_words[i])
                temp1.write('\n')
                temp1.write(revised_words[i])
                temp1.write('\n')
                temp1.write(str(Distances[j]))
                temp1.write('\n')
                temp1.write(str(Num_Candidates[j]))
                temp1.write('\n')
                temp1.write(Candidates[j])
                temp1.write('\n\n')
                if (d[original_words[i]] > 0):
                    temp2.write(original_words[i])
                    temp2.write('\n')
                    temp2.write(revised_words[i])
                    temp2.write('\n')
                    temp2.write(str(Distances[j]))
                    temp2.write('\n')
                    temp2.write(str(Num_Candidates[j]))
                    temp2.write('\n')
                    temp2.write(Candidates[j])
                    temp2.write('\n\n')
            else:
                temp3.write(str(Num_Candidates[j])+'\n')
                number_of_candidates_if_include_original_word.append(Num_Candidates[j])
temp1.close()
temp2.close()
temp3.close()

# Statistics on number_of_candidates_if_include_original_word
print('Statistics on the number_of_candidates_if_include_original_word: ')
print('Max: %d' % max(number_of_candidates_if_include_original_word))
print('Min: %d' % min(number_of_candidates_if_include_original_word))
print('Average: %d' % statistics.mean(number_of_candidates_if_include_original_word))
print('Median: %d' % statistics.median(number_of_candidates_if_include_original_word))
print('Standard Deviation: %d' % statistics.stdev(number_of_candidates_if_include_original_word))
print('Variance: %d' % statistics.variance(number_of_candidates_if_include_original_word))
less_than_5 = 0
less_than_10 = 0
zero = 0
one = 0
for num in number_of_candidates_if_include_original_word:
    if num==0:
        zero = zero + 1
    if num==1:
        one = one + 1
    if num<5:
        less_than_5 = less_than_5+1
    if num<10:
        less_than_10 = less_than_10+1
print('Total: %d' % len(number_of_candidates_if_include_original_word))
print('Zero: %d' % zero)
print('One: %d' % one)
print('Less than 5: %d' % less_than_5)
print('Less than 10: %d' % less_than_10)