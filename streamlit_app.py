import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Membaca data
all_data = pd.read_csv('all_data/data_grouped.csv')
aqi_data = pd.read_csv('all_data/AQI_df.csv')

# Membuat DataFrame
df_data = pd.DataFrame(all_data)
df_aqi = pd.DataFrame(aqi_data)

# Sidebar untuk memilih stasiun dan tahun
st.sidebar.title("Filter Data")
stasiun = st.sidebar.selectbox("Pilih Stasiun", df_aqi['station'].unique())
tahun = st.sidebar.selectbox("Pilih Tahun", df_aqi['year'].unique())

# Filter data berdasarkan pilihan
filtered_data = df_aqi[(df_aqi['station'] == stasiun) & (df_aqi['year'] == tahun)]

# Menampilkan data
st.title("Data Stasiun")
st.write(f"Data untuk {stasiun} pada tahun {tahun}:")
st.write(filtered_data)

# Menampilkan grafik (opsional)
if not filtered_data.empty:
    st.line_chart(filtered_data.set_index('year')['aqi_pm10'])  # Ganti 'Data' dengan kolom yang sesuai

# Mengambil lokasi stasiun yang dipilih
station_data = df_aqi[df_aqi['station'] == stasiun].iloc[0]
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
