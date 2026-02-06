import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Veritabanı bağlantısı
conn = sqlite3.connect('saha.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS kayitlar (tarih TEXT, bolge TEXT, manuel REAL, dron REAL)')
conn.commit()

st.title("🚁 Saha & Dron Analiz Paneli")

# Veri Girişi
with st.form("yeni_kayit"):
    bolge = st.text_input("Bölge Adı")
    m_olc = st.number_input("Saha Ölçümü", value=0.0)
    d_olc = st.number_input("Dron Ölçümü", value=0.0)
    if st.form_submit_button("Sisteme Kaydet"):
        tarih = datetime.now().strftime("%d-%m-%Y %H:%M")
        c.execute("INSERT INTO kayitlar VALUES (?,?,?,?)", (tarih, bolge, m_olc, d_olc))
        conn.commit()
        st.success("Veri başarıyla kaydedildi!")

# Tablo gösterimi
st.subheader("📋 Geçmiş Kayıtlar")
df = pd.read_sql_query("SELECT * FROM kayitlar", conn)
st.dataframe(df, use_container_width=True)
