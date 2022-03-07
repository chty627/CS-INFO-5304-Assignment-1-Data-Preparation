#!/usr/bin/env python
# coding: utf-8

# # Question 3: Outlier Detection (10 points)
# Chenran Ning (cn257)

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[21]:


# read data
df = pd.read_csv("prog_book.csv", thousands=',')
display(df)


# ## Task 1: Univariate Outlier detection (4 points)

# In[22]:


detection_rows = ["Rating", "Reviews", "Number_Of_Pages", "Price"]
def outlier_detection(df, name):
    data = df[[name]].to_numpy()
    # finding the 1st quartile
    q1 = np.quantile(data, 0.25)
    # finding the 3rd quartile
    q3 = np.quantile(data, 0.75)
    med = np.median(data)
    # finding the iqr region
    iqr = q3 - q1
    # finding upper and lower whiskers
    upper_bound = q3 + (1.5 * iqr)
    lower_bound = q1 - (1.5 * iqr)
#     print(iqr, upper_bound, lower_bound)
    # boxplot of data within the whisker
    data = data[(data >= lower_bound) & (data <= upper_bound)]
    plt.boxplot(data)
    plt.xticks([])
    plt.title(name)
    
plt.figure(figsize = (12,8))
i = 1
for name in detection_rows:
    plt.subplot(2,2,i)
    i += 1
    outlier_detection(df, name)
# plt.show()


# ## Task 2: Multivariate Outlier detection (6 points)

# ### bivariate analysis on all possible pairs of the above features and identify any outliers
# features = ["Rating", "Reviews", "Number_Of_Pages", "Price", "Type_category"]

# In[118]:


from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler, RobustScaler

df["Type_category"] = df["Type"].astype('category').cat.codes
features = ["Rating", "Reviews", "Number_Of_Pages", "Price", "Type_category"]
i = 1
j = 0
plt.figure(figsize=(25,16))

outliers = {}

for feature1 in features:
    for feature2 in features:
        if feature1 == feature2:
            continue
        plt.subplot(5,4,i)
        i += 1
        combined_feature = df[[feature1, feature2]].to_numpy()
        scaled_features = combined_feature.copy()
        # scale to 0,1
        scaler1 = MinMaxScaler()
        scaler1.fit(scaled_features[:,0].reshape(-1, 1))
        scaled_features[:,0] = scaler1.transform(scaled_features[:,0].reshape(-1, 1)).reshape(-1)
        
        scaler2 = MinMaxScaler()
        scaler2.fit(scaled_features[:,1].reshape(-1, 1))
        scaled_features[:,1] = scaler2.transform(scaled_features[:,1].reshape(-1, 1)).reshape(-1)
        
        clustering = DBSCAN(eps=0.3, min_samples=10).fit(scaled_features)
        labels = clustering.labels_
        
        title = feature1 + " " + feature2
        indexs = np.array(np.where(labels < 0)).reshape(-1)
        out = np.array(combined_feature[indexs])
        out = pd.DataFrame(data = out, index = indexs, columns = [feature1, feature2])
        outliers[title] = out
        
        plt.title(title)
        plt.scatter(combined_feature[:,0], combined_feature[:,1], c = labels)
        
plt.show()


# In[119]:


# print the index and value of outliers

print("Outlier indexs and values")
for title, outlier in outliers.items():
    print(title + " : ")
    display(outlier)


# ### all combinations of three variables

# In[128]:



df["Type_category"] = df["Type"].astype('category').cat.codes
features = ["Rating", "Reviews", "Number_Of_Pages", "Price", "Type_category"]
i = 1
j = 0
fig = plt.figure(figsize=(20,60))

outliers = {}

for feature1 in features:
    for feature2 in features:
        if feature1 == feature2:
            continue
        for feature3 in features:
            if feature2 == feature3 or feature3 == feature1:
                continue
            ax = fig.add_subplot(15, 4, i, projection='3d')
            i += 1
            combined_feature = df[[feature1, feature2, feature3]].to_numpy()
            scaled_features = combined_feature.copy()
            # scale to 0,1
            scaler1 = MinMaxScaler()
            scaler1.fit(scaled_features[:,0].reshape(-1, 1))
            scaled_features[:,0] = scaler1.transform(scaled_features[:,0].reshape(-1, 1)).reshape(-1)

            scaler2 = MinMaxScaler()
            scaler2.fit(scaled_features[:,1].reshape(-1, 1))
            scaled_features[:,1] = scaler2.transform(scaled_features[:,1].reshape(-1, 1)).reshape(-1)
            
            scaler3 = MinMaxScaler()
            scaler3.fit(scaled_features[:,2].reshape(-1, 1))
            scaled_features[:,2] = scaler3.transform(scaled_features[:,2].reshape(-1, 1)).reshape(-1)

            clustering = DBSCAN(eps=0.3, min_samples=10).fit(scaled_features)
            labels = clustering.labels_

            title = feature1 + " " + feature2 + " " + feature3
            indexs = np.array(np.where(labels < 0)).reshape(-1)
            out = np.array(combined_feature[indexs])
            out = pd.DataFrame(data = out, index = indexs, columns = [feature1, feature2, feature3])
            outliers[title] = out

            ax.set_title(title)
            ax.scatter3D(combined_feature[:,0], combined_feature[:,1], combined_feature[:,2], c = labels)
        
plt.show()


# In[129]:


print("Outlier indexs and values")
for title, outlier in outliers.items():
    print(title + " : ")
    display(outlier)

