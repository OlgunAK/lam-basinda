# Diyagramlar

Bu klasördeki her `.html` dosyası tek başına açılır: çift tıkla, tarayıcıda görünür.
Dış bağımlılığı yok (yalnız Google Fonts). Kaynağı SVG, yani PNG'ye de SVG'ye de dışa aktarılır.

## Dosya adları

| Dosya | Ne anlatır | Tip |
|---|---|---|
| `mimari.html` | Sistemin tek karede hâli: bileşenler ve aralarındaki bağlantı | Architecture |
| `akis-<konu>.html` | Bir kararın dallanması (ör. `akis-giris.html`) | Flowchart |
| `sira-<konu>.html` | Zaman sıralı mesajlaşma (ör. `sira-oturum.html`) | Sequence |
| `durum-<konu>.html` | Bir nesnenin durumları ve geçişleri | State machine |
| `veri-<konu>.html` | Kim hangi adımda hangi veriye dokunur | Data flow |

Kullanılmayan dosya tutma: yanlış diyagram, olmayan diyagramdan kötüdür.

## Stil

`stil-profili.md` bu deponun stil kılavuzudur. Diyagram üreten her oturum önce onu okur.
Renk, yazı ve kutu kuralları oradan gelir; HTML içine ham renk yazılır ama değerler o dosyadan alınır.

## Üretmek / güncellemek

Claude Code'a düz cümleyle söyle:

- "docs/diagrams/mimari.html'i güncelle, Firestore'a `sonuc` koleksiyonu eklendi"
- "quiz akışının sequence diyagramını çıkar, docs/diagrams/sira-quiz.html"

Araç kurulumu ve bulut oturumu için: kök `CLAUDE.md` içindeki "Diyagramlar" bölümü.

## Doğrulama

```bash
cd /tmp/dd/skills/diagram-design
python3 scripts/self_check.py <dosya>        # erişilebilirlik, tek dosya, viewBox taşması
python3 scripts/verify_geometry.py <dosya>   # ok kuralları: çapraz yok, maske çakışması yok
```

İkisi de sessizce geçmeli.
