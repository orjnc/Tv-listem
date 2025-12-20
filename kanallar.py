import requests
import re
import json
import time

def link_yakala(url):
    if ".m3u8" in url:
        return url
        
    try:
        # Web Video Caster'ın kullandığı Android kimliğini birebir taklit et
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "Referer": url,
            "Accept": "*/*",
            "Connection": "keep-alive"
        }

        # --- TAKTİK 1: BEKLEME VE TEKRARLI DENEME ---
        # Video oynatıcının arka planda linki oluşturması için 3 deneme yapıyoruz
        for deneme in range(3):
            # Eğer ilk deneme değilse, videonun yüklenmesi için 3 saniye bekle
            if deneme > 0:
                print(f"⏳ {url} için link bekleniyor (Deneme {deneme+1})...")
                time.sleep(3)

            # --- TAKTİK 2: ARKA KAPI (API) VE ANA SAYFA TARAMASI ---
            sorgu_listesi = []
            if "atv.com.tr" in url:
                sorgu_listesi.append("https://v.tmgrup.com.tr/getv_test?atv")
            elif "kanald.com.tr" in url:
                sorgu_listesi.append("https://www.kanald.com.tr/action/media/get-live-stream")
            elif "startv.com.tr" in url:
                sorgu_listesi.append("https://api.dogusdigital.com/video/contents/startv/live")
            
            sorgu_listesi.append(url) # Ana sayfayı da listeye ekle

            for hedef in sorgu_listesi:
                r = requests.get(hedef, headers=headers, timeout=15)
                # İçeriği temizle ve m3u8 avına çık
                icerik = r.text.replace("\\/", "/").replace("\\\\", "\\")
                
                # Detaylı Regex: WVC'nin yaptığı gibi tüm gizli köşelere bak
                pattern = r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']'
                match = re.search(pattern, icerik, re.IGNORECASE)
                
                if match:
                    link = match.group(1)
                    if "ads" not in link.lower() and "vpaid" not in link.lower():
                        return link

    except Exception as e:
        print(f"❌ Hata ({url}): {e}")
        
    return url

# --- KANAL LİSTESİ ---
kanallar = [
    {"isim": "TRT 1", "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"},
    {"isim": "ATV", "url": "https://www.atv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/atv.jpg"},
    {"isim": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"},
    {"isim": "Star TV", "url": "https://www.startv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/star.jpg"},
    {"isim": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/showtv.jpg"},
    {"isim": "NOW TV", "url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/now.jpg"},
    {"isim": "TV8", "url": "https://tv8.daioncdn.net/tv8/tv8.m3u8?app=7ddc255a-ef47-4e81-ab14-c0e5f2949788&ce=3", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tv8.jpg"},
    {"isim": "Beyaz TV", "url": "https://www.beyaztv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/beyaztv.jpg"},
    {"isim": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/teve2.jpg"},
    {"isim": "Kanal 7", "url": "https://www.kanal7.com/canli-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanal7.jpg"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"},
    {"isim": "TRT Spor", "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"}
]

m3u_icerik = "#EXTM3U\n"
print("🚀 Gecikmeli 'Network Hunter' Başlatıldı...")

for k in kanallar:
    canli_link = link_yakala(k["url"])
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'
    print(f"✅ {k['isim']} bitti.")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("\n🎯 Playlist güncellendi. Eğer hala bazı linkler web sitesi olarak dönüyorsa, o kanalın JS şifrelemesi çok ağırdır.")
