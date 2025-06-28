## Prediksi Penyewaan Sepeda Harian
Proyek ini membangun sistem prediksi jumlah sepeda yang akan disewa setiap hari berdasarkan data historis. Model prediktif dilatih dengan data yang mencakup variabel seperti musim, cuaca, suhu, dan hari dalam minggu.

Antarmuka pengguna dibangun menggunakan Streamlit, memungkinkan pengguna memasukkan parameter input dan langsung mendapatkan hasil prediksi jumlah sepeda yang disewa.

## Fitur Utama
Analisis data historis penyewaan sepeda

Feature engineering dari data waktu dan cuaca

Model prediksi regresi jumlah sepeda harian

Aplikasi interaktif berbasis Streamlit

Instalasi sederhana dengan requirements.txt

## Hasil Proyek
📈 Ditemukan bahwa jumlah penyewaan sepeda meningkat pada musim gugur dan hari kerja tertentu.

🌡️ Suhu dan kelembapan sangat memengaruhi tingkat penyewaan sepeda — semakin hangat dan kering, semakin tinggi jumlah sewa.

🧮 Model regresi mampu memprediksi jumlah penyewaan sepeda harian dengan akurasi yang memadai (R² score ditampilkan dalam notebook analisis).

🖥️ Streamlit UI menyediakan antarmuka sederhana untuk melakukan prediksi berdasarkan input manual seperti cuaca, musim, dan suhu.

## Struktur Proyek
Penyewaan-Sepeda-main/
│
├── Proyek_Analisis_Data.ipynb      # Notebook analisis data & modelling
├── dashboard.py                    # Streamlit app untuk prediksi
├── data_baru.csv                   # Dataset utama
├── requirements.txt                # Dependensi proyek
└── README.md                       # Dokumentasi proyek (file ini)

## Cara Menjalankan
1. Clone repositori ini:
git clone https://github.com/username/Penyewaan-Sepeda.git
cd Penyewaan-Sepeda
2. Install environment:
pip install -r requirements.txt
3. Jalankan aplikasi Streamlit:
streamlit run dashboard.py
