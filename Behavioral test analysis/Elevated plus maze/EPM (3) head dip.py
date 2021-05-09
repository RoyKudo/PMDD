#!/usr/bin/env python
# coding: utf-8

# In[10]:


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import more_itertools as mit
import csv
import os

folder = os.listdir('/Users/RoyKudo/Desktop/EPM results/vertices_only/')

for f in folder:
    l1 = []
    l_yrows = []
    with open('/Users/RoyKudo/Desktop/EPM results/vertices_only/' + f, "r") as fh:
            l = list(fh)
            for i in l:
                l1.append(int(i.replace('\n','')))
    
    l_xrows = list(l1[::2])
    l2 = list(l1[1::2])
    for j in l2:
        l_yrows.append(j)
        
    coor = list(zip(l_xrows, l_yrows))
    
    leftup_openarm = Polygon(coor[0:4])
    leftdown_closearm = Polygon(coor[4:8])
    center_square = Polygon(coor[8:12])
    rightup_closearm = Polygon(coor[12:16])
    rightdown_openarm = Polygon(coor[16:20])
    
    
    #for x axis:
    l3 = []
    with open('/Users/RoyKudo/Desktop/EPM results/coor csv/' + f.replace('.csv', '_coor.csv'), "r") as csv1:
        csv_reader1 = csv.reader(csv1, delimiter=',')
        for lines in csv_reader1:
            l3.append(lines[4])
    l4 = l3[3:]
    l_headcenter_x = []
    for k in l4:
        l_headcenter_x.append(float(k))

    #for y axis:
    l5 = []
    with open('/Users/RoyKudo/Desktop/EPM results/coor csv/' + f.replace('.csv', '_coor.csv'), "r") as csv4:
        csv_reader4 = csv.reader(csv4, delimiter=',')
        for lines in csv_reader4:
            l5.append(lines[5])
    l6 = l5[3:]
    l_headcenter_y = []
    for m in l6:
        l_headcenter_y.append(float(m))

    #make list containing x,y tuples
    coor_headcenter = list(zip(l_headcenter_x, l_headcenter_y))
    
    
    l_location_headcenter = []

    for n in coor_headcenter:
        if leftup_openarm.contains(Point(n)) or rightdown_openarm.contains(Point(n)):
            l_location_headcenter.append('Inside')
    
        elif leftdown_closearm.contains(Point(n)) or rightup_closearm.contains(Point(n)):
            l_location_headcenter.append('Inside')
    
        elif center_square.contains(Point(n)):
            l_location_headcenter.append('Inside')
    
        else:
            l_location_headcenter.append('Outside')

    with open('/Users/RoyKudo/Desktop/EPM results/head_dip_result/' + f.replace('.csv', '_headcenter_detection _result.csv'), 'a') as t:
        for o in l_location_headcenter:
            t.write(o)
            t.write('\n')
            

    l_bodycenter_location = []
    with open('/Users/RoyKudo/Desktop/EPM results/bodycenter_only/' + f.replace('.csv', '_bodycenter_detection_result.csv'), "r") as csv2:
        csv_reader2 = csv.reader(csv2, delimiter=',')
        for lines in csv_reader2:
            l_bodycenter_location.append(lines[0])

    l_headcenter_location = []
    with open('/Users/RoyKudo/Desktop/EPM results/head_dip_result/'+ f.replace('.csv', '_headcenter_detection _result.csv'), "r") as csv3:
        csv_reader3 = csv.reader(csv3, delimiter=',')
        for lines in csv_reader3:
            l_headcenter_location.append(lines[0])

    coor_head_dips = list(zip(l_bodycenter_location, l_headcenter_location))
    
    
    pre_headip_index = []
    for x, y in enumerate(coor_head_dips):
        if y[0] == 'Open' and y[1] == 'Outside':
            pre_headip_index.append(x)
            
            
    iterable = pre_headip_index
    L = [list(group) for group in mit.consecutive_groups(iterable)]

    start_head_dip = []
    for p in L:
        if len(p) >= 30: # only the status of 'head center outside the frame when body center inside open arm' > 30 frames (=1 sec) are counted
            start_head_dip.append(len(p))

    with open('/Users/RoyKudo/Desktop/EPM results/head_dip_result/EPM_head_dip_result.csv', 'a') as t:
        t.write(f.replace('.csv', '') +'_head_dip_times')
        t.write('\t')
        t.write(str(len( start_head_dip)))
        t.write('\n')


# # For 5 min data

# In[18]:


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import more_itertools as mit
import csv
import os

folder = os.listdir('/Users/RoyKudo/Desktop/EPM results/5_min_bodycenter_only/')

for f in folder:
    if '.csv' in f:
        l_bodycenter_location = []
        with open('/Users/RoyKudo/Desktop/EPM results/5_min_bodycenter_only/' + f, "r") as csv2:
            csv_reader2 = csv.reader(csv2, delimiter=',')
            for lines in csv_reader2:
                l_bodycenter_location.append(lines[1])

        l_headcenter_location = []
        with open('/Users/RoyKudo/Desktop/EPM results/5_min_head_dip_result/'+ f.replace('_bodycenter_detection_result.csv', '_headcenter_detection _result.csv'), "r") as csv3:
            csv_reader3 = csv.reader(csv3, delimiter=',')
            for lines in csv_reader3:
                l_headcenter_location.append(lines[1])

        coor_head_dips = list(zip(l_bodycenter_location, l_headcenter_location))
    
    
        pre_headip_index = []
        for x, y in enumerate(coor_head_dips):
            if y[0] == 'Open' and y[1] == 'Outside':
                pre_headip_index.append(x)
            
            
        iterable = pre_headip_index
        L = [list(group) for group in mit.consecutive_groups(iterable)]

        start_head_dip = []
        for p in L:
            if len(p) >= 30: # only the status of 'head center outside the frame when body center inside open arm' > 30 frames (=1 sec) are counted
                start_head_dip.append(len(p))

        with open('/Users/RoyKudo/Desktop/EPM results/5_min_head_dip_result/EPM5_min__head_dip_result.csv', 'a') as t:
            t.write(f.replace('.csv', '') +'_head_dip_times')
            t.write('\t')
            t.write(str(len( start_head_dip)))
            t.write('\n')


# In[ ]:




