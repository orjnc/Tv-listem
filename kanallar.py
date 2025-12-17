import requests
import re

def link_yakala(url):
    # Link zaten m3u8 ise (Tabii TV gibi) dokunma
    if ".m3u8" in url:
        return url
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=10)
        # Sayfadaki m3u8 linkini çek (Kanal D ve diğerleri için)
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', r.text.replace("\\/", "/"))
        if match:
            return match.group(1)
    except:
        pass
    return url

# --- TAM URL LOGOLAR VE GÜNCEL KANAL LİSTESİ ---
kanallar = [
    {
        "isim": "TRT 1", 
        "url": "https://www.canlitv.me/live/trt1-canli-kesintisiz-izle", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"
    },
    {
        "isim": "Kanal D HD", 
        "url": "https://www.kanald.com.tr/canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"
    },
    {
        "isim": "Tabii TV", 
        "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"
    },
    {
        "isim": "DMAX TR", 
        "url": "https://www.dmax.com.tr/canli-izle", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"
    },
    {
        "isim": "TLC TR", 
        "url": "https://www.tlctv.com.tr/canli-izle", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"
    },
    {
        "isim": "TRT Spor", 
        "url": "https://www.canlitv.me/live/trtspor-canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"
    },
    {
        "isim": "TRT Spor Yildiz", 
        "url": "https://www.canlitv.me/live/trtsporyildiz-hd", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"
    },
    {
        "isim": "Tabii Spor", 
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"
    }
]

m3u_icerik = "#EXTM3U\n"

for k in kanallar:
    canli_link = link_yakala(k["url"])
    m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("✅ Liste güncellendi. Nick kaldırıldı, logolar düzeltildi.")


