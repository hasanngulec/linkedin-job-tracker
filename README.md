# 📊 LinkedIn İş Başvurusu Analiz Platformu

LinkedIn üzerinden yaptığınız iş başvurularını otomatik olarak çeken ve analiz eden bir platform.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)
![n8n](https://img.shields.io/badge/n8n-Automation-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🔄 Bölüm 1: n8n Otomasyonu

n8n workflow'u, Gmail'den LinkedIn başvuru emaillerini otomatik olarak çeker, kategorize eder ve Google Sheets'e kaydeder.

### 📋 Workflow Yapısı

```
Manual Trigger → Gmail → Kategorize & Extract Data → Filter → Google Sheets
```

### 🔧 Workflow Node'ları

| Node | Açıklama |
|------|----------|
| **Manual Trigger** | Workflow'u manuel olarak başlatır |
| **Gmail** | LinkedIn'den gelen emailleri çeker (linkedin.com gönderici filtresi) |
| **Kategorize & Extract Data** | Emailleri analiz eder, şirket/pozisyon/durum bilgilerini çıkarır |
| **Filter** | Sadece iş başvurusu emaillerini filtreler |
| **Google Sheets** | Verileri Google Sheets'e kaydeder |

### 📧 Email Kategorileri

Workflow emailleri şu kategorilere ayırır:

| Kategori | Durum | Tetikleyici Kelimeler |
|----------|-------|----------------------|
| `application_submitted` | Applied | "application was sent", "your application to" |
| `application_viewed` | Under Review | "application was viewed" |
| `interview_invite` | Interview | "interview", "mülakat" |
| `rejected` | Rejected | "unfortunately", "not moving forward", "maalesef" |

### ⚙️ n8n Kurulumu

1. [n8n](https://n8n.io/) hesabı oluşturun (cloud veya self-hosted)
2. `applications.json` dosyasını n8n'e import edin
3. Credential'ları ayarlayın:

#### Gmail OAuth2 Credential
```
1. Google Cloud Console'da OAuth 2.0 credential oluşturun
2. Gmail API'yi etkinleştirin
3. n8n'de Gmail OAuth2 credential ekleyin
4. Workflow'da YOUR_GMAIL_CREDENTIAL_ID ve YOUR_GMAIL_CREDENTIAL_NAME değerlerini güncelleyin
```

#### Google Sheets OAuth2 Credential
```
1. Google Cloud Console'da OAuth 2.0 credential oluşturun
2. Google Sheets API'yi etkinleştirin
3. n8n'de Google Sheets OAuth2 credential ekleyin
4. Workflow'da YOUR_GOOGLE_SHEETS_CREDENTIAL_ID ve YOUR_GOOGLE_SHEETS_CREDENTIAL_NAME değerlerini güncelleyin
```

4. Google Sheets URL'nizi güncelleyin:
   - `YOUR_GOOGLE_SHEETS_URL` → Kendi Google Sheets linkiniz

### 📊 Google Sheets Sütunları

Workflow şu sütunları oluşturur:

| Sütun | Açıklama |
|-------|----------|
| Date | Başvuru tarihi |
| Time | Başvuru saati |
| Company | Şirket adı |
| Position | Pozisyon |
| Category | Kategori kodu |
| Status | Durum |
| Subject | Email konusu |
| Gmail Link | Gmail'deki email linki |
| Processed At | İşlenme zamanı |

### ▶️ Workflow'u Çalıştırma

1. n8n'de workflow'u açın
2. "Execute Workflow" butonuna tıklayın
3. Gmail'den emailler çekilir ve işlenir
4. Veriler Google Sheets'e kaydedilir
5. Google Sheets'ten CSV olarak export alın

---

## 📈 Bölüm 2: Streamlit Dashboard

Streamlit dashboard, n8n'den gelen verileri görselleştirir ve analiz eder.

### 🎯 Özellikler

- **Metrik Kartları**: Toplam başvuru, mülakat, red oranı
- **Durum Dağılımı**: Pasta grafiği ile görselleştirme
- **Zaman Trendi**: Günlük başvuru grafiği + 7 günlük ortalama
- **Şirket Analizi**: En çok başvurulan şirketler
- **Pozisyon Analizi**: Popüler pozisyonlar
- **Haftalık/Aylık Histogram**: Dönemsel aktivite
- **Yanıt Hunisi**: Başvuru → Görüntüleme → Mülakat akışı
- **Filtreleme**: Tarih, durum, şirket bazlı
- **HTML Export**: Tüm analizleri tek dosyada indirin

### 🚀 Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
streamlit run app.py
```

### 📋 Kullanım

1. **CSV Yükleme**: Sol panelden n8n'den aldığınız CSV'yi yükleyin
2. **Demo Modu**: CSV olmadan test etmek için "Demo veri kullan" seçeneği
3. **Filtreleme**: Tarih aralığı, durum ve şirket filtresi
4. **Export**: CSV veya HTML dashboard olarak indirin

### 🎨 Dashboard Bölümleri

#### Genel Bakış
- Toplam başvuru sayısı
- Farklı şirket sayısı
- Mülakat daveti sayısı
- İnceleniyor sayısı
- Red oranı

#### Detaylı Analizler
- Başvuru durumu dağılımı (pasta grafiği)
- Başvuru yanıt hunisi
- Günlük başvuru trendi
- En çok başvurulan şirketler (bar chart)
- En çok başvurulan pozisyonlar
- Haftalık/Aylık histogram (seçilebilir)
- Şirket bazlı durum dağılımı

#### Başvuru Detayları
- Tablo görünümü (ilk 50 kayıt)
- Gmail link'i ile doğrudan email erişimi

### 📊 Veri Formatı

Dashboard şu CSV formatını bekler:

```csv
Date,Company,Position,Category,Status,Subject,Gmail Link,Processed At
2025-01-15,Şirket A,Pozisyon 1,application_submitted,Applied,Your application...,https://mail...,2025-01-15T10:30:00.000Z
```

### 🖥️ HTML Dashboard Export

"Dashboard İndir" butonu ile tüm analizleri içeren interaktif HTML dosyası indirebilirsiniz:
- Tüm grafikler (Plotly interaktif)
- Metrik kartları
- Detaylı tablo
- Yazdırma uyumlu tasarım

---

## 📁 Proje Yapısı

```
linkedin_basvurular/
├── app.py              # Streamlit dashboard uygulaması
├── applications.json   # n8n workflow dosyası
├── sample_data.csv     # Örnek veri seti (anonim)
├── requirements.txt    # Python bağımlılıkları
├── .gitignore          # Git ignore dosyası
└── README.md           # Bu dosya
```

---

## 🔐 Güvenlik Notları

- `applications.json` dosyasındaki credential ID'leri placeholder değerlerdir
- Gerçek başvuru verilerinizi GitHub'a yüklemeyin
- `.gitignore` dosyası hassas verileri otomatik olarak ignore eder
- `sample_data.csv` tamamen anonim örnek veridir

---

## 🤝 Katkıda Bulunma

1. Bu repo'yu fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

## 🙏 Teknolojiler

- [n8n](https://n8n.io/) - Workflow otomasyon platformu
- [Streamlit](https://streamlit.io/) - Python dashboard framework
- [Plotly](https://plotly.com/) - İnteraktif grafikler
- [Pandas](https://pandas.pydata.org/) - Veri analizi

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
