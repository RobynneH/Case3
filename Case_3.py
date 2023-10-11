#!/usr/bin/env python
# coding: utf-8

# # Case 3: Elektrische auto's

# In[1]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from PIL import Image


# In[2]:


st.set_page_config(layout = "wide")


# In[3]:


st.title("Case 3")


# In[4]:


st.subheader("Team 4: Sten den Hartog, Robynne Hughes, Wolf Huiberts & Charles Huntington")


# In[5]:


image = Image.open('dataset-cover.png')
st.image(image)


# ## Brandstof van net gekochte auto's

# Functie voor het importeren van een dataset

# In[6]:


# functie om een dataset te importeren en verkleinen naar een nieuwe csv
def import_dataset(name_csv, select_column, import_csv, seperator = ','):
#     input: de name_csv en import_csv moeten in stringformaat zijn, en de select_column een lijst
#     de seperator input is niet verplicht, geef je met het aanroepen van de functie niks mee, dan gebruikt de functie een komma
    import_file = pd.read_csv(import_csv, sep = seperator, usecols = select_column)
    import_file.to_csv(name_csv, index = False)


# Importeer twee datasets van de RDW bestanden; het ene bestand bevat kentekens en brandstof type, het andere bestand bevat kentekens en de datum waarop het voertuig is overgezet

# In[7]:


# auto_dataset = import_dataset('auto.csv', ['Kenteken', 'Brandstof omschrijving'], 
#                               'Open_Data_RDW__Gekentekende_voertuigen_brandstof.csv', sep = ';')
# auto = pd.read_csv('auto.csv')
# auto.head()

# auto_aanschaf_dataset = import_dataset('auto_aanschaf.csv',['Kenteken', 'Datum tenaamstelling'], 
#                                'Open_Data_RDW__Gekentekende_voertuigen.csv',';')
# auto_aanschaf = pd.read_csv('auto_aanschaf.csv')
# auto_aanschaf.head()


# - Maak van deze een bestand door de kentekens te mergen van de twee dataframes, en hernoem de kolomnaam
# - Verander de string van de datum naar een echte datum, en verander de form naar yeaar-maand

# In[8]:


# auto_aanschaf_brandstof = auto.merge(auto_aanschaf, how = 'inner', on = 'Kenteken')
# auto_aanschaf_brandstof = auto_aanschaf_brandstof.rename(columns = {'Datum tenaamstelling':'Datum_tenaamstelling'})
# auto_aanschaf_brandstof.head()


# In[9]:


# auto_aanschaf_brandstof["Datum_tenaamstelling"].head()


# In[10]:


# auto_aanschaf_brandstof = auto_aanschaf_brandstof.assign(Datum_tenaamstelling = 
#                                                          pd.to_datetime(auto_aanschaf_brandstof['Datum_tenaamstelling'], 
#                                                                         format='%Y%m%d') )
# auto_aanschaf_brandstof['Datum_tenaamstelling'].head()


# In[11]:


# auto_aanschaf_brandstof['maand_jaar'] = auto_aanschaf_brandstof['Datum_tenaamstelling'].dt.to_period('M')
# auto_aanschaf_brandstof.head()


# Check of er NonAvailable values in het dataframe zitten en verwijder deze

# In[12]:


# auto_aanschaf_brandstof.isna().sum()


# In[13]:


# auto_aanschaf_brandstof_na = auto_aanschaf_brandstof.dropna()


# - Verdeel de dataframe in groupen op de brandstof omschrijving en de datum van tenaamstelling
# - Maak van deze dataframe een nieuw csv bestand, en schrijf code om deze csv in te laden

# In[14]:


# counts_total = auto_aanschaf_brandstof_na.groupby(['Brandstof omschrijving', 'maand_jaar']).count()
# counts_total_ind = counts_total.reset_index()

# counts_total_ind.to_csv('Counts_total.csv', index = False)


# In[15]:


counts_total_ind = pd.read_csv('Counts_total.csv')
counts_total_ind.head()


# - Verdeel de aantal van de groupen op datum in nieuwe dataframes per brandstof
# - Maak een lijndiagram met de type brandstof die gekocht zijn in speciefieke maanden, in de jaren voor 2000 is er weinig over de data te vertellen, dus de range start op het jaar 2000

