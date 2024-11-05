import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium


# Membaca data
all_data = pd.read_csv('all_data/AQI_all_df.csv')

# Membuat DataFrame
df_data = pd.DataFrame(all_data)

# Sidebar untuk memilih stasiun dan tahun
st.sidebar.title("Filter Data")
stasiun = st.sidebar.selectbox("Pilih Stasiun", df_data['station'].unique())
tahun = st.sidebar.selectbox("Pilih Tahun", df_data['year'].unique())

# Menampilkan data
st.header("Air Quality Index tahun 2013 - 2016")

# Mengambil lokasi stasiun yang dipilih
AQI_df = df_data.dropna(subset=['kualitas_udara'])
data_filtered_p = AQI_df[AQI_df['year'] == tahun]
station_data = AQI_df[AQI_df['station'] == stasiun].iloc[0]
location = [station_data['latitude'], station_data['longitude']]

# Membuat peta dengan lokasi stasiun yang dipilih
m = folium.Map(location=location, zoom_start=12, tiles='CartoDB positron')

# Menambahkan marker ke peta berdasarkan DataFrame
for index, row in data_filtered_p.iterrows():
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
st_folium(m, width=900, height=500)

# Menampilkan grafik rata-rata PM10
col1, col2 = st.columns(2)

with col1:
    # Filter data untuk grafik PM10
    data_grouped = all_data.dropna(subset=['month', 'PM10', 'musim'])
    rata_rata_pm10 = data_grouped[data_grouped['station'] == stasiun]
    
    # Membuat grafik garis
    fig = px.line(rata_rata_pm10, x='month', y='PM10', color='year',
              color_discrete_sequence=px.colors.qualitative.Set3)
    
    # Menentukan stasiun yang ingin diberi ketebalan garis berbeda
    thick_year = str(tahun)
    thick_line_width = 5
    default_line_width = 2
    
    # Mengupdate ketebalan garis
    for trace in fig.data:
        if str(trace.name) == thick_year:  # Pastikan keduanya adalah string
            trace.line.width = thick_line_width
        else:
            trace.line.width = default_line_width
    
    # Alternatif menggunakan update_traces
    fig.update_traces(line=dict(width=default_line_width))  # Set default line width
    fig.update_traces(selector=dict(name=thick_year), line=dict(width=thick_line_width))  # Set thick line

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
    st.plotly_chart(fig, width=650, height=500)

with col2:
    data_filtered_musim = data_grouped[(data_grouped['year'] == tahun) & (data_grouped['station'] == stasiun)]
    
    # Grouping dan menghitung rata-rata SO2
    rata_rata_musim = data_filtered_musim.groupby(['station', 'musim'])['PM10'].mean().reset_index()

    # Membuat plot dengan warna berbeda untuk stasiun yang disoroti
    fig_musim = px.bar(rata_rata_musim,
                 x='musim',
                 y='PM10',
                 title=f'Rata-rata PM10 per Musim Tahun {tahun} di stasiun {stasiun}',
                 labels={'musim': 'Musim', 'PM10': 'Rata-rata PM10'},
                 color='musim') # Menambahkan label yang lebih baik
    
    # Menampilkan plot
    st.plotly_chart(fig_musim, width=650, height=500)



