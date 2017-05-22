'''
After one round, some sentences and errors are not generated due to errors
This program finds which data are missing and generate them
'''

import pickle
print('done import pickle')
from add_spelling_errors import load_toxic_word
print('done from add_spelling_errors import load_toxic_word')
from revise_sentence_and_test import revise_sentence_and_test_list_5_ways_invalid_v2
print('done from revise_sentence_and_test import revise_sentence_and_test_list_5_ways_invalid_v2')

# find which data are missing

missing_inds = []

for i in range(361):
    in_file_name = 'output/separated_by_revised_type/add/'+str(i)+'_method0.txt'
    try:
        f = open(in_file_name, 'r')
    except:
        missing_inds.append(i)
        
print('missing indices:',missing_inds)
print('number of missing indices:',len(missing_inds)) # 39

# re-generate the missing data

Sentence_And_Toxic_Word = load_toxic_word('Sentence_And_Toxic_Word.pickle')

# 10 sentences per batch
folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for j in range( 8, 9):
    i = missing_inds[j]
    print('Processing the %d-th batch of 10 sentences\n' % i)
    if (i*10 < len(Sentence_And_Toxic_Word)):
        if (i*10+10 < len(Sentence_And_Toxic_Word)):
            All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word[i*10:i*10+10], Folder_List, str(i)+'_')
        else:
            All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid_v2(Sentence_And_Toxic_Word[i*10:len(Sentence_And_Toxic_Word)], Folder_List, str(i)+'_')
        out_file_name = 'All_Sentences_Scores/All_Sentences_Scores'+str(i)+'.pickle'
        with open(out_file_name, "wb") as handle:
            pickle.dump(All_Sentences_Scores, handle)
            

'''
# past version

from add_spelling_errors import readTag, modify_key_words_5_ways_readTag, modify_key_words_5_ways_readTag_invalid, load_toxic_word
from revise_sentence_and_test import revise_sentence_and_test_list_5_ways_invalid

missing_inds = []

for i in range(361):
    in_file_name = 'output/separated_by_revised_type/add/'+str(i)+'_method0.txt'
    try:
        f = open(in_file_name, 'r')
    except:
        missing_inds.append(i)
        
print('missing indices:',missing_inds)
print('number of missing indices:',len(missing_inds))

selected_inds, selected_words, tok_sent = readTag("tagged_test_toxic_data.txt")

inds = []
words = []
tok = []
#for i in range(len(missing_inds)):
#    inds.append(selected_inds[missing_inds[i]])
#    words.append(selected_words[missing_inds[i]])
#    tok.append(tok_sent[missing_inds[i]])

# 10 sentences per batch
folder_prefix = 'output/separated_by_revised_type/'
Folder_List = [folder_prefix+'add',folder_prefix+'delete',folder_prefix+'replace',folder_prefix+'permute',folder_prefix+'separate']
for j in range(0,int(len(missing_inds)/10)+1):
    i = missing_inds[j]
    print(i)
    print('Processing the %d-th batch of 10 sentences\n' % i)
    All_Sentences_Scores = revise_sentence_and_test_list_5_ways_invalid(selected_inds[i*10:i*10+10], selected_words[i*10:i*10+10], tok_sent[i*10:i*10+10], Folder_List, str(i)+'_')
    #print(len(All_Sentences_Scores))
'''