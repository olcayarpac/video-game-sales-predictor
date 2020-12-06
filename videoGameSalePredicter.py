import numpy as np
import pandas as pd
import sklearn 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, skew

data2 = pd.read_csv('vgsales-12-4-2019.csv')

# Original dataset that founded from kaggle
# Deleted the unneeded columns and converted it into new csv file for easier use

data = pd.read_csv('Video_Games.csv')
data = data.drop(['User_Count', 'Critic_Count', 'Developer'], axis=1)

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

print(data.isna().sum())
# handle the nan values

for index, row in data.iterrows():
    foundedInOtherDataset = data2.loc[data2['Name']==row['Name']]
    
    if pd.isnull(row['Rating']) and foundedInOtherDataset.size > 0:
        modeOfRating = foundedInOtherDataset['ESRB_Rating'].mode()
        if modeOfRating.size > 0:
            data.at[index, 'Rating'] = modeOfRating[0]
        
    if pd.isnull(row['Critic_Score']) and foundedInOtherDataset.size > 0:
        modeOfRating = foundedInOtherDataset['Critic_Score'].mode()
        if modeOfRating.size > 0:
            data.at[index, 'Critic_Score'] = modeOfRating[0] * 10.0
    
    if pd.isnull(row['User_Score']) and foundedInOtherDataset.size > 0:
        modeOfRating = foundedInOtherDataset['User_Score'].mode()
        if modeOfRating.size > 0:
            data.at[index, 'User_Score'] = modeOfRating[0]
    
    if pd.isnull(row['Year_of_Release']) and foundedInOtherDataset.size > 0:
        modeOfRating = foundedInOtherDataset['Year'].mode()
        if modeOfRating.size > 0:
            data.at[index, 'Year_of_Release'] = modeOfRating[0]
            
    
data.to_csv('ourNewData.csv', index=False)
dataFirstVersion = pd.read_csv('Video_Games.csv')




