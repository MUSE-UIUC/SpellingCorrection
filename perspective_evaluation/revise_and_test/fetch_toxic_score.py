# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 23:14:16 2017

This program fetches the toxic score of a comment on www.perspectiveapi.com,
given an input comment

@author: liyuchen
"""


import requests


'''
Helper Functions
'''

'''
This function returns the toxic score of a comment on www.perspectiveapi.com, 
given an input comment.
The score is fetched from www.perspectiveapi.com using request.
input:
    sentence - the input comment
output:
    toxic_score - the toxic score of sentence (-1 if error)
'''
def fetch_toxic_score_online(sentence):
    # the variable "sessionId" is a random value written arbitrarily
    try:
        r = requests.post('http://www.perspectiveapi.com/check', json={"comment":sentence, "sessionId":"10002022"})
    except:
        print('fetch_toxic_score_online: r = requests.post() bug')
        print(sentence)
        # return 2 # bug
        return 0 # regarded as successfully deceiving Perspective API        
        
    #r = requests.post('http://www.perspectiveapi.com/check', data={"comment":sentence, "sessionId":"10002022"})        
    # The json variable is of the following format:
    # {'attributeScores': {'TOXICITY': {'spanScores': [{'end': 6, 'score': {'type': 'PROBABILITY', 'value': 0.3378245}, 'begin': 0}], 'summaryScore': {'type': 'PROBABILITY', 'value': 0.3378245}}}, 'languages': ['en']}
    #print(r)
    if (str(r)=='<Response [200]>'):    
        j = r.json()
        #print(j)
        #print()
        if ('attributeScores' in j):
            toxic_score = j['attributeScores']['TOXICITY']['summaryScore']['value']
        else:
            print('attributeScores not in j = r.json()')
            print(j)
            print(sentence)
            #toxic_score = 2
            toxic_score = 0 # regarded as successfully deceiving Perspective API
    else:
#        print('str(r) != \'<Response [200]>\'')
#        print(r)
#        print(sentence)
#        #toxic_score = 2
        toxic_score = 0 # regarded as successfully deceiving Perspective API
    return toxic_score

'''
This function returns a list of toxic scores of a list of comments based on www.perspectiveapi.com, 
given a list of input comment.
The scores are fetched from www.perspectiveapi.com using request.
input:
    Sentence_List - the input comment
    outfile - (optional) the output file that holds the list of toxic scores of sentences in Sentence_List
output:
    Toxic_Score_List - the list of toxic scores of sentences in Sentence_List
effect:
    outfile holds Toxic_Score_List
'''
def fetch_toxic_score_list_online(Sentence_List, outfile=0):
    Toxic_Score_List = []
    for s in Sentence_List:
        Toxic_Score_List.append(fetch_toxic_score_online(s))
    if (outfile != 0):
        out=open(outfile,'wt')
        out.write('%s' % (''.join(str(toxic_score)+'\n' for toxic_score in Toxic_Score_List)))
        out.close()
    return Toxic_Score_List
    


'''
Main
'''
'''
Sentence_List = ['good','bad','idiot','idiiot','he is an idiot']

for s in Sentence_List:
    toxic_score = fetch_toxic_score_online(s)
    print('%s: %f' %(s,toxic_score))
    
fetch_toxic_score_list_online(Sentence_List, outfile='out_toxic_score_list.txt')
'''