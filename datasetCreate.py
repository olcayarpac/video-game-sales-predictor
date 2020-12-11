import numpy as np
import pandas as pd
import sklearn 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, skew


data = pd.read_csv('Video_Games.csv')
data2 = pd.read_csv('vgsales-12-4-2019.csv')
data = data.drop(['User_Count', 'Critic_Count', 'Developer'], axis=1)

print(data.isna().sum())

# handle the nan values

for index, row in data.iterrows():
    founded = data2.loc[data2['Name']==row['Name']]
    
    if pd.isnull(row['Rating']):
        filtered = founded[founded['ESRB_Rating'].notnull()]
        if not filtered.empty:
            data.at[index, 'Rating'] = filtered['ESRB_Rating'].iloc[0]
    
    if pd.isnull(row['Critic_Score']):
        filtered = founded[founded['Critic_Score'].notnull()]
        if not filtered.empty:
            data.at[index, 'Critic_Score'] = (filtered['Critic_Score'].iloc[0] * 10)
    
    if pd.isnull(row['User_Score']):
        filtered = founded[founded['User_Score'].notnull()]
        if not filtered.empty:
            data.at[index, 'User_Score'] = (filtered['User_Score'].iloc[0])
    
    if pd.isnull(row['Year_of_Release']):
        filtered = founded[founded['Year'].notnull()]
        if not filtered.empty:
            data.at[index, 'Year_of_Release'] = (filtered['Year'].iloc[0])
           
    print(index)
    
data.to_csv('video-game-sales-data.csv', index=False)


print(data.isna().sum())



