import requests
import re

# Web Video Caster'in kullandigi tarayici kimligini (User-Agent) taklit ediyoruz
WVC_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
    "X-Requested-With": "com.instantbits.cast.webvideo", # Uygulamanin imzasi
    "Accept": "*/*",
    "Connection": "keep-alive"
}

def wvc_stili_avla(url):
    try:
        print(f"🕵️ WVC Stili Avlaniyor: {url}")
        # Sayfaya gidiyoruz
        response = requests.get(url, headers=WVC_HEADERS, timeout=20)
        
        if response.status_code == 200:
            html = response.text
            # WVC'nin yaptigi gibi tum ag trafigini (html icindeki linkleri) tarayalim
            # Sadece m3u8 degil, gizlenmis tum stream linklerini arayan cok guclu regex
            patterns = [
                r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']',
                r'source\s*:\s*["\'](https?://[^"\']*?)["\']',
                r'file\s*:\s*["\'](https?://[^"\']*?)["\']'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html)
                if matches:
                    # Genelde en guncel link listenin sonundadir veya en uzun olanidir
                    link = matches[-1].replace("\\/", "/")
                    print(f"✅ WVC Mantigiyla BULUNDU: {link}")
                    return link
    except Exception as e:
        print(f"❌ WVC Modu Hatasi: {e}")
    return None

# --- KANAL LISTESI ---
kanallar = [
    {"isim": "TRT 1", "url": "https://www.tabii.com/tr/watch/live/trt1?trackId=150002", "logo": "trt1.jpg", "tip": "ara"},
    {"isim": "Kanal D HD", "url": "https://www.todtv.com.tr/canli-tv/kanal-d", "logo": "kanald.jpg", "tip": "wvc"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "tabiispor.jpg", "tip": "sabit"},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "dmax.jpg", "tip": "ara"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "tlc.jpg", "tip": "ara"},
    {"isim": "TRT Spor", "url": "https://www.tabii.com/tr/watch/live/trtspor?trackId=150002", "logo": "trtspor.jpg", "tip": "ara"},
    {"isim": "TRT Spor Yildiz", "url": "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor-yildiz", "logo": "trtsporyildiz.jpg", "tip": "ara"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "tabiispor.jpg", "tip": "ara"}
]

dosya_icerigi = "#EXTM3U\n"
for k in kanallar:
    logo_url = f"https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/{k['logo']}"
    if k['isim'] == "TRT Spor Yildiz": # Senin ozel logon
        logo_url = "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"

    if k['tip'] == "sabit":
        link = k['url']
    elif k['tip'] == "wvc":
        link = wvc_stili_avla(k['url']) or k['url']
    else:
        # Standart arama
        link = wvc_stili_avla(k['url']) or k['url']
        
    dosya_icerigi += f'#EXTINF:-1 tvg-logo="{logo_url}", {k["isim"]}\n{link}\n'

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)
    
