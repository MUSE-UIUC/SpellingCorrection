# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 14:58:27 2017

@author: liyuchen

This file contrains functions that can be used to deliberately add mis-spellings
to sentences.
"""

import random
import string
import pickle
from corpus_util import loadDict
    
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
A function that loads pickle files.
'''
def load_pickle(fn):
    with open(fn, "rb") as handle:
        Content = pickle.load(handle)
    return Content
        
    
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
- added on 2017.5.21
Add spelling errors to the toxic words in input file, and store the modified content, 
as well as the way in which each word is modified, in an output file.
input:
    Toxic_Words - a list of toxic words
    fn - the name of the input file
    out_fn - the name of the output file
output:
    original_and_modified_content - a string containing the original and the modified content in the file
    Correct_and_Wrong_Words - a list of (correct_word, wrong_word) tuples
effect:
    every toxic word is revised using one of the following methods: 
    0 - add, 1 - delete, 2 - replace, 3 - permute, 4 - separate
    
    output file format:
    
    original sentence
    revised sentence
    correct word, wrong word; correct word, wrong word; ……
'''
def modify_toxic_words_in_file(Toxic_Words, fn, out_fn):
    with open(fn) as f:
        sentence = f.read()
    Words_In_Sentence = sentence.split()
    New_Words_In_Sentence = []
    Correct_and_Wrong_Words = []
    for i in range(len(Words_In_Sentence)):
        if (Words_In_Sentence[i] in Toxic_Words):
            wrong_word = change_a_word_5_ways_invalid_v2(Words_In_Sentence[i])[0]
            New_Words_In_Sentence.append(wrong_word)
            Correct_and_Wrong_Words.append((Words_In_Sentence[i], wrong_word))
        else:
            New_Words_In_Sentence.append(Words_In_Sentence[i])
            
    modified_content = ''
    for i in range(len(New_Words_In_Sentence)):
        try:
            modified_content = modified_content + New_Words_In_Sentence[i] + ' '
        except:
            print(New_Words_In_Sentence[i])
            print(Words_In_Sentence[i])
            print(sentence)
    original_and_modified_content = (sentence, modified_content)

    with open(out_fn, "w") as f:
        try:
            f.write(sentence+'\n')
            f.write(modified_content+'\n')
            for j in range(len(Correct_and_Wrong_Words)):
                f.write(Correct_and_Wrong_Words[j][0]+', '+Correct_and_Wrong_Words[j][1]+'; ')
        except:
            print('modify_toxic_words_in_file: around line 600: write to file bug for sentence:')
            print('sentence:',sentence)
            print('modified_content:',modified_content)
            print('Correct_and_Wrong_Words:',Correct_and_Wrong_Words)

    return original_and_modified_content, Correct_and_Wrong_Words


'''
Main
'''

# load the list of words that are likely to be toxic
fn = 'preprocess/toxic_words.pickle'
Toxic_Words = load_pickle(fn)
Toxic_Words = Toxic_Words[0:200]

# add spelling errors to the toxic words in spam test data
Original_and_Modified_Content_List = []
Correct_and_Wrong_Words_List = []
Missing_Filenames = []
Except_Filenames = []
for i in range(11,164):
    fn = 'spam_data/'+'spam-test/'+'spmsga'+str(i)+'.txt'
    try:
        f = open(fn)
        f.close()
    except:
        Missing_Filenames.append(i)
    out_fn = 'spam_data/'+'spam-test-w-errors/a'+str(i)+'.txt'
    try:
        original_and_modified_content, Correct_and_Wrong_Words = modify_toxic_words_in_file(Toxic_Words, fn, out_fn)
        Original_and_Modified_Content_List.append(original_and_modified_content)
        Correct_and_Wrong_Words_List.append(Correct_and_Wrong_Words)
        print('processed file a', i)
    except:
        Except_Filenames.append(i)
        print('file a', i, 'has bug')
for i in range(5,164):
    fn = 'spam_data/'+'spam-test/'+'spmsgb'+str(i)+'.txt'
    try:
        f = open(fn)
        f.close()
    except:
        Missing_Filenames.append(i)
    out_fn = 'spam_data/'+'spam-test-w-errors/b'+str(i)+'.txt'
    try:
        original_and_modified_content, Correct_and_Wrong_Words = modify_toxic_words_in_file(Toxic_Words, fn, out_fn)
        Original_and_Modified_Content_List.append(original_and_modified_content)
        Correct_and_Wrong_Words_List.append(Correct_and_Wrong_Words)
        print('processed file a', i)
    except:
        Except_Filenames.append(i)
        print('file b', i, 'has bug')
for i in range(3,145):
    fn = 'spam_data/'+'spam-test/'+'spmsgc'+str(i)+'.txt'
    try:
        f = open(fn)
        f.close()
    except:
        Missing_Filenames.append(i)
    out_fn = 'spam_data/'+'spam-test-w-errors/c'+str(i)+'.txt'
    try:
        original_and_modified_content, Correct_and_Wrong_Words = modify_toxic_words_in_file(Toxic_Words, fn, out_fn)
        Original_and_Modified_Content_List.append(original_and_modified_content)
        Correct_and_Wrong_Words_List.append(Correct_and_Wrong_Words)
        print('processed file c', i)
    except:
        Except_Filenames.append(i)
        print('file c', i, 'has bug')
        
pickle_output_file_path_prefix = 'spam_data/spam-test-w-errors-pickle/'
with open(pickle_output_file_path_prefix+'Original_and_Modified_Content_List.pickle', "wb") as handle:
    pickle.dump(Original_and_Modified_Content_List, handle)
with open(pickle_output_file_path_prefix+'Correct_and_Wrong_Words_List.pickle', "wb") as handle:
    pickle.dump(Correct_and_Wrong_Words_List, handle)

print(Missing_Filenames)
print('length:',len(Missing_Filenames))
print(Except_Filenames)
print('length:',len(Except_Filenames))