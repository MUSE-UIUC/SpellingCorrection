# coding: utf-8

"""
Created on Sun Mar 19, 2017

This program 
(1) reads input file in .tsv data format
(2) for each comment, find the average value of toxicity and toxicity_score 
among all human annotations for that comment
(3) outputs a list of tuples of (toxicity, sentence) for a portion of sentences 
with the highest average toxicity

(*) Dataset Referrence: 
https://figshare.com/articles/Wikipedia_Talk_Labels_Toxicity/4563973/2
(**) Code Referrence: 
https://github.com/ewulczyn/wiki-detox/blob/master/src/figshare/Wikipedia%20Talk%20Data%20-%20Getting%20Started.ipynb
"""



import pandas as pd



'''
Helper Functions
'''

'''
Read .tsv files on sentence toxicity

functionality:
(1) reads input file in .tsv data format
(2) for each comment, find the average value of toxicity and toxicity_score 
among all human annotations for that comment
(3) outputs a list of tuples of (toxicity, sentence) for the num_out sentences 
with the highest average toxicity

input:
    comments_file - the name of the input file containing comments in .tsv data format
    annotations_file - the name of the input file containing annotations in .tsv data format
    num_out - (optional, default: all, range: 0-159686) the number of sentences with the highest 
              average toxicity that this program outputs           
output:
    Sentences_With_Labels - a list of tuples of (toxicity, sentence)
'''
def sentence_toxic_read_file(comments_file, annotations_file, num_out=-1):
    
    # read file
    comments = pd.read_csv(comments_file, sep = '\t', index_col = 0)
    annotations = pd.read_csv(annotations_file,  sep = '\t')
    
    # label the toxicity of a comment as the average of annoatators' labels
    # toxicity: Indicator variable for whether the worker thought the comment is toxic. 
    #           The annotation takes on the value 1 if the worker considered the comment toxic 
    #           (i.e worker gave a toxicity_score less than 0) and value 0 if the worker 
    #           considered the comment neutral or healthy (i.e worker gave a toxicity_score greater 
    #           or equal to 0). Takes on values in {0, 1}.
    toxicities = annotations.groupby('rev_id')['toxicity'].mean()

    # join labels and comments
    comments['toxicity'] = toxicities

    # remove newline and tab tokens
    comments['comment'] = comments['comment'].apply(lambda x: x.replace("NEWLINE_TOKEN", " "))
    comments['comment'] = comments['comment'].apply(lambda x: x.replace("TAB_TOKEN", " "))
    
    # convert pandas DataFrame to Numpy-arrau
    Data_Matrix = comments.as_matrix()
    Comment_Array = Data_Matrix[:,0]
    Toxicity_Array = Data_Matrix[:,6]
    
    # a list of tuples of (toxicity, sentence)
    All_Sentences_With_Labels = []
    for i in range(0, len(Comment_Array)):
        All_Sentences_With_Labels.append((Toxicity_Array[i], Comment_Array[i]))
    # return the num_out tuples with highest toxicity (all if num_out undefined)
    Sentences_With_Labels = sorted(All_Sentences_With_Labels, reverse=True)
    if (num_out != -1):    
        Sentences_With_Labels = Sentences_With_Labels[0:num_out]
    return Sentences_With_Labels


'''
Main
'''
comments_file = 'data/toxicity_annotated_comments.tsv'
annotations_file = 'data/toxicity_annotations.tsv'
Sentences_With_Labels = sentence_toxic_read_file(comments_file, annotations_file, num_out=1000)
print(Sentences_With_Labels[999])
print(len(Sentences_With_Labels))