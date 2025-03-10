import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("data_baru.csv")  
    data['dteday'] = pd.to_datetime(data['dteday'])
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    data['season_label'] = data['season'].map(season_mapping)
    return data

data = load_data()

# Filtering Data
st.title("Dashboard Penyewaan Sepeda")
col1, col2 = st.columns(2)

selected_season = st.selectbox("Pilih Musim", ["Semua"] + list(data["season_label"].unique()))

if selected_season != "Semua":
    season_data = data[data["season_label"] == selected_season]
    min_date = season_data['dteday'].min()
    max_date = season_data['dteday'].max()
else:
    min_date = data['dteday'].min()
    max_date = data['dteday'].max()

with col1:
    start_date = st.date_input("Tanggal Awal", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("Tanggal Akhir", max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.error("Tanggal awal harus sebelum tanggal akhir")

# Terapkan filter ke data
data_filtered = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]
if selected_season != "Semua":
    data_filtered = data_filtered[data_filtered["season_label"] == selected_season]

# Tabs pada dashboard
tab1, tab2, tab3, tab4 = st.tabs(["Total Penyewaan", "Waktu Penyewaan", "Cuaca & Musim", "Analisis Lanjutan"])

# TAB 1: Total Penyewaan
with tab1:
    st.title("Total Penyewaan Sepeda")
    st.subheader("Bagaimana jumlah total penyewaan sepeda dalam rentang waktu tertentu?")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x=data_filtered['dteday'], y=data_filtered['cnt_day'], ax=ax, color='blue')
    plt.xticks(rotation=45)
    plt.title("Total Penyewaan Sepeda Harian")
    st.pyplot(fig)

# TAB 2: Waktu Penyewaan
with tab2:
    st.title("Waktu Penyewaan Sepeda")
    st.subheader("Pada jam berapa penyewaan sepeda paling sering terjadi?")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    hourly_trend = data_filtered.groupby('hr')['cnt'].mean()
    sns.barplot(x=hourly_trend.index, y=hourly_trend.values, ax=ax, palette='Blues')
    plt.title("Rata-rata Penyewaan Sepeda per Jam")
    st.pyplot(fig)

# TAB 3: Cuaca & Musim
with tab3:
    st.title("Pengaruh Cuaca dan Musim terhadap Penyewaan Sepeda")
    st.subheader("Bagaimana cuaca dan musim memengaruhi jumlah penyewaan sepeda?")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    weather_avg = data_filtered.groupby('weathersit')['cnt'].mean()
    sns.barplot(x=weather_avg.index, y=weather_avg.values, ax=ax, palette='Blues')
    ax.set_xticklabels(["Cerah", "Berawan", "Hujan Ringan", "Hujan Lebat"])
    plt.title("Jumlah Penyewaan Sepeda berdasarkan Cuaca")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    season_avg = data_filtered.groupby('season_label')['cnt'].mean()
    sns.barplot(x=season_avg.index, y=season_avg.values, ax=ax, palette='viridis')
    plt.title("Jumlah Penyewaan Sepeda berdasarkan Musim")
    st.pyplot(fig)

# TAB 4: Analisis Lanjutan
with tab4:
    st.title("Analisis Lanjutan")
    st.subheader("RFM Analysis (Recency, Frequency, Monetary)")
    
    latest_date = data_filtered['dteday'].max()
    data_filtered['Recency'] = (latest_date - data_filtered['dteday']).dt.days
    data_filtered['Frequency'] = data_filtered.groupby('registered')['dteday'].transform('count')
    data_filtered['Monetary'] = data_filtered.groupby('registered')['cnt'].transform('sum')
    
    rfm_table = data_filtered[['registered', 'dteday', 'Recency', 'Frequency', 'Monetary']].drop_duplicates()
    st.dataframe(rfm_table)
    
    st.subheader("Clustering Berdasarkan Waktu & Musim")
    usage_clusters = data_filtered.copy()
    usage_clusters['Usage Cluster'] = pd.cut(usage_clusters['hr'], bins=[0, 7, 17, 24], labels=["Non-Sibuk", "Pagi (Jam Sibuk)", "Sore (Jam Sibuk)"])
    cluster_counts = usage_clusters['Usage Cluster'].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=cluster_counts.index, y=cluster_counts.values, ax=ax, palette='muted')
    plt.title("Jumlah Penyewaan Berdasarkan Waktu Penggunaan")
    st.pyplot(fig)

st.caption("---")
st.caption("@Yorris Siagian -2025-")
