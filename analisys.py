import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv('data/df.csv')
df.dropna(inplace=True)
df['datetime'] = pd.to_datetime(df['datetime'])
df['consumed'] = df['consumed'].apply(lambda x: x.split(' ')[0]).astype('float')
df[['hours', 'consumed']].corr()

sns.regplot(x='hours', y='consumed', data=df)
# grafico de correlacion
sns.heatmap(df[['hours', 'consumed']].corr(), annot=True)

df['hidragen'] = 'Si'
# despues del 17-06-2023 hidragen igual si
df.loc[df['datetime'] > '2023-06-18', 'hidragen'] = 'No'
df['ratio'] = df['consumed'] / df['hours']

sns.relplot(x='datetime', y='ratio', hue='hidragen', data=df)

# get a model to predict the ratio
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = df.query('hidragen == "Si"')[['hours']]
y = df.query('hidragen == "Si"')['consumed']

# splt data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

# train model
model = LinearRegression()
model.fit(X_train, y_train)
model.score(X_test, y_test)

# predict
hours = df.query('hidragen == "No"')['hours']
consumed = df.query('hidragen == "No"')['consumed']
y_pred = model.predict(hours.values.reshape(-1, 1))

y_total = np.concatenate([y, y_pred])
df['consumo_pred'] = y_total
df['ratio_pred'] = df['consumo_pred'] / df['hours']

sns.relplot(x='datetime', y='consumed', hue='hidragen', kind='line', data=df, height=5, aspect=2)
sns.relplot(x='datetime', y='consumo_pred', hue='hidragen', kind='line', data=df, height=5, aspect=2)

ratio = df.query('hidragen == "Si"')['consumed'].sum() / df.query('hidragen == "Si"')['hours'].sum()
ratio_real = df.query('hidragen == "No"')['consumed'].sum() / df.query('hidragen == "No"')['hours'].sum()
ratio_pred = df.query('hidragen == "No"')['consumo_pred'].sum() / df.query('hidragen == "No"')['hours'].sum()

variacion = (ratio_real - ratio_pred) / ratio_real