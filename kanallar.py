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

# --- KANAL LISTESI (Sadece Resmi Linkler) ---
kanallar = [
    {
        "isim": "TRT 1 HD",
        "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trt1[^"\']*?\.m3u8[^"\']*?)["\']', 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/TRT_1_logo.svg/1024px-TRT_1_logo.svg.png"
    },
    {
        "isim": "TRT Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trtspor[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/TRT_Spor_logo.svg/1024px-TRT_Spor_logo.svg.png"
    },
    {
        "isim": "Tabii Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002",
        # BURASI DUZELTILDI: Artik daha genis arama yapiyor, kesin bulacak.
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/TRT_Spor_Yildiz_logo.svg/1024px-TRT_Spor_Yildiz_logo.svg.png"
    },
    {
        "isim": "DMAX TR",
        "url": "https://www.dmax.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/DMAX_Logo_2016.svg/1024px-DMAX_Logo_2016.svg.png"
    },
    {
        "isim": "TLC TR",
        "url": "https://www.tlctv.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/TLC_Logo.svg/1024px-TLC_Logo.svg.png"
    }
]

# --- KAYDETME (Yedek Kontrolu Yok - Direkt Kayit) ---
dosya_icerigi = "#EXTM3U\n"

for k in kanallar:
    canli_link = link_bul(k["url"], k["regex"])
            
    if canli_link:
        dosya_icerigi += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("Liste guncellendi (Sadece bulunan kanallar eklendi).")
