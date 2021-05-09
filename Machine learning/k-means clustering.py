#!/usr/bin/env python
# coding: utf-8

# # k-means clustering
# ## 1. Use elbow method to choose the best number of clustering

# In[1]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans 

minmax55_main3 = pd.read_csv('/Users/RoyKudo/Desktop/data analysis result/approach 2/55 minmax 3 result.csv')
minmax55_main3 = minmax55_main3.drop(['number', 'Cluster'], 1)

distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(minmax55_main3)
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(8,4))
sns.lineplot(K, distortions, marker = 'o')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()


# ## 1.5. Double check: Use silhouette coefficient

# In[2]:


from sklearn.metrics import silhouette_score

df = pd.DataFrame(minmax55_main3)

for k1 in range(2, 10):
    clusterer = KMeans(n_clusters=k1)
    preds = clusterer.fit_predict(df)
    centers = clusterer.cluster_centers_

    score = silhouette_score(df, preds)
    print("For n_clusters = {}, silhouette score is {})".format(k1, score))


# ## 2. Perform clustering

# In[3]:


kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10, random_state=0)
pred_y = kmeans.fit_predict(minmax55_main3)
plt.scatter(minmax55_main3['EPM_10m_closearm_ratio'], minmax55_main3['FST_floating_ratio'])
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c='red')
plt.xlabel('EPM_10m_closearm_ratio ')
plt.ylabel('FST_floating_ratio')
plt.show()

print(kmeans.labels_)


# ## 3. Plot 3D figure to observe the scatter of data

# In[4]:


import plotly.express as px
minmax55_main3_result = pd.read_csv('/Users/RoyKudo/Desktop/data analysis result/approach 2/55 minmax 3 result.csv')
fig = px.scatter_3d(minmax55_main3_result, x='EPM_10m_closearm_ratio', y='FST_floating_ratio', z='OFT_center_ratio', color='Cluster')
fig.show()

