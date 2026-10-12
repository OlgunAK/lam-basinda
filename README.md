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
