# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 09:21:23 2017

@author: liyuchen
"""

import codecs
import matplotlib.pyplot as plt

def read_k_tuples(in_file_name, k):
    with codecs.open(in_file_name,'r',encoding='utf8') as f:
        content = f.read()
    List_Of_List = []
    if (content != ''):
        Content_List = content.split('\n')
        #print(len(Content_List))
        #print((len(Content_List)-1)/(k+1))
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
#List_Of_List = read_k_tuples('output/all_sentences_and_revised_scores0.txt', 5)
#for i in range(1,700):
#    in_file_name = 'output/all_sentences_and_revised_scores'+str(i)+'.txt'
#    List_Of_List = List_Of_List+read_k_tuples(in_file_name, 5)
    
List_Of_List = read_k_tuples('output/separated_by_revised_type/add/sentences_and_revised_scores0_method0.txt', 5)
for i in range(1,31):
    in_file_name = 'output/separated_by_revised_type/add/sentences_and_revised_scores'+str(i)+'_method0.txt'
    List_Of_List = List_Of_List+read_k_tuples(in_file_name, 5)

Folder_Names = ['add','delete','permute','replace','separate']
for j in range(1,5):
    for i in range(31):
        in_file_name = 'output/separated_by_revised_type/'+Folder_Names[j]+'/sentences_and_revised_scores'+str(i)+'_method'+str(j)+'.txt'
        List_Of_List = List_Of_List+read_k_tuples(in_file_name, 5)

print(len(List_Of_List))

Original_Sentences = []
Original_Scores = []
Revised_Sentences = []
Revised_Scores = []
for i in range(len(List_Of_List)):
    #print(i)
    Original_Sentences.append(List_Of_List[i][1])
    Original_Scores.append(float(List_Of_List[i][2]))
    Revised_Sentences.append(List_Of_List[i][3])
    Revised_Scores.append(float(List_Of_List[i][4]))
    
plt.plot(range(len(List_Of_List)),sorted(Original_Scores), label='original')
plt.plot(range(len(List_Of_List)),sorted(Revised_Scores), label='revised')
plt.legend(loc=0)
plt.xlabel('Example')
plt.ylabel('Score')
plt.title('Original vs. Revised Scores')
plt.show()