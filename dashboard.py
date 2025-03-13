import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("data_baru.csv")  
    data['dteday'] = pd.to_datetime(data['dteday'])
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    data['season_label'] = data['season'].map(season_mapping)
    return data

data = load_data()

# Filter tanggal
st.title("Dashboard Penyewaan Sepeda")
col1, col2 = st.columns(2)

min_date = data['dteday'].min()
max_date = data['dteday'].max()

with col1:
    start_date = st.date_input("Tanggal Awal", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("Tanggal Akhir", max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.error("Tanggal awal harus sebelum tanggal akhir")

# Terapkan filter
data_filtered = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

# Pastikan kolom 'weathersit' bertipe integer
data_filtered['weathersit'] = data_filtered['weathersit'].astype(int)

# Tabs utama: Pola Penyewaan dulu, lalu Analisis Lanjutan
tab1, tab2 = st.tabs(["Pola Penyewaan Sepeda", "Analisis Lanjutan"])

# TAB 1 - POLA PENYEWAAN (dengan subtab)
with tab1:
    subtab1, subtab2, subtab3 = st.tabs([
        "Pola Berdasarkan Waktu, Hari, Bulan, Musim",
        "Perbandingan Pengguna",
        "Waktu Optimal untuk Menambah Sepeda"
    ])

    # SUBTAB 1
    with subtab1:
        st.subheader("Pola Penyewaan Sepeda")

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Pola berdasarkan jam
        sns.lineplot(data=data_filtered, x='hr', y='cnt', ax=axes[0, 0])
        axes[0, 0].set_title("Pola Penyewaan Berdasarkan Jam")
        axes[0, 0].set_xlabel("Jam")
        axes[0, 0].set_ylabel("Total Penyewaan")

        # Pola berdasarkan hari
        data_filtered.groupby('weekday')['cnt'].sum().plot(kind='bar', ax=axes[0, 1])
        axes[0, 1].set_title("Pola Penyewaan Berdasarkan Hari")
        axes[0, 1].set_xlabel("Hari")
        axes[0, 1].set_ylabel("Total Penyewaan")

        # Pola berdasarkan bulan
        data_filtered.groupby('mnth')['cnt'].sum().plot(kind='bar', ax=axes[1, 0])
        axes[1, 0].set_title("Pola Penyewaan Berdasarkan Bulan")
        axes[1, 0].set_xlabel("Bulan")
        axes[1, 0].set_ylabel("Total Penyewaan")

        # Pola berdasarkan musim
        data_filtered.groupby('season_label')['cnt'].sum().plot(kind='bar', ax=axes[1, 1])
        axes[1, 1].set_title("Pola Penyewaan Berdasarkan Musim")
        axes[1, 1].set_xlabel("Musim")
        axes[1, 1].set_ylabel("Total Penyewaan")

        plt.tight_layout()
        st.pyplot(fig)

    # SUBTAB 2 - Perbandingan Pengguna
    with subtab2:
        st.subheader("Perbandingan Pengguna (Casual vs. Registered)")

        # Total penyewaan pengguna casual vs registered
        user_types = data_filtered[['casual', 'registered']].sum()
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        sns.barplot(x=user_types.index, y=user_types.values, palette='pastel', ax=ax2)
        ax2.set_title("Total Penyewaan: Casual vs. Registered")
        ax2.set_xlabel("Tipe Pengguna")
        ax2.set_ylabel("Total Penyewaan")
        st.pyplot(fig2)

        # Pola penyewaan casual vs registered berdasarkan jam
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=data_filtered, x='hr', y='casual', label='Casual', marker='o', ax=ax3)
        sns.lineplot(data=data_filtered, x='hr', y='registered', label='Registered', marker='o', ax=ax3)
        ax3.set_title("Pola Penyewaan Casual vs. Registered Berdasarkan Jam")
        ax3.set_xlabel("Jam")
        ax3.set_ylabel("Total Penyewaan")
        ax3.legend()
        st.pyplot(fig3)

    # SUBTAB 3
    with subtab3:
        st.subheader("Waktu Optimal untuk Menambah Sepeda")
        hourly_avg = data_filtered.groupby('hr')['cnt'].mean()

        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, marker='o', ax=ax4)
        ax4.set_title("Waktu Optimal untuk Menambah Sepeda")
        ax4.set_xlabel("Jam")
        ax4.set_ylabel("Rata-rata Penyewaan Sepeda")
        ax4.axvspan(7, 9, color='red', alpha=0.3, label='Jam Sibuk Pagi')
        ax4.axvspan(17, 19, color='blue', alpha=0.3, label='Jam Sibuk Sore')
        ax4.legend()
        st.pyplot(fig4)

# Footer
st.caption("---")
st.caption("@Yorris Siagian - 2025")
