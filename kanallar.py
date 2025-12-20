import requests
import re

def link_yakala(url):
    # Link zaten doğrudan m3u8 ise dokunma
    if ".m3u8" in url:
        return url
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": url
        }
        r = requests.get(url, headers=headers, timeout=10)
        # Sayfadaki m3u8 linkini çek (Kanal D ve diğerleri için)
        match = re.search(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', r.text.replace("\\/", "/"))
        if match:
            return match.group(1)
    except:
        pass
    return url

# --- TAM VE GÜNCEL KANAL LİSTESİ ---
kanallar = [
    {
        "isim": "TRT 1", 
        "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"
    },
    {
        "isim": "ATV", 
        "url": "https://www.atv.com.tr/canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/atv.jpg"
    },
    {
        "isim": "Kanal D", 
        "url": "https://www.kanald.com.tr/canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"
    },
    {
        "isim": "Star TV", 
        "url": "https://www.startv.com.tr/canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/star.jpg"
    },
    {
        "isim": "Show TV", 
        "url": "https://www.showtv.com.tr/canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/showtv.jpg"
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
        "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"
    },
    {
        "isim": "TRT Spor Yildiz", 
        "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", 
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

print("✅ ATV eski çalışan linke döndürüldü ve liste güncellendi.")
