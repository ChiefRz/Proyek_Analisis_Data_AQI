import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os
import folium
# Contoh data dummy
all_data = pd.read_csv('all_data/data_grouped.csv')
aqi_data = pd.read_csv('all_data/AQI_df.csv')

# Membuat DataFrame
df_data = pd.DataFrame(all_data)
df_aqi = pd.DataFrame(aqi_data)

# Sidebar untuk memilih stasiun dan tahun
st.sidebar.title("Filter Data")
stasiun = st.sidebar.selectbox("Pilih Stasiun", df_data['station'].unique())
tahun = st.sidebar.selectbox("Pilih Tahun", df_aqi['year'].unique())

# Filter data berdasarkan pilihan
filtered_data = df_aqi[(df_aqi['year'] == stasiun) & (df_aqi['year'] == tahun)]

# Menampilkan data
st.title("Data Stasiun")
st.write(f"Data untuk {station} pada tahun {year}:")
st.write(filtered_data)

# Menampilkan grafik (opsional)
if not filtered_data.empty:
    st.line_chart(filtered_data.set_index('Tahun')['Data'])
