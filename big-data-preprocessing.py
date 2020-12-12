import numpy as np
import pandas as pd
import sklearn 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, skew


data = pd.read_csv('video-game-sales-data.csv')

data.shape
corr = data.corr(method='pearson')
sns.heatmap(data.corr(), annot=True, linewidths=-1)
data.describe()
data.info()
data.isnull().sum()

data.head(5)
data.drop(['Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'], axis='columns', inplace=True)

# mark rare platforms as 'other' category
print(data['Platform'].value_counts())

data.loc[data['Platform'].isin((data['Platform'].value_counts()
                                [data['Platform'].value_counts() < 50]).index), 'Platform'] = 'Other'


# turn Genre column into dummy variable

dummyGenre = pd.get_dummies(data['Genre'])
data = pd.concat([data,dummyGenre], axis=1)
data.drop('Genre', axis=1, inplace=True)

cols = data.columns.tolist()
cols = cols[:3] + cols[4:] + cols[3:4]
data = data[cols]
data.head(5)



# we will be predicting the Global Sales, so for independent variables we don't
# take EU, NA, JPN and OTHER Sales

x = data.iloc[:, :-1].values
y = data.iloc[:,-1:].values

data2 = data.iloc[:5,:]
