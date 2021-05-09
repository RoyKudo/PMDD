#!/usr/bin/env python
# coding: utf-8

# In[98]:


# create scale for pixel-cm from verticses of leftup_open arm
import math
from math import sqrt
import csv
import os
folder = os.listdir('/Users/RoyKudo/Desktop/EPM results/vertices_only/')

for f in folder:
    if 'vertices' not in f and '.csv' in f:
        with open('/Users/RoyKudo/Desktop/EPM results/vertices_only/' + f, "r") as fh:
            reader = csv.reader(fh)
            ls = list(reader)
            
        all_vertices = []
        for i in ls[0]:
            all_vertices.append(int(i))
        for j in ls[1]:
            all_vertices.append(int(j))
        for k in ls[6]:
            all_vertices.append(int(k))
        for m in ls[7]:
            all_vertices.append(int(m))
                
        x1 = all_vertices[0]
        y1 = all_vertices[1]
        x2 = all_vertices[2]
        y2 = all_vertices[3]
        
        dpix=sqrt((x1-x2)**2+(y1-y2)**2)
        
        actual_length = 50 # (cm)
        
        # get x, y coordinates of bodycenter from DLC result csv & calculate total distance(cm)
        #for x axis:
        l = []
        with open('/Users/RoyKudo/Desktop/EPM results/5_min_coor_csv/' + f.replace('.csv', '_coor.csv'), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                l.append(lines[2])
        l1 = l[3:]
        l_bodycenter_x = []
        for n in l1:
            l_bodycenter_x.append(float(n))
            
        #for y axis:
        l2 = []
        with open('/Users/RoyKudo/Desktop/EPM results/5_min_coor_csv/' + f.replace('.csv', '_coor.csv'), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                l2.append(lines[3])
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
            
        total_distance_in_cm = (actual_length * total_distance_in_pixel) / dpix
        
        with open('/Users/RoyKudo/Desktop/EPM results/EPM_5min_total_distance_result.csv', 'a') as t:
            t.write(f.replace('.csv', '') + '_total_distance(cm)')
            t.write('\t')
            t.write(str(total_distance_in_cm))
            t.write('\n')


# In[ ]:




