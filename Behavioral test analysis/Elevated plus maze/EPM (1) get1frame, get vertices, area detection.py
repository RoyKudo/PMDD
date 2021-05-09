#!/usr/bin/env python
# coding: utf-8

# # Get 1 frame from each video

# In[ ]:


import os
import cv2


# In[ ]:


def get1frame(f):
    cap = cv2.VideoCapture('/Users/RoyKudo/Desktop/EPM videos/' + f)
    total_frames = cap.get(1)
    ret, frame = cap.read()
    cv2.imwrite('/Users/RoyKudo/Desktop/EPM results/get1frame/' + f.replace('.mp4', '.png'), frame)
    
for f in os.listdir('/Users/RoyKudo/Desktop/EPM videos/'):
    if f.endswith('mp4'):
        get1frame(f)


# # Get vertices of area from each frame

# In[8]:


import matplotlib.pyplot as plt
import cv2
import numpy as np


# ## (Create a csv with titles of vertices)

# In[ ]:


l1 = ['left_open_', 'left_close_', 'center_square_', 'right_close_', 'right_open_']
l2 = ['leftup_', 'rightup_', 'rightdown_', 'leftdown_']
l3 = ['x: ', 'y: ']
l4 = []

for i in l1:
    for j in l2:
        for k in l3:
            l4.append(i+j+k)

with open('/Users/RoyKudo/Desktop/EPM results/getvertices/title_of vertices.csv', 'a') as t:
    for m in l4:
        t.write(m)
        t.write('\n')


# ## (Do this to each video to get the coordinates of vertices)

# In[ ]:


# get coor of all the vertices in frame by clicking on the picture
# clicking order: (always start from the leftest point of the area) upper-left open arm, lower-left closed arm, square in center, upper-right closed arm, lower-right open arm
#change path of each video
img = cv2.imread('/Users/RoyKudo/Desktop/EPM results/get1frame/79.png')

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        
        with open('/Users/RoyKudo/Desktop/EPM results/getvertices/79.csv', 'a') as t:
            t.write(str(x))
            t.write('\n')
            t.write(str(y))
            t.write('\n')
        
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        cv2.imshow("image", img)

cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)

while(True):
    try:
        cv2.waitKey(100)
    except Exception:
        cv2.destroyWindow("image")
        break
        
cv2.waitKey(0)
cv2.destroyAllWindow()


# ## (Optional: merge two files of titles and vertices)

# In[1]:


import csv
with open('/Users/RoyKudo/Desktop/EPM results/getvertices/title_of vertices.csv') as infile1, open('/Users/RoyKudo/Desktop/EPM results/getvertices/79.csv') as infile2, open('/Users/RoyKudo/Desktop/EPM results/getvertices/79_vertices.csv', 'w') as outfile:
    writer = csv.writer(outfile, delimiter='\t')
    for row1,row2 in zip(csv.reader(infile1, delimiter='\t'), csv.reader(infile2, delimiter='\t')):
        writer.writerow(row1+row2)


# # Create area of polygons by shapely & detect bodycenter

# In[2]:


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# ## (Turn vertices in csv into list of tuple)

# In[3]:


import csv

l1 = []
l_yrows = []

with open('/Users/RoyKudo/Desktop/EPM results/getvertices/79.csv', 'r') as f:
    l = list(f)
    for i in l:
        l1.append(int(i.replace('\n','')))
        
l_xrows = list(l1[::2])
l2 = list(l1[1::2])

for j in l2: # have to reverse the y axis since they're the opposites in cv2 & sharply
     l_yrows.append(j)

coor = list(zip(l_xrows, l_yrows))


# ## (create area polygons)

# In[4]:


leftup_openarm = Polygon(coor[0:4])
leftdown_closearm = Polygon(coor[4:8])
center_square = Polygon(coor[8:12])
rightup_closearm = Polygon(coor[12:16])
rightdown_openarm = Polygon(coor[16:20])


# ## (Get x, y coordinates of bodycenter from DLC result csv)

# In[5]:


import csv

#for x axis:
l = []
with open('/Users/RoyKudo/Desktop/EPM results/coor csv/79_coor.csv', "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
        l.append(lines[1])
l1 = l[3:]
l_bodycenter_x = []
for i in l1:
    l_bodycenter_x.append(float(i))

#for y axis:
l2 = []
with open('/Users/RoyKudo/Desktop/EPM results/coor csv/79_coor.csv', "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
        l2.append(lines[2])
l3 = l2[3:]
l_bodycenter_y = []
for j in l3:
    l_bodycenter_y.append(float(j))

#make list containing x,y tuples
coor_bodycenter = list(zip(l_bodycenter_x, l_bodycenter_y))


# ## (Detect locations of bodycenter)

# In[6]:


l_location_bodycenter = []

for i in coor_bodycenter:
    if leftup_openarm.contains(Point(i)) or rightdown_openarm.contains(Point(i)):
        l_location_bodycenter.append('Open')
    
    elif leftdown_closearm.contains(Point(i)) or rightup_closearm.contains(Point(i)):
        l_location_bodycenter.append('Close')
    
    elif center_square.contains(Point(i)):
        l_location_bodycenter.append('Center')
    
    else:
        l_location_bodycenter.append('Outlier')

with open('/Users/RoyKudo/Desktop/EPM results/area_detection_result/79_bodycenter_detection_result.csv', 'a') as t:
    for j in l_location_bodycenter:
        t.write(j)
        t.write('\n')


# # Calculate the time ratio in close arms

# In[7]:


def closearm_ratio():
    with open('/Users/RoyKudo/Desktop/EPM results/area_detection_result/79_bodycenter_detection_result.csv', "r") as fh:
        fhstr = fh.read()
        close_count = fhstr.count('Close')
        total_count = close_count + fhstr.count('Open') + fhstr.count('Center') + fhstr.count('Outlier')
        close_time_ratio = close_count / total_count
        return str(close_time_ratio)

with open('/Users/RoyKudo/Desktop/EPM results/area_detection_result/closearm_ratio_result.csv', 'a') as t:
    t.write('79_bodycenter_detection_result.csv')
    t.write('\t')
    t.write(closearm_ratio())
    t.write('\n')


# In[ ]:




