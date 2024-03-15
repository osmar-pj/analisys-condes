import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from model.getUnit import getUnits
from model.reportDatos import Datos
# from model.getResource import getResources

units = getUnits()

start = datetime(2023, 5, 1, 0, 0, 0)
end = datetime(2024, 1, 31, 23, 59, 59)
unit = 26646581

total, summary = Datos(unit, start, end)

df = total

# df['ratio'] = df['Consumed']/df['EngineHours']

df['wasser'] = 'No'
df['etapa'] = 1
df.loc[df['Grouping'] > datetime(2023, 9, 27, 0, 0, 0), 'etapa'] = 2
df.loc[df['Grouping'] > datetime(2023, 10, 11, 0, 0, 0), 'etapa'] = 3
df.loc[df['Grouping'] > datetime(2023, 10, 25, 0, 0, 0), 'etapa'] = 4
df.loc[df['Grouping'] > datetime(2023, 11, 7, 0, 0, 0), 'etapa'] = 5
df.loc[df['Grouping'] > datetime(2023, 11, 22, 0, 0, 0), 'etapa'] = 6
df.loc[df['Grouping'] > datetime(2023, 12, 6, 0, 0, 0), 'etapa'] = 7
df.loc[df['Grouping'] > datetime(2023, 12, 20, 0, 0, 0), 'etapa'] = 8
df.loc[df['Grouping'] > datetime(2023, 11, 7, 0, 0, 0), 'wasser'] = 'Si'

df.groupby('etapa').agg({'Consumed': 'sum', 'EngineHours': 'sum', 'Grouping': ['min', 'max']})
df.groupby('wasser').agg({'Consumed': 'sum', 'EngineHours': 'sum', 'Grouping': ['min', 'max']})


df['week'] = df['Grouping'].dt.strftime('%U')
# month in spanish
df['nroMonth'] = df['Grouping'].dt.strftime('%m')
df['month'] = df['Grouping'].dt.strftime('%B')
df['month'] = df['month'].str.capitalize()
df['month'] = df['month'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df['year'] = df['Grouping'].dt.strftime('%Y')

# resample weeks
diario_week = df.resample('W-Mon', on='Grouping').sum().reset_index().sort_values(by='Grouping')

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

# fig.add_trace(go.Bar(x=df.index, y=df['ratio'], name="ratio"), row=1, col=1)
fig.add_trace(go.Scatter(x=df['Grouping'], y=df['Consumed'], name="Consumed"), row=2, col=1)
fig.add_trace(go.Scatter(x=df['Grouping'], y=df['EngineHours'], name="EngineHours"), row=2, col=1)

# Calcular y agregar la línea de tendencia para 'ratio' cuando 'wasser' es "Si"
trendline_si = go.Scatter(x=df.loc[df['wasser'] == "Si"].index,
                          y=np.poly1d(np.polyfit(df.loc[df['wasser'] == "Si"].index,
                                                    df.loc[df['wasser'] == "Si"]['ratio'], 1))(df.loc[df['wasser'] == "Si"].index),
                          mode='lines', name='Trendline Wasser Si')
fig.add_trace(trendline_si, row=1, col=1)

# Calcular y agregar la línea de tendencia para 'ratio' cuando 'wasser' es "No"
trendline_no = go.Scatter(x=df.loc[df['wasser'] == "No"].index,
                          y=np.poly1d(np.polyfit(df.loc[df['wasser'] == "No"].index,
                                                    df.loc[df['wasser'] == "No"]['ratio'], 1))(df.loc[df['wasser'] == "No"].index),
                          mode='lines', name='Trendline Wasser No')
fig.add_trace(trendline_no, row=1, col=1)

fig.update_layout(height=600, width=800, title_text="Stacked Subplots")
fig.show()

week = df.groupby(['month', 'week', 'etapa', 'wasser']).agg({'ratio': 'mean'})
d = df.groupby(['etapa', 'wasser']).agg({'Consumed':['mean', 'sum'],'EngineHours':['mean', 'sum'], 'ratio': 'mean'})
d['ratio_cumm'] = d['Consumed']['sum'] / d['EngineHours']['sum']
d['diff_ratio'] = d['ratio_cumm'].diff()*100/d['ratio_cumm']
d

# graficar Consumed y EngineHours wn twinx,
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=df.loc[df['wasser'] == "No"]['Grouping'], y=df.loc[df['wasser'] == "No"]['ratio'], name="No"), secondary_y=True)
fig.add_trace(go.Bar(x=df.loc[df['wasser'] == "Si"]['Grouping'], y=df.loc[df['wasser'] == "Si"]['ratio'], name="Si"), secondary_y=True)
fig.update_layout(height=600, width=1800, title_text="Stacked Subplots")
fig.show()

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=df['Grouping'], y=df['Consumed'], name="Consumed"), secondary_y=True)
fig.add_trace(go.Scatter(x=df['Grouping'], y=df['EngineHours'], name="EngineHours"), secondary_y=False)
fig.update_layout(height=600, width=1800, title_text="Stacked Subplots")
fig.show()

