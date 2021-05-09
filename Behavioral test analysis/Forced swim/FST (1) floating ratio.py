#!/usr/bin/env python
# coding: utf-8

# In[14]:


import csv
from shapely.geometry.polygon import Polygon
import os
from math import sqrt
import numpy as np
import pandas as pd

folder = os.listdir('/Users/RoyKudo/Desktop/FST results/coor csv/')

for f in folder:
    if '.csv' in f:
# put x, y coordinates of headcenter, tailbase, lbc, rbc in lists
        l = []
        l2 = []
        l4 = []
        l6 = []
        l8 = []
        l10 = []
        l12 = []
        l14 = []
        with open('/Users/RoyKudo/Desktop/FST results/coor csv/' + f, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for lines in csv_reader:
                l.append(lines[4])
                l2.append(lines[5])
                l4.append(lines[7])
                l6.append(lines[8])
                l8.append(lines[10])
                l10.append(lines[11])
                l12.append(lines[13])
                l14.append(lines[14])
        l1 = l[3:]
        l3 = l2[3:]
        l5 = l4[3:]
        l7 = l6[3:]
        l9 = l8[3:]
        l11 = l10[3:]
        l13 = l12[3:]
        l15 = l14[3:]
        headcenter_x = []
        headcenter_y = []
        tailbase_x = []
        tailbase_y = []
        LBC_x = []
        LBC_y = []
        RBC_x = []
        RBC_y = []
        for i in l1:
            headcenter_x.append(float(i))
        for j in l3:
            headcenter_y.append(float(j))
        for k in l5:
            tailbase_x.append(float(k))
        for m in l7:
            tailbase_y.append(float(m))
        for n in l9:
            LBC_x.append(float(n))
        for o in l11:
            LBC_y.append(float(o))
        for p in l13:
            RBC_x.append(float(p))
        for q in l15:
            RBC_y.append(float(q))
    
#  pair the x & y
        headcenter_coor = list(zip(headcenter_x, headcenter_y))
        tailbase_coor = list(zip(tailbase_x, tailbase_y))
        LBC_coor = list(zip(LBC_x, LBC_y))
        RBC_coor = list(zip(RBC_x, RBC_y))

# get polygon area (in cm**2) of each frame
        corners_coor = list(zip(headcenter_coor, LBC_coor, tailbase_coor, RBC_coor))
    
        with open('/Users/RoyKudo/Desktop/FST results/diameter_only/' + f.replace('_coor.csv', '.csv')) as fh:
            reader = csv.reader(fh)
            ls = list(reader)
            
        pix_dia_len = sqrt((int(ls[0][0])-int(ls[2][0]))**2+(int(ls[1][0])-int(ls[3][0]))**2)
        actual_dia_len = 38 #(cm)
        
        def PolygonArea(corners):
            n = len(corners) # of corners
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += corners[i][0] * corners[j][1]
                area -= corners[j][0] * corners[i][1]
            area = abs(area) / 2.0
            return area

        polygen_area = []
        for r in corners_coor:
            polygen_area.append(PolygonArea(list(r)) * ((actual_dia_len ** 2) / (pix_dia_len ** 2)))

        def RollingPositiveAverage(listA, window=11):
            s = pd.Series(listA)
            s[s < 0] = np.nan
            result = s.rolling(window, center=True, min_periods=1).mean()
            result.iloc[:window // 2] = np.nan
            result.iloc[-(window // 2):] = np.nan
            return list(result)

        rolling_mean = RollingPositiveAverage(polygen_area)

        l70 = []
        for a, b in zip(polygen_area, rolling_mean):
            l70.append(abs(a - b))
    
        l71 = []
        for t in l70:
            if t < (60 * ((actual_dia_len ** 2) / (pix_dia_len ** 2))): 
                # 15 px^2 for mice so 60 px^2 for rats (15 is based on previous research of mice) (rats are with about twice length than mice)
                l71.append('Float')   
            else:
                l71.append('Swim')

        with open('/Users/RoyKudo/Desktop/actual_floating_ratio_result.csv', 'a') as t:
            t.write(f.replace('.csv', '') + '_floating_ratio_result.csv')
            t.write('\t')
            t.write(str(l71.count('Float') / len(l71)))
            t.write('\n')


# In[ ]:




