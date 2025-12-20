import requests
import re
import json

def link_yakala(url):
    # Eğer listede zaten doğrudan m3u8 varsa dokunma
    if ".m3u8" in url:
        return url
        
    try:
        # TAKTİK 1: Web Video Caster gibi Mobil (Android) kimliği kullan
        # Bu, bazı sitelerin korumasını doğrudan devre dışı bırakır.
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
            "Referer": url,
            "Accept": "*/*"
        }

        # TAKTİK 2: Arka Kapı (API) Taraması
        # Sitenin kendisi yerine, linki asıl üreten "bilgi servislerine" git.
        sorgu_url = url
        if "atv.com.tr" in url:
            sorgu_url = "https://v.tmgrup.com.tr/getv_test?atv"
        elif "kanald.com.tr" in url:
            sorgu_url = "https://www.kanald.com.tr/action/media/get-live-stream"
        elif "startv.com.tr" in url:
            sorgu_url = "https://api.dogusdigital.com/video/contents/startv/live"

        # Sayfayı veya API'yi indir
        r = requests.get(sorgu_url, headers=headers, timeout=15)
        # Karakter temizliği yaparak ham veriyi oku
        ham_veri = r.text.replace("\\/", "/").replace("\\\\", "\\")

        # TAKTİK 3: Derin Regex (WVC gibi her yerdeki .m3u8'i tara)
        # JSON objeleri, JS değişkenleri ve HTML etiketleri dahil her yere bakar.
        desenler = [
            r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']',
            r'(?:src|url|file|videoUrl)["\']?\s*[:=]\s*["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']'
        ]

        for desen in desenler:
            match = re.search(desen, ham_veri, re.IGNORECASE)
            if match:
                bulunan_link = match.group(1)
                # Reklamları ele ve gerçek yayını döndür
                if "ads" not in bulunan_link.lower() and "vpaid" not in bulunan_link.lower():
                    return bulunan_link

    except Exception as e:
        print(f"Hata ({url}): {e}")
        
    return url

# --- SENİN TAM KANAL LİSTEN ---
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

# --- PLAYLIST OLUŞTURMA ---
m3u_icerik = "#EXTM3U\n"
print("📡 Taktiksel tarama başlatıldı...")

for k in kanallar:
    canli_link = link_yakala(k["url"])
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'
    print(f"✔️ {k['isim']} işlendi.")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("\n✅ Tam otomatik playlist başarıyla güncellendi.")
