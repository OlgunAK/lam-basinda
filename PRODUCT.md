# Product

Lam Başında: diş hekimliği 4. sınıf patoloji dersleri için canlı ders sistemi, ders slaytları ve düzenleyici.

## Platform

web

## Stack

Statik HTML/CSS/JS, GitHub Pages (`main` dalı). Canlı oturum Firebase (Firestore) ile; `canli/*.js` derlenmiş paketler, kaynakları repoda yok. Slaytlar `ortak/slayt.js` ile tarayıcıda çizilir; toplu çizim Playwright (`tools/slaytlar/ciz.mjs`). Derleyici, framework, Tailwind yok.

## Users

- **Hoca** (dersi veren patolog): kumandayı telefondan kullanır, slaytları düzenleyiciden (bilgisayarda) düzenler; programcı değildir.
- **Öğrenciler** (diş hekimliği 4. sınıf): telefondan karekodla katılır, soruları cevaplar; sınav hedefi DUS ve fakülte sınavı.
- **Perde**: amfide projeksiyon. Sınıf **aydınlık** (ışıklar açık, perde soluk görünür); arka sıradan okunmalı.

## Product Purpose

Ağır patoloji konularını derste akılda kalacak az sayıda maddeye indirmek ve her maddeyi hemen bir soruyla pekiştirmek. Ayrıntı isteğe bağlıdır: sınıf "devam" derse açılır.

## Positioning

Ders kitabının (Neville 5. baskı, WHO 2022) sınıf içi, etkileşimli karşılığı. Kitap gibi güvenilir, ders notu gibi kısa.

## Operating Context

- Blok ders (M3 + M4 arka arkaya, 17 Kasım 2026). Her ders başı: kapak ve katılım, 8 ana madde (her biri slayt + telefondan soru, ~8–9 dk), "Tamam mı, devam mı?" anketi, isteğe bağlı kısaltılmış ayrıntı, çıkış bileti, liderlik.
- Hoca konuşma notlarını kumandada okur; notlardaki zaman damgaları tempo göstergesini besler.
- Ders dışında öğrenciler PowerPoint (internetsiz) ve quiz sayfasını kullanır.

## Capabilities and Constraints

- Slayt kareleri 1920×1080 JPG; canlı ders dosyası biçimi (`canli/dersler/<ID>.json`) derlenmiş paketlerin okuduğu biçimle birebir aynı kalmalı.
- Düzenleyici kurulumsuz çalışır, GitHub'a tek commit ile yazar; tarayıcıda çizilen kare Playwright çıktısıyla aynı olmalı (canvas içeren öğe kullanılamaz, foreignObject ile dışa aktarılır).
- Kitap fotoğrafları repoda (`canli/img/<ID>/`); kitap PDF'leri yok.

## Brand Commitments

- H&E dünyası: hematoksilen moru (yapı, ana eylem), eozin pembesi ("şu an"), kehribar yalnız dikkat (DUS, tempo). Gradyan yok.
- Literata (başlık, soru) + Figtree (geri kalan).
- Dil: Türkçe, mecazsız, klinik ve sakin. Kaynaklar farklıysa açıkça söylenir ("patoloji kaynaklarında böyle geçer; Neville'de doğrulayamadım"). "Resmi slayt" gibi ifadeler kullanılmaz.

## Evidence on Hand

Neville 5. baskı ve Laskaris 4. baskı fotoğrafları (eski slaytlardan kesildi), fakülte ders notu görselleri (`tools/slaytlar/yeni/resmi/`), Neville örnek sınav soruları (quiz).

## Product Principles

1. Akılda kalacak olan önce gelir; ayrıntı sonradan ve isteğe bağlı.
2. Her madde bir soruyla biter; soru klinik vakadır, doğru şık her seferinde başka yerde.
3. Slayt arka sıradan okunur: büyük foto, kısa cümle, tek vurgu.
4. Canlı ders dosyasının biçimi bozulmaz; düzenleyicide yapılan her şey yayına aynı görünür.

## Accessibility & Inclusion

Metin kontrastı ≥4,5:1 (aydınlık amfide perde kontrastı düşer; slayt metni ≥7:1 hedeflenir), renk tek başına anlam taşımaz (doğru/yanlış işaret ve yazıyla), telefon dokunma alanı ≥44 px, `prefers-reduced-motion` desteklenir.