# In[16]:


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
                 legend_title_text='Brandstof type', xaxis_title="Datum per jaar/maand", 
                  yaxis_title="Aantal gekochtte auto's per brandstof")

# Add range slider
fig.update_layout(xaxis=dict(range = ['2000-01', '2023-12'], rangeslider=dict(visible=True),type="date"))

st.plotly_chart(fig)


# # Map

# In[ ]:


st.divider()


# In[18]:


# # Define the API URL
# api_url = "https://api.openchargemap.io/v3/poi/"

# # Define parameters for the API request with a large maxresults value
# params = {
#     'output': 'json',
#     'countrycode': 'NL',
#     'maxresults': 10000,  # Set a large number
#     'compact': 'true',
#     'verbose': 'false',
#     'key': '49603f59-44ce-4ddf-91b2-7d06f4e9c937'
# }

# # Make the API request
# response = requests.get(api_url, params=params)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the JSON data from the response
#     data = response.json()

#     # Convert to a DataFrame
#     openchargemap = pd.json_normalize(data)

#     # Save the DataFrame as a CSV file in the working directory
#     openchargemap.to_csv('openchargemap_data.csv', index=False)

#     # Display the DataFrame
#     print(openchargemap.head())

# else:
#     # Print an error message if the request was not successful
#     print(f"Error: {response.status_code}")
#     print(response.text)


# In[19]:


openchargemap = pd.read_csv('openchargemap_data.csv')


# In[ ]:


import folium
from folium import plugins
from folium import IFrame
import pandas as pd
import streamlit as st

# Assuming openchargemap is your DataFrame
openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']] = openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']].apply(pd.to_numeric, errors='coerce')
openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']] = openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']].fillna(0)

# Create a folium map centered around the Netherlands
map_center = [52.1326, 5.2913]  # Latitude and Longitude for the center of the Netherlands
charging_map = folium.Map(location=map_center, zoom_start=7, min_zoom=7, max_bounds=True)

# Add TileLayer for CartoDB Positron as the default layer
folium.TileLayer('cartodbpositron', name='CartoDB Positron').add_to(charging_map)

# Use MarkerCluster to prevent overlapping markers
marker_cluster = plugins.MarkerCluster().add_to(charging_map)

# Use vectorized operations and create markers
for _, row in openchargemap.iterrows():
    lat, lon, cost = row['AddressInfo.Latitude'], row['AddressInfo.Longitude'], row['UsageCost']
    address_id, address_title, access_comments = row['AddressInfo.ID'], row['AddressInfo.Title'], row['AddressInfo.AccessComments']
    num_points, status_type = row['NumberOfPoints'], row['StatusTypeID']
    last_status_update_time = pd.to_datetime(row['DateLastStatusUpdate']).strftime('%B %d, %Y, %H:%M:%S %Z')
    
    # Set color based on charging cost
    color = 'blue' if cost <= 0.2 else 'cyan' if cost <= 0.4 else 'lime' if cost <= 0.6 else 'yellow' if cost <= 0.8 else 'red'
    
    # Customize popup content without images
    popup_content = (
        f"<b>ID:</b> {address_id}<br>"
        f"<b>Title:</b> {address_title}<br>"
        f"<b>Access Comments:</b> {access_comments if pd.notna(access_comments) else 'No additional info'}<br>"
        f"<b>Latitude:</b> {lat}<br>"
        f"<b>Longitude:</b> {lon}<br>"
        f"<b>Cost:</b> {cost}<br>"
        f"<b>Number of Points:</b> {num_points}<br>"
        f"<b>Status Type:</b> {status_type}<br>"
        f"<b>Last Status Update Time:</b> {last_status_update_time}<br>"
    )

    # Add Marker to the MarkerCluster
    folium.Marker([lat, lon], icon=None, popup=folium.Popup(IFrame(popup_content, width=300, height=200))).add_to(marker_cluster)

# Add LayerControl to enable switching between map layers
folium.LayerControl().add_to(charging_map)

# Display the map in Streamlit
# st_folium(charging_map)
charging_map


# In[ ]:




