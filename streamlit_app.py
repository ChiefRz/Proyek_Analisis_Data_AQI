import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium


# Membaca data
all_data = pd.read_csv('all_data/AQI_all_data.csv')

# Membuat DataFrame
df_data = pd.DataFrame(all_data)

# Sidebar untuk memilih stasiun dan tahun
st.sidebar.title("Filter Data")
stasiun = st.sidebar.selectbox("Pilih Stasiun", df_data['station'].unique())
tahun = st.sidebar.selectbox("Pilih Tahun", df_data['year'].unique())

# Menampilkan data
st.title("Air Quality Index tahun 2013 - 2016")

# Mengambil lokasi stasiun yang dipilih
AQI_df = df_data.dropna(subset=['kualitas_udara'])
station_data = AQI_df[AQI_df['station'] == stasiun].iloc[0]
location = [station_data['latitude'], station_data['longitude']]

# Membuat peta dengan lokasi stasiun yang dipilih
m = folium.Map(location=location, zoom_start=12, tiles='CartoDB positron')

# Menambahkan marker ke peta berdasarkan DataFrame
for index, row in df_aqi.iterrows():
    if row['kualitas_udara'] == 'Baik':
        color = 'green'
    elif row['kualitas_udara'] == 'Sedang':
        color = 'orange'
    else:  # 'Buruk'
        color = 'red'

    popup_text = f"Station: {row['station']}<br>Tahun: {row['year']}<br>Indeks Kualitas Udara: {row['kualitas_udara']}<br>Rata-Rata PM10/Tahun: {row['aqi_pm10']}"

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        tooltip=row['station'],
        popup=folium.Popup(popup_text, max_width=200),
        icon=folium.Icon(color=color)
    ).add_to(m)

# Menampilkan peta
st.subheader("Peta Kualitas Udara")
st_folium(m, width=700, height=500)

# Menampilkan grafik rata-rata PM10
st.subheader(f'Grafik Rata-Rata PM10 di Stasiun {stasiun} pada Tahun {tahun}')

# Filter data untuk grafik PM10
data_grouped = all_data.dropna(subset=['month', 'PM10', 'musim'])
rata_rata_pm10 = data_grouped[data_grouped['station'] == stasiun]

# Membuat grafik garis
fig = px.line(rata_rata_pm10, x='month', y='PM10', color='year',
              color_discrete_sequence=px.colors.qualitative.Set3)

# Menentukan stasiun yang ingin diberi ketebalan garis berbeda
thick_year = tahun
thick_line_width = 5
default_line_width = 2

# Mengupdate ketebalan garis
for trace in fig.data:
    if trace.name == thick_year:
        trace.line.width = thick_line_width
    else:
        trace.line.width = default_line_width

# Atur sumbu x sebagai tipe data kategorikal
fig.update_xaxes(type='category')

# Atur label pada sumbu x
fig.update_xaxes(ticktext=rata_rata_pm10['month'].unique(), tickvals=rata_rata_pm10['month'].unique())

# Menambahkan judul dan label
fig.update_layout(title=f'Rata-Rata PM10 setiap bulan di stasiun {stasiun} pada tahun {tahun}',
                  yaxis_title='Rata-Rata PM10',
                  xaxis_title='Bulan',
                  legend_title='Tahun')

# Menampilkan plot
st.plotly_chart(fig)
