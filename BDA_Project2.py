import numpy as np
import pandas as pd
import sklearn 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, skew

def isNumericalString(s):
    for char in s:
        if not (char.isnumeric() or char == '.'):
            return False
    return True

    
data = pd.read_csv('video-game-sales-data.csv')

# visualize critic score point and global sales relationship
plt.scatter(data['Critic_Score'], data['Global_Sales'], s=10)
plt.ylabel('Global_Sales', fontsize=13)
plt.xlabel('Critic_Score', fontsize=13)
plt.show()

# as shown in scatter plot, we have to delete the outlier

data = data.drop(data[(data['Critic_Score']>60) & (data['Global_Sales']>60)].index)

# by plotting again, we can see that we got rid of from an outlier

plt.scatter(data['Critic_Score'], data['Global_Sales'], s=10)
plt.ylabel('Global_Sales', fontsize=13)
plt.xlabel('Critic_Score', fontsize=13)
plt.show()


print(data['Year_of_Release'].max())
data.loc[data['Year_of_Release'] > 2020, "Year_of_Release"] /= 10 
print(data['Year_of_Release'].max())

plt.scatter(data['Year_of_Release'], data['Global_Sales'], s=10)
plt.ylabel('Global_Sales', fontsize=13)
plt.xlabel('Year_of_Release', fontsize=13)
plt.show()

# most of the data in 'User_Score' column is not numerical, so convert them

for index, row in data.iterrows():
    var = row['User_Score']
    if isinstance(var, float):
        continue
    if isNumericalString(var):
        data.at[index, 'User_Score'] = float(var) * 10.0
    else:
        data.at[index, 'User_Score'] = np.nan
    
data['User_Score'] = data['User_Score'].apply(pd.to_numeric)
    
plt.scatter(data['User_Score'], data['Global_Sales'], s=10)
plt.ylabel('Global_Sales', fontsize=13)
plt.xlabel('User_Score', fontsize=13)
plt.show()



for index, row in data.iterrows():
    if row['Rating'] == 'E10+':
        data.at[index, 'Rating'] = 'E10'

groupedByRating = data.groupby('Rating')
meanRating = groupedByRating.mean()
meanRating = meanRating.reset_index()

fig = plt.figure()
plt.bar(meanRating['Rating'], meanRating['User_Score'])
plt.ylim(ymin=40)
plt.xlabel('Content Rating') 
plt.ylabel('Average User Score') 
plt.title('Average User Scores of Content Rating Categories') 
plt.show() 

fig = plt.figure()
plt.bar(meanRating['Rating'], meanRating['Global_Sales'])
plt.xlabel('Content Rating') 
plt.ylabel('Average Global Sale (Millions)') 
plt.title('Average Global Sale Amount of Content Rating Categories') 
plt.show() 
    

data.loc[data['Platform'].isin((data['Platform'].value_counts()
                                [data['Platform'].value_counts() < 50]).index), 'Platform'] = 'Other'

groupedByPlatform = data.groupby('Platform')
sumPlatform = groupedByPlatform.sum().reset_index()
meanPlatform = groupedByPlatform.mean().reset_index()

fig = plt.figure()
plt.bar(sumPlatform['Platform'], sumPlatform['Global_Sales'])
plt.xlabel('Platform') 
plt.xticks(rotation='vertical')
plt.ylabel('Total Global Sales(Millions)') 
plt.title('Total Global Sale Amount of Platforms') 
plt.show() 

fig = plt.figure()
plt.bar(meanPlatform['Platform'], meanPlatform['Global_Sales'])
plt.xlabel('Platform') 
plt.xticks(rotation='vertical')
plt.ylabel('Average Global Sales(Millions)') 
plt.title('Average Global Sale Amount of Platforms') 
plt.show() 




data2 = pd.read_csv('video-game-sales-data.csv')







