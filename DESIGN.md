# Lam Başında · Tasarım

Bu dosya sitenin ve yeni slaytların (M3, M4 ve düzenleyiciyle yapılan her ders) görsel kurallarıdır. Token'lar `ortak/tasarim.css` içinde; slaytlar aynı değerleri `ortak/slayt.js` içinde kullanır.

## Dünya

Ad "lam başında": mikroskop lamı ve H&E boyası. Renkler boyadan gelir ve her biri tek bir iş yapar:

| Rol | Açık | Koyu | Ne için |
|---|---|---|---|
| `--c-accent` (hematoksilen) | `#4A2C82` | `#BBA3F0` | Ana eylem, seçim, yapı. Bir ekranda tek dolu düğme. |
| `--c-now` (eozin) | `#B0275B` | `#F283AA` | "Şu an": açık soru, slaytta o anki adım, canlı durum. |
| `--c-attn` (kehribar) | `#F2B705` | aynı | Yalnız dikkat: DUS etiketi, tempo uyarısı. Üstüne her zaman koyu yazı. |
| `--c-ok` / `--c-bad` | yeşil / kırmızı | | Doğru/yanlış, bağlantı var/yok. Hep yanında bir işaret ya da yazı. |
| Zemin | lam camı `#FAF7FB` | gece `#160F21` | Açık tema gündüz telefon ve web; koyu tema kumanda ve perde (karanlık sınıf). |

Ölçülen kontrastlar: metin/zemin 15,9:1; ikincil metin 6,9:1; eozin/zemin 6,0:1; beyaz/eozin 6,4:1; koyu temada ikincil metin 7,7:1. Girdi kenarları ≥3:1.

## Yazı

- **Literata** (kitap yüzü, ders kitabını hatırlatır): başlıklar, soru metni, slayt başlıkları. 650 ağırlık, `-0.01em`.
- **Figtree**: geri kalan her şey. Rakamlar değişiyorsa `tabular-nums`.
- Eşaralıklı (mono) yazı yok; oturum kodu da Figtree, geniş aralıklı ve tabular.
- Ölçek (rem): 0,8125 · 0,875 · 1 · 1,125 · 1,375 · 1,75 · 2,5. Gövde 1,5 satır aralığı, başlık 1,2.
- Slaytta (1920×1080): başlık 60 px, madde 34 px, açıklama 22 px, en küçük yazı 18 px.

## Düzen

- Boşluk adımları 4 · 8 · 12 · 16 · 24 · 32 · 48. Grup içi aralığın en az iki katı gruplar arası.
- Köşe: kontrol 12, kart 16, hap 999. İç içe yüzeyde dış köşe = iç köşe + iç boşluk.
- Dokunma alanı en az 44 px.
- Telefon önce: tek sütun, 16 px kenar boşluğu.

## Yasaklar (skill kuralları)

- Başlığın üstünde küçük büyük harfli etiket (eyebrow) yok; tarih ve sayı başlığın altında, sakin satırda.
- Kartlarda, maddelerde, kutularda 1 px'ten kalın renkli sol kenar çizgisi yok. Vurgu zemin tonuyla.
- Emoji ya da ok karakteri ikon olarak kullanılmaz; ikonlar tek çizgi kalınlığında SVG.
- Gradyan yazı, süs amaçlı bulanıklık, `transition: all` yok.
- Görsel kenarı: `1px` siyah/beyaz %10 iç çizgi.

## Hareket

- Durum değişimi 150 ms `ease-out`; basılan düğme `0.96` ölçek, devre dışı düğme ölçeklenmez.
- `prefers-reduced-motion` açıksa hareket yok.

## Slaytlar

- Açık tema içerik, koyu tema soru ve vaka.
- Adım adım slayt: geçmiş maddeler soluk, o anki madde eozin tonlu zeminde ve kalın, gelecek maddeler yer tutar ama görünmez. Görsel solda, altyazısı görselin altında (üstüne binmez).
- Alt şerit: ders adı, çerçevenin grupları (o anki grup hematoksilen dolu), sayfa numarası, kaynak.
- Soru slaytı: üstte "Telefonda açık" hapı (eozin nokta), soru Literata, şıklar mor harf dairesiyle.
