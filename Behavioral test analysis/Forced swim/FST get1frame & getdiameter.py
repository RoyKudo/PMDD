#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# get 1 frame from each video
import os
import cv2
def get1frame(f):
    cap = cv2.VideoCapture('/Users/RoyKudo/Desktop/FST results/videos/' + f)
    total_frames = cap.get(1)
    ret, frame = cap.read()
    cv2.imwrite('/Users/RoyKudo/Desktop/FST results/get1frame/' + f.replace('.mp4', '.png'), frame)
    
for f in os.listdir('/Users/RoyKudo/Desktop/FST results/videos/'):
    if f.endswith('mp4'):
        get1frame(f)


# In[ ]:


# create a csv with titles of vertices
l1 = ['left_', 'right_']
l2 = ['x: ', 'y: ']
l3 = []

for i in l1:
    for j in l2:
            l3.append(i+j)

with open('/Users/RoyKudo/Desktop/FST results/getdiameter/title_of vertices.csv', 'a') as t:
    for k in l3:
        t.write(k)
        t.write('\n')


# In[ ]:


import matplotlib.pyplot as plt
import cv2
import numpy as np

# get coor of busket in frame by clicking on the picture
# clicking order: left side of busket, right side of busket (use two point to measure the diameter of the busket)
# remember to change path of each video
img = cv2.imread('/Users/RoyKudo/Desktop/FST results/get1frame/79.png')

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        
        with open('/Users/RoyKudo/Desktop/FST results/getdiameter/79.csv', 'a') as t:
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


# In[1]:


# optional: merge title csv & coor csv
import csv
with open('/Users/RoyKudo/Desktop/FST results/getdiameter/title_of vertices.csv') as infile1, open('/Users/RoyKudo/Desktop/FST results/getdiameter/79.csv') as infile2, open('/Users/RoyKudo/Desktop/FST results/getdiameter/79_busket_dia_coor.csv', 'w') as outfile:
    writer = csv.writer(outfile, delimiter='\t')
    for row1,row2 in zip(csv.reader(infile1, delimiter='\t'), csv.reader(infile2, delimiter='\t')):
        writer.writerow(row1+row2)


# In[ ]:




