const oneriListesi = [
    { title: "UZAK ŞEHİR", desc: "Bu Akşam 20:00'da Kanal D'de!", image: "https://i.imgur.com/reWzIZ1.jpeg", targetChannel: "Kanal D" },
    { title: "BERGEN", desc: "Bu Akşam 20:00'da ATV'de!", image: "https://i.imgur.com/jnhG97F.jpeg", targetChannel: "ATV" },
    { title: "MASTERCHEF", desc: "20:00'da Yeni Bölüm Heyecanı Başlıyor!", image: "https://i.imgur.com/tfiSe30.jpeg", targetChannel: "TV8" }
];

let aktifSira = 0;

// İŞTE BURAYA YAPIŞTIRIYORSUN:
function setupFeatured() {
    const card = document.getElementById('featured-card');
    const title = document.getElementById('featured-title');
    const desc = document.getElementById('featured-desc');

    if (!card || oneriListesi.length === 0) return;

    const veri = oneriListesi[aktifSira];

    // Önce resmi arka planda yükletelim ki beyaz/boş görünmesin
    const imgPreload = new Image();
    imgPreload.src = veri.image;
    
    imgPreload.onload = () => {
        card.style.opacity = "0"; // Değişim anında yumuşak geçiş için sıfırla
        
        setTimeout(() => {
            title.innerText = veri.title;
            desc.innerText = veri.desc;
            card.style.backgroundImage = `url('${veri.image}')`; // URL tırnaklarına dikkat!
            card.style.opacity = "1"; // Resim hazır olduğunda göster
        }, 300);
    };

    aktifSira = (aktifSira + 1) % oneriListesi.length;
}

function playFeatured() {
    let suAnkiIndex = (aktifSira === 0) ? oneriListesi.length - 1 : aktifSira - 1;
    const veri = oneriListesi[suAnkiIndex];
    const channel = allChannels.find(k => k.ad === veri.targetChannel);
    if (channel) playChannel(channel.url, channel.ad, false, channel.kategori);
}

// Başlatma (Burası aynı kalıyor)
setTimeout(() => {
    setupFeatured();
    setInterval(setupFeatured, 5000);
}, 1000);
