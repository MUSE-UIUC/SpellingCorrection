# -*- coding: utf-8 -*-
"""
Created on Mon May 15 23:19:59 2017

@author: liyuchen
"""

fname = 'revise_sentence_and_test.py'

with open(fname) as f:
    content = f.readlines()

for i in range(1,38):
    out_file_name = 'r'+str(i)+'.py'
    with open(out_file_name, "w") as f:
        for j in range(len(content)):
            if (j != 349):
                f.write(content[j])
            else:
                # for i in range( $(i-1)*10$, $i*10$ ):
                f.write('for i in range( '+str((i-1)*10)+', '+str(i*10)+'):\n')