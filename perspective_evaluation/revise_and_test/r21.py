# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 18:50:16 2017

@author: liyuchen
"""

from add_spelling_errors import readTag, modify_key_words_5_ways_readTag, modify_key_words_5_ways_readTag_invalid, modify_key_words_5_ways_readTag_invalid_v2, load_toxic_word
from fetch_toxic_score import fetch_toxic_score_online, fetch_toxic_score_list_online
from sentence_toxic_tsv import sentence_toxic_read_file
import codecs
import string
from find_toxic_word import most_toxic_word
import pickle

'''
(1) Delete all punctuations of a sentence 
(2) Test its toxic score on Google Perpective API 
(3) Modify each key words in the sentence one at a time, and test toxic score on API
(4) record the (toxic score, sentence, method) tuples, including the original sentence
the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate, -1 - original
input:
    sentence - a sentence as a string
output:
    Sentences_Scores - a list of (score, sentence, method, original_word, new_word) tuples, where each sentence is 
                       without punctuations, and the first pair is for the original sentence
'''
def revise_sentence_and_test_5_ways(indices,sentence):
    Sentences_Scores = []    
    score = fetch_toxic_score_online(sentence)
    Sentences_Scores.append((score,sentence,-1,None))
    
    Modified_Sentences_And_Words = modify_key_words_5_ways_readTag(indices,sentence)
    for l in Modified_Sentences_And_Words:
        #print(l)
        score = fetch_toxic_score_online(l[0])
        Sentences_Scores.append((score,l[0],l[1],l[2]))
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
    Sentences_Scores - a list of (score, sentence, method, original_word, new_word) tuples, where each sentence is 
                       without punctuations, and the first pair is for the original sentence
'''
def revise_sentence_and_test_5_ways_invalid(indices,sentence):
    Sentences_Scores = []    
    score = fetch_toxic_score_online(sentence)
    Sentences_Scores.append((score,sentence,-1,None,None))
    
    Modified_Sentences_And_Words = modify_key_words_5_ways_readTag_invalid(indices,sentence)
    for l in Modified_Sentences_And_Words:
        #print(l)
        score = fetch_toxic_score_online(l[0])
        try:
            Sentences_Scores.append((score,l[0],l[1],l[2],l[3]))
        except:
            pass
    return Sentences_Scores
    
'''
- added on 2017.5.15
Difference from the above:
(1) do not include ' ' in revise method "add".
(2) try 10 times to add an error to a word, if it is still in the dictionary in all 10 times, try to add an star ( * ) into the word
- especially "add" and "replace"
- keep the original way for "permute"
(3) "delete" can be used only for word with length >= 8
(4) cancel the "separation" method

What the program does:
(1) Delete all punctuations of a sentence 
(2) Test its toxic score on Google Perpective API 
(3) Modify each key words in the sentence one at a time, and test toxic score on API
(4) record the (toxic score, sentence, method) tuples, including the original sentence
the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate, -1 - original
input:
    sentence - a sentence as a string
output:
    Sentences_Scores - a list of (score, sentence, method, original_word, new_word_list) tuples, where each sentence is 
                       without punctuations, and the first pair is for the original sentence
'''
def revise_sentence_and_test_5_ways_invalid_v2(indices,sentence):
    Sentences_Scores = []    
    score = fetch_toxic_score_online(sentence)
    Sentences_Scores.append((score,sentence,-1,None,None))
    
    Modified_Sentences_And_Words = modify_key_words_5_ways_readTag_invalid_v2(indices,sentence)
    for l in Modified_Sentences_And_Words:
        #print(l)
        score = fetch_toxic_score_online(l[0])
        try:
            Sentences_Scores.append((score,l[0],l[1],l[2],l[3]))
            if (l[1]==4):
                print('revise_sentence_and_test_5_ways_invalid_v2 bug: method==separation')
                print(l)
        except:
            print('len(l)<4:',l)
            pass
        #Sentences_Scores.append((score,l[0],l[1],l[2],l[3]))
    return Sentences_Scores

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
def revise_sentence_and_test_list_5_ways(selected_inds, selected_words, tok_sent, Folder_List=0, out_file_name_prefix=0):
    All_Sentences_Scores = [[],[],[],[],[]]
    count = 0    
    for i in range(len(selected_inds)):
        count = count+1
        if (count%100==0):
            print('\t%d sentences processed' % count)
        #print('\t%d sentences processed' % count)
        Sentences_Scores = revise_sentence_and_test_5_ways(selected_inds[i],tok_sent[i])
        best_revise = sorted(Sentences_Scores)[0]
        if (len(best_revise)<4):
            print(best_revise)
        revised_toxic_score = best_revise[0]
        revised_sentence = best_revise[1]
        revised_method = best_revise[2]
        revised_word = best_revise[3]
        if ((Sentences_Scores[0][0] != -1) and (revised_toxic_score != -1)):
            print('\tmethod:',revised_method,Sentences_Scores[0][0],revised_toxic_score)
            All_Sentences_Scores[revised_method].append((Sentences_Scores[0][1],Sentences_Scores[0][0],revised_sentence,revised_toxic_score, revised_word))
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
def revise_sentence_and_test_list_5_ways_invalid(selected_inds, selected_words, tok_sent, Folder_List=0, out_file_name_prefix=0):
    All_Sentences_Scores = [[],[],[],[],[]]
    count = 0    
    for i in range(len(selected_inds)):
        count = count+1
        Sentences_Scores = revise_sentence_and_test_5_ways_invalid(selected_inds[i],tok_sent[i])
        best_revise = sorted(Sentences_Scores)[0]
        if (len(best_revise)<5):
            print('best_revise:',best_revise)
            print('len(best_revise)<5 for index =',i)
            print(Sentences_Scores)
        revised_toxic_score = best_revise[0]
        revised_sentence = best_revise[1]
        revised_method = best_revise[2]
        revised_word = best_revise[3]
        new_word = best_revise[4]
        if ((Sentences_Scores[0][0] != -1) and (revised_toxic_score != -1)):
            print('\tmethod:',revised_method,Sentences_Scores[0][0],revised_toxic_score)
            All_Sentences_Scores[revised_method].append((Sentences_Scores[0][1],Sentences_Scores[0][0],revised_sentence,revised_toxic_score, revised_word, new_word))
        if (count%10==0):
            print('\t%d sentences processed' % count)
            #print('\t%d sentences processed' % count)
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
                    try:
                        for j in range(4):  
                            #print(All_Sentences_Scores[i][j]) 
                            temp.write(str(All_Sentences_Scores[k][i][j])+'\n')
                        temp.write(str(All_Sentences_Scores[k][i][4])+', '+str(All_Sentences_Scores[k][i][5])+';\n')
                        temp.write('\n')   
                    except:
                        pass
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
 - added on 2017.5.15 
Difference from the above: 
(1) see revise_sentence_and_test_5_ways_invalid_v2
(2) for each sentence, add errors only to the world determined in find_toxic_word.most_toxic_word
to be the most toxic word in the sentence 

Return a list of (rev_id, sentence, toxic_score, revised_sentence, revised_toxic_score, method)
input:
    Sentence_And_Toxic_Word - a list of (toxic_score, sentence, most_toxic_word)
    Folder_List - (optional) a list of folders that store the outputs for the 5 methods of revision
    out_file_name_prefix - (optional) the prefix of the output file name
output:
    All_Sentences_Scores - a list [0..4] of list of (original_sentence, original_score, revised_sentence, revised_toxic_score, revised_word, new_word)
effect (below to be revised):
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
def revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word, Folder_List=0, out_file_name_prefix=0):
    All_Sentences_Scores = [[],[],[],[],[]]
    count = 0    
    for i in range(len(Sentence_And_Toxic_Word)):
        count = count+1
        Words_In_Sentence = Sentence_And_Toxic_Word[i][1].split()
        indices = [j for j, x in enumerate(Words_In_Sentence) if x == Sentence_And_Toxic_Word[i][2]]
        Sentences_Scores = revise_sentence_and_test_5_ways_invalid_v2(indices[0:1],Sentence_And_Toxic_Word[i][1])
        best_revise = sorted(Sentences_Scores)[0]
        if (len(best_revise)<5):
            print('best_revise:',best_revise)
            print('len(best_revise)<5 for index =',i)
            print(Sentences_Scores)
        revised_toxic_score = best_revise[0]
        revised_sentence = best_revise[1]
        revised_method = best_revise[2]
        revised_word = best_revise[3]
        new_word = best_revise[4]
        if ((Sentences_Scores[0][0] != 2) and (revised_toxic_score != 2)):
            print('\tmethod:',revised_method,Sentences_Scores[0][0],revised_toxic_score)
            All_Sentences_Scores[revised_method].append((Sentences_Scores[0][1],Sentences_Scores[0][0],revised_sentence,revised_toxic_score, revised_word, new_word))
        if (count%10==0):
            print('\t%d sentences processed' % count)
    
    if (len(All_Sentences_Scores[4]) > 0):
        print('revise_sentence_and_test_list_5_ways_invalid_v2 bug: method==separation not empty')
        print(All_Sentences_Scores[4])
        
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
                    try:
                        for j in range(4):  
                            #print(All_Sentences_Scores[i][j]) 
                            temp.write(str(All_Sentences_Scores[k][i][j])+'\n')
                        for j in range(len(All_Sentences_Scores[k][i][5])):
                            temp.write(str(All_Sentences_Scores[k][i][4])+', '+str(All_Sentences_Scores[k][i][5][j])+'; ')
                        temp.write('\n\n')   
                    except:
                        pass
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


#selected_inds, selected_words, tok_sent = readTag("tagged_test_toxic_data.txt")
#print('Number of sentences:',len(selected_inds))

Sentence_And_Toxic_Word = load_toxic_word('Sentence_And_Toxic_Word.pickle')
print('number of sentences: ',len(Sentence_And_Toxic_Word))

# 10 sentences per batch
folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for i in range( 200, 210):
    print('Processing the %d-th batch of 10 sentences\n' % i)
    All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word[i*10:i*10+10], Folder_List, str(i)+'_')
    #print(len(All_Sentences_Scores))
    out_file_name = 'All_Sentences_Scores/All_Sentences_Scores'+str(i)+'.pickle'
    with open(out_file_name, "wb") as handle:
        pickle.dump(All_Sentences_Scores, handle)
    

'''
# 100 sentences per batch
folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for i in range(0,int(len(selected_inds)/100)+1):
    print('Processing the %d-th batch of 100 sentences\n' % i)
    All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid(selected_inds[i*100:i*100+100], selected_words[i*100:i*100+100], tok_sent[i*100:i*100+100], Folder_List, 'sentences_and_revised_scores'+str(i)+'_')
    #print(len(All_Sentences_Scores))
'''


## 10 sentences per batch
#folder_prefix = 'output/separated_by_revised_type/'
#Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
#for i in range(0,int(len(selected_inds)/10)+1):
#    print('Processing the %d-th batch of 10 sentences\n' % i)
#    All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid(selected_inds[i*10:i*10+10], selected_words[i*10:i*10+10], tok_sent[i*10:i*10+10], Folder_List, str(i)+'_')
#    #print(len(All_Sentences_Scores))


#==============================================================================
# # debug
# selected_inds, selected_words, tok_sent = readTag("tagged_test_toxic_data.txt")
# print(tok_sent[1])
# #selected_inds = 
# #selected_words = 
# #tok_sent = 
# All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid(selected_inds[1:2], selected_words[1:2], tok_sent[1:2])
# 
#==============================================================================