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
- **Perde**: Duvardaki ekranda açık kalır, gelen cevapları ve katılımcı sayısını canlı gösterir. Yeni oturum başladığında onu takip eder. Üst çubukta öğrencilerin gördüğü ad "Lam Başında" ve "Soru 7/12" sayacıdır; iç kodlar (W7) görünmez. Alt kontrol çubuğu slayt gösterilirken 2,5 saniye sonra kendiliğinden gizlenir (fare oynayınca geri gelir); katılım ekranındaki "başlamak için →" notu artık yalnız bu çubukta, öğrenciye görünmez.
  - **Açık uçlu cevaplar** aynı metinler tek kartta toplanır (×6 rozeti), sayfa başına 18 kart; sayfa kumandadaki **Cevapları yönet** düğmeleriyle ya da perdede `[` `]` tuşlarıyla çevrilir.
  - **Kelime bulutu** "aft / afta / aftlar" gibi kök + 3 harfe kadar uzantıları tek kelimede birleştirir; boyut sayıyla doğrusal büyür (en çok söylenen en büyük).
  - **Moderasyon** paylaşımlıdır: kumandadan ya da perdede çift tıklayarak gizlenen cevap/kelime oturum belgesine yazılır (`hidden.*`, `hiddenWords`), her perdede aynı anda kalkar.
  - **Vakaya dönüş** anketinde doğru şıkkın ders başındaki ve şimdiki yüzdesi büyük rakamla ve farkla gösterilir; **senaryo uyum testinde** (SCT) uzman cevabının bir yanındaki şık yarım puan alır.
  - Dersin sonunda perdede ve son slaytta **çağrı** (`cta` alanı: ödev, son tarih, ödül) görünür.

Katılım ekranı, ders başlığı slaytını karekod ve oturum koduyla yan yana gösterir; öğrenciler daha ilk slaytta okutur. L tuşu (kumandada Katılım) kaplamayı kapatıp yalnız slaytı gösterir, tekrar basınca geri gelir.

Oturumu iki yoldan başlatabilirsin:

1. **Perdeden** (girişli perde: **perde hesabı** ya da hocanın Google hesabı): derste **Kumandayla başlat** ya da **Kumandasız başlat** seçilir. Kumandayla seçilince perde 4 haneli kodu gösterip bekler; telefondaki kumandada aynı dersin kartında anında **Perde kumanda bekliyor · Katıl** düğmesi belirir. Dokununca iki ekran da yeşil yanar ve kumanda açılır. Kumandasız başlatılan oturuma da kumanda sonradan **Perdedeki oturuma katıl** ile bağlanabilir.
2. **Kumandadan**: **Yeni oturum başlat** iki kod üretir (oturum ve bağlantı kodu); bu kodlar girişsiz perdeye yazılır. Perde bağlanınca telefon titrer ve iki ekran yeşil onay verir.
   Kodlar bir kez yazılır: eşleşen perde güven kaydını kendisi yazar ve 12 saat boyunca hocanın **güvenilir ekranı** olur (`guven/{hoca}/ekran/{perde}`), sonraki oturumlara kod gerekmeden kendiliğinden bağlanır. Oturum bitince bekler, hoca yeni oturum açınca (kumanda yenilenmiş olsa bile) yarım saniye içinde geçer; perde sayfası yenilense de kaldığı yerden devam eder. Yalnız mevcut oturumdan daha yeni oturumlara geçer, eski açık kalmış oturumlara atlamaz.

Kumandadaki ders listesi açık oturumu canlı izler; perdede açılan oturum bir saniye içinde görünür.

**Perde hesabı (önerilen):** Sınıf bilgisayarı Google yerine sabit bir e-posta/şifre hesabıyla girer: perde sayfasındaki **Perde hesabıyla gir** kutusuna şifre yazılır, e-posta `canli/config.js` içindeki `PERDE_EPOSTA` (`perde@lam-basinda.app`) ile sabittir. Bir kez girince tarayıcı girişi saklar; kod eşleşmesi, güven kaydı ya da süre sınırı yoktur. Bu perde hocanın açtığı her oturumu (kumandadan ya da başka perdeden, son 12 saat içinde açılmış ve bitmemiş) kendiliğinden izler, ders bitince sıradakine geçer, sayfa yenilense ya da bilgisayar uyuyup uyansa kaldığı oturuma döner; eşleşme ekranına bir daha düşmez. Kurulum (bir kez):

1. Firebase konsolu → **Authentication → Sign-in method** → **Email/Password** sağlayıcısını aç.
2. **Authentication → Users → Add user**: e-posta `perde@lam-basinda.app`, istediğin şifre.
3. `firestore.rules` dosyasını yeniden yayımla (`perdeListesi()` içinde aynı e-posta yazılı olmalı).
4. Sınıf bilgisayarında `canli/perde.html` aç, şifreyi yaz, **Gir**.

Hesabın e-postasını değiştirmek için `canli/config.js` içindeki `PERDE_EPOSTA` ve kurallardaki `perdeListesi()` birlikte güncellenir.

**Soru aralığı (`qopen`):** Bir slayta `"qopen": "W3"` yazılırsa soru o slayta gelince telefonlarda açılır ama perde slaytı göstermeye devam eder (açılış vakası: vaka metni ve fotoğraf perdede, şıklar telefonda). Oylama, sorunun kendi slaytına (`"q": "W3"`, dağılım) kadar ve geri gidişlerde açık kalır; ancak o slaytta → ile kapanır.

**Kumandadaki araçlar:** Üst sırada Aç/Kapat (oylama), Sonuçlar, Cevap, Süre (sorunun kendi süresi), Katılım (karekod ekranı), Liderlik, Slaytlar (slayta git) ve **Daha ⋯**. Notların üstünde açık sorunun canlı dağılımı görünür (seçenek başına çubuk ve sayı, doğru şık ✓, katılım yüzdesi). Daha ⋯ menüsü:

- **Hızlı anket:** slaytta olmayan bir soruyu anında sor; A–E, A–D, Evet/Hayır, Doğru/Yanlış, 1–5 ya da kelime bulutu. Perde slaytı gizleyip dağılımı gösterir, telefonlarda şıklar açılır; puanlanmaz. İleri tuşu anketi kapatır, bir daha basınca slayta döner (oturum belgesinde `adhoc`).
- **Süre seç:** 15–120 sn geri sayım (`timer` komutu `s` ile), süre bitince oylama kapanır; **Süreyi durdur** (`tstop`).
- **Duyuru:** perdede 12 sn büyük yazı (`msg`), telefonlarda bildirim (`notice`); hazır metinler (10 dk ara…).
- **Karartma:** perde simsiyah olur (`black`; perdede `.` tuşu); tekrar dokununca slayt geri gelir.
- **Katılım rozeti:** slaytın köşesinde karekod + kişi sayısı.
- **Kişiler:** katılımcı listesi; **Çıkar** kişinin kaydını ve ad kaydını siler, ad serbest kalır, telefon "Hoca seni dersten çıkardı" görür; aynı ad ve PIN ile yeniden katılabilir.
- **Soruyu sıfırla:** açık sorunun cevaplarını siler ve soruyu yeniden açar (iki dokunuşla onay).
- **Yoklama / sonuçları indir:** CSV (noktalı virgül, Excel uyumlu): ad, kimlik, katılım saati, her sorunun cevabı, doğru ve cevap sayısı. Telefonda paylaşım penceresi, bilgisayarda indirme.
- **Öğrenci bağlantısını paylaş:** katılım bağlantısını paylaşır ya da panoya kopyalar.
- **Cevapları yönet:** açık sorunun serbest metin cevaplarını (gruplanmış, yazan adıyla) ve bulut kelimelerini listeler; Gizle/Göster perdeye anında yansır. Açık uçlu soruda perdenin sayfasını çevirir.

