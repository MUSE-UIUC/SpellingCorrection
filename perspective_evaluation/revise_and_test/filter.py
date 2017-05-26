# -*- coding: utf-8 -*-
"""
Created on Tue May 23 18:40:42 2017

(1) check the (sentence, most toxic word) list. 
- If len(most toxic word) <= 2
- If the most toxic word appears less than 100 times in the dictionary, then discard the sentence.
- if the most toxic word is auxiliary verb
(2) check how many sentences are deleted.

@author: liyuchen
"""

import pickle
from corpus_util import loadDict
import codecs

'''
Read a file containing groups separated by newline characters, in which
k lines form a group. Each patter contains the k lines and an additional empty line.
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

# for i = 0..4
# All_Sentences_Scores[i] is a list of 
# (original_sentence, original_score, revised_sentence, revised_toxic_score, old_word, new_word_list) tuples
All_Sentences_Scores = []
for i in range(5):
    All_Sentences_Scores.append([])

# find the data files whose new_word is an empty string.
empty_inds = []

# read data files and create a single pickle file to store them
folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add/',folder_prefix+'delete/',folder_prefix+'replace/',folder_prefix+'permute/']

for i in range(len(Folder_List)):
    folder = Folder_List[i]
    for j in range(361):
        fn = folder+str(j)+'_method'+str(i)+'.txt'
        List_Of_List = read_k_tuples(fn, 5)
        for group in List_Of_List:
            # [original_sentence, original_score, new_sentence, new_score, correct word and wrong word pairs, empty line]
            original_sentence = group[0]
            original_score = group[1]
            new_sentence = group[2]
            new_score = group[3]
            correct_and_wrong_word_pairs = group[4].replace(';',' ').replace(',',' ').split()
            correct_word = correct_and_wrong_word_pairs[0]
            if (correct_and_wrong_word_pairs.count(correct_word) != len(correct_and_wrong_word_pairs)/2):
                print('bug: new word is empty', folder, j)
                print(correct_word)
                empty_inds.append(j)
            else:
                new_word_list = []
                k = 1
                while (k<len(correct_and_wrong_word_pairs)):
                    new_word_list.append(correct_and_wrong_word_pairs[k])
                    k = k+2
                All_Sentences_Scores[i].append((original_sentence, original_score, new_sentence, new_score, correct_word, new_word_list))
    
#        try:
#            List_Of_List = read_k_tuples(fn, 6)
#            for group in List_Of_List:
#                # [original_sentence, original_score, new_sentence, new_score, correct word and wrong word pairs, empty line]
#                original_sentence = group[0]
#                original_score = group[1]
#                new_sentence = group[2]
#                new_score = group[3]
#                correct_and_wrong_word_pairs = re.findall(r"[\w']+", group[4])
#                correct_word = correct_and_wrong_word_pairs[0]
#                if (correct_and_wrong_word_pairs.count(correct_word) != len(correct_and_wrong_word_pairs)/2):
#                    print('bug: new word is empty', folder, j)
#                else:
#                    new_word_list = []
#                    k = 1
#                    while (k<len(correct_and_wrong_word_pairs)):
#                        new_word_list.append(correct_and_wrong_word_pairs[k])
#                        k = k+2
#                    All_Sentences_Scores[i].append((original_sentence, original_score, new_sentence, new_score, correct_word, new_word_list))
#        except:
#            print('bug:', folder, j)
            
with open("All_Sentences_Scores.pickle", "wb") as handle:
    pickle.dump(All_Sentences_Scores, handle)
    
print('empty_inds:',empty_inds)
print('data size before filtering:', len(All_Sentences_Scores[0])+len(All_Sentences_Scores[1])+len(All_Sentences_Scores[2])+len(All_Sentences_Scores[3])+len(All_Sentences_Scores[4]))



#(1) check the (sentence, most toxic word) list. 
#- If len(most toxic word) <= 2
#- If the most toxic word appears less than 100 times in the dictionary, then discard the sentence.
#- if the most toxic word is auxiliary verb
#(2) check how many sentences are deleted.


All_Sentences_Scores_Filtered = []
for i in range(5):
    All_Sentences_Scores_Filtered.append([])
    
cnt = loadDict()
Auxiliary_Verbs = ['be', 'am', 'are', 'is', 'was', 'were', 'being', 'been', 'can', 'could', 'dare', 'do', 'does', 'did', 'have' 'has', 'had', 'having', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']

count_len_at_most_2 = 0
count_freq_less_than_100 = 0
count_auxiliary_verb = 0

for i in range(5):
    for j in range(len(All_Sentences_Scores[i])):
        flag = True
        if (len(All_Sentences_Scores[i][j][4]) <= 2):
            flag = False
            count_len_at_most_2 = count_len_at_most_2 + 1
        if (cnt[All_Sentences_Scores[i][j][4]] < 100):
            flag = False
            count_freq_less_than_100 = count_freq_less_than_100 + 1
        if (All_Sentences_Scores[i][j][4] in Auxiliary_Verbs):
            flag = False
            count_auxiliary_verb = count_auxiliary_verb + 1
        if (flag):
            All_Sentences_Scores_Filtered[i].append(All_Sentences_Scores[i][j])

with open("All_Sentences_Scores_Filtered.pickle", "wb") as handle:
    pickle.dump(All_Sentences_Scores_Filtered, handle)
            
print('data size after filtering:', len(All_Sentences_Scores_Filtered[0])+len(All_Sentences_Scores_Filtered[1])+len(All_Sentences_Scores_Filtered[2])+len(All_Sentences_Scores_Filtered[3])+len(All_Sentences_Scores_Filtered[4]))
print('count_len_at_most_2:',count_len_at_most_2)
print('count_freq_less_than_100:',count_freq_less_than_100)
print('count_auxiliary_verb:',count_auxiliary_verb)