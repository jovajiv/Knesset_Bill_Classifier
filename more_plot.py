
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns





print('reading csv')
df = pd.read_csv('./bill_with_categories.csv')
print('filtering ids not in csv')
#df = df[~df.id.isin(file_names)]
df_toxic = df.drop(['bill_id'], axis=1)
print(df_toxic)
counts=[]


#number of laws per category
categories = list(df_toxic.columns.values)
for i in categories:
    counts.append((i,df_toxic[i].sum()))
df_stats=pd.DataFrame(counts,columns=['category','number_of_laws'])
print(df_stats)

df_stats.plot(x='category', y='number_of_laws', kind='bar', legend=False, grid=True, figsize=(8, 5))
plt.title("Number of bills per category")
plt.ylabel('# of Occurrences', fontsize=12)
plt.xlabel('category', fontsize=12)
plt.show()




#number of laws with multiple categories
rowsums = df.iloc[:,2:].sum(axis=1)
x=rowsums.value_counts()

#plot
plt.figure(figsize=(8,5))
ax = sns.barplot(x.index, x.values)
plt.title("number of bills with Multiple categories")
plt.ylabel('# of Occurrences', fontsize=12)
plt.xlabel('# of categories', fontsize=12)
plt.show()