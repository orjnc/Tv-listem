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

# --- KANAL LISTESI ---
kanallar = [
    # 1. TRT 1
    {
        "isim": "TRT 1",
        "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trt1[^"\']*?\.m3u8[^"\']*?)["\']', 
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg",
        "tip": "ara"
    },
    # 2. KANAL D HD (TOD TV - Bulamazsa bile listeye girecek)
    {
        "isim": "Kanal D HD",
        "url": "https://www.todtv.com.tr/canli-tv/kanal-d",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg",
        "tip": "ara"
    },
    # 3. TABII TV (SABIT)
    {
        "isim": "Tabii TV",
        "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8",
        "regex": None,
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg",
        "tip": "sabit" 
    },
    # 4. DMAX
    {
        "isim": "DMAX TR",
        "url": "https://www.dmax.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg",
        "tip": "ara"
    },
    # 5. TLC
    {
        "isim": "TLC TR",
        "url": "https://www.tlctv.com.tr/canli-izle",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg",
        "tip": "ara"
    },
    # 6. TRT SPOR
    {
        "isim": "TRT Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002",
        "regex": r'["\'](https:[^"\']*?trtspor[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg",
        "tip": "ara"
    },
    # 7. TRT SPOR YILDIZ (Resmi Site - Bulamazsa bile ekleyecek)
    {
        "isim": "TRT Spor Yildiz",
        "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg",
        "tip": "ara"
    },
    # 8. TABII SPOR
    {
        "isim": "Tabii Spor",
        "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002",
        "regex": r'["\'](https:[^"\']*?\.m3u8[^"\']*?)["\']',
        "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg",
        "tip": "ara"
    }
]

# --- KAYDETME ---
dosya_icerigi = "#EXTM3U\n"

for k in kanallar:
    canli_link = None
    
    # 1. Adim: Link turune gore islem yap
    if k.get("tip") == "sabit":
        canli_link = k["url"]
        print(f"SABIT EKLENDI: {k['isim']}")
    else:
        canli_link = link_bul(k["url"], k["regex"])
        
    # 2. Adim: Eger link BULUNAMADIYSA bile kanali oldurme!
    # Sitenin ana adresini yaz ki listede gozuksun.
    if not canli_link:
        print(f"UYARI: {k['isim']} linki bulunamadi. Yine de listeye ekleniyor.")
        canli_link = k["url"]
            
    # Listeye yaz
    dosya_icerigi += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("Liste guncellendi: Hicbir kanal silinmedi!")
