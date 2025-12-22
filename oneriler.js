const oneriListesi = [
    {
        title: "UZAK ŞEHİR",
        desc: "Bu Akşam 20:00'da Kanal D'de!",
        image: "https://i.imgur.com/reWzIZ1.jpeg", 
        targetChannel: "Kanal D"
    },
    {
        title: "BERGEN",
        desc: "Bu Akşam 20:00'da ATV'de!",
        image: "https://i.imgur.com/jnhG97F.jpeg", 
        targetChannel: "ATV"
    },
    {
        title: "MASTERCHEF",
        desc: "20:00'da Yeni Bölüm Heyecanı Başlıyor!",
        image: "https://i.imgur.com/ebSpKg0.jpeg",
        targetChannel: "TV8"
    }
];

let aktifSira = 0;

function setupFeatured() {
    const card = document.getElementById('featured-card');
    const title = document.getElementById('featured-title');
    const desc = document.getElementById('featured-desc');

    if (!card || oneriListesi.length === 0) return;

    const veri = oneriListesi[aktifSira];

    // Fade efekti
    card.style.opacity = "0.3";

    setTimeout(() => {
        title.innerText = veri.title;
        desc.innerText = veri.desc;
        card.style.backgroundImage = `url('${veri.image}')`;
        card.style.opacity = "1";
    }, 400);

    aktifSira = (aktifSira + 1) % oneriListesi.length;
}

function playFeatured() {
    let idx = (aktifSira === 0) ? oneriListesi.length - 1 : aktifSira - 1;
    const veri = oneriListesi[idx];
    
    // index.html'deki allChannels'ı kullanır
    if (typeof allChannels !== 'undefined') {
        const channel = allChannels.find(k => k.ad === veri.targetChannel);
        if (channel) {
            playChannel(channel.url, channel.ad, false, channel.kategori);
        }
    }
}

// Başlatıcı
document.addEventListener('DOMContentLoaded', () => {
    // 1.5 saniye bekle (Kanalların yüklenmesi için zaman tanı)
    setTimeout(() => {
        setupFeatured();
        setInterval(setupFeatured, 5000);
    }, 1500);
});
