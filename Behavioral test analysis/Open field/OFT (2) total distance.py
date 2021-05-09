#!/usr/bin/env python
# coding: utf-8

# In[2]:


import math
from math import sqrt
import csv
import os
folder = os.listdir('/Users/RoyKudo/Desktop/OFT results/vertices_only/')

# use bodycenter
for f in folder:
    if '.csv' in f:
        with open('/Users/RoyKudo/Desktop/OFT results/vertices_only/' + f) as fh:
            reader = csv.reader(fh)
            ls = list(reader)
            
        pix_dia_len = sqrt((int(ls[0][0])-int(ls[2][0]))**2+(int(ls[1][0])-int(ls[3][0]))**2)
        actual_dia_len = 75 #(cm)
        
        # get x, y coordinates of bodycenter from DLC result csv & calculate total distance(cm)
        #for x axis:
        l = []
        with open('/Users/RoyKudo/Desktop/OFT results/coor csv/' + f.replace('.csv', '_coor.csv'), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                l.append(lines[1])
        l1 = l[3:]
        l_bodycenter_x = []
        for n in l1:
            l_bodycenter_x.append(float(n))
            
        #for y axis:
        l2 = []
        with open('/Users/RoyKudo/Desktop/OFT results/coor csv/' + f.replace('.csv', '_coor.csv'), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                l2.append(lines[2])
        l3 = l2[3:]
        l_bodycenter_y = []
        for o in l3:
            l_bodycenter_y.append(float(o))
            
        # calculate total_distance_in_pixel:
        xx = []
        for p in l_bodycenter_x:
            xx.append(p)
            xx.append(p)
        xxx = xx[1:(len(xx)-1)]
        
        yy = []
        for q in l_bodycenter_y:
            yy.append(q)
            yy.append(q)
        yyy = yy[1:(len(yy)-1)]
        
        l4 = []
        l5 = list(range(len(xxx)-1))
        l6 = list(l5[::2])
        for a in l6:
            l4.append(xxx[1+a]-xxx[0+a])
            
        l7 = []
        l8 = list(range(len(yyy)-1))
        l9 = list(l8[::2])
        
        for b in l9:
            l7.append(yyy[1+b]-yyy[0+b])
            
        
        total_distance_in_pixel = 0
        
        for c, d in zip(l4, l7):
            total_distance_in_pixel += sqrt( c ** 2 + d ** 2)
            
        total_distance_in_cm = (actual_dia_len * total_distance_in_pixel) / pix_dia_len
        
        with open('/Users/RoyKudo/Desktop/OFT results/OFT_total_distance_result.csv', 'a') as t:
            t.write(f.replace('.csv', '') + '_total_distance(cm)')
            t.write('\t')
            t.write(str(total_distance_in_cm))
            t.write('\n')


# In[ ]:




