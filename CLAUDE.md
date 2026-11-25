
## Diyagramlar

Bu deponun mimari çizimleri `docs/diagrams/` altında, tek dosyalık HTML+SVG olarak durur.
Üreten araç: [diagram-design](https://github.com/cathrynlavery/diagram-design) (Agent Skill).

**Stil:** `docs/diagrams/stil-profili.md` bu deponun stil kılavuzudur (H&E paleti, Literata + Figtree).
Diyagram çizmeden önce onu oku; varsayılan tema (turuncu accent, Geist/Instrument Serif) kullanma.
Kök dizindeki `.diagram-design` dosyası aynı profili yerel kurulum için adlandırır (`olgun-he`).

**Skill yoksa** (bulut oturumu, `/plugin` kurulumu yok):

```bash
git clone --depth 1 https://github.com/cathrynlavery/diagram-design.git /tmp/dd
```

Sonra `/tmp/dd/skills/diagram-design/SKILL.md` ile ilgili `references/type-*.md` dosyasını oku,
`assets/template.html` ya da `assets/example-<tip>.html` dosyasını iskelet al, `stil-profili.md`
token'larıyla çiz. Bitince doğrula:

```bash
cd /tmp/dd/skills/diagram-design && python3 scripts/self_check.py <dosya> && python3 scripts/verify_geometry.py <dosya>
```

**Ne zaman güncellenir:** mimariyi değiştiren bir iş yaptıysan (yeni servis, yeni koleksiyon,
yeni rol, akış değişikliği) ilgili diyagramı aynı PR'da güncelle. Diyagram yanlışsa yokmuş gibi davran.

**Kural:** diyagram tek dosya kalır; dış görsel, dış JS yok. Düğüm sayısı 9'u geçerse ikiye böl
(genel bakış + ayrıntı). Accent (eozin) diyagram başına en çok 2 öğede.
