<!-- diagram-design-profile
name: Olgun · H&E
slug: olgun-he
source-url: https://github.com/OlgunAK/lam-basinda/blob/main/DESIGN.md
created: 2026-11-25
updated: 2026-11-25
notes: H&E paleti; ortak/tasarim.css token'larindan türetildi
-->
# Style Guide

**Tek doğruluk kaynağı: renk, tipografi, token.** Her diyagram buradan okunur.

Bu profil `lam-basinda/ortak/tasarim.css` ve `DESIGN.md` dosyalarından türetildi: hematoksilen–eozin paleti, Literata + Figtree.

---

## Tokens

### Semantic roles

| Role | Purpose | Light | Dark |
|---|---|---|---|
| `paper` | Sayfa zemini, varsayılan düğüm dolgusu | `#faf7fb` (lam camı) | `#160f21` (gece) |
| `paper-2` | Diyagram kabı, ikincil dolgu | `#f1ecf6` | `#2d2243` |
| `ink` | Ana yazı, ana çizgi | `#22163a` (hema-900) | `#f3edf8` (night-50) |
| `ink-strong` | Dolu accent üstündeki yazı | `#ffffff` | `#160f21` |
| `muted` | İkincil yazı, varsayılan ok | `#5e5070` (glass-600) | `#afa1c2` (night-300) |
| `soft` | Alt etiket, bölge etiketi | `#6e5f84` (night-500) | `#8f80a3` (glass-400) |
| `rule` | Saç teli kenar | `rgba(34,22,58,0.12)` | `rgba(243,237,248,0.12)` |
| `rule-solid` | Güçlü kenar, taban çizgisi | `#8f80a3` | `#6e5f84` |
| `accent` | Odak / diyagram başına 1–2 | `#b0275b` (eozin-700) | `#f283aa` (eozin-300) |
| `accent-tint` | Accent kenarlı kutunun dolgusu | `rgba(176,39,91,0.08)` | `rgba(242,131,170,0.10)` |
| `link` | HTTP/API çağrısı, dış ok | `#4a2c82` (hema-700) | `#bba3f0` (hema-300) |

**Rol eşlemesi (neden böyle).** `DESIGN.md`'de eozin "şu an"ı, hematoksilen yapıyı ve ana eylemi taşır. Diyagramda odak = o anda bakılan şey olduğu için `accent` eozin; bağlantı/çağrı çizgileri hematoksilen (`link`). Kehribar (`#f2b705`) diyagramlarda kullanılmaz: tek accent kuralı var ve kehribar sitede yalnız "dikkat" içindir.

### Contrast contract

Ölçülen oranlar (WCAG 2.x, kendi zemininde):

| Token | Light | Dark | Eşik |
|---|---|---|---|
| `ink` | 15,89:1 | 16,26:1 | 4,5 |
| `muted` | 6,92:1 | 7,74:1 | 4,5 |
| `soft` | 5,44:1 | 5,14:1 | 4,5 |
| `accent` | 6,01:1 | 7,65:1 | 4,5 |
| `link` | 10,01:1 | 8,55:1 | 4,5 |
| `rule-solid` | 3,42:1 | 3,23:1 | 3 |
| `ink-strong` dolu accent üstünde | 6,39:1 | — | 4,5 |

Hepsi geçiyor. Bu sayılar `DESIGN.md`'nin ölçtüğü değerlerle (15,9 · 6,9 · 6,0 · 6,4) birebir uyuşuyor.

### Inversion rule (light → dark)

`rgba(34,22,58,X)` → `rgba(243,237,248,X)`. Opaklık aynı, RGB ters. Accent koyu temada eozin-300'e açılır.

### Series palette (yalnız çok serili grafikler)

| Token | Light | Dark |
|---|---|---|
| `series-1` | `#4a3d60` | `#afa1c2` |
| `series-2` | `#5e7a9b` | `#82a0c0` |
| `series-3` | `#17744e` | `#5fcb97` |
| `series-4` | `#a8302b` | `#f47d74` |
| `series-5` | `#8f80a3` | `#6e5f84` |

