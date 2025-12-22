const oneriListesi = [
    {
        title: "UZAK ŞEHİR",
        desc: "Bu Akşam 20:00'da Kanal D'de!",
        image: "https://i.imgur.com/NKiF8WO.jpeg",
        targetChannel: "Kanal D"
    },
    {
        title: "BERGEN",
        desc: "Bu Akşam 20:00'da ATV'de!",
        image: "https://i.imgur.com/LNW86ek.jpeg",
        targetChannel: "ATV"
    },
    {
        title: "MASTERCHEF",
        desc: "20:00'da Yeni Bölüm Heyecanı Başlıyor!",
        image: "https://i.imgur.com/wAX4TER.jpeg",
        targetChannel: "TV8"
    }
];

let aktifSira = 0;

function updatePromo() {
    const veri = oneriListesi[aktifSira];
    const card = document.getElementById('featured-card');
    const title = document.getElementById('featured-title');
    const desc = document.getElementById('featured-desc');

    if (card && title && desc) {
        // Kartın içeriğini güncelle
        title.innerText = veri.title;
        desc.innerText = veri.desc;
        card.style.backgroundImage = `url('${veri.image}')`;
        
        // Bir sonraki öneriye geç
        aktifSira = (aktifSira + 1) % oneriListesi.length;
    }
}

// Öne çıkan karta tıklandığında ilgili kanalı açar
function playFeatured() {
    // aktifSira bir artırıldığı için bir önceki veriyi alıyoruz
    const suankiSira = (aktifSira === 0) ? oneriListesi.length - 1 : aktifSira - 1;
    const veri = oneriListesi[suankiSira];
    
    // allChannels içinden ismi eşleşen kanalı bul
    const channel = allChannels.find(k => k.ad === veri.targetChannel);
    
    if (channel) {
        playChannel(channel.url, channel.ad, false, channel.kategori);
    } else {
        console.log("Kanal bulunamadı: " + veri.targetChannel);
    }
}

// Sayfa açıldığında başlat ve 5 saniyede bir değiştir
setInterval(updatePromo, 5000);
updatePromo(); 
