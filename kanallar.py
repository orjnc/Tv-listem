import requests
import re

# --- STRATEJIK AYARLAR ---
# Kendimizi tamamen Web Video Caster ve Android cihaz olarak tanimliyoruz
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36",
    "X-Requested-With": "com.instantbits.cast.webvideo",
    "Referer": "https://www.todtv.com.tr/",
    "Accept-Language": "tr-TR,tr;q=0.9"
}

def gercek_linki_sok(url):
    """Sayfadaki gizli oynatici ayarlarindan m3u8 linkini ayristirir."""
    try:
        # 1. Sayfayi indir
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200: return url
        
        # 2. Ters slashlari temizleyerek ham metne donustur
        content = r.text.replace("\\/", "/")
        
        # 3. MANTIK: Oynatici nesneleri (VideoJS/Dailymotion vb.) icindeki linkleri tara
        # Bu regex, st ve e parametrelerini (tokenlari) en saglikli sekilde yakalar
        patterns = [
            r'["\'](https?://[^"\']*?\.m3u8\?st=[^"\']*?)["\']', # Sifreli/Tokenli linkler
            r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']'      # Standart linkler
        ]
        
        for p in patterns:
            found = re.search(p, content)
            if found:
                link = found.group(1)
                # Eger ercdn veya daioncdn geciyorsa dogru link budur
                if "ercdn" in link or "daion" in link or "kanald" in link:
                    print(f"✅ SÖKÜLDÜ: {url}")
                    return link
                    
    except Exception as e:
        print(f"❌ Hata: {e}")
    return url

# --- KANAL LISTESI ---
kanallar = [
    {"isim": "TRT 1", "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "logo": "trt1.jpg"},
    {"isim": "Kanal D HD", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "kanald.jpg"},
    {"isim": "Nickelodeon", "url": "https://www.todtv.com.tr/canli-tv/nickelodeon-sd", "logo": "nickelodeon.jpg"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "tabiispor.jpg", "sabit": True},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "dmax.jpg"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "tlc.jpg"},
    {"isim": "TRT Spor", "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002", "logo": "trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz", "logo": "trtsporyildiz.jpg", "ozel": True},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "tabiispor.jpg"}
]

# --- PLAYLIST OLUSTURMA ---
m3u_text = "#EXTM3U\n"
for k in kanallar:
    link = k["url"] if k.get("sabit") else gercek_linki_sok(k["url"])
    logo_path = "refs/heads/main/" if k.get("ozel") else ""
    logo_url = f"https://raw.githubusercontent.com/orjnc/Tv-listem/{logo_path}logolar/{k['logo']}"
    m3u_text += f'#EXTINF:-1 tvg-logo="{logo_url}", {k["isim"]}\n{link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_text)
print("🚀 Islem Tamamlandi.")
