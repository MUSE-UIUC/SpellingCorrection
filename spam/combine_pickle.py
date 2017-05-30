# -*- coding: utf-8 -*-
"""
Created on Thu May 25 15:51:00 2017

combine the pickle files into one

@author: liyuchen
"""

import pickle
from add_spelling_errors_spam import load_pickle

'''
Main
'''
Original_and_Modified_Content_List = []
Correct_and_Wrong_Words_List = []

pickle_output_file_path_prefix = 'spam_data/spam-test-w-errors-pickle/'
for i in range(1,7):
    fn = pickle_output_file_path_prefix+'Original_and_Modified_Content_List'+str(i)+'.pickle'
    Original_and_Modified_Content = load_pickle(fn)
    Original_and_Modified_Content_List = Original_and_Modified_Content_List + Original_and_Modified_Content
    fn = pickle_output_file_path_prefix+'Correct_and_Wrong_Words_List'+str(i)+'.pickle'
    Correct_and_Wrong_Words = load_pickle(fn)
    Correct_and_Wrong_Words_List = Correct_and_Wrong_Words_List + Correct_and_Wrong_Words
    
with open(pickle_output_file_path_prefix+'Original_and_Modified_Content_List.pickle', "wb") as handle:
    pickle.dump(Original_and_Modified_Content_List, handle)
with open(pickle_output_file_path_prefix+'Correct_and_Wrong_Words_List.pickle', "wb") as handle:
    pickle.dump(Correct_and_Wrong_Words_List, handle)
