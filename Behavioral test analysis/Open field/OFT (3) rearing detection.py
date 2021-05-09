#!/usr/bin/env python
# coding: utf-8

# # Supportive + unsupportive rearing detection

# In[8]:


# get the coor of headcenter, bodycenter, tailbase to know the len of rat in each frame
from math import sqrt
import csv
import more_itertools as mit
import numpy as np
import os

folder = os.listdir('/Users/RoyKudo/Desktop/OFT results/coor csv/')

for f in folder:
    if '.csv' in f:
        l1 = []
        l7 = []
        headcenter_x = []
        l2 = []
        l8 = []
        headcenter_y = []
        l3 = []
        l9 = []
        bodycenter_x = []
        l4 = []
        l10 = []
        bodycenter_y = []
        l5 = []
        l11 = []
        tailbase_x = []
        l6 = []
        l12 = []
        tailbase_y = []

        with open('/Users/RoyKudo/Desktop/OFT results/coor csv/' + f, "r") as csv1:
            csv_reader1 = csv.reader(csv1, delimiter=',')
            for lines in csv_reader1:
                l1.append(lines[4])
                l2.append(lines[5])
                l3.append(lines[1])
                l4.append(lines[2])
                l5.append(lines[7])
                l6.append(lines[8])
        l7 = l1[3:]
        l8 = l2[3:]
        l9 = l3[3:]
        l10 = l4[3:]
        l11 = l5[3:]
        l12 = l6[3:]

        for i in l7:
            headcenter_x.append(float(i))
        for j in l8:
            headcenter_y.append(float(j))
        for k in l9:
            bodycenter_x.append(float(k))
        for m in l10:
            bodycenter_y.append(float(m))
        for n in l11:
            tailbase_x.append(float(n))
        for o in l12:
            tailbase_y.append(float(o))

        body_len = []
        for p, q, r, s, t, u in zip(headcenter_x, headcenter_y, bodycenter_x, bodycenter_y, tailbase_x, tailbase_y):
            body_len.append(sqrt((p - r) ** 2 + (q - s) ** 2) + sqrt((r - t) ** 2 + (s - u) ** 2))
    
        body_len_percentile = np.percentile(body_len, (25, 50, 75), interpolation='midpoint')

        plain_body_len = body_len_percentile[1] # pick out median to represent body length of rat
        short_body_len = body_len_percentile[0] # pickout the first quartile

        rearing_body_index = []
        for v, w in enumerate(body_len):
            if short_body_len <= w <= plain_body_len: # except the shortest body lengths to avoid to include times of rest and grooming
                rearing_body_index.append(v)
        
        iterable = rearing_body_index
        L = [list(group) for group in mit.consecutive_groups(iterable)]

        L1 = []
        for a in L:
            if len(a) >= 10: # count only when the actions last more than 1/3 sec (10 frames)
                L1.append(a)
         
        L2 = []
        for b in range(len(L1)): # get the first index of every action
            L2.append(L[b][0])
    
        L3 = []
        for c in L2:
            L3.append(round(c/30, 2)) # change the unit from frame to sec

        L4 = []
        for d in L3:
            L4.append(int(d))
            
        with open('/Users/RoyKudo/Desktop/OFT results/rearing_result.csv', 'a') as t:
            t.write(f.replace('.csv', '_rearing_result'))
            t.write('\t')
            t.write(str(len(set(L4)))) # only get the results happen in different seconds (e.g. 8.17(sec) & 8.79(sec) counted as once)
            t.write('\n')


# In[ ]:




