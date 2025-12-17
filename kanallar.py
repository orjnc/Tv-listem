import requests
import re

# --- UST DUZEY TARAYICI TAKLIDI (TOD ICIN OZEL) ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.todtv.com.tr/",
    "Origin": "https://www.todtv.com.tr"
}

def link_bul(url, regex_pattern):
    try:
        print(f"Taraniyor (HD Kalite Icin): {url}")
        r = requests.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            # 1. Deneme: Standart m3u8
            match = re.search(regex_pattern, r.text)
            if match:
                temiz_link = match.group(1).replace("\\/", "/")
                print(f"✅ BULUNDU: {temiz_link}")
                return temiz_link
            
            # 2. Deneme: Gizli Tokenli Linkler (TOD ozel)
            # TOD bazen linki JSON icinde saklar
            gizli_match = re.search(r'["\'](https:.*?\.m3u8.*?)["\']', r.text)
            if gizli_match:
                temiz_link = gizli_match.group(1).replace("\\/", "/")
                print(f"✅ BULUNDU (Gizli): {temiz_link}")
                return temiz_link
                
    except Exception as e:
        print(f"❌ Hata: {e}")
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
    # 2. KANAL D HD (SADECE TOD TV KAYNAGI)
    {
        "isim": "Kanal D HD",
        "url": "https://www.todtv.com.tr/canli-tv/kanal-d",
        # TOD icin genis kapsamli arama
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
    # 7. TRT SPOR YILDIZ
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
    
    # Eger tip "sabit" ise direkt URL'yi kullan
    if k.get("tip") == "sabit":
        canli_link = k["url"]
        print(f"SABIT EKLENDI: {k['isim']}")
    else:
        canli_link = link_bul(k["url"], k["regex"])
            
    # Eger link bulunamazsa, kanal silinmesin. Site adresini yazsin.
    if not canli_link:
        print(f"⚠️ UYARI: {k['isim']} (TOD) linki cekilemedi. Site adresi yaziliyor.")
        canli_link = k["url"]
            
    dosya_icerigi += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("Liste guncellendi: Kanal D icin sadece TOD zorlandi.")
