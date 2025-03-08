import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("data_baru.csv")  # Gunakan path relatif

    # Convert dteday ke datetime
    data['dteday'] = pd.to_datetime(data['dteday'])
    
    # Mapping musim ke label
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    data['season_label'] = data['season'].map(season_mapping)
    
    return data

data = load_data()

# Sidebar untuk filter
st.sidebar.title("Filter Data")
selected_date = st.sidebar.date_input("Pilih Tanggal", data['dteday'].min())
selected_hour = st.sidebar.slider("Pilih Jam", 0, 23, 12)

# Filter musim
selected_season = st.sidebar.selectbox("Pilih Musim", ["Semua"] + list(data["season_label"].unique()))

# Terapkan filter musim
if selected_season != "Semua":
    data = data[data["season_label"] == selected_season]

# Filter data berdasarkan pilihan user
daily_data = data[data['dteday'] == pd.to_datetime(selected_date)]
hourly_data = data[data['hr'] == selected_hour]

# Tabs pada dashboard
tab1, tab2, tab3 = st.tabs(["Visualisasi", "Data Per Hari & Jam", "Analisis Lanjutan"])

#TAB 1: VISUALISASI
with tab1:
    st.title("Dashboard Penyewaan Sepeda")
    
    # Tren Penyewaan Sepeda Harian
    st.subheader("Tren Penyewaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x=data['dteday'], y=data['cnt_day'], ax=ax, color='blue')
    plt.xticks(rotation=45)
    plt.title("Tren Penyewaan Sepeda Harian")
    st.pyplot(fig)
    
    # Tren Penyewaan Sepeda Per Jam
    st.subheader("Rata-rata Penyewaan Sepeda per Jam")
    fig, ax = plt.subplots(figsize=(12, 5))
    hourly_trend = data.groupby('hr')['cnt'].mean()
    sns.barplot(x=hourly_trend.index, y=hourly_trend.values, ax=ax, palette='Reds')
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    plt.title("Rata-rata Penyewaan Sepeda per Jam")
    st.pyplot(fig)

    # Pengaruh Hari dalam Seminggu
    st.subheader("Pengaruh Hari dalam Seminggu")
    fig, ax = plt.subplots(figsize=(10, 5))
    weekday_avg = data.groupby('weekday')['cnt'].mean()
    sns.barplot(x=weekday_avg.index, y=weekday_avg.values, ax=ax, palette='coolwarm')
    ax.set_xticklabels(["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
    plt.title("Rata-rata Penyewaan Sepeda per Hari")
    st.pyplot(fig)

    # Pengaruh Musim
    st.subheader("Pengaruh Musim terhadap Penyewaan")
    fig, ax = plt.subplots(figsize=(8, 5))
    season_avg = data.groupby('season_label')['cnt'].mean()
    sns.barplot(x=season_avg.index, y=season_avg.values, ax=ax, palette='viridis')
    plt.title("Jumlah Penyewaan Sepeda berdasarkan Musim")
    st.pyplot(fig)

    #Pengaruh Cuaca terhadap Penyewaan Sepeda
    st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(8, 5))
    weather_avg = data.groupby('weathersit')['cnt'].mean()
    sns.barplot(x=weather_avg.index, y=weather_avg.values, ax=ax, palette='Blues')
    ax.set_xticklabels(["Cerah", "Berawan", "Hujan Ringan", "Hujan Lebat"])
    plt.title("Jumlah Penyewaan Sepeda berdasarkan Cuaca")
    st.pyplot(fig)

#TAB 2: DATA PER HARI & JAM
with tab2:
    st.subheader("Data Penyewaan Sepeda Per Hari")
    
    #Cek apakah data ditemukan
    if daily_data.empty:
        st.warning("Tidak ada data yang cocok dengan tanggal yang dipilih.")
    else:
        st.dataframe(daily_data)

    st.subheader("Data Penyewaan Sepeda Per Jam")
    st.dataframe(hourly_data)

#TAB 3: ANALISIS LANJUTAN
with tab3:
    st.title("Analisis Lanjutan")

    # RFM Analysis #
    st.subheader("RFM Analysis (Recency, Frequency, Monetary)")

    # Menghitung Recency (Hari sejak terakhir menyewa)
    latest_date = data['dteday'].max()
    recency = data.groupby('registered')['dteday'].max().reset_index()
    recency['Recency'] = (latest_date - recency['dteday']).dt.days

    # Menghitung Frequency (Total transaksi per user)
    frequency = data.groupby('registered')['cnt'].count().reset_index()
    frequency.columns = ['registered', 'Frequency']

    # Menghitung Monetary (Total sepeda yang disewa per user)
    monetary = data.groupby('registered')['cnt'].sum().reset_index()
    monetary.columns = ['registered', 'Monetary']

    # Gabungkan hasil RFM
    rfm = recency.merge(frequency, on='registered').merge(monetary, on='registered')

    # Tampilkan hasil RFM Analysis
    st.dataframe(rfm)

    # Clustering Berdasarkan Waktu & Musim
    st.subheader("Clustering Berdasarkan Waktu & Musim")

    def categorize_usage(hour):
        if 6 <= hour <= 9:
            return "Pagi (Jam Sibuk)"
        elif 17 <= hour <= 19:
            return "Sore (Jam Sibuk)"
        else:
            return "Non-Sibuk"

    data['Usage Cluster'] = data['hr'].apply(categorize_usage)

    # Visualisasi Clustering
    fig, ax = plt.subplots(figsize=(8, 5))
    cluster_counts = data['Usage Cluster'].value_counts()
    sns.barplot(x=cluster_counts.index, y=cluster_counts.values, ax=ax, palette="Set2")
    plt.title("Jumlah Penyewaan Berdasarkan Waktu Penggunaan")
    st.pyplot(fig)

    # Geospatial Analysis (Jika Ada Data Lokasi)
    if 'lat' in data.columns and 'long' in data.columns:
        st.subheader("Geospatial Analysis (Distribusi Penyewaan)")

        # Membuat peta dengan Folium
        map_center = [data['lat'].mean(), data['long'].mean()]
        m = folium.Map(location=map_center, zoom_start=12)

        for _, row in data.iterrows():
            folium.Marker([row['lat'], row['long']], popup=f"Penyewaan: {row['cnt']}").add_to(m)

        folium_static(m)

# Footer
st.caption("---")
st.caption("Dashboard ini dibuat untuk analisis penyewaan sepeda berdasarkan tren waktu, musim, dan kondisi cuaca.")
