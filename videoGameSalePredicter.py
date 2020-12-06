import numpy as np
import pandas as pd
import sklearn 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, skew

# Original dataset that founded from kaggle
# Deleted the unneeded columns and converted it into new csv file for easier use

data = pd.read_csv('Video_Games.csv')
data = data.drop(['User_Count', 'Critic_Count', 'Developer'], axis=1)

# visualize critic score point and global sales relationship
plt.scatter(data['Critic_Score'], data['Global_Sales'], s=10)
plt.ylabel('Global_Sales', fontsize=13)
plt.xlabel('Critic_Score', fontsize=13)
plt.legend()
plt.show()

# as shown in scatter plot, we have to delete the outlier
data = data.drop(data[(data['Critic_Score']>60) & (data['Global_Sales']>60)].index)

# by plotting again, we can see that we got rid of from an outlier
plt.scatter(data['Critic_Score'], data['Global_Sales'], s=10)
plt.ylabel('Global_Sales', fontsize=13)
plt.xlabel('Critic_Score', fontsize=13)
plt.legend()
plt.show()



