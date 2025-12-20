import requests
import re

def link_yakala(url):
    # Link zaten doğrudan m3u8 ise dokunma
    if ".m3u8" in url:
        return url
    
    # ATV için özel API yönlendirmesi
    if "atv.com.tr" in url:
        target_url = "https://v.atv.com.tr/videodeti/atv"
    else:
        target_url = url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.atv.com.tr/"
        }
        r = requests.get(target_url, headers=headers, timeout=10)
        sayfa_icerigi = r.text.replace("\\/", "/")
        
        # Sayfadaki bütün m3u8 linklerini bul
        links = re.findall(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', sayfa_icerigi)
        
        if links:
            # Star TV özelinde filtre: İçinde 'star' geçen m3u8'i bul
            if "star" in url:
                for l in links:
                    if "star" in l.lower():
                        return l
            # Diğer kanallar için ilk bulduğunu ver
            return links[0]
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
        "url": "https://puhutv.com/star-tv-canli-yayin", 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/star.jpg"
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

print("✅ Liste başarıyla güncellendi. Star TV ve ATV düzeltildi.")
