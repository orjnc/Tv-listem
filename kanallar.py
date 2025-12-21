import time
import requests
import re
from playwright.sync_api import sync_playwright

def youtube_link_yakala(kanal_url):
    """YouTube üzerinden yayın yapan kanallar için m3u8 çekici"""
    try:
        # YouTube linkinden canlı yayın m3u8 adresini ayıklayan basit regex
        r = requests.get(kanal_url, timeout=10)
        match = re.search(r'hlsManifestUrl["\']:\s*["\'](https?://[^"\']*?\.m3u8)', r.text)
        if match:
            return match.group(1)
    except: pass
    return None

def eski_yontem_link(url):
    """Hızlı regex yöntemi - Altın link önceliği"""
    if "youtube.com" in url or "youtu.be" in url:
        return youtube_link_yakala(url)
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": url
        }
        r = requests.get(url, headers=headers, timeout=10)
        text = r.text.replace("\\/", "/")
        matches = re.findall(r'["\'](https?://[^"\']*?\.m3u8[^"\']*?)["\']', text)
        
        if matches:
            # ÖNCELİK 1: daioncdn + token (Altın Link)
            for m in matches:
                if "daioncdn" in m and any(x in m for x in ["st=", "dfp", "ppid", "app="]):
                    return m
            # ÖNCELİK 2: Herhangi bir daioncdn veya kaliteli CDN
            for m in matches:
                if any(cdn in m for cdn in ["daioncdn", "duhnet", "ercdn"]):
                    return m
            return matches[0]
    except: pass
    return None

def tarayici_link_yakala(context, kanal_adi, url):
    """Playwright - 40 Saniye Sabırlı Takip ve YouTube Desteği"""
    if "youtube.com" in url or "youtu.be" in url:
        yt_link = youtube_link_yakala(url)
        return yt_link if yt_link else url

    page = context.new_page()
    bulunan_link = [url]

    def istek_kontrol(request):
        u = request.url
        if ".m3u8" in u.lower() and not any(x in u.lower() for x in ["ads", "vpaid", "telemetry"]):
            # Kalite hiyerarşisi
            yeni_altin = "daioncdn" in u and any(x in u for x in ["st=", "dfp", "ppid"])
            su_anki_altin = "daioncdn" in bulunan_link[0] and "st=" in bulunan_link[0]

            if yeni_altin:
                bulunan_link[0] = u
            elif "daioncdn" in u and not su_anki_altin:
                bulunan_link[0] = u
            elif bulunan_link[0] == url:
                bulunan_link[0] = u

    page.on("request", istek_kontrol)
    try:
        page.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(3)
        page.mouse.click(50, 50) 
        
        # 40 Saniye pusuda bekle
        for _ in range(40):
            if "daioncdn" in bulunan_link[0] and "st=" in bulunan_link[0]:
                break
            time.sleep(1)
    except: pass
    finally: page.close()
    return bulunan_link[0]

