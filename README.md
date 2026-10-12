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

Oturumu iki yoldan başlatabilirsin:

1. **Perdeden** (Google ile girişli perde): derste **Kumandayla başlat** ya da **Kumandasız başlat** seçilir. Kumandayla seçilince perde 4 haneli kodu gösterip bekler; telefondaki kumandada aynı dersin kartında anında **Perde kumanda bekliyor · Katıl** düğmesi belirir. Dokununca iki ekran da yeşil yanar ve kumanda açılır. Kumandasız başlatılan oturuma da kumanda sonradan **Perdedeki oturuma katıl** ile bağlanabilir.
2. **Kumandadan**: **Yeni oturum başlat** iki kod üretir (oturum ve bağlantı kodu); bu kodlar girişsiz perdeye yazılır. Perde bağlanınca telefon titrer ve iki ekran yeşil onay verir.

Kumandadaki ders listesi açık oturumu canlı izler; perdede açılan oturum bir saniye içinde görünür.
- **Öğrenci ekranı**: Öğrenciler telefondan açıp oturum koduyla katılır ve soruları cevaplar. Tek sütun, telefon öncelikli tasarlanmıştır.

## Ders içerikleri

Canlı oturumlardaki sorular `canli/dersler/` altında JSON olarak durur, slaytlar `canli/slaytlar/` altındadır.

| Kod | Ders | Tarih |
|---|---|---|
| M1 | Mukozal Hastalıklar 1 | 27 Ekim 2026 |
| M2 | Mukozal Hastalıklar 2 ve Dil Hastalıkları | 27 Ekim 2026 |

## Klasör yapısı

```
index.html          Ana sunum
canli/
  index.html        Öğrenci ekranı
  perde.html        Perde
  kumanda.html      Kumanda
  dersler/          Ders ve soru tanımları (M1.json, M2.json, index.json)
  slaytlar/         Ders slaytları (M1, M2)
  img/              Soru görselleri
```
