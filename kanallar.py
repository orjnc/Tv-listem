import requests
import re
import os

# --- 1. ADIM: GİZLİ BİLGİLER ---
USER_EMAIL = os.getenv('TOD_EMAIL')
USER_PASS = os.getenv('TOD_PASSWORD')

# --- 2. ADIM: GELİŞMİŞ OTURUM YÖNETİMİ ---
def oturum_hazirla():
    session = requests.Session()
    
    # TOD'un web sitesine bir kez gidip başlangıç çerezlerini alalım
    try:
        ana_sayfa = "https://www.todtv.com.tr/giris"
        headers_ilk = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        session.get(ana_sayfa, headers=headers_ilk, timeout=10)
        
        # Giriş için asıl API ucu (Daha yaygın kullanılan endpoint)
        login_url = "https://www.todtv.com.tr/api/v1/login" 
        
        payload = {
            "email": USER_EMAIL, # Bazı API'ler 'username' yerine 'email' ister
            "password": USER_PASS,
            "rememberMe": True
        }
        
        headers_login = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Referer": "https://www.todtv.com.tr/giris",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        r = session.post(login_url, json=payload, headers=headers_login, timeout=15)
        
        if r.status_code == 200:
            print("✅ GİRİŞ BAŞARILI: Oturum anahtarları alındı.")
            return session
        else:
            print(f"❌ GİRİŞ HATASI: Durum Kodu {r.status_code}")
            # Hata mesajının içeriğini bas ki sorunu anlayalım
            print(f"Sunucu Yanıtı: {r.text[:200]}") 
    except Exception as e:
        print(f"⚠️ KRİTİK HATA: {e}")
        
    return requests # Başarısız olursa normal requests ile devam et

# --- 3. ADIM: GENEL SÖKÜCÜ ---
def kanal_sokucu(url, baglanti):
    if ".m3u8" in url:
        return url
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.todtv.com.tr/"
        }
        # Oturum açıksa 'baglanti' objesi session'dır, değilse requests'tir
        r = baglanti.get(url, headers=headers, timeout=10)
        
        # HTML içinde m3u8 avı
        text = r.text.replace("\\/", "/")
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', text)
        
        if match:
            return match.group(1)
        else:
            # Eğer m3u8 yoksa ama sayfa geldiyse linkleri tek tek logla (Hata çözmek için)
            if "bbc-first" in url:
                print("🚨 BBC Sayfası yüklendi ama m3u8 bulunamadı! Sayfa içeriği giriş yapmamış gibi görünüyor olabilir.")
    except:
        pass
    return url

# --- 4. ADIM: LİSTE VE ÇALIŞTIRMA ---
kanallar = [
    {"isim": "TRT 1", "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"},
    {"isim": "Kanal D HD", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"},
    {"isim": "BBC First", "url": "www.todtv.com.tr/canli-tv/bbc-first", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/bbcfirst.jpg"},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"},
    {"isim": "TRT Spor", "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"}
]

aktif_baglanti = oturum_hazirla()
m3u_icerik = "#EXTM3U\n"

for k in kanallar:
    canli_link = kanal_sokucu(k["url"], aktif_baglanti)
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("✅ İşlem bitti. Logları kontrol et.")

