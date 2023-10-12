#!/usr/bin/env python
# coding: utf-8

# # Case 3: Elektrische auto's

# In[1]:


# pip install streamlit-folium


# In[4]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from streamlit_folium import st_folium


# In[5]:


st.set_page_config(layout = "wide")


# In[6]:


st.title("Case 3: Elektrisch vervoer")


# In[7]:


st.subheader("Team 4: Sten den Hartog, Robynne Hughes, Wolf Huiberts & Charles Huntington")


# In[8]:


image = Image.open('dataset-cover.jpg')
st.image(image)


# In[9]:


st.write("Dit dashboard maakt gebruik van een aantal datasets. De dataset 'Laadpalen' hebben wij van de docenten verkregen en kunt u met de knop hieronder downloaden:")

with open('laadpalen_schoon.csv') as file:
    st.download_button(label = 'Download laadpaaldata als csv', data = file, file_name = 'laadpalen_schoon.csv', mime = 'text/csv')
    
st.write('De tweede dataset gebruiken we via een API, deze dataset hebben wij via de API gedownload en staat nu in de GitHub als .csv-bestand.')
st.write('De laatste dataset hebben we gedownload via de RDW site (link hieronder). De datasets die wij gebruikt hebben zijn: "Open_Data_RDW__Gekentekende_voertuigen" en "Open_Data_RDW__Gekentekende_voertuigen_brandstof".')
st.link_button("Data RDW", "https://opendata.rdw.nl/")
st.divider()


# # Data import en opschoning

# In[10]:


st.header("Data Cleaning")


# In[11]:


Laadpalen_schoon=pd.read_csv("laadpalen_schoon.csv")


# In[12]:


# Laadpalen_schoon.columns


# In[13]:


#Choose only relevant columns

Laadpalen_schoon=Laadpalen_schoon[['DateLastVerified',
       'NumberOfPoints', 'DateLastStatusUpdate', 'DateCreated',
       'AddressInfo.ID', 'AddressInfo.Title', 'AddressInfo.AddressLine1',
       'AddressInfo.Town', 'AddressInfo.StateOrProvince',
       'AddressInfo.Postcode', 'AddressInfo.Latitude',
       'AddressInfo.Longitude','LevelID','Amps', 'Voltage', 'PowerKW']]


# In[14]:


head = Laadpalen_schoon.head()
st.write('Eerste vijf regels van laadpalen: ', head)


# In[15]:


Laadpalen_schoon.head()


# In[16]:


code = '''Laadpalen_schoon.isna().sum()
Laadpalen_schoon['AddressInfo.Town'] = Laadpalen_schoon['AddressInfo.Town'].fillna('Missing')
Laadpalen_schoon['AddressInfo.Postcode'] = Laadpalen_schoon['AddressInfo.Postcode'].fillna('Missing')
Laadpalen_schoon['AddressInfo.AddressLine1'] = Laadpalen_schoon['AddressInfo.AddressLine1'].fillna('Missing')
Laadpalen_schoon['AddressInfo.StateOrProvince'] = Laadpalen_schoon['AddressInfo.StateOrProvince'].fillna('Missing')'''
st.code(code, language='python')


# In[17]:


Laadpalen_schoon.isna().sum()


# In[18]:


Laadpalen_schoon['AddressInfo.Town'] = Laadpalen_schoon['AddressInfo.Town'].fillna('Missing')
Laadpalen_schoon['AddressInfo.Postcode'] = Laadpalen_schoon['AddressInfo.Postcode'].fillna('Missing')
Laadpalen_schoon['AddressInfo.AddressLine1'] = Laadpalen_schoon['AddressInfo.AddressLine1'].fillna('Missing')
Laadpalen_schoon['AddressInfo.StateOrProvince'] = Laadpalen_schoon['AddressInfo.StateOrProvince'].fillna('Missing')


# In[19]:


#Before datetime manipulation


Laadpalen_schoon.info()


# In[20]:


code = '''#Number of points with modus
mode_points = Laadpalen_schoon['NumberOfPoints'].mode().values[0]  # Calculate the mode
Laadpalen_schoon['NumberOfPoints'] = Laadpalen_schoon['NumberOfPoints'].fillna(mode_points)


#Postcode with filled with "Missing"
Laadpalen_schoon['AddressInfo.Postcode'] = Laadpalen_schoon['AddressInfo.Postcode'].fillna('Missing')

# PowerKW by looking at LevelID
def fill_power_kw(row):
    if pd.isna(row['PowerKW']):
        if row['LevelID'] == 1:
            return 2.3
        elif row['LevelID'] == 2:
            return 11
        elif row['LevelID'] == 3:
            return 100
    return row['PowerKW']  # Keep the existing value if "PowerKW" is not missing

# Apply the fill_power_kw function to fill missing values in "PowerKW"
Laadpalen_schoon['PowerKW'] = Laadpalen.apply(fill_power_kw, axis=1)

#The rest is done with using the modus
mode_value = Laadpalen_schoon['PowerKW'].mode().values[0]  # Calculate the mode
Laadpalen_schoon['PowerKW'] = Laadpalen_schoon['PowerKW'].fillna(mode_value)

# LevelID by looking at PowerKW
def fill_Level_id(row):
    if pd.isna(row['LevelID']):
        if row['PowerKW'] <= 10:
            return 1
        elif row['PowerKW'] < 100:
            return 2
        elif row['PowerKW'] >= 100:
            return 3
    return row['LevelID']  # Keep the existing value if "LevelID" is not missing

# Apply the fill_Level_id function to fill missing values in "LevelID"
Laadpalen_schoon['LevelID'] = Laadpalen_schoon.apply(fill_Level_id, axis=1)

# Voltage by looking at LevelID
def fill_voltage(row):
    if pd.isna(row['Voltage']):
        if row['LevelID'] == 1:
            return 230
        elif row['LevelID'] == 2:
            return 400
        elif row['LevelID'] == 3:
            return 440
    return row['Voltage']  # Keep the existing value if "PowerKW" is not missing

# Apply the fill_power_kw function to fill missing values in "PowerKW"
Laadpalen_schoon['Voltage'] = Laadpalen_schoon.apply(fill_voltage, axis=1)

# LevelID by looking at PowerKW
def fill_amps(row):
    if pd.isna(row['Amps']):
        if row['PowerKW'] <= 30 :
            return 16
        elif row['PowerKW'] < 100:
            return 26
        elif row['PowerKW'] >= 100:
            return 250
    return row['Amps']  # Keep the existing value if "LevelID" is not missing

# Apply the fill_Level_id function to fill missing values in "LevelID"
Laadpalen_schoon['Amps'] = Laadpalen_schoon.apply(fill_amps, axis=1)'''
st.code(code, language='python')


# In[21]:


# #Number of points with modus
# mode_points = Laadpalen['NumberOfPoints'].mode().values[0]  # Calculate the mode
# Laadpalen['NumberOfPoints'] = Laadpalen['NumberOfPoints'].fillna(mode_points)


# #Postcode with filled with "Missing"
# Laadpalen['AddressInfo.Postcode'] = Laadpalen['AddressInfo.Postcode'].fillna('Missing')

# # PowerKW by looking at LevelID
# def fill_power_kw(row):
#     if pd.isna(row['PowerKW']):
#         if row['LevelID'] == 1:
#             return 2.3
#         elif row['LevelID'] == 2:
#             return 11
#         elif row['LevelID'] == 3:
#             return 100
#     return row['PowerKW']  # Keep the existing value if "PowerKW" is not missing

# # Apply the fill_power_kw function to fill missing values in "PowerKW"
# Laadpalen['PowerKW'] = Laadpalen.apply(fill_power_kw, axis=1)

# #The rest is done with using the modus
# mode_value = Laadpalen['PowerKW'].mode().values[0]  # Calculate the mode
# Laadpalen['PowerKW'] = Laadpalen['PowerKW'].fillna(mode_value)

# # LevelID by looking at PowerKW
# def fill_Level_id(row):
#     if pd.isna(row['LevelID']):
#         if row['PowerKW'] <= 10:
#             return 1
#         elif row['PowerKW'] < 100:
#             return 2
#         elif row['PowerKW'] >= 100:
#             return 3
#     return row['LevelID']  # Keep the existing value if "LevelID" is not missing

# # Apply the fill_Level_id function to fill missing values in "LevelID"
# Laadpalen['LevelID'] = Laadpalen.apply(fill_Level_id, axis=1)

# # Voltage by looking at LevelID
# def fill_voltage(row):
#     if pd.isna(row['Voltage']):
#         if row['LevelID'] == 1:
#             return 230
#         elif row['LevelID'] == 2:
#             return 400
#         elif row['LevelID'] == 3:
#             return 440
#     return row['Voltage']  # Keep the existing value if "PowerKW" is not missing

# # Apply the fill_power_kw function to fill missing values in "PowerKW"
# Laadpalen['Voltage'] = Laadpalen.apply(fill_voltage, axis=1)

# # LevelID by looking at PowerKW
# def fill_amps(row):
#     if pd.isna(row['Amps']):
#         if row['PowerKW'] <= 30 :
#             return 16
#         elif row['PowerKW'] < 100:
#             return 26
#         elif row['PowerKW'] >= 100:
#             return 250
#     return row['Amps']  # Keep the existing value if "LevelID" is not missing

# # Apply the fill_Level_id function to fill missing values in "LevelID"
# Laadpalen['Amps'] = Laadpalen.apply(fill_amps, axis=1)


# In[22]:


import plotly.graph_objects as go

# Create a Plotly figure
fig = go.Figure()

# Add bars for each variable
fig.add_trace(go.Histogram(x=Laadpalen_schoon["Amps"], name='Amps', marker_color='LightCoral', opacity=1))
fig.add_trace(go.Histogram(x=Laadpalen_schoon["Voltage"], name='Voltage', marker_color='MediumPurple', opacity=1))
fig.add_trace(go.Histogram(x=Laadpalen_schoon["PowerKW"], name='PowerKW', marker_color='CadetBlue', opacity=1))
# Update the layout
fig.update_layout(
    updatemenus=[
        dict(
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.155,
            xanchor="left",
            y=1.09,
            yanchor="top",
            font=dict(color='Indigo', size=14),
            buttons=[
                dict(
                    label="All",
                    method="update",
                    args=[{"visible": [True, True, True]},
                          {'showlegend': True}
                    ]),
                dict(
                    label="Amps",
                    method="update",
                    args=[{"visible": [True, False, False]},
                          {'showlegend': False}
                    ]),
                dict(
                    label="Voltage",
                    method="update",
                    args=[{"visible": [False, True, False]},
                          {'showlegend': False}
                    ]),
                dict(
                    label='PowerKW',
                    method="update",
                    args=[{"visible": [False, False, True]},
                          {'showlegend': False}
                    ]),
            ],
        ),
    ])

fig.update_layout(
    annotations=[
        dict(text="Choose:", showarrow=False,
             x=0.1, y=1.065, yref="paper", align="right",
             font=dict(size=16, color='DarkSlateBlue'))])

fig.update_layout(title="The Distribution of <b>Amps, Voltage, and PowerKW<b>",
                  title_x=0.5,
                  title_font=dict(size=20, color='MidnightBlue'),
                  height=700)

# # Show the figure
# fig.show()

st.plotly_chart(fig)


# ## Nieuwe data for merge

# In[23]:


# # import te grote datasets
# Hybrid=pd.read_csv("auto_hybride.csv")
# brands=pd.read_csv("Elektrische_ autos_informatie.csv")


# # selecteer van de dataframes de benodigde colommen en maak een nieuwe csv
# hybride_auto_klein = Hybrid[['Kenteken','Klasse hybride elektrisch voertuig']]
# hybride_auto_klein.to_csv('hybride_auto_klein.csv', index =False)

# # selecteer de colommen en verdeel de rows in twee, maak hiervan twee bestanden
# brands_kleiner1 = pd.read_csv("Elektrische_ autos_informatie.csv", nrows = 749303,
#                               usecols = ['Kenteken', 'Voertuigsoort', 'Merk'])
# brands_kleiner2 = pd.read_csv("Elektrische_ autos_informatie.csv", skiprows = 749304,
#                               usecols = ['Kenteken', 'Voertuigsoort', 'Merk'], names = ['Kenteken', 'Voertuigsoort', 'Merk'])
# brands_kleiner1.to_csv('brands1.csv', index = False)
# brands_kleiner2.to_csv('brands2.csv', index = False)

#  roep de kleine datasets aan met de originele dataframe naam
Hybrid=pd.read_csv("hybride_auto_klein.csv")
brands1=pd.read_csv("brands1.csv")
brands2=pd.read_csv("brands2.csv")
brands=pd.concat([brands1,brands2])
Hybrid.head()


# In[24]:


ev=pd.read_csv("Counts_total.csv")
ev.head()


# In[25]:


kenteken= Hybrid
kenteken.head()


# In[26]:


brands.head()


# In[27]:


# columns_to_drop = ["Catalogusprijs","Handelsbenaming", "Europese voertuigcategorie", "Type","Variant","Uitvoering","Zuinigheidsclassificatie","Datum tenaamstelling"]  # List of column names to drop
# brands.drop(columns=columns_to_drop, axis=1, inplace=True)


# In[28]:


merged_brands = brands.merge(kenteken, on="Kenteken", how="inner")


# In[29]:


merged_brands.head()


# In[30]:


head_merge = merged_brands.head()
st.write("We hebben van de twee datasets van de RDW een paar kolommen geselecteerd en deze met de merge functie samen gevoegd tot één dataframe.")
st.write('De eerste vijf regels van de dataset: ', head_merge)


# In[31]:


#To confirm only electric vehicles are present

# merged_brands["Brandstof omschrijving"].unique()


# In[32]:


#To check type of data

merged_brands.info()


# In[33]:


#Check for missing data

merged_brands.isna().sum()


# In[34]:


#Drop Na value in merk
merged_brands.dropna(subset=["Merk"], inplace=True)

#Klasse hybride elektrisch voertuig with filled with "Not"
merged_brands['Klasse hybride elektrisch voertuig'] = merged_brands['Klasse hybride elektrisch voertuig'].fillna('Not')


# In[35]:


#No more na values
merged_brands.info()


# In[36]:


# Check for duplicates


duplicates3 = merged_brands.duplicated(subset=['Kenteken', 'Voertuigsoort', 'Merk',
       'Klasse hybride elektrisch voertuig'])

# To count the number of duplicate rows
num_duplicates3 = duplicates3.sum()

# num_duplicates3


# In[37]:


merged_brands['Merk'] = merged_brands['Merk'].str.lower()


# In[38]:


#Count how many electric cars are not hybrid

count_not_values = (merged_brands["Klasse hybride elektrisch voertuig"] == "Not").sum()
# count_not_values


# In[39]:


#Count how many electric cars are ALSO hybrid

count_hybrid_values = (merged_brands["Klasse hybride elektrisch voertuig"] != "Not").sum()
# count_hybrid_values


# In[40]:


# Calculate the total count
total_count = count_not_values + count_hybrid_values

# Calculate the percentages
percentage_not = count_not_values / total_count * 100
percentage_hybrid = count_hybrid_values / total_count * 100

# Create a Plotly figure
fig = go.Figure()

# Define the width of the bars
bar_width = 0.4  # You can adjust this value

# Add a bar trace for "not" values
fig.add_trace(go.Bar(x=['Combined'], y=[count_not_values], name='Fully electric', marker_color='Green', text=[f'{percentage_not:.2f}%'], textposition='inside', textfont=dict(color='white', size=14), width=[bar_width]))

# Add a bar trace for Hybrid values with "not" as the base
fig.add_trace(go.Bar(x=['Combined'], y=[count_hybrid_values], name='Hybrid', marker_color='Blue', base=[count_not_values], text=[f'{percentage_hybrid:.2f}%'], textposition='inside', textfont=dict(color='white', size=14), width=[bar_width]))

# Update the layout
fig.update_layout(barmode='relative', title='Stacked Bar Chart of Hybrid vs Electric')

# Show the figure
# fig.show()

col3, col4 = st.columns(2)

with col3:
    st.write("Deze dataframe hebben we opgeschoond (Na-values verwijderd, dubbele waardes verwijderd, alle merknamen zonder capslock).")
    st.write("We hebben hierna het aantal volledig elektrische en de hybride auto's geteld. Deze verdeling is te zien in de barplot.")

with col4:
    st.plotly_chart(fig)


# In[1]:


# Count the frequency of each value
value_counts = merged_brands['Merk'].value_counts()

# Sort the values and counts from high to low
sorted_counts = value_counts.sort_values(ascending=False)

# Select the top 25 values
top_25 = sorted_counts.head(25)

# Define a darker color
darker_color = 'darkblue'

# Create a histogram trace with the top 25 values and the darker color
trace = go.Bar(
    x=top_25.index,  # Top 25 values (labels)
    y=top_25.values,  # Corresponding counts
    name='Histogram',  # Name for the trace
    marker=dict(color=darker_color),  # Set the color to the darker color
)

# Create a layout for the plot
layout = go.Layout(
    title='Top 25 Values Histogram',  # Title for the plot
    xaxis=dict(title='Value'),  # X-axis label
    yaxis=dict(
        title='Frequency',  # Y-axis label
        range=[0, top_25.max()]  # Set the y-axis range to cover the maximum count in the top 25 values
    ),
)

# Create a figure
fig = go.Figure(data=[trace], layout=layout)

# Show the plot
# fig.show()


col5, col6 = st.columns(2)

with col5:
    st.write("Hiernaast zijn de 25 meest voorkomende merken van de elektrische auto's")
with col6:
    st.plotly_chart(fig)
st.divider()


# In[42]:


path = 'laadpaaldata.csv'
laadpaal = pd.read_csv(path)
laadpaal['Started'] = pd.to_datetime(laadpaal['Started'], errors='coerce') #verwijderd één varibale die in het schikkeljaar viel
laadpaal['Ended'] = pd.to_datetime(laadpaal['Ended'], errors = 'coerce')
laadpaal = laadpaal[laadpaal['ChargeTime']>= 0]
laadpaal['Connected_Zonder_Laden'] = laadpaal['ConnectedTime']- laadpaal['ChargeTime']

twenty_fifth = laadpaal["MaxPower"].quantile(0.25)
MaxPower_median = laadpaal["MaxPower"].median()
seventy_fifth = laadpaal["MaxPower"].quantile(0.75)
power_labels = ['Extreem_laag', 'Laag', 'Medium', 'Hoog']
power_ranges = [0, twenty_fifth, MaxPower_median, seventy_fifth, laadpaal["MaxPower"].max()]
laadpaal['levels'] = pd.cut(laadpaal["MaxPower"], bins=power_ranges, labels=power_labels)


# In[68]:


fig = go.Figure()
# Kleuren
colors = ['blue', 'green', 'red', 'purple']

# Histogrammen
fig.add_trace(go.Histogram(x=laadpaal['TotalEnergy'], name='Totaal energie', marker_color=colors[0]))
fig.add_trace(go.Histogram(x=laadpaal['ChargeTime'], name='Laad tijd', visible='legendonly', marker_color=colors[1]))
fig.add_trace(go.Histogram(x=laadpaal['MaxPower'], name='Maximaal vermogen', visible='legendonly', marker_color=colors[2]))
fig.add_trace(go.Histogram(x=laadpaal['Connected_Zonder_Laden'], name='Aangesloten zonder te laden', visible='legendonly', marker_color=colors[3]))
# Dropdown menu
buttons = [
    {
        'label': 'Totaal energy',
        'method': 'update',
        'args': [{'visible': [True, False, False, False]}, {'xaxis.title.text': 'Totaal energy in Watt'}]
    },
    {
        'label': 'Laadtijd',
        'method': 'update',
        'args': [{'visible': [False, True, False, False]}, {'xaxis.title.text': 'Laadtijd in uren'}]
    },
    {
        'label': 'Maximaal vermogen',
        'method': 'update',
        'args': [{'visible': [False, False, True, False]}, {'xaxis.title.text': 'Maximaal vermogen in watt'}]
    },
    { 'label': 'Aangesloten zonder te laden',
      'method': 'update',
      'args': [{'visible': [False, False, False, True]}, {'xaxis.title.text': 'Aangesloten zonder te laden in uren'}]
    }
]

fig.update_layout(
    updatemenus=[
        {
            'buttons': buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }
    ]
)
# Layout
fig.update_layout(
    title='Histogram: Totaal energie, Oplaad tijd, Maximaal vermogen en Aangesloten zonder te laden',
    xaxis_title='Totaal Energie in Watt en tijd in Uren',
    yaxis_title='Ferquentie'
)
# Laten zien
col7, col8 = st.columns(2)

with col8:
    st.write()
    st.write()
    st.write("In dit histogram kan je de data zien van het laadpaal.csv document. ")
    st.write("De totaal energie heeft een mediaan van 7121 Watt en een mean van 9352 watt.")
    st.write("De laad tijd heeft een mediaan van 2.2 uur en een mean van 2.5 uur.")
    st.write("Het Maximaal vermogen heeft  een mediaan van 3393 watt en mean van 4090 watt.")
    
with col7:
    st.plotly_chart(fig)
st.divider()


# In[44]:


#Maak seizoene
Seizoenen = ['Lente', 'Zomer', 'Herfst', 'Winter']
Seizoen_start = pd.to_datetime(['03-21', '06-21', '09-21', '12-21'], format='%m-%d')

# start van de seizoenen
start_Winter = Seizoen_start[3]
start_lente = Seizoen_start[0]
start_herfst = Seizoen_start[2]
start_zomer =Seizoen_start[1]

# Schrijf functie om de seizoen per maand te pakken
def get_season(date):
    if pd.notna(date):
        month = date.month
        if month in [12, 1, 2]:
            return Seizoenen[3]  # Winter
        elif month in [3, 4, 5]:
            return Seizoenen[0]  # lente
        elif month in [6, 7, 8]:
            return Seizoenen[1]  # zomer
        elif month in [9, 10, 11]:
            return Seizoenen[2]  # herfst
    return None  

# Maak seizoenen collomn aan
laadpaal['Seizoen'] = laadpaal['Started'].apply(get_season)


# In[69]:


x0 = laadpaal['ConnectedTime']
x1 = laadpaal['ChargeTime']
# Maak histogram  van plotly
fig = go.Figure()
fig.add_trace(go.Histogram(x=x0, name='Aangesloten tijd', marker_color='skyblue'))
fig.add_trace(go.Histogram(x=x1, name='Laad tijd', marker_color='lightcoral'))
fig.update_layout(barmode='overlay')

# bereken median
median_connected_time = x0.median()
median_charge_time = x1.median()

# Maak de layout
fig.update_layout(
    title='Histogram van de laadtijd, aangesloten tijd en de dichtheid ervan',
    xaxis_title='Tijd in uren',
    yaxis_title='ferquentie',
    showlegend=True,
)

# Maak een x-as slider
fig.update_xaxes(title_text='Tijd in uren', rangeslider=dict(visible=True), type='linear')

# zet de connected time en charge time median in de rechter hoek
fig.add_annotation(
    xref='paper', yref='paper',
    x=0.95, y=0.90,
    text=f'Median van aangesloten tijd: {median_connected_time:.2f}',
    font=dict(size=10),
    showarrow=False,
    bgcolor='white',
)

fig.add_annotation(
    xref='paper', yref='paper',
    x=0.95, y=0.95,
    text=f'Median van laadtijd: {median_charge_time:.2f}',
    font=dict(size=10),
    showarrow=False,
    bgcolor='white',
)

# Maak een distrubties plot
kde_fig = ff.create_distplot([x0, x1], ['Aangesloten tijd KDE', 'Laad tijd KDE'])

# plot layout
kde_fig.update_layout(
    title='Distribution Plot (KDE) Van Aangesloten tijd en Laad Tijd',
    xaxis_title='Tijd in uren',
    yaxis_title='Dichtheid',
)
kde_fig.update_xaxes(title = 'Tijd in uren', rangeslider = dict(visible=True), type = 'linear')
fig.add_trace(kde_fig['data'][0])
fig.add_trace(kde_fig['data'][1])

col9, col10 = st.columns(2)

with col9:
    st.write("Hiernaast zie je de aangesloten tijd en de laadtijd. Ook kan je de distributie zien. Voor duidelijkere grafiek kan je de slider gebruiken om in en uit te zoomen. ")
with col10:
    st.plotly_chart(fig)
    st.plotly_chart(kde_fig)
st.divider()


# In[70]:

# Maak histogram van de connected zonder te laden
fig = px.histogram(laadpaal, x='Connected_Zonder_Laden', 
                   title='Aangesloten zonder te laden',
                   color_discrete_sequence=['lightcoral'])
fig.update_xaxes(title_text='Aangesloten zonder te laden in uren')
fig.update_yaxes(title_text='Ferquentie')

#maak slider zodat je kan inzoemen
fig.update_xaxes(rangeslider_visible=True)

col11, col12 = st.columns(2)

with col12:
    st.write()
    st.write()
    st.write()
    st.write("Hiernaast zie je dat auto`s meestal 0 uren aangesloten zijn zonder te laden. Alleen in extremen gevallen kan de aangesloten tijde zonder op te laden voorbij de 160 uur gaan. Dit is natuurlijk niet gewenst.")
with col11:
    st.plotly_chart(fig)
st.divider()

# In[47]:



# connected_zonder_laden = laadpaal['Connected_Zonder_Laden']
# max_power = laadpaal['MaxPower']

# # Maak scatterplot
# plt.figure(figsize=(8, 6))
# plt.scatter(connected_zonder_laden, max_power, c='blue', alpha=0.5)

# # maak de regressie lijn
# m, b = np.polyfit(connected_zonder_laden, max_power, 1)
# plt.plot(connected_zonder_laden, m * connected_zonder_laden + b, color='red', label=f'Regressie lijn: y = {m:.2f}x + {b:.2f}')

# # layout
# plt.xlabel('Aangesloten zonder laden', fontsize=14)
# plt.ylabel('Max vermogen in Watt', fontsize=14)
# plt.title('Scatterplot van Max vermogen in Watt per aangesloten zonder laden in uren', fontsize=16)


# plt.legend()
# plt.grid()
# plt.show() 


# In[71]:


st.title("Seizoenen")
fig = go.Figure()
# maak seizoenen aan
seasons = laadpaal['Seizoen'].unique()
# Kleuren
colors = px.colors.qualitative.Set1

