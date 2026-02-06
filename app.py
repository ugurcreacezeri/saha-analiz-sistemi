import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Veritabanı bağlantısı ve yeni sütunlar (Enlem/Boylam)
conn = sqlite3.connect('saha_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS kayitlar 
             (tarih TEXT, bolge TEXT, enlem REAL, boylam REAL, manuel REAL, dron REAL, fark REAL)''')
conn.commit()

st.set_page_config(page_title="Saha & Koordinat Takip", layout="wide")
st.title("🚁 Saha, Dron & Koordinat Analiz Paneli")

# Veri Giriş Formu
with st.form("yeni_kayit"):
    col1, col2 = st.columns(2)
    with col1:
        bolge = st.text_input("Bölge/Nokta Adı")
        enlem = st.number_input("Enlem (Latitude)", format="%.6f")
        boylam = st.number_input("Boylam (Longitude)", format="%.6f")
    with col2:
        m_olc = st.number_input("Saha Ölçümü", value=0.0)
        d_olc = st.number_input("Dron Ölçümü", value=0.0)
    
    submit = st.form_submit_button("Sisteme Kaydet")

    if submit:
        tarih = datetime.now().strftime("%d-%m-%Y %H:%M")
        fark = abs(m_olc - d_olc)
        c.execute("INSERT INTO kayitlar VALUES (?,?,?,?,?,?,?)", 
                  (tarih, bolge, enlem, boylam, m_olc, d_olc, fark))
        conn.commit()
        st.success(f"{bolge} noktası koordinatlarıyla kaydedildi!")

# Kayıtları Göster
st.subheader("📋 Koordinatlı Saha Kayıtları")
df = pd.read_sql_query("SELECT * FROM kayitlar", conn)
st.dataframe(df, use_container_width=True)

# Küçük bir harita özelliği (Eğer veri varsa)
if not df.empty:
    st.subheader("📍 Saha Noktaları Haritası")
    # Harita için sütun isimlerini ayarlıyoruz
    map_df = df.rename(columns={'enlem': 'lat', 'boylam': 'lon'})
    st.map(map_df)