fig = px.bar(df, x="Grouping", y="ratio", color="wasser", barmode="group")
fig.show()

# filtrar EngineHourse between 8 an 10 hours
diario = df[(df['ratio'] >= 3) & (df['ratio'] <= 6)]
diario = df[(df['EngineHours'] >= 3) & (df['EngineHours'] <= 10)]
diario.groupby(['month', 'week', 'etapa', 'wasser']).agg({'Consumed':['mean', 'sum'],'EngineHours':['mean', 'sum'], 'ratio': 'mean'})
d = diario.groupby(['etapa', 'wasser']).agg({'Consumed':['mean', 'sum'],'EngineHours':['mean', 'sum'], 'ratio': 'mean'})
d['ratio_cumm'] = d['Consumed']['sum'] / d['EngineHours']['sum']
d
# week.reset_index(inplace=True)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=diario.loc[diario['wasser'] == "No"]['Grouping'], y=diario.loc[diario['wasser'] == "No"]['ratio'], name="No"), secondary_y=True)
fig.add_trace(go.Bar(x=diario.loc[diario['wasser'] == "Si"]['Grouping'], y=diario.loc[diario['wasser'] == "Si"]['ratio'], name="Si"), secondary_y=True)
fig.update_layout(height=600, width=1800, title_text="Stacked Subplots")
fig.show()

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=diario['Grouping'], y=diario['Consumed'], name="Consumed"), secondary_y=True)
fig.add_trace(go.Scatter(x=diario['Grouping'], y=diario['EngineHours'], name="EngineHours"), secondary_y=False)
fig.update_layout(height=600, width=1800, title_text="Stacked Subplots")
fig.show()

# resample 3 days
sample = diario[['Grouping', 'EngineHours', 'Consumed']].resample('3D', on='Grouping').sum().reset_index().sort_values(by='Grouping')
sample['ratio'] = sample['Consumed']/sample['EngineHours']
sample['wasser'] = "Si"
sample['etapa'] = 1
df.loc[df['Grouping'] > datetime(2023, 6, 8, 0, 0, 0), 'wasser'] = "No"
df.loc[df['Grouping'] > datetime(2023, 6, 8, 0, 0, 0), 'etapa'] = 2
df.loc[df['Grouping'] > datetime(2023, 9, 4, 0, 0, 0), 'wasser'] = "Si"
df.loc[df['Grouping'] > datetime(2023, 9, 4, 0, 0, 0), 'etapa'] = 3
df.loc[df['Grouping'] > datetime(2023, 9, 11, 0, 0, 0), 'wasser'] = "No"
df.loc[df['Grouping'] > datetime(2023, 9, 11, 0, 0, 0), 'etapa'] = 4
df.loc[df['Grouping'] > datetime(2023, 11, 7, 0, 0, 0), 'wasser'] = "Si"
df.loc[df['Grouping'] > datetime(2023, 11, 7, 0, 0, 0), 'etapa'] = 5
df.loc[df['Grouping'] > datetime(2024, 1, 3, 0, 0, 0), 'wasser'] = "No"
df.loc[df['Grouping'] > datetime(2024, 1, 3, 0, 0, 0), 'etapa'] = 6

fig = px.bar(sample, x="Grouping", y="ratio", color="wasser", barmode="group")
fig.show()

df1 = df.groupby(['etapa', 'wasser']).agg({'Consumed': ['mean', 'sum'], 'EngineHours': ['mean', 'sum'], 'ratio': 'mean'})
df1.reset_index(inplace=True)
df1.columns = ['etapa', 'wasser', 'Consumed_mean', 'Consumed_sum', 'EngineHours_mean', 'EngineHours_sum', 'ratio_mean']
df1['ratio_acc'] = df1['Consumed_sum']/df1['EngineHours_sum']

df1 = diario.query('etapa == "2da etapa"').head(21)
df1['etapa'] = "1ra etapa"
df2 = diario.query('etapa == "2da etapa"').tail(21)
df3 = diario.query('etapa == "3ra etapa"').head(21)
df4 = pd.concat([df1, df2, df3])
df4.reset_index(inplace=True)

fig = px.bar(df4, x=df4.index, y="ratio", color="etapa", barmode="group")
fig.show()

df5 = df4.groupby(['etapa', 'wasser']).agg({'Consumed':['mean', 'sum'],'EngineHours':['mean', 'sum'], 'ratio': 'mean'})
df5.reset_index(inplace=True)
df5.columns = ['etapa', 'wasser', 'Consumed_mean', 'Consumed_sum', 'EngineHours_mean', 'EngineHours_sum', 'ratio_mean']
df5['ratio_acc'] = df4['Consumed_sum']/df4['EngineHours_sum']

# grafico violin de df
fig = px.violin(df, y="ratio", x="etapa", color="wasser", box=True, points="all", hover_data=df.columns)
fig.show()