#!/usr/bin/env python
# coding: utf-8

# # Case 3: Elektrische auto's

# In[2]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st


# In[ ]:


st.title("Case 3")


# In[ ]:


# functie om een dataset te importeren en verkleinen naar een nieuwe csv
def import_dataset(name_csv, select_column, import_csv, seperator = ','):
#     input: de name_csv en import_csv moeten in stringformaat zijn, en de select_column een lijst
#     de seperator input is niet verplicht, geef je met het aanroepen van de functie niks mee, dan gebruikt de functie een komma
    import_file = pd.read_csv(import_csv, sep = seperator, usecols = select_column)
    import_file.to_csv(name_csv, index = False)


# In[ ]:


# auto_dataset = import_dataset('auto.csv', ['Kenteken', 'Brandstof omschrijving'], 
#                               'Open_Data_RDW__Gekentekende_voertuigen_brandstof.csv', sep = ';')
# auto = pd.read_csv('auto.csv')
# auto.head()


# In[ ]:


# auto_aanschaf_dataset = import_dataset('auto_aanschaf.csv',['Kenteken', 'Datum tenaamstelling'], 
#                                'Open_Data_RDW__Gekentekende_voertuigen.csv',';')
# auto_aanschaf = pd.read_csv('auto_aanschaf.csv')
# auto_aanschaf.head()


# In[ ]:


# auto_aanschaf_brandstof = auto.merge(auto_aanschaf, how = 'inner', on = 'Kenteken')
# auto_aanschaf_brandstof = auto_aanschaf_brandstof.rename(columns = {'Datum tenaamstelling':'Datum_tenaamstelling'})


# In[ ]:


# auto_aanschaf_brandstof.to_csv('auto_aanschaf_brandstof.csv', index = False)


# In[ ]:


# auto_aanschaf_brandstof1 = pd.read_csv('auto_aanschaf_brandstof.csv', nrows = 8000000)
# auto_aanschaf_brandstof1.to_csv('auto_aanschaf_brandstof1.csv')


# In[ ]:


# auto_aanschaf_brandstof2 = pd.read_csv('auto_aanschaf_brandstof.csv', skiprows = 8000000)
# auto_aanschaf_brandstof2.to_csv('auto_aanschaf_brandstof2.csv')


# In[ ]:


# auto_aanschaf_brandstof1 = pd.reaf_csv('auto_aanschaf_brandstof1.csv')
# auto_aanschaf_brandstof2 = pd.read_csv('auto_aanschaf_brandstof.csv')
# auto_aanschaf_brandstof = pd.concat([auto_aanschaf_brandstof1,auto_aanschaf_brandstof2])


# In[3]:


# auto_aanschaf_brandstof = pd.read_csv('auto_aanschaf_brandstof.csv')
# auto_aanschaf_brandstof.head()


# In[4]:


# auto_aanschaf_brandstof["Datum_tenaamstelling"].head()


# In[5]:


# auto_aanschaf_brandstof = auto_aanschaf_brandstof.assign(Datum_tenaamstelling = 
#                                                          pd.to_datetime(auto_aanschaf_brandstof['Datum_tenaamstelling'], 
#                                                                         format='%Y%m%d') )
# auto_aanschaf_brandstof['Datum_tenaamstelling'].head()


# In[6]:


# auto_aanschaf_brandstof['maand_jaar'] = auto_aanschaf_brandstof['Datum_tenaamstelling'].dt.to_period('M')
# auto_aanschaf_brandstof.head()


# In[7]:


# auto_aanschaf_brandstof.isna().sum()


# In[8]:


# auto_aanschaf_brandstof_na = auto_aanschaf_brandstof.dropna()


# In[9]:


# auto_aanschaf_brandstof_na.isna().sum()


# In[10]:


# counts_total = auto_aanschaf_brandstof_na.groupby(['Brandstof omschrijving', 'maand_jaar']).count()
# counts_total_ind = counts_total.reset_index()

# counts_total_ind.to_csv('Counts_total.csv', index = False)


# In[16]:


counts_total_ind = pd.read_csv('Counts_total.csv')
counts_total_ind.head()


# In[12]:


counts_alcohol = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Alcohol']
counts_benzine = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Benzine']
counts_diesel = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Diesel']
counts_elektriciteit = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Elektriciteit']
counts_lpg = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'LPG']
counts_cng = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'CNG']
counts_lng = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'LNG']
counts_waterstof = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Waterstof']
counts_benzine.head()


# In[17]:


fig = go.Figure()

fig.add_trace(go.Scatter(y = counts_alcohol['Datum_tenaamstelling'], x = counts_alcohol['maand_jaar'],
                         mode = 'lines', name = 'Alcohol'))
fig.add_trace(go.Scatter(y = counts_benzine['Datum_tenaamstelling'], x = counts_benzine['maand_jaar'],
                         mode = 'lines', name = 'Benzine'))
fig.add_trace(go.Scatter(y = counts_diesel['Datum_tenaamstelling'], x = counts_diesel['maand_jaar'],
                         mode = 'lines', name = 'Diesel'))
fig.add_trace(go.Scatter(y = counts_elektriciteit['Datum_tenaamstelling'], x = counts_elektriciteit['maand_jaar'],
                         mode = 'lines', name = 'Elektriciteit'))
fig.add_trace(go.Scatter(y = counts_lpg['Datum_tenaamstelling'], x = counts_lpg['maand_jaar'],
                         mode = 'lines', name = 'LPG'))
fig.add_trace(go.Scatter(y = counts_cng['Datum_tenaamstelling'], x = counts_cng['maand_jaar'],
                         mode = 'lines', name = 'CNG'))
fig.add_trace(go.Scatter(y = counts_lng['Datum_tenaamstelling'], x = counts_lng['maand_jaar'],
                         mode = 'lines', name = 'LNG'))
fig.add_trace(go.Scatter(y = counts_waterstof['Datum_tenaamstelling'], x = counts_waterstof['maand_jaar'],
                         mode = 'lines', name = 'Waterstof'))

# Add title
fig.update_layout(title_text="Aankop van auto's met specifieke brandstof per maand",
                 legend_title_text='Brandstof type', xaxis_title="Datum per maand", 
                  yaxis_title="Aantal gekochtte auto's per brandstof")

# Add range slider
fig.update_layout(xaxis=dict(range = ['2000-01', '2023-12'], rangeslider=dict(visible=True),type="date"))

st.plotly_chart(fig)


# In[ ]:




