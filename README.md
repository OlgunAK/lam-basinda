# Lam Başında

Diş hekimliği 4. sınıf patoloji dersleri için hazırlanan, tarayıcıda çalışan sunum ve canlı etkileşim sayfaları.

Tüm sayfalar GitHub Pages üzerinden yayınlanır. Aşağıdaki bağlantılar çalışan sayfalara gider (`github.com/.../blob/...` adresleri sayfayı değil kaynak kodunu gösterir).

## Bağlantılar

| Sayfa | Adres | Kimin için |
|---|---|---|
| Ana sayfa (Lam Başında) | https://olgunak.github.io/lam-basinda/ | Ders sunumu |
| Canlı oturum, öğrenci ekranı | https://olgunak.github.io/lam-basinda/canli/ | Öğrenciler (telefondan) |
| Perde | https://olgunak.github.io/lam-basinda/canli/perde.html | Projeksiyon / duvardaki ekran |
| Kumanda | https://olgunak.github.io/lam-basinda/canli/kumanda.html | Dersi yöneten hoca |

### Nasıl kullanılır

- **Kumanda**: Hoca bu sayfadan oturumu ve soruları yönetir.
- **Perde**: Duvardaki ekranda açık kalır, gelen cevapları ve katılımcı sayısını canlı gösterir. Yeni oturum başladığında onu takip eder.

Katılım ekranı, ders başlığı slaytını karekod ve oturum koduyla yan yana gösterir; öğrenciler daha ilk slaytta okutur. L tuşu (kumandada Katılım) kaplamayı kapatıp yalnız slaytı gösterir, tekrar basınca geri gelir.

Oturumu iki yoldan başlatabilirsin:

1. **Perdeden** (Google ile girişli perde): derste **Kumandayla başlat** ya da **Kumandasız başlat** seçilir. Kumandayla seçilince perde 4 haneli kodu gösterip bekler; telefondaki kumandada aynı dersin kartında anında **Perde kumanda bekliyor · Katıl** düğmesi belirir. Dokununca iki ekran da yeşil yanar ve kumanda açılır. Kumandasız başlatılan oturuma da kumanda sonradan **Perdedeki oturuma katıl** ile bağlanabilir.
2. **Kumandadan**: **Yeni oturum başlat** iki kod üretir (oturum ve bağlantı kodu); bu kodlar girişsiz perdeye yazılır. Perde bağlanınca telefon titrer ve iki ekran yeşil onay verir.
   Kodlar bir kez yazılır: kumandadan sonraki oturum açıldığında perde yeni oturuma kendiliğinden geçer (bağlantı kodu yalnız eşleşmiş perdenin okuyabildiği yere yazılır). Perde sayfası yenilense ya da bilgisayar uyandırılsa da aynı yerden devam eder; tarayıcı kapanıp site verisi silinmedikçe kod istemez.

Kumandadaki ders listesi açık oturumu canlı izler; perdede açılan oturum bir saniye içinde görünür.

**Soru aralığı (`qopen`):** Bir slayta `"qopen": "W3"` yazılırsa soru o slayta gelince telefonlarda açılır ama perde slaytı göstermeye devam eder (açılış vakası: vaka metni ve fotoğraf perdede, şıklar telefonda). Oylama, sorunun kendi slaytına (`"q": "W3"`, dağılım) kadar ve geri gidişlerde açık kalır; ancak o slaytta → ile kapanır.

**Tempo göstergesi:** Kumandanın üstündeki şerit, slayt notlarındaki plan damgalarını (`[12:30–13:15]`) gerçek süreyle karşılaştırır. Yeşil "Planda", kırmızı "Hızlan · 2:31 geride", sarı "Yavaşla · 1:10 ileride"; başlık çubuğu da aynı renge boyanır. Saat ikinci slayta geçince başlar; şeride dokununca plan o anki slayta eşitlenir.

**Blok ders (arka arkaya iki ders):** Birinci ders bitince kumandadan ya da perdeden ikinci dersin oturumu açılır. Öğrencilerin telefonunda "Sıradaki ders: … · Sıradaki derse geç" kartı belirir; tek dokunuşla aynı takma adla yeni oturuma geçerler, tekrar karekod okutmaları gerekmez. Eski karekod bağlantısı da kendiliğinden yeni oturuma yönlendirir. Girişli perde yeni oturumu kendiliğinden izler ve kumandaya yeşil onay verir.
- **Öğrenci ekranı**: Öğrenciler telefondan açıp oturum koduyla katılır ve soruları cevaplar. Tek sütun, telefon öncelikli tasarlanmıştır.
  Takma ad yazan öğrenci 4 haneli bir PIN de belirler: ad o derste ona ait olur, aynı adı ikinci kişi alamaz; cihaz değiştirirse ad + PIN ile devam eder. Blok geçişinde ad ve PIN telefonda saklı kaldığı için yeni oturumda da aynı ad kendiliğinden alınır.

## Güvenlik ve Firestore kuralları

- `canli/config.js` içindeki Firebase web anahtarı gizli değildir; tarayıcıya gitmek için tasarlanmıştır ve sitede zaten herkes görür. GitHub'ın `AIza…` uyarısı bu yüzden "False positive" olarak kapatılabilir. Yine de Google Cloud Console → APIs & Services → Credentials altında anahtara **Website restrictions** (`olgunak.github.io/*`, `lam-basinda.firebaseapp.com/*`) ve **API restrictions** (Identity Toolkit, Cloud Firestore, Firebase Installations) ekleyin.
- Asıl koruma Firestore kurallarıdır. Repo kökündeki `firestore.rules` dosyası canlı oturumun tüm koleksiyonlarını kapsar:
  - `aktif/{ders}`: herkes okur, yalnız hoca yazar.
  - `sessions/{kod}`: herkes okur; yalnız hoca oluşturur; hoca ya da bağlantı koduyla eşleşmiş perde günceller (yeni `remote`, `remoteSeen`, `src`, `wantRemote` alanları dahil).
  - `gizli/pin`: yalnız hoca.
  - `ekran/{uid}`: perde kendi belgesini ancak doğru bağlantı koduyla yazabilir.
  - `participants/{uid}` ve `answers/{soru_uid}`: öğrenci yalnız kendi belgesini yazar; hoca ve eşleşmiş perde okur.
  - `nicks/{ad}`: takma ad kaydı. İlk alan sahip olur; aynı adı başkası alamaz ("bu derste başkasında" uyarısı). Ad sahibi başka bir cihazdan aynı PIN ile adını geri alabilir. PIN sunucuda karşılaştırılır, telefona okunmaz.
- Kurallar main'e her gidişinde GitHub Actions (`.github/workflows/firestore-rules.yml`) tarafından Firebase'e kendiliğinden yayınlanır. Bunun için repo ayarlarında (Settings → Secrets and variables → Actions) iki gizli anahtar olmalı:
  - `HOCA_EPOSTA` (isteğe bağlı): hoca e-postalarını dosyadaki listenin yerine koymak için; virgülle birden fazla yazılabilir.
  - `FIREBASE_SERVICE_ACCOUNT`: Firebase Console → Proje ayarları (dişli) → Service accounts → **Generate new private key** ile inen JSON dosyasının tamamı.
  - İş akışı Actions sekmesinden elle de çalıştırılabilir (**Run workflow**).
- Elle yayınlamak istersen: dosyanın tamamını Firebase Console → Firestore Database → Rules sekmesine yapıştır ve **Publish** de.

## Ders içerikleri

Canlı oturumlardaki sorular `canli/dersler/` altında JSON olarak durur, slaytlar `canli/slaytlar/` altındadır.

| Kod | Ders | Tarih |
|---|---|---|
| M1 | Mukozal Hastalıklar 1 | 27 Ekim 2026 |
| M2 | Mukozal Hastalıklar 2 ve Dil Hastalıkları | 27 Ekim 2026 |

## Klasör yapısı

```
index.html          Ana sunum
firestore.rules     Firestore güvenlik kuralları (Actions ile yayınlanır)
firebase.json       Firebase CLI ayarı (kural dosyasının yeri)
.github/workflows/  Kuralları Firebase'e yayınlayan iş akışı
canli/
  index.html        Öğrenci ekranı
  perde.html        Perde
  kumanda.html      Kumanda
  dersler/          Ders ve soru tanımları (M1.json, M2.json, index.json)
  slaytlar/         Ders slaytları (M1, M2)
  img/              Soru görselleri
```
