# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 18:41:01 2017

This file contrains functions that can be used to deliberately add mis-spellings
to sentences.
"""

from nltk import word_tokenize, pos_tag
import random
import string

'''
Return a list of words that are likely to be important in feeling
input:
    list_of_str - a list of sentences as strings
output:
    selected_word_list - a list of list of words that are likely to be important in feeling
Example:
    input: [“he likes tea", "it has good flavor"]
    output: [["likes", "tea"], ["has", "good", "flaor"]]
''' 
def getContentWords(list_of_str):
    tag_set = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS",\
               "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    selected_word_list = []
    for s in list_of_str:
        text = word_tokenize(s)
        word_pos_list = pos_tag(text)
        words = [item[0] for item in word_pos_list if item[1] in tag_set]
        selected_word_list.append(words)
    return selected_word_list

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
Modify certain words in a sentence
input:
    sentence - a string representing the sentence
    Words_List - a list of words that should be modified
output:
    Modified_Sentences - a list of sentences, with each being the input sentence
                         with one word from Words_List modified. (without punctuations)
'''
def modify_one_word(sentence, Words_List):
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
def modify_key_words(sentence):
    #Words_In_Sentence = sentence.split()
    selected_word_list = getContentWords([sentence])
    selected_word_list = list(set(selected_word_list[0]))
    Modified_Sentences = modify_one_word(sentence, selected_word_list)
    return Modified_Sentences
    
    
    
'''
Main
'''
'''
print('\nTesting function change_a_word_dis1: \n')
for i in range(10):
    print(change_a_word_dis1('123456789'))
print('\n')

#
#print('Testing modify_key_words')
#sentence = '<><> You bunch of fwcking twssers.' 
#print('Original sentence: %s\n\n' %sentence)
#print('Content words: ')
#print(getContentWords(sentence))
#print('Modified sentences: \n\n')
#Modified_Sentences = modify_key_words(sentence)
#for s in Modified_Sentences:
#    print('%s\n\n' % s)


print('Testing modify_key_words\n')
sentence = 'Today is Saturday ha ha ha.' 
print('Original sentence: %s\n' %sentence)
print('Content words: ')
print(getContentWords([sentence]))
print()
print('Modified sentences: \n')
Modified_Sentences = modify_key_words(sentence)
for s in Modified_Sentences:
    print('%s' % s)
'''