Dolgu açıkta `0.18`, koyuda `0.22` opaklıkta; çizgi tam renk. Accent odak seriye saklı.

### Terminal skin

Kullanılmaz. Bu profil markalı çıktı içindir.

---

## Typography

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | Literata | 1.75rem | 650 | Sayfa H1 |
| `node-name` | Figtree | 12px | 600 | Düğüm adı |
| `sublabel` | Figtree | 9px | 500 | Alt etiket, teknik değer (`tabular-nums` rakamda) |
| `eyebrow` | Figtree | 8px | 600, aralık 0.14em, BÜYÜK | Bölge ve tip etiketi |
| `arrow-label` | Figtree | 8px | 600, aralık 0.08em, BÜYÜK | Ok etiketi |
| `callout` | Literata *italik* | 14px | 400 | Yalnız editoryal not |

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,650&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```
--font-serif: "Literata", Georgia, "Times New Roman", serif;
--font-sans:  "Figtree", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
```

### Font source

Font source: `web`

`system` istenirse `<link>` düşer, yığınlar olduğu gibi kalır (her biri genel bir aile ile bitiyor).

### Bilinçli sapma: mono yazı yok

Varsayılan Diagram Design iskeleti alt etiket, eyebrow ve ok etiketini **mono** yazar. `DESIGN.md` mono'yu yasaklıyor ("Eşaralıklı (mono) yazı yok; oturum kodu da Figtree, geniş aralıklı ve tabular"). Bu profilde o üç rol **Figtree 500/600**, büyük harf ve aralıklı. Teknik değer ile adı ayıran şey ailenin değişmesi değil, boyut ve ağırlık: ad 12px/600, teknik değer 9px/500 `soft` renkte.

Genişlik bütçesi: dar karakter 0.56em (Figtree), tam genişlikli karakter 1em. Türkçe harfler (ğ ş ı İ ö ü ç) dar sayılır. Kutu genişliğini 4'ün katına yuvarla.

---

## Stroke, radius, spacing

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | `0.8` | Tip kutusu, yaprak düğüm |
| `stroke-default` | `1` | Çoğu çizgi |
| `stroke-strong` | `1.2` | Vurgu |
| `radius-sm` | `4` | Küçük etiket |
| `radius-md` | `8` | Düğüm kutusu (`DESIGN.md` kontrol köşesi 12 → SVG'de 8) |
| `radius-lg` | `12` | Kap, halka |
| `grid` | `4` | Her koordinat, ölçü ve boşluk 4'e bölünür (katı kural) |

Boşluk adımları: 4 · 8 · 12 · 16 · 24 · 32 · 48 (`DESIGN.md` ile aynı).

---

## Node type → treatment

| Type | Fill | Stroke |
|---|---|---|
| `focal` (1–2 max) | `accent-tint` | `accent` |
| `backend` | `#ffffff` | `ink` |
| `store` | `ink @ 0.05` | `muted` |
| `external` | `ink @ 0.03` | `ink @ 0.30` |
| `input` | `muted @ 0.10` | `soft` |
| `optional` | `ink @ 0.02` | `ink @ 0.20` kesik `4,3` |
| `security` | `accent @ 0.05` | `accent @ 0.50` kesik `4,4` |

---

## Yasaklar (DESIGN.md'den devralınan)

- Gölge yok. Kenar çizgisi var.
- Başlığın üstünde eyebrow yok (sayfa başlığı için; SVG içindeki bölge etiketleri bu kuralın dışında).
- Kartta/kutuda 1px'ten kalın renkli sol kenar çizgisi yok.
- Emoji ya da ok karakteri ikon değil; ikon tek çizgi kalınlığında SVG.
- Gradyan yazı, süs bulanıklığı, `transition: all` yok.
- İki accent yok. Markanın 5 rengi varsa diyagramda 3'ü kullanılır.
