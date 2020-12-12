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
dummyPlatform = pd.get_dummies(data['Platform'])
data = pd.concat([data,dummyGenre], axis=1)
data = pd.concat([data, dummyPlatform], axis=1)
data.drop(['Genre', 'Platform'], axis=1, inplace=True)


cols = data.columns.tolist()
cols = cols[:2] + cols[3:] + cols[2:3]
data = data[cols]
data.head(5)

data = data.dropna()

from sklearn.preprocessing import LabelEncoder
lblEncoderRating = LabelEncoder()
lblEncoderPublisher = LabelEncoder()


data['Rating'] = lblEncoderRating.fit_transform(data['Rating'].astype(str))
data['Publisher'] = lblEncoderPublisher.fit_transform(data['Publisher'].astype(str))



from sklearn.model_selection import train_test_split

x = data.loc[:, data.columns != 'Global_Sales']
y = data.loc[:, data.columns == 'Global_Sales']

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)



