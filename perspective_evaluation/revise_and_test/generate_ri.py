# -*- coding: utf-8 -*-
"""
Created on Mon May 15 23:19:59 2017

@author: liyuchen
"""

fname = 'find_missing.py'

with open(fname) as f:
    content = f.readlines()

for i in range(1,40):
    out_file_name = 'f'+str(i)+'.py'
    with open(out_file_name, "w") as f:
        for j in range(len(content)):
            if (j != 33):
                f.write(content[j])
            else:
                # for i in range( $(i-1)*10$, $i*10$ ):
                #f.write('for i in range( '+str((i-1)*10)+', '+str(i*10)+'):\n')
                # for i in range( $(i-1)$, $i$ ):
                #f.write('for i in range( '+str(i-1)+', '+str(i)+'):\n')
                # i = $(i-1)
                #f.write('i = '+str(i-1)+'\n')
                # for j in range(i-1,i):
                f.write('for j in range( '+str(i-1)+', '+str(i)+'):\n')