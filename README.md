# 🏙️ EmlakScout Pro | Türkiye Emlak Veri Takip & Bot Otomasyonu

Türkçe Streamlit emlak panosu: interaktif filtreler, tarama simülasyonu ve loglar, fırsat etiketleri, fiyat/m² grafikleri ve Excel/CSV dışa aktarımı. `sample_data.csv` demo amaçlı 120 ilan içerir. Tarama düğmesi **simülasyondur**, gerçek sitelerden ilan çekmez.

## Yerelde test
1. Python 3.9+ kurun ve bu proje klasörüne geçin.
2. (İsteğe bağlı) sanal ortam: `python -m venv .venv`; etkinleştirin.
3. Bağımlılıklar: `pip install -r requirements.txt`
4. Başlatın: `streamlit run app.py`
5. Tarayıcıda `http://localhost:8501` adresini açın.

## Streamlit Community Cloud (ücretsiz)
1. Proje dosyalarının tamamını GitHub reposuna yükleyin; gizli `.streamlit/config.toml` dosyasını da ekleyin.
2. [share.streamlit.io](https://share.streamlit.io) hesabınızla oturum açın ve **Create app / New app** seçin.
3. GitHub repo ve branch'i seçin, ana dosya yolunu `app.py` girin.
4. **Deploy** düğmesine basın. İlk kurulum bağımlılıkları yükleyince uygulama URL'si oluşturulur. GitHub'a yeni commit gönderince yeniden dağıtılır.

## Render
1. GitHub repo → Render'da **New + → Web Service** ile bağlayın.
2. Runtime Python 3; Build Command: `pip install -r requirements.txt`
3. Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Deploy edin; Render'ın sağladığı URL'den açın. Ücretsiz plan ve uyku/başlatma davranışları Render'ın güncel planına bağlıdır.

## Proje dosyaları
- `app.py`: Streamlit arayüzü ve grafikler
- `sample_data.csv`: Türkiye şehirlerinden örnek ilanlar, konum ve fiyatlar
- `requirements.txt`: Python bağımlılıkları
- `.streamlit/config.toml`: Tema ve sunucu ayarları

> Fiyatlar ve kur dönüşümü örnek veridir, yatırım tavsiyesi değildir. Gerçek scraping eklemeden önce kaynak sitelerin kullanım koşulları ve mevzuatı incelenmelidir.
