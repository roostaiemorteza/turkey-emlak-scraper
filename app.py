# -*- coding: utf-8 -*-
import io, time, datetime
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="EmlakScout Pro", page_icon="🏙️", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"] {font-family:Inter,sans-serif}
.hero{background:linear-gradient(130deg,#101d2d,#155e75 70%,#0f766e);padding:1.55rem 2rem;border-radius:17px;color:white;margin-bottom:1rem}
.hero h1{font-size:1.65rem;font-weight:800;margin:0}.hero p{opacity:.86;margin:.4rem 0 0}
div[data-testid="stMetric"]{background:rgba(120,140,170,.10);border:1px solid rgba(120,140,170,.25);border-radius:14px;padding:1rem}
footer{visibility:hidden}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🏙️ EmlakScout Pro | Türkiye Emlak Veri Takip & Bot Otomasyonu</h1><p>Bot tarama simülasyonu · Fiyat/m² analitiği · Fırsat tespiti · Excel/CSV raporları</p></div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv("sample_data.csv", encoding="utf-8-sig")
    data["Tarama_Tarihi"] = pd.to_datetime(data["Tarama_Tarihi"])
    return data
df = load_data()

with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    st.caption("Portföy filtreleri")
    cities = st.multiselect("📍 Şehir", sorted(df["Şehir"].unique()), default=sorted(df["Şehir"].unique()))
    status = st.multiselect("🏷️ Durum", sorted(df["Durum"].unique()), default=sorted(df["Durum"].unique()))
    lo, hi = int(df.Fiyat_TL.min()), int(df.Fiyat_TL.max())
    price = st.slider("💰 Fiyat aralığı (TL)", lo, hi, (lo, hi), step=100000)
    deals_only = st.checkbox("🔥 Yalnız fırsat ilanları")
    st.divider()
    st.caption("Bot Otomasyonu v2.4 · Demo veri seti")
    st.caption(datetime.datetime.now().strftime("🕐 %d.%m.%Y %H:%M"))

filtered = df[df["Şehir"].isin(cities) & df["Durum"].isin(status) & df["Fiyat_TL"].between(*price)].copy()
if deals_only:
    filtered = filtered[filtered["Fırsat_Etiketi"] == "FIRSAT"]
st.subheader("🤖 Bot Otomasyonu")
run_col, info_col = st.columns([1, 3])
with run_col: trigger = st.button("▶️ Taramayı başlat", type="primary", use_container_width=True)
if trigger:
    lines = ["🌐 Sistem başlatıldı — TR/DE proxy havuzu bağlandı.", "🔐 CAPTCHA çözücü modülü aktif.", "🛰️ İlan kaynakları taranıyor…", "📄 Sahibinden: 128 ilan listelendi.", "📄 Hepsiemlak: 96 ilan listelendi.", "📄 Zingat: 57 ilan listelendi.", "🧮 Fiyat/m² normalizasyonu çalışıyor…", "🧠 Fırsat modeli tamamlandı (eşik 0.75).", "💾 Rapor hazır — tarama tamamlandı! ✅"]
    box, bar = st.empty(), st.progress(0, text="Tarama başlıyor…")
    for i, line in enumerate(lines):
        box.code("\n".join(lines[:i+1]), language="bash")
        bar.progress((i+1)/len(lines), text=line)
        time.sleep(.32)
    st.success("Tarama simülasyonu tamamlandı. Örnek veri panoda görüntüleniyor.")
else:
    st.info("Taramayı başlat düğmesi, gerçek scraping yapmayan canlı işlem simülasyonunu çalıştırır.")

if filtered.empty:
    st.warning("Bu filtrelerle ilan bulunamadı. Filtreleri genişletin.")
    st.stop()
c1,c2,c3,c4,c5=st.columns(5)
c1.metric("📋 Toplam ilan", f"{len(filtered):,}")
c2.metric("🌍 Şehir", filtered.Şehir.nunique())
c3.metric("💵 Ortalama fiyat", f"₺{filtered.Fiyat_TL.mean():,.0f}")
c4.metric("📐 Ortalama m² fiyatı", f"₺{filtered.m2_fiyat_TL.mean():,.0f}")
c5.metric("🔥 Fırsat ilan", int((filtered.Fırsat_Etiketi=="FIRSAT").sum()))
st.divider()
left,right=st.columns(2)
with left:
    st.subheader("📦 Şehre göre m² fiyatı")
    fig=px.box(filtered,x="Şehir",y="m2_fiyat_TL",color="Şehir",points="all",hover_data=["İlçe","Fiyat_TL"])
    fig.update_layout(showlegend=False,height=420,yaxis_title="TL / m²")
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("🎯 Alan ve m² fiyatı ilişkisi")
    fig=px.scatter(filtered,x="m2",y="m2_fiyat_TL",color="Şehir",symbol="Fırsat_Etiketi",size="Fiyat_TL",hover_name="Başlık",hover_data=["İlçe","Durum","Fiyat_EUR"])
    fig.update_layout(height=420,xaxis_title="Alan (m²)",yaxis_title="TL / m²")
    st.plotly_chart(fig,use_container_width=True)
st.subheader("📊 İlan veri tablosu")
st.dataframe(filtered.sort_values("Fırsat_Skoru",ascending=False), use_container_width=True, hide_index=True,
             column_config={"Fırsat_Skoru":st.column_config.ProgressColumn("Fırsat skoru",min_value=0,max_value=1,format="%.2f"),"Fırsat_Etiketi":st.column_config.TextColumn("Fırsat etiketi"),"Fiyat_TL":st.column_config.NumberColumn("Fiyat (TL)",format="₺%d"),"Fiyat_EUR":st.column_config.NumberColumn("Fiyat (EUR)",format="€%d"),"m2_fiyat_TL":st.column_config.NumberColumn("TL / m²",format="₺%d")})
st.subheader("⬇️ Dışa aktar")
a,b=st.columns(2)
buf=io.BytesIO()
with pd.ExcelWriter(buf,engine="openpyxl") as writer: filtered.to_excel(writer,index=False,sheet_name="EmlakVerisi")
a.download_button("📥 Excel (.xlsx) indir",buf.getvalue(),"emlakscout_rapor.xlsx",use_container_width=True)
b.download_button("📥 CSV indir",filtered.to_csv(index=False).encode("utf-8-sig"),"emlakscout_rapor.csv",use_container_width=True)
st.caption("© EmlakScout Pro · Örnek/demo verileridir; canlı veri toplama içermez.")
