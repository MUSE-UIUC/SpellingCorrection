# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 22:58:43 2017

@author: liyuchen
"""

import codecs
import matplotlib.pyplot as plt
import numpy as np
from closest_edit_distance import closest_words_edit_distance_pickle

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

List_Of_List = read_k_tuples('output/separated_by_revised_type/add/sentences_and_revised_scores0_method0.txt', 5)
for i in range(1,100):
    in_file_name = 'output/separated_by_revised_type/add/sentences_and_revised_scores'+str(i)+'_method0.txt'
    List_Of_List = List_Of_List+read_k_tuples(in_file_name, 5)

Folder_Names = ['add','delete','permute','replace','separate']
for j in range(1,5):
    if (j != 2 and j != 4):
        for i in range(100):
            in_file_name = 'output/separated_by_revised_type/'+Folder_Names[j]+'/sentences_and_revised_scores'+str(i)+'_method'+str(j)+'.txt'
            List_Of_List = List_Of_List+read_k_tuples(in_file_name, 5)

print(len(List_Of_List))

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
revised_words = []
for i in range(len(Revised_Sentences)):
    original_sentence_split = Original_Sentences[i].split()
    revised_sentence_split = Revised_Sentences[i].split()
    for j in revised_sentence_split:
        if j not in original_sentence_split:
            revised_words.append(j.lower())
revised_words = np.unique(revised_words)
print(len(revised_words))            

# Calculate the number of candidates with edit distance 1 for each revised word
for i in range(int(len(revised_words)/100)):
    out_file_name = 'count_output/dist1_candidate_numbers'+str(i)+'.txt'
    candidate_numbers = []
    with codecs.open(out_file_name, "w", "utf-8-sig") as temp:
        for j in range(100):
            word = revised_words[i*100+j]
            close_words = closest_words_edit_distance_pickle(word)
            candidate_numbers.append(len(close_words))
            temp.write(word)
            temp.write('\n')
            temp.write(str(len(close_words)))
            temp.write('\n')
            temp.write(', '.join(str(c) for c in close_words))
            temp.write('\n\n')
        temp.close()
    print(str(i*100),'words processed')

i = int(len(revised_words)/100)
out_file_name = 'count_output/dist1_candidate_numbers'+str(i)+'.txt'
candidate_numbers = []
with codecs.open(out_file_name, "w", "utf-8-sig") as temp:
    for j in range(100*i,len(revised_words)):
        word = revised_words[j]
        close_words = closest_words_edit_distance_pickle(word)
        candidate_numbers.append(len(close_words))
        temp.write(word)
        temp.write('\n')
        temp.write(str(len(close_words)))
        temp.write('\n')
        temp.write(', '.join(str(c) for c in close_words))
        temp.write('\n\n')
    temp.close()
print('all words processed')

'''
plt.plot(range(len(List_Of_List)),sorted(Original_Scores), label='original')
plt.plot(range(len(List_Of_List)),sorted(Revised_Scores), label='revised')
plt.legend(loc=0)
plt.xlabel('Example')
plt.ylabel('Score')
plt.title('Original vs. Revised Scores')
plt.show()
'''