# --- KANAL LİSTESİ (YouTube linkleri güncellenebilir) ---
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
    {"isim": "360", "url": "https://www.tv360.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/360.jpg"},
    {"isim": "a2", "url": "https://www.atv.com.tr/a2tv/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/a2.jpg"},
    {"isim": "Kanal 7", "url": "https://www.kanal7.com/canli-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/kanal7.jpg"},
    {"isim": "Tabii TV", "url": "https://ceokzokgtd.erbvr.com/tabiitv/tabiitv.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"},
    {"isim": "FX", "url": "https://saran-live.ercdn.net/fx/index.m3u8?checkedby:iptvcat.com", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/fx.jpg"},
    {"isim": "DMAX", "url": "https://www.dmax.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dmax.jpg"},
    {"isim": "TLC", "url": "https://www.tlctv.com.tr/canli-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tlc.jpg"},
    {"isim": "CNBC-e", "url": "https://www.cnbce.com/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/cnbce.jpg"},
    {"isim": "TRT 2", "url": "https://www.tabii.com/watch/live/trt2?trackId=150007", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trt2.jpg"},
    {"isim": "CNN TÜRK", "url": "https://www.cnnturk.com/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/cnnturk.jpg"},
    {"isim": "TRT Haber", "url": "https://www.trthaber.com/canli-yayin-izle.html", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trthaber.jpg"}, 
    {"isim": "Habertürk", "url": "https://m.haberturk.com/canliyayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/haberturk.jpg"},
    {"isim": "NTV", "url": "https://www.youtube.com/live/pqq5c6k70kk", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/ntv.jpg"},
    {"isim": "Halk TV", "url": "https://halktv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/halktv.jpg"},
    {"isim": "Sözcü", "url": "https://www.youtube.com/live/ztmY_cCtUl0", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/sozcu.jpg"},
    {"isim": "Ekol TV", "url": "https://www.ekoltv.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/ekoltv.jpg"},
    {"isim": "A Haber", "url": "https://www.youtube.com/live/nmY9i63t6qo", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/ahaber.jpg"},
    {"isim": "tv100", "url": "https://www.tv100.com/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tv100.jpg"},
    {"isim": "tvnet", "url": "https://www.tvnet.com.tr/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tvnet.jpg"},
    {"isim": "TGRT Haber", "url": "https://www.tgrthaber.com/canli", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tgrt.jpg"},
    {"isim": "24 TV", "url": "https://www.yirmidort.tv/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/24.jpg"},
    {"isim": "KRT", "url": "https://www.youtube.com/live/sKTq8zmzBvo", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/krt.jpg"},
    {"isim": "TYT Türk", "url": "https://tytturk.com/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tytturk.jpg"},
    {"isim": "Haber Global", "url": "https://haberglobal.com/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/haberglobal.jpg"},
    {"isim": "FB TV", "url": "https://www.fenerbahce.org/fenerbahcetv/canliyayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/fbtv.jpg"},
    {"isim": "HT Spor", "url": "https://www.htspor.com/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/htspor.jpg"},
    {"isim": "A Spor", "url": "https://www.aspor.com.tr/webtv/canli-yayin", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/aspor.jpg"},
    {"isim": "Bein Sports Haber", "url": "https://www.youtube.com/live/9xVXWLwT0vA", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/beinsportshaber.jpg"},
    {"isim": "TRT Spor", "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/trtspor.jpg"},
    {"isim": "TRT Spor Yildiz", "url": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/refs/heads/main/logolar/trtsporyildiz.jpg"},
    {"isim": "Tabii Spor", "url": "https://www.tabii.com/tr/watch/live/trtsporyildiz?trackId=150002", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/tabiispor.jpg"},
    {"isim": "Sports TV", "url": "https://www.sportstv.com.tr/canli/sportstv", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/sportstv.jpg"},
    {"isim": "Powertürk TV", "url": "https://www.powerapp.com.tr/tvs/power-tvs/powerturktv/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/powerturk.jpg"},
    {"isim": "Power TV", "url": "https://www.powerapp.com.tr/tvs/power-tvs/powertv/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/powertv.jpg"},
    {"isim": "Power Love TV", "url": "https://www.powerapp.com.tr/tvs/power-tvs/powerlovetv/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/powerlove.jpg"},
    {"isim": "PowerTürk Akustik TV", "url": "https://www.powerapp.com.tr/tvs/power-tvs/powerturkakustiktv/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/powerturkakustik.jpg"},
    {"isim": "PowerTürk Slow TV", "url": "https://www.powerapp.com.tr/tvs/power-tvs/powertrslowtv/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/powerturkslow.jpg"},
    {"isim": "PowerTürk Taptaze TV", "url": "https://www.powerapp.com.tr/tvs/power-tvs/powerturktaptazetv/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/pttaptaze.jpg"},
    {"isim": "Nr1 Türk", "url": "https://www.numberone.com.tr/2015/12/20/number1-turk-tv-canli-yayin/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/nr1turk.jpg"},
    {"isim": "Nr1", "url": "https://www.numberone.com.tr/2015/12/18/nr1-tv-canli-yayin/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/nr1.jpg"},
    {"isim": "Nr1 Aşk", "url": "https://www.numberone.com.tr/2017/10/05/nr1-ask-tv-canli-yayin-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/nr1ask.jpg"},
    {"isim": "Nr1 Dance", "url": "https://www.numberone.com.tr/2017/10/03/number1-dance-ty-canli-yayin-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/nr1dance.jpg"},
    {"isim": "Nr1 Rap", "url": "https://www.numberone.com.tr/2017/10/05/number1-rap-tv-canli-yayin-izle/", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/nr1rap.jpg"},
    {"isim": "Dream Türk", "url": "https://www.dreamturk.com.tr/canli-yayin-izle", "logo": "https://raw.githubusercontent.com/orjnc/Tv-listem/main/logolar/dreamturk.jpg"},
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    m3u_icerik = "#EXTM3U\n"
    for k in kanallar:
        # YouTube, Regex veya Tarayıcı ile link yakala
        canli_link = eski_yontem_link(k["url"])
        
        # Eğer link hala bulunamadıysa veya sadece kanalın sitesi döndüyse tarayıcıyı ZORLA
        if not canli_link or ".m3u8" not in canli_link or canli_link == k["url"]:
            canli_link = tarayici_link_yakala(context, k["isim"], k["url"])
        
        # Referer Ayarı
        if "atv" in k["url"] or "a2tv" in k["url"] or "aspor" in k["url"]:
            ref = "https://www.atv.com.tr/"
        elif "cnbce" in k["url"]:
            ref = "https://www.cnbce.com/"
        elif "youtube" in canli_link:
            ref = "https://www.youtube.com/"
        else:
            ref = k["url"]

        # TRT ve Tabii linklerine ekleme yapmıyoruz
        if any(x in canli_link for x in ["trt.daioncdn", "medya.trt.com.tr", "erbvr.com"]):
             m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}\n'
        else:
             m3u_icerik += f'#EXTINF:-1 tvg-logo="{k["logo"]}", {k["isim"]}\n{canli_link}|User-Agent=Mozilla/5.0&Referer={ref}\n'
        
        print(f"✅ {k['isim']} bitti.")
    
    browser.close()

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)
    