for i, season in enumerate(seasons):
    filtered_data = laadpaal[laadpaal['Seizoen'] == season]

    # maak scatterplot
    scatter = go.Scatter(x=filtered_data.index, y=filtered_data['TotalEnergy'], mode='lines+markers',
                        name=season, line=dict(color=colors[i]))

    fig.add_trace(scatter)
    
# Maak de layout op
fig.update_layout(
    yaxis_title="Totaal energie in Watt",
    title="Totaal energie per seizoen"
)

# x-axis per seizoen (handmatig)
x_labels = ['Winter', 'Lente', 'Zomer', 'Herfst', 'Winter']
x_positions = [0, 2500, 5000, 7250, 9500]


fig.update_xaxes(
    tickvals=x_positions,
    ticktext=x_labels,
    title="Seizoenen"
)
col13, col14 = st.columns(2)

with col13:
    st.write("Hiernaast zie je de totalen energie geladen per seizoen. Het is vrij eerlijk verdeeld alleen in de winter wordt er net meet geladen dan in de rest van de seizoenen. Dit kan komen omdat mensen dan minder graag de fiets nemen of omdat de batterij van de auto minder goed werkt door de kou.")
with col14:
    st.plotly_chart(fig)


# ## Brandstof van net gekochte auto's

# Functie voor het importeren van een dataset

# In[49]:


st.divider()
st.header("Gekochtte auto's per brandstoftype")


# In[50]:


# functie om een dataset te importeren en verkleinen naar een nieuwe csv
def import_dataset(name_csv, select_column, import_csv, seperator = ','):
#     input: de name_csv en import_csv moeten in stringformaat zijn, en de select_column een lijst
#     de seperator input is niet verplicht, geef je met het aanroepen van de functie niks mee, dan gebruikt de functie een komma
    import_file = pd.read_csv(import_csv, sep = seperator, usecols = select_column)
    import_file.to_csv(name_csv, index = False)


# Importeer twee datasets van de RDW bestanden; het ene bestand bevat kentekens en brandstof type, het andere bestand bevat kentekens en de datum waarop het voertuig is overgezet

# In[51]:


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

# In[52]:


# auto_aanschaf_brandstof = auto.merge(auto_aanschaf, how = 'inner', on = 'Kenteken')
# auto_aanschaf_brandstof = auto_aanschaf_brandstof.rename(columns = {'Datum tenaamstelling':'Datum_tenaamstelling'})
# auto_aanschaf_brandstof.head()


# In[53]:


# auto_aanschaf_brandstof["Datum_tenaamstelling"].head()


# In[54]:


# auto_aanschaf_brandstof = auto_aanschaf_brandstof.assign(Datum_tenaamstelling = 
#                                                          pd.to_datetime(auto_aanschaf_brandstof['Datum_tenaamstelling'], 
#                                                                         format='%Y%m%d') )
# auto_aanschaf_brandstof['Datum_tenaamstelling'].head()


# In[55]:


# auto_aanschaf_brandstof['maand_jaar'] = auto_aanschaf_brandstof['Datum_tenaamstelling'].dt.to_period('M')
# auto_aanschaf_brandstof.head()


# Check of er NonAvailable values in het dataframe zitten en verwijder deze

# In[56]:


# auto_aanschaf_brandstof.isna().sum()


# In[57]:


# auto_aanschaf_brandstof_na = auto_aanschaf_brandstof.dropna()


# - Verdeel de dataframe in groupen op de brandstof omschrijving en de datum van tenaamstelling
# - Maak van deze dataframe een nieuw csv bestand, en schrijf code om deze csv in te laden

# In[58]:


# counts_total = auto_aanschaf_brandstof_na.groupby(['Brandstof omschrijving', 'maand_jaar']).count()
# counts_total_ind = counts_total.reset_index()

# counts_total_ind.to_csv('Counts_total.csv', index = False)


# In[59]:


counts_total_ind = pd.read_csv('Counts_total.csv')
counts_total_ind.head()


# - Verdeel de aantal van de groupen op datum in nieuwe dataframes per brandstof
# - Maak een lijndiagram met de type brandstof die gekocht zijn in speciefieke maanden, in de jaren voor 2000 is er weinig over de data te vertellen, dus de range start op het jaar 2000

# In[60]:


counts_alcohol = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Alcohol']
counts_benzine = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Benzine']
counts_diesel = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Diesel']
counts_elektriciteit = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Elektriciteit']
counts_lpg = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'LPG']
counts_cng = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'CNG']
counts_lng = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'LNG']
counts_waterstof = counts_total_ind[counts_total_ind['Brandstof omschrijving'] == 'Waterstof']
counts_benzine.head()


# In[61]:


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


col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig)
with col2:
    st.write("De lijngrafiek laat het aantal aangeschaftte auto's zien per jaar. Het eerste beeld wat je van de grafiek ziet, zijn de aangeschaftte auto's in de periode 2000 tot 2023.")
    st.write("De slider onder de grafiek is te gebruiken om een duidelijker beeld te krijgen van een specifieke periode.")


# # Map

# In[62]:


st.divider()


# In[63]:


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


# In[64]:


openchargemap = pd.read_csv('openchargemap_data.csv')


# In[65]:


# Function to determine province based on postcode
def bepaal_provincie(postcode):
    if 1000 <= postcode <= 1299:
        return 'Noord-Holland'
    elif 1300 <= postcode <= 1379:
        return 'Flevoland'
    elif 1380 <= postcode <= 1384:
        return 'Noord-Holland'
    elif 1390 <= postcode <= 1393:
        return 'Utrecht'
    elif 1394 <= postcode <= 1396:
        return 'Noord-Holland'
    elif 1398 <= postcode <= 1425:
        return 'Noord-Holland'
    elif 1426 <= postcode <= 1427:
        return 'Utrecht'
    elif 1428 <= postcode <= 1429:
        return 'Zuid-Holland'
    elif 1430 <= postcode <= 2158:
        return 'Noord-Holland'
    elif 2159 <= postcode <= 2164:
        return 'Zuid-Holland'
    elif 2165 <= postcode <= 2165:
        return 'Noord-Holland'
    elif 2170 <= postcode <= 3381:
        return 'Zuid-Holland'
    elif 3382 <= postcode <= 3464:
        return 'Utrecht'
    elif 3465 <= postcode <= 3466:
        return 'Zuid-Holland'
    elif 3467 <= postcode <= 3769:
        return 'Utrecht'
    elif 3770 <= postcode <= 3794:
        return 'Gelderland'
    elif 3795 <= postcode <= 3836:
        return 'Utrecht'
    elif 3837 <= postcode <= 3888:
        return 'Gelderland'
    elif 3890 <= postcode <= 3899:
        return 'Flevoland'
    elif 3900 <= postcode <= 3924:
        return 'Utrecht'
    elif 3925 <= postcode <= 3925:
        return 'Gelderland'
    elif 3926 <= postcode <= 3999:
        return 'Utrecht'
    elif 4000 <= postcode <= 4119:
        return 'Gelderland'
    elif 4120 <= postcode <= 4125:
        return 'Utrecht'
    elif 4126 <= postcode <= 4129:
        return 'Utrecht'
    elif 4130 <= postcode <= 4146:
        return 'Utrecht'
    elif 4147 <= postcode <= 4162:
        return 'Gelderland'
    elif 4163 <= postcode <= 4169:
        return 'Utrecht'
    elif 4170 <= postcode <= 4199:
        return 'Gelderland'
    elif 4200 <= postcode <= 4209:
        return 'Zuid-Holland'
    elif 4211 <= postcode <= 4212:
        return 'Gelderland'
    elif 4213 <= postcode <= 4213:
        return 'Zuid-Holland'
    elif 4214 <= postcode <= 4219:
        return 'Gelderland'
    elif 4220 <= postcode <= 4229:
        return 'Zuid-Holland'
    elif 4230 <= postcode <= 4239:
        return 'Utrecht'
    elif 4240 <= postcode <= 4241:
        return 'Zuid-Holland'
    elif 4242 <= postcode <= 4249:
        return 'Utrecht'
    elif 4250 <= postcode <= 4299:
        return 'Noord-Brabant'
    elif 4300 <= postcode <= 4599:
        return 'Zeeland'
    elif 4600 <= postcode <= 4671:
        return 'Noord-Brabant'
    elif 4672 <= postcode <= 4679:
        return 'Zeeland'
    elif 4680 <= postcode <= 4681:
        return 'Noord-Brabant'
    elif 4682 <= postcode <= 4699:
        return 'Zeeland'
    elif 4700 <= postcode <= 5299:
        return 'Noord-Brabant'
    elif 5300 <= postcode <= 5335:
        return 'Gelderland'
    elif 5340 <= postcode <= 5765:
        return 'Noord-Brabant'
    elif 5766 <= postcode <= 5817:
        return 'Limburg'
    elif 5820 <= postcode <= 5846:
        return 'Noord-Brabant'
    elif 5850 <= postcode <= 6019:
        return 'Limburg'
    elif 6020 <= postcode <= 6029:
        return 'Noord-Brabant'
    elif 6030 <= postcode <= 6499:
        return 'Limburg'
    elif 6500 <= postcode <= 6583:
        return 'Gelderland'
    elif 6584 <= postcode <= 6599:
        return 'Limburg'
    elif 6600 <= postcode <= 7399:
        return 'Gelderland'
    elif 7400 <= postcode <= 7438:
        return 'Overijssel'
    elif 7439 <= postcode <= 7439:
        return 'Gelderland'
    elif 7440 <= postcode <= 7739:
        return 'Overijssel'
    elif 7740 <= postcode <= 7766:
        return 'Drenthe'
    elif 7767 <= postcode <= 7799:
        return 'Overijssel'
    elif 7800 <= postcode <= 7949:
        return 'Drenthe'
    elif 7950 <= postcode <= 7955:
        return 'Overijssel'
    elif 7956 <= postcode <= 7999:
        return 'Drenthe'
    elif 8000 <= postcode <= 8049:
        return 'Overijssel'
    elif 8050 <= postcode <= 8054:
        return 'Gelderland'
    elif 8055 <= postcode <= 8069:
        return 'Overijssel'
    elif 8070 <= postcode <= 8099:
        return 'Gelderland'
    elif 8100 <= postcode <= 8159:
        return 'Overijssel'
    elif 8160 <= postcode <= 8195:
        return 'Gelderland'
    elif 8196 <= postcode <= 8199:
        return 'Overijssel'
    elif 8200 <= postcode <= 8259:
        return 'Flevoland'
    elif 8260 <= postcode <= 8299:
        return 'Overijssel'
    elif 8300 <= postcode <= 8322:
        return 'Flevoland'
    elif 8323 <= postcode <= 8349:
        return 'Overijssel'
    elif 8350 <= postcode <= 8354:
        return 'Drenthe'
    elif 8355 <= postcode <= 8379:
        return 'Overijssel'
    elif 8380 <= postcode <= 8387:
        return 'Drenthe'
    elif 8388 <= postcode <= 9299:
        return 'Friesland'
    elif 9300 <= postcode <= 9349:
        return 'Drenthe'
    elif 9350 <= postcode <= 9399:
        return 'Groningen'
    elif 9400 <= postcode <= 9478:
        return 'Drenthe'
    elif 9479 <= postcode <= 9479:
        return 'Groningen'
    elif 9480 <= postcode <= 9499:
        return 'Drenthe'
    elif 9500 <= postcode <= 9509:
        return 'Groningen'
    elif 9510 <= postcode <= 9539:
        return 'Drenthe'
    elif 9540 <= postcode <= 9563:
        return 'Groningen'
    elif 9564 <= postcode <= 9564:
        return 'Drenthe'
    elif 9565 <= postcode <= 9569:
        return 'Groningen'
    elif 9570 <= postcode <= 9579:
        return 'Drenthe'
    elif 9580 <= postcode <= 9653:
        return 'Groningen'
    elif 9654 <= postcode <= 9659:
        return 'Drenthe'
    elif 9660 <= postcode <= 9748:
        return 'Groningen'
    elif 9749 <= postcode <= 9749:
        return 'Drenthe'
    elif 9750 <= postcode <= 9759:
        return 'Groningen'
    elif 9760 <= postcode <= 9769:
        return 'Drenthe'
    elif 9770 <= postcode <= 9849:
        return 'Groningen'
    elif 9850 <= postcode <= 9859:
        return 'Friesland'
    elif 9860 <= postcode <= 9869:
        return 'Groningen'
    elif 9870 <= postcode <= 9879:
        return 'Friesland'
    elif 9880 <= postcode <= 9999:
        return 'Groningen'
    else:
        return 'Onbekende provincie'

