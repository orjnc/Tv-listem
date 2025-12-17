import requests
import re

# --- AYARLAR ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

def link_bul(url, regex_pattern):
    try:
        print(f"Taraniyor: {url}")
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            match = re.search(regex_pattern, r.text)
            if match:
                temiz_link = match.group(1).replace("\\/", "/")
                print(f"BULUNDU: {temiz_link}")
                return temiz_link
    except Exception as e:
        print(f"Hata: {e}")
    return None

# --- KANAL LISTESI (6 KANAL) ---
kanallar = [
    # 1. TRT 1
    {
        "isim": "TRT 1",
        "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trt1[^"\']*?\.m3u8[^"\']*?)["\']', 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"
    },
    # 2. TRT SPOR
    {
        "isim": "TRT Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trtspor[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"
    },
    # 3. TRT SPOR YILDIZ (Senin istedigin site: trtspor.com.tr)
    {
        "isim": "TRT Spor Yildiz",
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150028",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"
    },
    # 4. TABII SPOR (Saglam Link - Geri Geldi)
    {
        "isim": "Tabii Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"
    },
    # 5. DMAX
    {
        "isim": "DMAX TR",
        "url": "https://www.dmax.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"
    },
    # 6. TLC
    {
        "isim": "TLC TR",
        "url": "https://www.tlctv.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"
    }
]

# --- KAYDETME ---
dosya_icerigi = "#EXTM3U\n"

for k in kanallar:
    canli_link = link_bul(k["url"], k["regex"])
            
    if canli_link:
        dosya_icerigi += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("Liste guncellendi: 6 Kanal (TRT Yildiz ve Tabii Spor dahil).")