**Tempo göstergesi:** Kumandanın üstündeki şerit, slayt notlarındaki plan damgalarını (`[12:30–13:15]`) gerçek süreyle karşılaştırır. Yeşil "Planda", kırmızı "Hızlan · 2:31 geride", sarı "Yavaşla · 1:10 ileride"; başlık çubuğu da aynı renge boyanır. Saat ikinci slayta geçince başlar; şeride dokununca plan o anki slayta eşitlenir.

**Blok ders (arka arkaya iki ders):** Birinci ders bitince kumandadan ya da perdeden ikinci dersin oturumu açılır. Öğrencilerin telefonunda "Sıradaki ders: … · Sıradaki derse geç" kartı belirir; tek dokunuşla aynı takma adla yeni oturuma geçerler, tekrar karekod okutmaları gerekmez. Eski karekod bağlantısı da kendiliğinden yeni oturuma yönlendirir. Girişli perde yeni oturumu kendiliğinden izler ve kumandaya yeşil onay verir.
- **Öğrenci ekranı**: Öğrenciler telefondan açıp oturum koduyla katılır ve soruları cevaplar. Tek sütun, telefon öncelikli tasarlanmıştır.
  Takma ad yazan öğrenci 4 haneli bir PIN de belirler: ad o derste ona ait olur, aynı adı ikinci kişi alamaz. Kayıt bir kez açıldıktan sonra PIN eşleşmeden kimse (adın şu anki telefonu bile) o adla giremez ya da PIN'i değiştiremez; yanlış PIN "ad başkasında" uyarısı alır. Blok derste yeni oturum bir öncekini hatırlar (`prev`): birinci derste PIN ile alınmış ad ikinci derste de yalnız aynı PIN ile alınabilir, önce gelen biri başka PIN ile o adı kapamaz. Kimlik ad üzerinden yürür: aynı ad + PIN ile başka cihazdan girince kayıt (cevaplar, puan) oradan devam eder, eski cihaz "Başka cihazdan giriş yapıldı" ekranı görür ve cevap yazamaz; liderlik tablosunda kişi tek satırdır. Üstteki sarı **Skor** düğmesi (ya da oturum kodu) puan durumunu açar: ad, cevaplanan ve doğru sayısı, sıra ve ilk 10; her cevap açıklamasında perde puan durumunu yeniler. Yeni soru açılınca bu pencere kendiliğinden kapanır. Blok geçişinde ad ve PIN telefonda saklı kaldığı için yeni oturumda da aynı ad kendiliğinden alınır.

## Güvenlik ve Firestore kuralları

