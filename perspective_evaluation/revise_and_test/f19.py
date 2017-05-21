# -*- coding: utf-8 -*-
"""
Created on Mon May 15 18:12:54 2017

@author: liyuchen
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 15 17:13:21 2017

@author: liyuchen
"""

from fetch_toxic_score import fetch_toxic_score_online
from add_spelling_errors import readTag
import pickle
    
'''
Return a list of (toxic_score, sentence, most_toxic_word)
input:
    selected_inds - a list of a list of inds corresponding to selected_words below
    selected_words - a list of a list of important words that readTag selects for each sentence
    tok_sent - a list of sentences, each being a string
output:
    Sentence_And_Toxic_Word - a list of (toxic_score, sentence, most_toxic_word)
effect:
for each sentence in the input 
(1) Call the function revise_sentence_and_test, including
- delete all punctuations of a sentence 
- test its toxic score on Google Perpective API 
- modify each key words in the sentence one at a time, and test toxic score on API
- record the (toxic_score, sentence, method) tuples, including the original sentence
(2) pick the word whose removal results in the lowest toxic score for the sentence
'''
def most_toxic_word(selected_inds, selected_words, tok_sent):
    Sentence_And_Toxic_Word = []   
    for i in range(len(selected_inds)):
        print(i)
        score = fetch_toxic_score_online(tok_sent)
        Scores_After_Deletion = [] # a list of (score_after_deletion, deleted_word)
        for j in range(len(selected_inds[i])):
            sentence_with_deletion = tok_sent[i].replace(selected_words[i][j],'')
            score_after_deletion = fetch_toxic_score_online(sentence_with_deletion)
            Scores_After_Deletion.append((score_after_deletion, selected_words[i][j]))
        best_deletion = sorted(Scores_After_Deletion)[0]
        if (len(best_deletion) != 2):
            print('best_deletion:',best_deletion)
            print('len(best_deletion) != 2 for index =', i)
            print(Scores_After_Deletion)
        if (best_deletion[0] == -1 or best_deletion[0] == 2):
            print('score == -1 or 2 for index = ', i)
            print(best_deletion)
        Sentence_And_Toxic_Word.append((score, tok_sent[i], best_deletion[1]))
    return Sentence_And_Toxic_Word
    
'''
Main
'''
selected_inds, selected_words, tok_sent = readTag("tagged_test_toxic_data.txt")

# different for each process
i = 18

if (i*100 < len(selected_inds)):
    if (i*100+100 <= len(selected_inds)):
        Sentence_And_Toxic_Word = most_toxic_word(selected_inds[i*100:i*100+100], selected_words[i*100:i*100+100], tok_sent[i*100:i*100+100])
    else:
        Sentence_And_Toxic_Word = most_toxic_word(selected_inds[i*100:len(selected_inds)], selected_words[i*100:len(selected_inds)], tok_sent[i*100:len(selected_inds)])
print('number of sentences',len(Sentence_And_Toxic_Word))
#print(Sentence_And_Toxic_Word[0])

fn = 'Sentence_And_Toxic_Words/Sentence_And_Toxic_Word'+str(i)+'.pickle'
with open(fn, "wb") as handle:
    pickle.dump(Sentence_And_Toxic_Word, handle)
