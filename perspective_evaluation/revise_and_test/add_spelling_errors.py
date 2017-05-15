# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 14:58:27 2017

@author: liyuchen

This file contrains functions that can be used to deliberately add mis-spellings
to sentences.
"""

import random
import string
from corpus_util import loadDict
    
"""
    - added on 2017.4.30 
    input: fn - pos-tagged file
    output: a list of a list of inds, a list of a list of words, a list of sentences
"""
def readTag(fn):
    TARGET_TAG_SET = ["V", "N", "A"]    
    f = open(fn, "r")
    lines = f.readlines()
    selected_inds = []
    selected_words = []
    tok_sent = []
    for line in lines:
        try:
            sent, tag, score, orig_sent = line.strip().split("\t")
        except:
            continue
        tag_seq = tag.split()
        sent_seq = sent.split()
        inds = [ind for ind in range(len(tag_seq)) if tag_seq[ind] in TARGET_TAG_SET]
        selected_inds.append(inds[:])
        words = [sent_seq[ind] for ind in inds]
        selected_words.append(words[:])
        tok_sent.append(sent)
        #if (len(selected_words)>=2):
        #    break
    return selected_inds, selected_words, tok_sent
    
'''
A method to change a word that maintains edit distance 1
input:
    word - the input word
output:
    modified_word - a word that has edit distance 1 from the input word
'''
def change_a_word_dis1(word):
    Alphabet_List = list(string.ascii_lowercase)
    Alphabet_List.append(' ')
    
    # 0 - add
    # 1 - delete
    # 2 - change    
    method = random.randint(0, 2)
    
    if (method==0):
        pos = random.randint(0, len(word))
        word1 = word[0:pos]
        word2 = word[pos:len(word)]
        add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+add+word2
        
    elif (method==1):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        return word1+word2
        
    elif (method==2):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        change = word[pos]
        while (change==word[pos]):        
            change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+change+word2

'''
A method to change a word that randomly picks one of {add 1 char, delete 1 char, 
replace 1 char, permute 2 adjacent chars, separate all chars with ' '}.
input:
    word - the input word
output:
    modified_word - a word that has edit distance 1 from the input word
    method - the method used to modify. (0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate)
'''
def change_a_word_5_ways(word):
    Alphabet_List = list(string.ascii_lowercase)
    Alphabet_List.append(' ')
    
    # 0 - add
    # 1 - delete
    # 2 - replace  
    # 3 - permute
    # 4 - separate
    method = random.randint(0, 4) # if method>4, then no return value
    
    if (method==0):
        pos = random.randint(0, len(word))
        word1 = word[0:pos]
        word2 = word[pos:len(word)]
        add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+add+word2, 0
        
    elif (method==1):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        return word1+word2, 1
        
    elif (method==2):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        change = word[pos]
        while (change==word[pos]):        
            change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
        return word1+change+word2, 2
        
    elif (method==3):
        if (len(word)<=1):
            return word, 3
        else:
            pos = random.randint(0, len(word)-2)
            word1 = word[0:pos]
            word2 = word[pos+2:len(word)]
            return word1+word[pos+1]+word[pos]+word2, 3
        
    elif (method==4):
        modified_word = ''        
        for c in list(word):
            modified_word = modified_word+' '+c
        modified_word = modified_word[1:len(modified_word)]
        return modified_word, 4
        
'''
- added on 2017.5.13 
A method to change a word that randomly picks one of {add 1 char, delete 1 char, 
replace 1 char, permute 2 adjacent chars, separate all chars with ' '}.
input:
    word - the input word
output:
    modified_word - a word that has edit distance 1 from the input word
    method - the method used to modify. (0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate)
effect:
    make sure that the revised word cannot be a valid word in the dictionary
'''
def change_a_word_5_ways_invalid(word):
    Alphabet_List = list(string.ascii_lowercase)
    Alphabet_List.append(' ')
    cnt = loadDict()
    
    # 0 - add
    # 1 - delete
    # 2 - replace  
    # 3 - permute
    # 4 - separate
    method = random.randint(0, 4) # if method>4, then no return value
    ret_word_and_method = ('',-1)
    count = 0
    ret_flag = False
    
    while (ret_flag == False and count < 10):
        
        count = count + 1
    
        if (method==0):
            pos = random.randint(0, len(word))
            word1 = word[0:pos]
            word2 = word[pos:len(word)]
            add = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method = (word1+add+word2, 0)
            
        elif (method==1):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            ret_word_and_method = (word1+word2, 1)
            
        elif (method==2):
            pos = random.randint(0, len(word)-1)
            word1 = word[0:pos]
            word2 = word[pos+1:len(word)]
            change = word[pos]
            while (change==word[pos]):        
                change = Alphabet_List[random.randint(0, len(Alphabet_List)-1)]
            ret_word_and_method =( word1+change+word2, 2)
            
        elif (method==3):
            if (len(word)<=1):
                ret_word_and_method = (word, 3)
            else:
                pos = random.randint(0, len(word)-2)
                word1 = word[0:pos]
                word2 = word[pos+2:len(word)]
                ret_word_and_method = (word1+word[pos+1]+word[pos]+word2, 3)
            
        elif (method==4):
            modified_word = ''        
            for c in list(word):
                modified_word = modified_word+' '+c
            modified_word = modified_word[1:len(modified_word)]
            ret_word_and_method = (modified_word, 4)
            
        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag == True
            
    return ret_word_and_method[0], ret_word_and_method[1]

'''
Modify certain words in a sentence
input:
    sentence - a string representing the sentence
    Words_List - a list of words that should be modified
output:
    Modified_Sentences - a list of sentences, with each being the input sentence
                         with one word from Words_List modified. (without punctuations)
'''
def modify_one_word_dis1(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()
    #print(Words_In_Sentence)
    Modified_Sentences = []
    #print(Words_List)    
    for word in Words_List:
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        #print(New_Words_In_Sentence)
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        #print(Indices)
        for i in Indices:
            #print(New_Words_In_Sentence[i])
            New_Words_In_Sentence[i] = change_a_word_dis1(New_Words_In_Sentence[i])
            #print(New_Words_In_Sentence[i])
        new_sentence = ''
        for w in New_Words_In_Sentence:
            new_sentence = new_sentence + w + ' '
        Modified_Sentences.append(new_sentence)
    return Modified_Sentences

'''
Modify certain words in a sentence that are likely to be important in feeling
input:
    sentence - a string representing the sentence
output:
    Modified_Sentences - a list of sentences, with each being the input sentence
                         with one word that are likely to be important in feeling modified.
'''
#def modify_key_words_dis1(sentence):
#    #Words_In_Sentence = sentence.split()
#    selected_word_list = getContentWords([sentence])
#    selected_word_list = list(set(selected_word_list[0]))
#    Modified_Sentences = modify_one_word_dis1(sentence, selected_word_list)
#    return Modified_Sentences
    
'''
Modify certain words in a sentence
input:
    sentence - a string representing the sentence
    Words_List - a list of words that should be modified
output:
    Modified_Sentences - a list of [sentence, method] list, with each being the input sentence
                         with one word from Words_List modified (punctuations are deleted), and
                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
                         4 - separate
'''
def modify_one_word_5_ways(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()
    #print(Words_In_Sentence)
    Modified_Sentences = []
    #print(Words_List)    
    for word in Words_List:
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        #print(New_Words_In_Sentence)
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        #print(Indices)
        method = -1        
        for i in Indices:
            #print(New_Words_In_Sentence[i])
            #print(type(New_Words_In_Sentence))
            #s = New_Words_In_Sentence            
            #print('s=',s)            
            New_Words_In_Sentence[i], method = change_a_word_5_ways(New_Words_In_Sentence[i])            
            #print(New_Words_In_Sentence[i])
        new_sentence = ''
        for w in New_Words_In_Sentence:
            new_sentence = new_sentence + w + ' '
        Modified_Sentences.append([new_sentence, method])
    return Modified_Sentences
    
'''
- added on 2017.5.13 
Modify certain words in a sentence
input:
    sentence - a string representing the sentence
    Words_List - a list of words that should be modified
output:
    Modified_Sentences - a list of [sentence, method, original_sentence, new_sentence] list, with each being the input sentence
                         with one word from Words_List modified (punctuations are deleted), and
                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
                         4 - separate
effect:
    make sure that the revised word cannot be a valid word in the dictionary
'''
def modify_one_word_5_ways_invalid(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p,'')
    Words_In_Sentence = s_wo_punctuation.split()

    Modified_Sentences = []
  
    for word in Words_List:
        for p in list(string.punctuation):
            word = word.replace(p,'')
        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        if (len(Indices)>0):  
            method = -1        
            for i in Indices:
                New_Words_In_Sentence[i], method = change_a_word_5_ways_invalid(New_Words_In_Sentence[i])            
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([new_sentence, method, word, New_Words_In_Sentence[Indices[0]]])
    return Modified_Sentences
    
#'''
#- added on 2017.5.14 (debug)
#Modify certain words in a sentence
#input:
#    sentence - a string representing the sentence
#    Words_List - a list of words that should be modified
#output:
#    Modified_Sentences - a list of [sentence, method, original_sentence, new_sentence] list, with each being the input sentence
#                         with one word from Words_List modified (punctuations are deleted), and
#                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
#                         4 - separate
#effect:
#    make sure that the revised word cannot be a valid word in the dictionary
#'''
#def modify_one_word_5_ways_invalid(sentence, Words_List):
#    s_wo_punctuation = sentence
#    for p in list(string.punctuation):
#        s_wo_punctuation = s_wo_punctuation.replace(p,'')
#    Words_In_Sentence = s_wo_punctuation.split()
#
#    Modified_Sentences = []
#    for word in Words_List[25::]:
#        for p in list(string.punctuation):
#            word = word.replace(p,'')
#        New_Words_In_Sentence = Words_In_Sentence[:] # Note that Python by default passes by reference
#        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
#        method = -1        
#        for i in Indices:
#            New_Words_In_Sentence[i], method = change_a_word_5_ways_invalid(New_Words_In_Sentence[i])            
#        new_sentence = ''
#        for w in New_Words_In_Sentence:
#            new_sentence = new_sentence + w + ' '
#        try:
#            Modified_Sentences.append([new_sentence, method, word, New_Words_In_Sentence[Indices[0]]])
#        except:
#            print(Indices)
#            print(Words_In_Sentence)
#            print('word:',word)
#            print(New_Words_In_Sentence)
#            print(method)
#            
#    return Modified_Sentences

'''
Modify certain words in a sentence that are likely to be important in feeling
input:
    sentence - a string representing the sentence
output:
    Modified_Sentences - a list of [sentence, method] list, with each being the input sentence
                         with one word that are likely to be important in feeling modified. 
                         (punctuations are deleted) and
                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
                         4 - separate
'''
#def modify_key_words_5_ways(sentence):
#    #Words_In_Sentence = sentence.split()
#    selected_word_list = getContentWords([sentence])
#    selected_word_list = list(set(selected_word_list[0]))
#    Modified_Sentences = modify_one_word_5_ways(sentence, selected_word_list)
#    return Modified_Sentences

'''
- added on 2017.5.4 
Modify certain words in a sentence that are likely to be important in feeling
input:
    indices - a list of indices of keywords
    sentence - a string representing the sentence
output:
    Modified_Sentences_And_Words - a list of [sentence, method, revised_word] list, 
                         with each being the input sentence with one word that are 
                         likely to be important in feeling modified. (punctuations are deleted) and
                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
                         4 - separate
'''

def modify_key_words_5_ways_readTag(indices,sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list)) # unique
    Modified_Sentences = modify_one_word_5_ways(sentence, selected_word_list)
    #print(Modified_Sentences)
    Modified_Sentences_And_Words = [[Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i]] for i in range(len(selected_word_list))]
    #print(Modified_Sentences_And_Words)    
    return Modified_Sentences_And_Words 
    
'''
- added on 2017.5.13 
Modify certain words in a sentence that are likely to be important in feeling
input:
    indices - a list of indices of keywords
    sentence - a string representing the sentence
output:
    Modified_Sentences_And_Words - a list of [sentence, method, original_word, new_word] list, 
                         with each being the input sentence with one word that are 
                         likely to be important in feeling modified. (punctuations are deleted) and
                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
                         4 - separate
effect:
    make sure that the revised word cannot be a valid word in the dictionary
'''

def modify_key_words_5_ways_readTag_invalid(indices,sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list)) # unique
    Modified_Sentences = modify_one_word_5_ways_invalid(sentence, selected_word_list)
    #print(Modified_Sentences)
    Modified_Sentences_And_Words = [[Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i], Modified_Sentences[i][3]] for i in range(len(selected_word_list))]
    #print(Modified_Sentences_And_Words)    
    return Modified_Sentences_And_Words 
    
'''
Main
'''
'''
selected_inds, selected_words, tok_sent = readTag("tagged_test.txt")
print (selected_inds[0:2],'\n\n')
print (selected_words[0:2],'\n\n')
print (tok_sent[0:2],'\n\n')

for i in range(2):
    Modified_Sentences_And_Words = modify_key_words_5_ways_readTag(selected_inds[i],tok_sent[i])
    print(Modified_Sentences_And_Words)
'''