# Create a new column 'NumericPostcode' containing only the numeric part of the postcode
openchargemap['NumericPostcode'] = openchargemap['AddressInfo.Postcode'].str.extract('(\d+)').astype(float)

# Apply the function to create a new 'Province' column
openchargemap['Province'] = openchargemap['NumericPostcode'].apply(bepaal_provincie)

# Display the resulting DataFrame
print(openchargemap[['NumericPostcode', 'Province']])


# In[66]:


# Count the number of charging points in each province
province_counts = openchargemap['Province'].value_counts()

# Plot the bar chart with annotations
fig, ax = plt.subplots(figsize=(6, 3))  # Adjust the figsize as needed
bars = province_counts.sort_values(ascending=False).plot(kind='bar', color='skyblue', ax=ax)

# Annotate each bar with its count
for bar in bars.patches:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(bar.get_height())}', ha='center', va='bottom')

ax.set_xlabel('Provincie')
ax.set_ylabel('Aantal laadpunten')
ax.set_title('Aantal laadpunten per provincie')

# Display the plot in Streamlit
st.pyplot(fig)

# Add text next to the plot
st.write("""
    Het bovenstaande figuur geeft de verdeling van laadpalen per provincie weer.
""")


# In[67]:


import folium
from folium import plugins
from folium import IFrame
from streamlit_folium import folium_static
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
folium_static(charging_map, width=800, height=400)  # Adjust the width and height as needed
st.write("""
    Deze interactieve kaart geeft de locaties van alle laadpalen in Nederland weer.
    Om overlapping te voorkomen worden de markers gegroupeerd en op deze manier weergegeven. 
    Bij het inzoomen zullen deze groepen onderverdeeld worden en hou je uiteindelijk individuele markers over. 
    Deze markers zijn ook interactief, wanneer je er op drukt krijg je nuttige informatie over de laadpaal te zien. 
    Er is rechtsbovenin ook een optie om tussen map layers te wisselen. 
    Ten slotte is er ook een begrenzing die er voor zorgt dat de gebruiker niet te ver uitzoomt.
""")

# In[47]:



laadpaal.index = laadpaal.index.astype(int)

 

# maak scatterplot
fig = px.scatter(laadpaal, x='Connected_Zonder_Laden', y='MaxPower', trendline='ols')

 

# layout
fig.update_layout(
    title='Aangesloten zonder te laden tegen maximaal vermogen',
    xaxis_title='Aangesloten zonder te laden in uren',
    yaxis_title='Maximaal vermogen in Watt',
    showlegend=True
)

 

fig.update_traces(
    line=dict(
        color='red',  
        width=2  
    ),
    marker =dict(
    color = 'blue')
)
col13, col14 = st.columns(2)

 

with col13:
    st.write('')
    st.write('')
    st.write('')
    st.write("Hiernaast zie je dat de maximaal laadvermogen van autos negatief gecorreleerd is met het aangesloten zonder te laden. Dit wil zeggen dat hoe zwakker het maximale laad vermogen hoe langer iemand gemiddeld aangesloten is zonder te laden.")
with col14:
    st.plotly_chart(fig)


# In[64]:


with st.expander("Sources"):
    st.write("Bron cover afbeelding: ", 
             "https://www.kaggle.com/datasets/geoffnel/evs-one-electric-vehicle-dataset")


# In[ ]:




