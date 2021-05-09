#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

df_geneid = pd.read_csv('/Users/RoyKudo/Desktop/Exp records/DAVID/210315 featureCounts_origin updown without0 without_unknown 5047.csv')
geneid_list_734 = [k for k in df_geneid['ENSEMBL_GENE_ID']]
df_normalized = pd.read_csv('/Users/RoyKudo/Desktop/Exp records/DAVID/210312 featureCounts origin updown without0 5797.csv')
data = df_normalized[df_normalized.NAME.isin(geneid_list_734)]

data = data.T # row and column transfer
new_header = data.iloc[2] #grab the first row for the header
data = data[3:] #take the data less the header row
data.columns = new_header #set the header row as the df header
data['cluster'] = ['3', '3', '3', '3', '2', '2', '2', '2', '1', '1', '1', '1']

X = data.iloc[:, :-1]  #independent columns
y = data.iloc[:,-1]    #target column i.e price range

data


# In[2]:


# define the evaluation method
cv = RepeatedStratifiedKFold(n_splits=4, n_repeats=3, random_state=1)

# define the pipeline to evaluate
model = LinearSVC(random_state=0)
fs = SelectKBest(score_func=f_classif)
pipeline = Pipeline(steps=[('anova',fs), ('linearsvc', model)])

# define the grid
grid = dict()
grid['anova__k'] = [i+1 for i in range(X.shape[1])]

# define the grid search
search = GridSearchCV(pipeline, grid, scoring='accuracy', cv=cv, n_jobs=-1, verbose=1)

# perform the search
results = search.fit(X, y)

# summarize best
print('Best Mean Accuracy: %.3f' % results.best_score_)
print('Best Config: %s' % results.best_params_)


# In[3]:


import numpy as np

fs = results.best_estimator_.named_steps['anova']
feature_names_example = np.array(list(X))
selected_features = fs.transform(feature_names_example.reshape(1, -1))

print(selected_features[0])
print(len(selected_features[0]))


# In[4]:


import csv
import os
import numpy
from matplotlib import pyplot

coef_array = results.best_estimator_._final_estimator.coef_
importance = coef_array[0]
sf_array = np.array(selected_features[0])

# summarize feature importance
for i,v in zip(sf_array, importance):
    print('Feature:', i, 'Score', round(v, 5))
        
# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()


# In[5]:


l = selected_features[0]
np.set_printoptions(threshold=np.inf)
l
