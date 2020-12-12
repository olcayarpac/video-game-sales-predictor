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
fig = plt.figure(dpi=1200)
plt.scatter(data['Critic_Score'], data['Global_Sales'], s=10)
plt.ylabel('Global_Sales', fontsize=13)
plt.xlabel('Critic_Score', fontsize=13)
plt.show()

# as shown in scatter plot, we have to delete the outlier

data = data.drop(data[(data['Critic_Score']>60) & (data['Global_Sales']>60)].index)

# by plotting again, we can see that we got rid of from an outlier

fig = plt.figure(dpi=1200)
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

fig = plt.figure(dpi=1200)
plt.bar(meanRating['Rating'], meanRating['User_Score'])
plt.ylim(ymin=40)
plt.xlabel('Content Rating') 
plt.ylabel('Average User Score') 
plt.title('Average User Scores of Content Rating Categories') 
plt.show() 

fig = plt.figure(dpi=1200)
plt.bar(meanRating['Rating'], meanRating['Global_Sales'])
plt.xlabel('Content Rating') 
plt.ylabel('Average Global Sale (Millions)') 
plt.title('Average Global Sale Amount of Content Rating Categories') 
plt.show() 

# mark platform as other

data.loc[data['Platform'].isin((data['Platform'].value_counts()
                                [data['Platform'].value_counts() < 50]).index), 'Platform'] = 'Other'

groupedByPlatform = data.groupby('Platform')
sumPlatform = groupedByPlatform.sum().reset_index()
meanPlatform = groupedByPlatform.mean().reset_index()

fig = plt.figure(dpi=1200)
plt.bar(sumPlatform['Platform'], sumPlatform['Global_Sales'])
plt.xlabel('Platform') 
plt.xticks(rotation='vertical')
plt.ylabel('Total Global Sales (Millions)') 
plt.title('Total Global Sale Amount of Platforms') 
plt.show() 

fig = plt.figure(dpi=1200)
plt.bar(meanPlatform['Platform'], meanPlatform['Global_Sales'])
plt.xlabel('Platform') 
plt.xticks(rotation='vertical')
plt.ylabel('Average Global Sales (Millions)') 
plt.title('Average Global Sale Amount of Platforms') 
plt.show() 

fig = plt.figure(dpi=1200, figsize=(16,8))
ax1 = plt.subplot(121, aspect='equal')
sumPlatform.plot(kind='pie', y = 'Global_Sales', ax=ax1, autopct='%1.1f%%', 
        startangle=90, shadow=False, labels=sumPlatform['Platform'], legend = False, 
        title='Global Sale Distribution and Platform', fontsize=10)
plt.show()


# genre visualization

groupedByGenre = data.groupby('Genre')
sumGenre = groupedByGenre.sum().reset_index()
meanGenre = groupedByGenre.mean().reset_index()

fig = plt.figure(dpi=1200)
plt.bar(sumGenre['Genre'], sumGenre['Global_Sales'])
plt.xlabel('Genre') 
plt.xticks(rotation='vertical')
plt.ylabel('Total Global Sales (Millions)') 
plt.title('Global Sale Amount and Genre ') 
plt.show() 


fig = plt.figure(dpi=1200)
plt.bar(sumGenre['Genre'], meanGenre['User_Score'])
plt.xlabel('Genre') 
plt.xticks(rotation='vertical')
plt.ylabel('Average User Score') 
plt.ylim(ymin=60)
plt.title('Average User Score and Genre ') 
plt.show() 

fig = plt.figure(dpi=1200, figsize=(16,8))
ax1 = plt.subplot(121, aspect='equal')
sumGenre.plot(kind='pie', y = 'Global_Sales', ax=ax1, autopct='%1.1f%%', 
        startangle=90, shadow=False, labels=sumGenre['Genre'], legend = False, 
        title='Global Sales Distribution and Genre', fontsize=10)
plt.show()

# TOP 100 Selled Games

top100 = data.sort_values('Global_Sales',ascending = False).head(100)
top100GroupedGenre = top100.groupby('Genre')
top100GroupedPublisher = top100.groupby('Publisher')
top100SumGenre = top100GroupedGenre.sum().reset_index()
top100SumPublisher = top100GroupedPublisher.sum().reset_index()

fig = plt.figure(dpi=1200, figsize=(16,8))
ax1 = plt.subplot(121, aspect='equal')
top100SumGenre.plot(kind='pie', y = 'Global_Sales', ax=ax1, autopct='%1.1f%%', 
        startangle=90, shadow=False, labels=top100SumGenre['Genre'], legend = False, 
        title='TOP 100 Selled Game, Sales Distribution and Genre', fontsize=10)
plt.show()

fig = plt.figure(dpi=1200, figsize=(16,8))
ax1 = plt.subplot(121, aspect='equal')
top100SumPublisher.plot(kind='pie', y = 'Global_Sales', ax=ax1, autopct='%1.1f%%', 
        startangle=90, shadow=False, labels=top100SumPublisher['Publisher'], legend = False, 
        title='TOP 100 Selled Game, Sale Distributions and Publisher Company', fontsize=10)
plt.show()


# in the dataset, each row specified with a platform, so one game that has multiple
# platform oppurtunity, exists in dataset multiple times. To visualize most selled
# games by ingoring platform we need to group them by name

groupedByName = data.groupby('Name')
top20AllPlatforms = groupedByName.sum().reset_index()
top20AllPlatforms = top20AllPlatforms.sort_values('Global_Sales', ascending=False).head(20)

fig = plt.figure(dpi=1200)
plt.bar(top20AllPlatforms['Name'], top20AllPlatforms['Global_Sales'])
plt.ylim(ymin=20)
plt.xlabel('Name') 
plt.xticks(rotation='vertical')
plt.ylabel('Global Sales (Millions)') 
plt.title('Most Selled Games in All Platforms') 
plt.show() 

# total sale amounts in global by year

groupedByYear = data.groupby('Year_of_Release')
sumByYear = groupedByYear.sum().reset_index()

fig = plt.figure(dpi=1200)
plt.plot(sumByYear['Year_of_Release'], sumByYear['Global_Sales'])
plt.xlabel('Year')
plt.xlim(xmin=1975, xmax=2010)
plt.xticks(rotation='vertical')
plt.ylabel('Total Global Sales (Millions)')
plt.title('Total Sales in Global')
plt.show() 


data.to_csv('video-game-sales-data.csv', index=False)




