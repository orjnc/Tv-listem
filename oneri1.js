// ÖNE ÇIKAN İÇERİK AYARLARI
const featuredConfig = {
    title: "UZAK ŞEHİR",
    desc: "Bu Akşam 20:00'da Kanal D'de!",
    image: "https://i.imgur.com/NKiF8WO.jpeg", 
    targetChannel: "Kanal D" // JSON'daki kanal adıyla aynı olmalı
};

// Pano Kurulumu
function setupFeatured() {
    const card = document.getElementById('featured-card');
    const title = document.getElementById('featured-title');
    const desc = document.getElementById('featured-desc');

    if (card && title && desc) {
        title.innerText = featuredConfig.title;
        desc.innerText = featuredConfig.desc;
        card.style.backgroundImage = `linear-gradient(to bottom, transparent, rgba(0,0,0,0.8)), url('${featuredConfig.image}')`;
        card.style.backgroundSize = "cover";
        card.style.backgroundPosition = "center";
    }
}

// Panoya tıklandığında kanalı oynat
function playFeatured() {
    // allChannels değişkenine index.html üzerinden erişiyoruz
    const channel = allChannels.find(k => k.ad === featuredConfig.targetChannel);
    if (channel) {
        playChannel(channel.url, channel.ad);
    } else {
        console.error("Öneri kanalı bulunamadı: " + featuredConfig.targetChannel);
    }
}

// Sayfa tamamen yüklendikten 1 saniye sonra verileri bas
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(setupFeatured, 1000);
});