- `canli/config.js` içindeki Firebase web anahtarı gizli değildir; tarayıcıya gitmek için tasarlanmıştır ve sitede zaten herkes görür. GitHub'ın `AIza…` uyarısı bu yüzden "False positive" olarak kapatılabilir. Yine de Google Cloud Console → APIs & Services → Credentials altında anahtara **Website restrictions** (`olgunak.github.io/*`, `lam-basinda.firebaseapp.com/*`) ve **API restrictions** (Identity Toolkit, Cloud Firestore, Firebase Installations) ekleyin.
- Asıl koruma Firestore kurallarıdır. Repo kökündeki `firestore.rules` dosyası canlı oturumun tüm koleksiyonlarını kapsar:
  - `aktif/{ders}`: herkes okur, yalnız hoca yazar.
  - `sessions/{kod}`: herkes okur; yalnız hoca oluşturur; hoca ya da bağlantı koduyla eşleşmiş perde günceller (yeni `remote`, `remoteSeen`, `src`, `wantRemote` alanları dahil).
  - `gizli/pin`: yalnız hoca.
  - `ekran/{uid}`: perde kendi belgesini ancak doğru bağlantı koduyla yazabilir.
  - `participants/{pid}` ve `answers/{soru_pid}`: kişi kimliği (pid) takma adın anahtarı ya da anonim uid; bir adın altında yalnız adın güncel sahibi yazabilir. Hoca ve eşleşmiş perde okur.
  - `guven/{hoca}/ekran/{perde}`: kumandanın yazdığı güvenilir ekran kaydı (12 saat); perde bununla kod girmeden sonraki oturumlara eşleşir.
  - `sessions/{kod}/nicks/{ad}`: ad kaydı `{uid, ph, nick, t}`; `ph` PIN özeti. Kayıt varsa yazmak için `ph` eşleşmeli; oturum belgesinde `prev` varsa (blokta önceki oturum, 3 saat içinde açılmışsa yazılır) önceki dersin aynı ad kaydıyla da eşleşmeli.
  - Perde hesabı (`perdeListesi()`): oturum açıp yönetebilir, bağlantı kodunu okuyup kendi ekran kaydını yazar; cevap ve katılımcı listelerini okur. Öğrenci verisini silemez, `guven` kayıtlarına dokunamaz.
  - `nicks/{ad}`: takma ad kaydı (herkes okur). PIN düz metin saklanmaz, SHA-256 özeti (`ph`) tutulur. İlk alan sahip olur; aynı adı başkası alamaz ("bu derste başkasında" uyarısı). Ad sahibi başka bir cihazdan aynı PIN ile adını geri alır. Kayıt kurallar yüzünden reddedilirse telefon bunu ayrı bir mesajla söyler ("Sunucu kuralları güncel olmayabilir").
- Kurallar main'e her gidişinde GitHub Actions (`.github/workflows/firestore-rules.yml`) tarafından Firebase'e kendiliğinden yayınlanır. Bunun için repo ayarlarında (Settings → Secrets and variables → Actions) iki gizli anahtar olmalı:
  - `HOCA_EPOSTA` (isteğe bağlı): hoca e-postalarını dosyadaki listenin yerine koymak için; virgülle birden fazla yazılabilir.
  - `FIREBASE_SERVICE_ACCOUNT`: Firebase Console → Proje ayarları (dişli) → Service accounts → **Generate new private key** ile inen JSON dosyasının tamamı.
  - İş akışı Actions sekmesinden elle de çalıştırılabilir (**Run workflow**).
- Elle yayınlamak istersen: dosyanın tamamını Firebase Console → Firestore Database → Rules sekmesine yapıştır ve **Publish** de.

## Ders içerikleri

Canlı oturumlardaki sorular `canli/dersler/` altında JSON olarak durur, slaytlar `canli/slaytlar/` altındadır. İki dersin çerçevesi adlandırıldı: M1 **3D** (Dağılım, Düzey, Desen), M2 **3G** (Gazlı bezle gider mi, gerince geçer mi, gerekçesi var mı); slayt alt şeridi ve soru etiketleri bu adları taşır (`frame` alanı).

Ders JSON'undaki özel slayt alanları: `lobby` (katılım ekranı), `qopen` (soru açılır, slayt kalır), `q` (soru/dağılım), `board` + `top: 5` (ara liderlik, ilk 5), `cloud: {"q":"W11","from":"prev"}` (bir önceki oturumun kelime bulutu; M2 böyle açılır ve M1'in çıkış biletini cevaplar), `cta` (bitiş çağrısı). Soru bölgesi türleri: `rect`, `ellipse`, `ring` (halka: biyopsiyi lezyonun kenarından alma sorusu).

Slaytlar `tools/slaytlar/build.py` + `build2.py` ile orijinal görsellerden yeniden üretilir (PIL; Lora ve Lato fontları; orijinal slaytlar ilk sürümden: `git show 2d6da82:canli/slaytlar/M1/01.jpg`). M2'deki "Mikroskopta displazi" slaytı iki fotoğraf bekler: `canli/img/displazi_normal.jpg` ve `canli/img/displazi_agir.jpg` (H&E kesit). Dosyalar konup slaytlar yeniden üretilince çerçevelere yerleşir; şimdilik çerçevelerde yer tutucu yazı var.

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
