# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 14:58:27 2017

@author: liyuchen

This file contrains functions that can be used to deliberately add mis-spellings
to sentences.
"""

import random
import string
from corpus_util import loadDict, loadDict_std
import pickle
    
"""
    - added on 2017.4.30 
    input: fn - pos-tagged file
    output: a list of a list of inds, a list of a list of words, a list of sentences as strings
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
load a list of (toxic_score, sentence, most_toxic_word)
'''
def load_toxic_word(fn):
    with open(fn, "rb") as handle:
        Sentence_And_Toxic_Word = pickle.load(handle)
    return Sentence_And_Toxic_Word
        
    
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
    modified_word - a word that has an incorrect spelling
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
            ret_flag = True
        else:
            method = random.randint(0, 3)
            
    return ret_word_and_method[0], ret_word_and_method[1]

'''
- added on 2017.5.15
Difference from the above:
(1) do not include ' ' in revise method "add".
(2) try 10 times to add an error to a word, if it is still in the dictionary in all 10 times, try to add an star ( * ) into the word
- especially "add" and "replace"
- keep the original way for "permute"
(3) "delete" can be used only for word with length >= 8
(4) cancel the "separation" method

A method to change a word that randomly picks one of {add 1 char, delete 1 char, 
replace 1 char, permute 2 adjacent chars}.
input:
    word - the input word
output:
    modified_word - a word that has an incorrect spelling
    method - the method used to modify. (0 - add, 1 - delete, 2 - replace, 3 - permute)
effect:
    make sure that the revised word cannot be a valid word in the dictionary
'''
def change_a_word_5_ways_invalid_v2(word):
    Alphabet_List = list(string.ascii_lowercase)
    cnt = loadDict()
    
    # 0 - add
    # 1 - delete
    # 2 - replace  
    # 3 - permute
    method = random.randint(0, 3) 
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
            if (len(word)<8):
                while (method==1):
                    method = random.randint(0, 4)
                continue
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
            
        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag = True
        else:
            method = random.randint(0, 3)
    
    if (ret_flag == False and count >= 10 and ret_word_and_method[1]==0):
        pos = random.randint(0, len(word))
        word1 = word[0:pos]
        word2 = word[pos:len(word)]
        add = '*'
        ret_word_and_method = (word1+add+word2, 0)
    elif (ret_flag == False and count >= 10 and ret_word_and_method[1]==2):
        pos = random.randint(0, len(word)-1)
        word1 = word[0:pos]
        word2 = word[pos+1:len(word)]
        change = '*'
        ret_word_and_method =( word1+change+word2, 2)
    
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
    
'''
- added on 2017.5.15
Difference from above: see change_a_word_5_ways_invalid_v2
Modify certain words in a sentence
input:
    sentence - a string representing the sentence
    Words_List - a list of words that should be modified
output:
    Modified_Sentences - a list of [new_sentence, method, original_word, new_word_list] list, with each being the input sentence
                         with one word from Words_List modified (punctuations are deleted), and
                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
                         4 - separate
                         the new_word_list contains (possibly multuple and mutually different if the word occurs multuple times in the sentence) 
                         revisions to the input word.
effect:
    make sure that the revised word cannot be a valid word in the dictionary
'''
def modify_one_word_5_ways_invalid_v2(sentence, Words_List):
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
                New_Words_In_Sentence[i], method = change_a_word_5_ways_invalid_v2(New_Words_In_Sentence[i])            
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([new_sentence, method, word, [New_Words_In_Sentence[i] for i in Indices]])
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
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([[Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i], Modified_Sentences[i][3]]])
        except:
            print('len(Modified_Sentences) < 4:',i)
    #print(Modified_Sentences_And_Words)    
    return Modified_Sentences_And_Words
    
'''
- added on 2017.5.15
Difference from above: see change_a_word_5_ways_invalid_v2
Modify certain words in a sentence that are likely to be important in feeling
input:
    indices - a list of indices of keywords
    sentence - a string representing the sentence
output:
    Modified_Sentences_And_Words - a list of [sentence, method, original_word, new_word_list] list, 
                         with each being the input sentence with one word that are 
                         likely to be important in feeling modified. (punctuations are deleted) and
                         the method is an int 0 - add, 1 - delete, 2 - replace, 3 - permute, 
                         4 - separate
effect:
    make sure that the revised word cannot be a valid word in the dictionary
'''

def modify_key_words_5_ways_readTag_invalid_v2(indices,sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list)) # unique
    Modified_Sentences = modify_one_word_5_ways_invalid_v2(sentence, selected_word_list)
    #print(Modified_Sentences)
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([Modified_Sentences[i][0], Modified_Sentences[i][1], selected_word_list[i], Modified_Sentences[i][3]])
        except:
            print('len(Modified_Sentences) < 4:',i)
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

#Sentence_And_Toxic_Word = load_toxic_word('Sentence_And_Toxic_Word.pickle')
#print('number of sentences: ',len(Sentence_And_Toxic_Word))
##print(Sentence_And_Toxic_Word[0])
##print(Sentence_And_Toxic_Word[len(Sentence_And_Toxic_Word)-1])
#
## check which toxic words are not in the dictionary
#Toxic_Word_Invalid = []
#cnt = loadDict()
#for i in range(len(Sentence_And_Toxic_Word)):
#    if (cnt[Sentence_And_Toxic_Word[i][2]]==0):
#        Toxic_Word_Invalid.append(Sentence_And_Toxic_Word[i][2])
#print(Toxic_Word_Invalid)
#with open("Toxic_Word_Invalid.pickle", "wb") as handle:
#    pickle.dump(Toxic_Word_Invalid, handle)
    


#Sentence_And_Toxic_Word = load_toxic_word('Sentence_And_Toxic_Words/Sentence_And_Toxic_Word0.pickle')
#
#for i in range(1,37):
#    fn = 'Sentence_And_Toxic_Words/Sentence_And_Toxic_Word'+str(i)+'.pickle'
#    Sentence_And_Toxic_Word = Sentence_And_Toxic_Word + load_toxic_word(fn)
#    
#with open("Sentence_And_Toxic_Word.pickle", "wb") as handle:
#    pickle.dump(Sentence_And_Toxic_Word, handle)

#All_Sentences_Scores = load_toxic_word('All_Sentences_Scores/All_Sentences_Scores0.pickle')
#for i in range(370):
#    fn = 'All_Sentences_Scores/All_Sentences_Scores'+str(i)+'.pickle'
#    l = load_toxic_word(fn)
#    print(len(l), len(l[0]), len(l[1]), len(l[2]), len(l[3]), len(l[4]))
#    for i in range(5):
#        All_Sentences_Scores[i] = All_Sentences_Scores[i] + l[i]
    
#with open("All_Sentences_Scores.pickle", "wb") as handle:
#    pickle.dump(All_Sentences_Scores, handle)
    
#with open("All_Sentences_Scores_separate.pickle", "wb") as handle:
#    pickle.dump(All_Sentences_Scores[4], handle)

#All_Sentences_Scores = load_toxic_word('All_Sentences_Scores_separate/All_Sentences_Scores0.pickle')
#for i in range(51):
#    fn = 'All_Sentences_Scores_separate/All_Sentences_Scores'+str(i)+'.pickle'
#    l = load_toxic_word(fn)
#    print(len(l))
#    All_Sentences_Scores = All_Sentences_Scores + l
#print(len(All_Sentences_Scores))