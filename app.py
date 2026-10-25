import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# تنظیمات اولیه صفحه (باید اولین دستور باشد)
st.set_page_config(page_title="EmlakScout Pro", layout="wide", page_icon="🏢")

# --- CSS سفارشی برای ظاهر مدرن ---
def local_css():
    st.markdown("""
    <style>
    /* تغییر رنگ پس‌زمینه کل صفحه */
    .stApp {
        background-color: #0b0f19;
    }
    
    /* استایل کارت‌های متریک (Metric Cards) */
    div[data-testid="metric-container"] {
        background-color: #1a2235;
        border: 1px solid #2d3748;
        padding: 5% 5% 5% 10%;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }
    
    /* تغییر رنگ متن متریک‌ها */
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-weight: bold;
    }
    div[data-testid="metric-container"] div {
        color: #f8fafc !important;
    }
    
    /* استایل دکمه‌ها */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1d4ed8, #1e40af);
        border: none;
    }
    
    /* استایل سایدبار */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- سایدبار ---
st.sidebar.title("⚙️ Kontrol Paneli")
st.sidebar.markdown("---")
selected_cities = st.sidebar.multiselect("Şehir", ["Alanya", "Antalya", "İstanbul", "İzmir"], default=["Antalya", "İstanbul"])
selected_status = st.sidebar.multiselect("Durum", ["Kiralık", "Satılık"], default=["Satılık"])
price_range = st.sidebar.slider("Fiyat aralığı (TL)", 1000000, 50000000, (5000000, 20000000))
st.sidebar.checkbox("🔥 Yalnız fırsat ilanları")

# --- محتوای اصلی ---
st.title("🏢 EmlakScout Pro - Yönetici Paneli")
st.markdown("Türkiye Gayrimenkul Yatırım & Analiz Platformu")

# دکمه اسکرپینگ
if st.button("▶ Taramayı başlat"):
    st.info("Sistem canlı verileri çekiyor... Lütfen bekleyin.")

st.markdown("<br>", unsafe_allow_html=True)

# --- ویژگی‌های جدید برای مدیران ---
st.subheader("📊 Portföy Özeti")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="📄 Toplam İlan", value="1,240", delta="12 Yeni")
with col2:
    st.metric(label="💰 Ortalama Fiyat (TL)", value="₺ 25.6M", delta="-%2.4")
with col3:
    st.metric(label="📐 Ortalama m² Fiyatı", value="₺ 238,500", delta="+%1.2")
with col4:
    st.metric(label="🔥 Fırsat İlanları", value="36", delta="Acil Satılık")

st.markdown("---")

# --- بخش‌های تحلیلی برای مدیر سرمایه‌گذاری ---
st.subheader("📈 Yatırım Analizi (ROI) ve Trendler")

col_chart1, col_chart2 = st.columns(2)

# ساخت داده تستی برای نمودار
dates = pd.date_range(start="2023-01-01", periods=12, freq="M")
trend_data = pd.DataFrame({
    'Tarih': dates,
    'Antalya': np.random.randint(150000, 250000, 12),
    'İstanbul': np.random.randint(200000, 350000, 12)
})

with col_chart1:
    st.markdown("**Bölgelere Göre m² Fiyat Trendi**")
    fig1 = px.line(trend_data, x='Tarih', y=['Antalya', 'İstanbul'], template="plotly_dark")
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.markdown("**ROI (Yıllık Kira Getirisi) Karşılaştırması**")
    roi_data = pd.DataFrame({
        'Bölge': ['Antalya', 'İstanbul', 'İzmir', 'Alanya'],
        'ROI (%)': [10.2, 7.5, 6.8, 8.9]
    })
    fig2 = px.bar(roi_data, x='Bölge', y='ROI (%)', color='Bölge', template="plotly_dark")
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# --- سیستم هشدار هوشمند (ویژگی مدیریتی) ---
st.markdown("---")
st.subheader("🔔 Akıllı Yatırım Uyarıları (AI)")
alerts_col1, alerts_col2 = st.columns(2)
with alerts_col1:
    st.success("📈 **Yüksek Potansiyel:** Antalya/Lara bölgesinde m² fiyatları son 1 ayda %5 arttı. Alım için uygun zaman.")
with alerts_col2:
    st.warning("⚖️ **Döviz Kuru Etkisi:** Euro bazında İzmir'deki lüks konutlarda %3 değer kaybı tespit edildi.")
