# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 09:14:24 2017

@author: liyuchen
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 09:21:23 2017

@author: liyuchen
"""

import codecs
import matplotlib.pyplot as plt
import statistics

'''
Helper Functions
'''

def read_k_tuples(in_file_name, k):
    with codecs.open(in_file_name,'r',encoding='utf8') as f:
        content = f.read()
    List_Of_List = []
    if (content != ''):
        Content_List = content.split('\n')
        #print(len(Content_List))
        #print((len(Content_List)-1)/(k+1))
        for i in range(int((len(Content_List)-1)/(k+1))):
            List = []
            for j in range(i*(k+1),i*(k+1)+k):
                List.append(Content_List[j])
            List_Of_List.append(List)
    f.close()
    return List_Of_List
    
'''
Main
'''

# read data
List_Of_List = read_k_tuples('count_output/dist1_candidate_numbers0.txt', 3)
for i in range(1,42):
    in_file_name = 'count_output/dist1_candidate_numbers'+str(i)+'.txt'
    List_Of_List = List_Of_List+read_k_tuples(in_file_name, 3)
print(len(List_Of_List))

# process data
Revised_Words = []
Num_Candidates = []
Candidates = [] # each entry is a string containing all candidates, comma separated
for i in range(len(List_Of_List)):
    Revised_Words.append(List_Of_List[i][0])
    Num_Candidates.append(int(List_Of_List[i][1]))
    Candidates.append(List_Of_List[i][2])
    
# plot a non-decreasing curve
plt.plot(range(len(List_Of_List)),sorted(Num_Candidates), label='sorted number of candidates')
plt.legend(loc=0)
plt.xlabel('Word')
plt.ylabel('Number')
plt.title('Number of Candidates with Edit Distance At Most 1')
plt.show()

# plot a distribution
plt.hist(Num_Candidates, bins = 100)
plt.title("Number of Candidates with Edit Distance At Most 1")
plt.xlabel("Number of Candidates")
plt.ylabel("Number of Words")
plt.show()

# Statistics
print('Statistics on the number of candidates: ')
print('Max: %d' % max(Num_Candidates))
print('Min: %d' % min(Num_Candidates))
print('Average: %d' % statistics.mean(Num_Candidates))
print('Median: %d' % statistics.median(Num_Candidates))
print('Standard Deviation: %d' % statistics.stdev(Num_Candidates))
print('Variance: %d' % statistics.variance(Num_Candidates))
less_than_5 = 0
less_than_10 = 0
zero = 0
one = 0
for num in Num_Candidates:
    if num==0:
        zero = zero + 1
    if num==1:
        one = one + 1
    if num<5:
        less_than_5 = less_than_5+1
    if num<10:
        less_than_10 = less_than_10+1
print('Total: %d' % len(Num_Candidates))
print('Zero: %d' % zero)
print('One: %d' % one)
print('Less than 5: %d' % less_than_5)
print('Less than 10: %d' % less_than_10)