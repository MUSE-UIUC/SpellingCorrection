# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 18:50:16 2017

@author: liyuchen
"""

from add_spelling_errors import modify_key_words_5_ways
from fetch_toxic_score import fetch_toxic_score_online, fetch_toxic_score_list_online
from sentence_toxic_tsv import sentence_toxic_read_file
import codecs
import string


'''
(1) Delete all punctuations of a sentence 
(2) Test its toxic score on Google Perpective API 
(3) Modify each key words in the sentence one at a time, and test toxic score on API
(4) record the (toxic score, sentence) pairs, including the original sentence
input:
    sentence - a sentence as a string
output:
    Sentences_Scores - a list of (score, sentence) pairs, where each sentence is without punctuations. 
                       and the first pair is for the original sentence
'''
def revise_sentence_and_test(sentence):
    Sentences_Scores = []    
    s_wo_punctuation = sentence    
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    score = fetch_toxic_score_online(s_wo_punctuation)
    Sentences_Scores.append((score,s_wo_punctuation))
    
    Modified_Sentences = modify_key_words(s_wo_punctuation)
    for s in Modified_Sentences:
        #print(s)
        score = fetch_toxic_score_online(s)
        Sentences_Scores.append((score,s))
    return Sentences_Scores

'''
(1) Delete all punctuations of a sentence 
(2) Test its toxic score on Google Perpective API 
(3) Modify each key words in the sentence one at a time, and test toxic score on API
(4) record the (toxic score, sentence, method) tuples, including the original sentence
the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate, -1 - original
input:
    sentence - a sentence as a string
output:
    Sentences_Scores - a list of (score, sentence, method) tuples, where each sentence is 
                       without punctuations, and the first pair is for the original sentence
'''
def revise_sentence_and_test_5_ways(sentence):
    Sentences_Scores = []    
    s_wo_punctuation = sentence    
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    score = fetch_toxic_score_online(s_wo_punctuation)
    Sentences_Scores.append((score,s_wo_punctuation,-1))
    
    Modified_Sentences = modify_key_words_5_ways(s_wo_punctuation)
    for l in Modified_Sentences:
        #print(l[0])
        score = fetch_toxic_score_online(l[0])
        Sentences_Scores.append((score,l[0],l[1]))
    return Sentences_Scores

'''
Return a list of (rev_id, sentence, toxic_score, revised_sentence, revised_toxic_score)
input:
    Sentences_With_Labels - a list of (toxicity, sentence, rev_id)
    out_file_name - (optional) the name of the output file
output:
    All_Sentences_Scores - a list of (rev_id, sentence, toxic_score, revised_sentence, revised_toxic_score)
effect:
for each sentence in the input 
(1) Call the function revise_sentence_and_test, including
- delete all punctuations of a sentence 
- test its toxic score on Google Perpective API 
- modify each key words in the sentence one at a time, and test toxic score on API
- record the (sentence,toxic) pairs, including the original sentence
(2) pick the revised sentence with the lowest toxic score
(3) append (rev_id, sentence, toxic_score, revised_sentence, revised_toxic_score) to the 
list to be returned
(4) record the returned list of tuples on out_file_name
'''
def revise_sentence_and_test_list(Sentences_With_Labels, out_file_name=0):
    All_Sentences_Scores = []
    count = 0    
    for tup in Sentences_With_Labels:
        count = count+1
        if (count%100==0):
            print('\t%d sentences processed' % count)
        #print('\t%d sentences processed' % count)
        Sentences_Scores = revise_sentence_and_test(tup[1])
        best_revise = sorted(Sentences_Scores)[0]  
        revised_toxic_score = best_revise[0]
        revised_sentence = best_revise[1]
        if ((Sentences_Scores[0][0] != -1) and (revised_toxic_score != -1)):
            All_Sentences_Scores.append((tup[2],Sentences_Scores[0][1],Sentences_Scores[0][0],revised_sentence,revised_toxic_score))
    if (out_file_name != 0):
        with codecs.open(out_file_name, "w", "utf-8-sig") as temp:
            for i in range(0,len(All_Sentences_Scores)):
                for j in range(len(All_Sentences_Scores[i])):  
                    #print(All_Sentences_Scores[i][j])                
                    temp.write(str(All_Sentences_Scores[i][j]))
                    temp.write('\n')
                temp.write('\n')
            temp.close()
#        outFile=open(out_file_name,'wt')
#        for i in range(0,len(All_Sentences_Scores)):
#            for j in range(len(All_Sentences_Scores[i])):  
#                print(All_Sentences_Scores[i][j])                
#                outFile.write(str(All_Sentences_Scores[i][j]))
#                outFile.write('\n')
#            outFile.write('\n')
#        outFile.close()   
    return All_Sentences_Scores

'''
Return a list of (rev_id, sentence, toxic_score, revised_sentence, revised_toxic_score, method)
input:
    Sentences_With_Labels - a list of (toxicity, sentence, rev_id)
    out_file_name - (optional) the prefix of the output file name
    Folder_List - (optional) a list of folders that store the outputs for the 5 methods of revision
output:
    All_Sentences_Scores - a list of (rev_id, sentence, toxic_score, revised_sentence, revised_toxic_score, method)
effect:
for each sentence in the input 
(1) Call the function revise_sentence_and_test, including
- delete all punctuations of a sentence 
- test its toxic score on Google Perpective API 
- modify each key words in the sentence one at a time, and test toxic score on API
- record the (toxic_score, sentence, method) tuples, including the original sentence
- the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate, -1 - original
(2) pick the revised sentence with the lowest toxic score
(3) append (rev_id, sentence, toxic_score, revised_sentence, revised_toxic_score, method) to the 
list to be returned
(4) record the returned list of tuples on five output files named out_file_name_prefix+str(method)
'''
def revise_sentence_and_test_list_5_ways(Sentences_With_Labels, Folder_List=0, out_file_name_prefix=0):
    All_Sentences_Scores = [[],[],[],[],[]]
    count = 0    
    for tup in Sentences_With_Labels:
        count = count+1
        if (count%100==0):
            print('\t%d sentences processed' % count)
        #print('\t%d sentences processed' % count)
        Sentences_Scores = revise_sentence_and_test_5_ways(tup[1])
        best_revise = sorted(Sentences_Scores)[0]
        if (len(best_revise)<3):
            print(best_revise)
        revised_toxic_score = best_revise[0]
        revised_sentence = best_revise[1]
        revised_method = best_revise[2]
        if ((Sentences_Scores[0][0] != -1) and (revised_toxic_score != -1)):
            print('\tmethod:',revised_method)
            All_Sentences_Scores[revised_method].append((tup[2],Sentences_Scores[0][1],Sentences_Scores[0][0],revised_sentence,revised_toxic_score))
    if (out_file_name_prefix != 0):
        for k in range(5):        
            if (Folder_List != 0):
                out_file_name = Folder_List[k]+'/'
            else:
                out_file_name = ''
            out_file_name = out_file_name + out_file_name_prefix + 'method'+str(k)+'.txt'
            with codecs.open(out_file_name, "w", "utf-8-sig") as temp:
                #print('\twriting to folder',k)
                for i in range(0,len(All_Sentences_Scores[k])):
                    #print(k)
                    for j in range(len(All_Sentences_Scores[k][i])):  
                        #print(All_Sentences_Scores[i][j]) 
                        temp.write(str(All_Sentences_Scores[k][i][j]))
                        temp.write('\n')
                    temp.write('\n')
                temp.close()
    #        outFile=open(out_file_name,'wt')
    #        for i in range(0,len(All_Sentences_Scores)):
    #            for j in range(len(All_Sentences_Scores[i])):  
    #                print(All_Sentences_Scores[i][j])                
    #                outFile.write(str(All_Sentences_Scores[i][j]))
    #                outFile.write('\n')
    #            outFile.write('\n')
    #        outFile.close()   
    return All_Sentences_Scores



'''
Main
'''

'''
print('\nTesting function sentence_toxic_read_file: \n')
comments_file = 'data/toxicity_annotated_comments.tsv'
annotations_file = 'data/toxicity_annotations.tsv'
Sentences_With_Labels = sentence_toxic_read_file(comments_file, annotations_file, num_out=100)
#print(Sentences_With_Labels[99])
print(len(Sentences_With_Labels))

print('\nTesting function fetch_toxic_score_online: \n')
#print(fetch_toxic_score_online(Sentences_With_Labels[9999][1]))
#for i in range(10):
    #print(Sentences_With_Labels[i][1])    
    #print(fetch_toxic_score_online(Sentences_With_Labels[i][1]))

#print('\nTesting function revise_sentence_and_test: \n')
#Sentences_Scores = revise_sentence_and_test(Sentences_With_Labels[99][1])
#print(len(Sentences_Scores))
#for tup in Sentences_Scores:
#    print(tup)
#    
#print('\nTesting function revise_sentence_and_test_list: \n')
#All_Sentences_Scores = revise_sentence_and_test_list(Sentences_With_Labels[0:10], 'try_output.txt')
#print(len(All_Sentences_Scores))
#print(All_Sentences_Scores)

print('\nTesting function revise_sentence_and_test_5_ways: \n')
Sentences_Scores = revise_sentence_and_test_5_ways(Sentences_With_Labels[99][1])
print(len(Sentences_Scores))
#for tup in Sentences_Scores:
#    print(tup)
    
print('\nTesting function revise_sentence_and_test_list_5_ways: \n')
All_Sentences_Scores = revise_sentence_and_test_list_5_ways(Sentences_With_Labels[0:20], 'try_output')
len_count = 0
for i in range(5):
    len_count = len_count+len(All_Sentences_Scores[i])
print('len_count:',len_count)
#print(All_Sentences_Scores)
'''


comments_file = 'data/toxicity_annotated_comments.tsv'
annotations_file = 'data/toxicity_annotations.tsv'
Sentences_With_Labels = sentence_toxic_read_file(comments_file, annotations_file, num_out=10000)
print('last:',Sentences_With_Labels[len(Sentences_With_Labels)-1])
print(len(Sentences_With_Labels))

folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for i in range(34,int(len(Sentences_With_Labels)/100)+1):
    print('Processing the %d-th batch of 100 sentences\n' % i)
    All_Sentences_Scores = revise_sentence_and_test_list_5_ways(Sentences_With_Labels[i*100:i*100+100], Folder_List, 'sentences_and_revised_scores'+str(i)+'_')
    #print(len(All_Sentences_Scores))


#for i in range(3,100):
#    print('Processing the %d-th batch of 100 sentences\n' % i)
#    All_Sentences_Scores = revise_sentence_and_test_list(Sentences_With_Labels[i*100:i*100+100], 'all_sentences_and_revised_scores'+str(i)+'.txt')
#    print(len(All_Sentences_Scores))

#for i in range(3,4):
#    print('Processing the %d-th batch of 100 sentences\n' % i)
#    All_Sentences_Scores = revise_sentence_and_test_list(Sentences_With_Labels[i*100:i*100+100], 'all_sentences_and_revised_scores'+str(i)+'.txt')
#    print(len(All_Sentences_Scores))

#for i in range(311,315):
#    print('Processing the %d-th sentence\n' % i)
#    All_Sentences_Scores = revise_sentence_and_test_list(Sentences_With_Labels[i:i+1], 'output/all_sentences_and_revised_scores'+str(i)+'.txt')
#    print(len(All_Sentences_Scores))