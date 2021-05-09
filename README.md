# PMDD

## Behavioral test analysis
1. Getting coordinates of every frame of behavioral test videos by using DeepLabCut  
↓  
2. Calculating parameters by codes in "Behavioral test analysis" folder:  
Elevated plus maze: total distance traveled, time ratio in closed arms, number of head dips in open arms  
Open field: total distance traveled, time ratio in center zone, number of rearing  
Forced swim: total distance traveled, immobile time ratio  
↓  
3. Clustering by k-means  
Parameters:  
(1) Time ratio in closed arms in elevated plus maze  
(2) Time ratio in center zone in open field  
(3) Immobile time ratio in forced swim  
  
  
## Feature selection  
Linear SVM and SelectKBest in Grid search cv of Repeated stratified k fold  
  
### ・Tools:  
numpy, pandas, cv2, matplotlib, seaborn, plotly.express, k-means, RepeatedStratifiedKFold, SelectKBest, LinearSVC, GridSearchCV
