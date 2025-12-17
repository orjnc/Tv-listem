import requests
import re

# --- AYARLAR ---
# Sitelere kendimizi "Google Chrome" gibi tanitiyoruz ki kapiyi acsinlar.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

def link_bul(url, regex_pattern):
    try:
        print(f"Taraniyor: {url}")
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            # Sayfa icindeki m3u8 linkini regex ile avliyoruz
            match = re.search(regex_pattern, r.text)
            if match:
                # Bazen linkin icine kacis karakteri (\) koyarlar, onlari temizliyoruz
                temiz_link = match.group(1).replace("\\/", "/")
                print(f"BULUNDU: {temiz_link}")
                return temiz_link
    except Exception as e:
        print(f"Hata olustu: {e}")
    return None

# --- KANAL LISTESI ---
# Burasi robotun gorev listesidir.
kanallar = [
    {
        "isim": "TRT 1 HD (Tabii)",
        "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002",
        # Regex: Icinde 'trt1' gecen m3u8 linkini bulur
        "regex": r'["\'](https:[^"\']*?trt1[^"\']*?\.m3u8[^"\']*?)["\']', 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/TRT_1_logo.svg/1024px-TRT_1_logo.svg.png",
        "yedek": "https://tv-trt1.live.trt.com.tr/master.m3u8" # Tabii cokkuse devreye girer
    },
    {
        "isim": "TRT 4K (Ultra HD)",
        "tur": "sabit", # Bu kanal statiktir, aramaya gerek yok
        "link": "https://tv-trt4k.live.trt.com.tr/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/TRT_4K_logo.svg/1024px-TRT_4K_logo.svg.png"
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

# --- DOSYAYI OLUSTUR ---
dosya_icerigi = "#EXTM3U\n"

for k in kanallar:
    canli_link = None
    
    if k.get("tur") == "sabit":
        canli_link = k["link"]
    else:
        canli_link = link_bul(k["url"], k["regex"])
        # Eger link bulunamazsa ve yedek varsa onu kullan
        if not canli_link and "yedek" in k:
            canli_link = k["yedek"]
            
    if canli_link:
        dosya_icerigi += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

# Playlist.m3u olarak kaydet
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("Islem Tamam! Playlist guncellendi.")

