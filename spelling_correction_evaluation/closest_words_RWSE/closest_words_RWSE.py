# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 19:43:35 2017

This program 
(1) reads input file in RWSE data format, see 
https://www.ukp.tu-darmstadt.de/data/spelling-correction/rwse-datasets/
(2) for each misspelled word, find a list of possible corrections
(3) outputs all sentences, and for each sentence, outputs the indice of the 
misspelled word in it, and a list of possible corrections
(4) Dataset Referrence: 
Torsten Zesch. Measuring Contextual Fitness Using Error Contexts Extracted 
from the Wikipedia Revision History. In: Proceedings of the 13th Conference of 
the European Chapter of the Association for Computational Linguistics 
(EACL 2012), April 2012.

"""



import difflib
from nltk.corpus import words



'''
Helper Functions
'''

'''
Read RWSE data file
input:
    in_file_name - the name of the input file in RWSE data format
output:
    Correct_Words - the list of correct words in order
    Incorrect_Words - the list of incorrect words in order
    Sentences - the list of sentences in order
'''
def read_RWSE(in_file_name):
    inFile=open(in_file_name,'rt')
    content = inFile.read()
    Info = content.split('\n')
    Correct_Words = []
    Incorrect_Words = []
    Sentences = []
    for i in range(3,len(Info),7):
        Correct_Words.append(Info[i])
    for i in range(2,len(Info),7):
        Incorrect_Words.append(Info[i])    
    for i in range(5,len(Info),7):
        Sentences.append(Info[i])
    inFile.close()
    return Correct_Words, Incorrect_Words, Sentences

'''
Read RWSE data file and then find closest words for each incorrect word
input:
    in_file_name - the name of the input file in RWSE data format
    num_data - (optional, default: 1000) the number of data that this program processes
    n0 - (optional, default: 3) the max number of closest matches that is found 
        for each incorrect word
    cutoff0 - (optional, default: 0.6) the cutoff above which closest matches 
             are found for each incorrect word
    outfile1 - (optional, default: 0) the name of the output file that stores
               the list Sentences_And_Idx
    outfile2 - (optional, default: 0) the name of the output file that stores
               the list of list Closest_Words
    outfile3 - (optional, default: 0) the name of the output file that stores
               the list Correct_Words           
output:
    Sentences_And_Idx - the list of tuples of (sentences, idx) in order.
                        idx is the 0-indexed position of the incorrect word 
                        appearing in the sentence
    Closest_Words - a list of list of closest matches to each incorrect word
    Correct_Words - the list of correct words in order
effect:
    outfile1 - the output file that stores the list Sentences_And_Idx
    outfile2 - the output file that stores the list of list Closest_Words
    outfile3 - the output file that stores the list Correct_Words
    console output - prints the progess of this function completed
'''
def possible_corrections(in_file_name, num_data=1000, n0=3, cutoff0=0.6, outfile1=0, outfile2=0, outfile3=0):
    Correct_Words, Incorrect_Words, Sentences = read_RWSE(in_file_name)
    Correct_Words = Correct_Words[0:num_data]
    Incorrect_Words = Incorrect_Words[0:num_data]
    Sentences = Sentences[0:num_data]
    word_list = words.words()
    length = len(Correct_Words)
    count = 0
    Closest_Words = []
    for word in Incorrect_Words:
        close_matches = difflib.get_close_matches(word, word_list, n=n0, cutoff=cutoff0)    
        Closest_Words.append(close_matches)
        count = count+1
        if (int(length/100) != 0 and count % int(length/100) == 0):
            print(1.0*count/length)
    Sentences_And_Idx = []
    for i in range(len(Sentences)):
        Sentence_As_Word_List = Sentences[i].split()
        idx = Sentence_As_Word_List.index(Incorrect_Words[i])
        Sentences_And_Idx.append((Sentence_As_Word_List, idx))        
    if (outfile1 != 0):
        out1=open(outfile1,'wt')
        out1.write('%s' % (''.join(str(tup[1])+' '+str(tup[0])+'\n' for tup in Sentences_And_Idx)))
        out1.close()
    if (outfile2 != 0):
        out2=open(outfile2,'wt')
        for i in range(len(Closest_Words)):        
            out2.write('%s\n\n' % (''.join(str(intStr)+' ' for intStr in Closest_Words[i])))
        out2.close()
    if (outfile3 != 0):
        out3=open(outfile3,'wt')
        out3.write('%s' % (''.join(str(intStr)+'\n' for intStr in Correct_Words)))
        out3.close()
    return Sentences_And_Idx, Closest_Words, Correct_Words   
        
        
        
'''
Main
'''

a, b, c = possible_corrections('data/RWSE/en_artificial_token.txt', num_data=10, n0=5, outfile1='Sentences_And_Idx.txt', outfile2='Closest_Words.txt', outfile3='Correct_Words.txt')
print(len(a))
print(a[0])
print(len(b))
print(b[0])
print(len(c))
print(c[0])

