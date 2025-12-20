import time
from playwright.sync_api import sync_playwright

def link_yakala(context, kanal_adi, url):
    if ".m3u8" in url:
        return url
    
    page = context.new_page()
    bulunan_link = [url]

    def istek_kontrol(request):
        if ".m3u8" in request.url and "ads" not in request.url:
            bulunan_link[0] = request.url

    page.on("request", istek_kontrol)
    
    try:
        page.goto(url, wait_until="commit", timeout=30000)
        # Link yakalanana kadar bekle (max 12 sn), bulunca hemen diğerine geç
        for _ in range(12):
            if bulunan_link[0] != url: break
            time.sleep(1)
    except: pass
    
    page.close()
    return bulunan_link[0]

kanallar = [
    {"isim": "TRT 1", "url": "https://trt.daioncdn.net/trt-1/master.m3u8?app=web", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt1.jpg"},
    {"isim": "ATV", "url": "https://www.atv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/atv.jpg"},
    {"isim": "Kanal D", "url": "https://www.kanald.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanald.jpg"},
    {"isim": "Star TV", "url": "https://www.startv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/star.jpg"},
    {"isim": "Show TV", "url": "https://www.showtv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/showtv.jpg"},
    {"isim": "NOW TV", "url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/now.jpg"},
    {"isim": "TV8", "url": "https://tv8.daioncdn.net/tv8/tv8.m3u8?app=7ddc255a-ef47-4e81-ab14-c0e5f2949788&ce=3", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tv8.jpg"},
    {"isim": "Beyaz TV", "url": "https://www.beyaztv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/beyaztv.jpg"},
    {"isim": "Teve2", "url": "https://www.teve2.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/teve2.jpg"},
    {"isim": "Kanal 7", "url": "https://www.kanal7.com/canli-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanal7.jpg"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"},
    {"isim": "DMAX TR", "url": "https://www.dmax.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"},
    {"isim": "TLC TR", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"},
    {"isim": "TRT Spor", "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"}
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    m3u_icerik = "#EXTM3U\n"
    for k in kanallar:
        link = link_yakala(context, k["isim"], k["url"])
        m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{link}\n'
        print(f"✅ {k['isim']} hazır.")
    
    browser.close()

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)
    
