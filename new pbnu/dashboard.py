import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import io
import chardet

# Fungsi untuk mendeteksi encoding file
def detect_encoding(file):
    raw_data = file.read()
    file.seek(0)  # Reset file pointer
    result = chardet.detect(raw_data)
    return result['encoding']

# Fungsi untuk memuat data dari CSV yang diunggah
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            # Deteksi encoding
            encoding = detect_encoding(uploaded_file)
            # Baca file dengan encoding yang terdeteksi
            data = pd.read_csv(uploaded_file, encoding=encoding)
            # Konversi kolom 'text' menjadi string
            data['text'] = data['text'].astype(str)
            return data
        except Exception as e:
            st.error(f"Error saat membaca file: {e}")
            return None
    return None

# Judul aplikasi
st.title('Visualisasi Data Sentimen Twitter')

# Upload file CSV
uploaded_file = st.file_uploader("Pilih file CSV", type="csv")

if uploaded_file is not None:
    # Memuat data
    data = load_data(uploaded_file)

    if data is not None:
        # Pastikan kolom yang diperlukan ada
        required_columns = ['text', 'Sentimen', 'Lokasi']
        if not all(col in data.columns for col in required_columns):
            st.error(f"File CSV harus memiliki kolom: {', '.join(required_columns)}")
        else:
            # Lanjutkan dengan visualisasi seperti sebelumnya
            # Bar chart untuk distribusi sentimen
            st.subheader('Distribusi Sentimen')
            sentiment_counts = data['Sentimen'].value_counts()
            fig, ax = plt.subplots()
            sentiment_counts.plot(kind='bar', ax=ax)
            st.pyplot(fig)

            # Pie chart untuk distribusi sentimen
            st.subheader('Distribusi Sentimen (Pie Chart)')
            fig, ax = plt.subplots()
            sentiment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            st.pyplot(fig)

            # Bar chart untuk top 10 lokasi
            st.subheader('Top 10 Lokasi')
            top_locations = data['Lokasi'].value_counts().nlargest(10)
            fig, ax = plt.subplots()
            top_locations.plot(kind='bar', ax=ax)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)

            # Fungsi untuk mendapatkan frekuensi kata
            def get_word_freq(texts):
                words = ' '.join(texts.astype(str)).split()
                return Counter(words)

            # Top 10 kata yang sering muncul
            st.subheader('Top 10 Kata yang Sering Muncul')
            word_freq = get_word_freq(data['text'])
            top_words = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10])
            fig, ax = plt.subplots()
            ax.bar(top_words.keys(), top_words.values())
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)

            # Word Cloud
            st.subheader('Word Cloud')
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(data['text'].astype(str)))
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

            # Menampilkan data mentah
            st.subheader('Data Mentah')
            st.write(data)
    else:
        st.error("Tidak dapat memuat data. Pastikan format CSV Anda benar.")
else:
    st.write("Silakan unggah file CSV Anda.")