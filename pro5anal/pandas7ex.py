import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 5-1
df=pd.read_csv('titanic_data.csv')

bins=[1,20,35,60,150]
labels=["소년","청년","장년","노년"]
df['나이대']=pd.cut(df['Age'],bins=bins,labels=labels)
result=df.groupby('나이대',observed=True)['Survived'].sum()
result=result.reset_index()
result.columns=['나이대','생존자수']
print(result)
print()

# 5-2
pivot1 = df.pivot_table(
    values='Survived',
    index='Sex',
    columns='Pclass',
    aggfunc='mean'
).round(2)
print(pivot1)
print()

pivot2 = df.pivot_table(
    values='Survived',
    index=['Sex', '나이대'],
    columns='Pclass',
    aggfunc='mean',
    observed=True
)
pivot2 = (pivot2 * 100).round(2)
print(pivot2)
print()

print('------------------')

# 6-1
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/human.csv",skipinitialspace=True)
print(df)
df.columns = df.columns.str.strip()
print(df.dropna(subset=["Group"]))
df1 = df.dropna(subset=["Group"])
print(df1[['Career', 'Score']])
print(df1[['Career', 'Score']].mean())
print()

# 6-2
df3 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tips.csv")
print(df3.info())
print(df3.head(3))
print(df3.describe())
print(df3["smoker"].value_counts())
print(df3["day"].unique())

