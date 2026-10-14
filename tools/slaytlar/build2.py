# -*- coding: utf-8 -*-
"""Second content pass on top of build.py: fixes from the review (algorithm, cards, map, dysplasia,
new questions, frame names, promise/teaser/CTA boxes, references)."""
import os, sys, json, copy, re
import numpy as np
from PIL import Image, ImageDraw
import build as B
from build import (S, F, pill, rrect, tw, wrap, cover_rect, redraw_box, rich_line, top_right_tag, bgcolor, is_dark,
                   NAVY, NAVY2, PURPLE, PINK, YELLOW, LILAC, ROSE, WHITE, SOFT, GREY, rep)

GREEN = (23, 116, 78)
RED = (170, 40, 50)
IMG = os.path.join(B.ROOT, "img")

def ctext(d, cx, y, text, font, fill):
    d.text((cx - tw(font, text) / 2, y), text, font=font, fill=fill)

def wrapped_center(d, box, text, font, fill, lh=1.25):
    lines = wrap(font, text, box[2] - box[0] - 24)
    h = len(lines) * font.size * lh
    y = (box[1] + box[3]) / 2 - h / 2
    for ln in lines:
        ctext(d, (box[0] + box[2]) / 2, y, ln, font, fill); y += font.size * lh

def arrow(d, x0, y0, x1, y1, color, w=3, head=10):
    d.line((x0, y0, x1, y1), fill=color, width=w)
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    for s in (2.6, -2.6):
        d.line((x1, y1, x1 - head * math.cos(a + s), y1 - head * math.sin(a + s)), fill=color, width=w)

def text_rows(img, box, dark_thresh=140):
    """Rows (y0,y1) of text inside box, found by scanning for dark pixels on a light bg."""
    a = np.array(img.crop(box).convert("L")).astype(int)
    m = (a < dark_thresh).any(axis=1)
    rows, start = [], None
    for i, v in enumerate(m):
        if v and start is None: start = i
        if not v and start is not None:
            rows.append((box[1] + start, box[1] + i)); start = None
    if start is not None: rows.append((box[1] + start, box[1] + len(m)))
    # merge rows closer than 8px (accents)
    out = []
    for r in rows:
        if out and r[0] - out[-1][1] < 8: out[-1] = (out[-1][0], r[1])
        else: out.append(r)
    return out

# ================= M1 =================
def m1_s1_teaser(img):
    d = ImageDraw.Draw(img)
    rrect(d, (112, 880, 1180, 985), 18, YELLOW)
    d.text((140, 902), "Dört aydır geçmeyen yaralar, iki diş hekimi, tanı yok.", font=F("serif", 40), fill=NAVY)

def m2_s1_teaser(img):
    d = ImageDraw.Draw(img)
    rrect(d, (112, 880, 1215, 985), 18, YELLOW)
    d.text((140, 902), "Altı aydır dilde silinmeyen bir plak, kırk paket-yıl.", font=F("serif", 40), fill=NAVY)

def m1_s4_hide(img):
    """Opening case without the back photo and without Nikolsky: the surprise is kept for the return."""
    d = ImageDraw.Draw(img); bg = bgcolor(img)
    d.rectangle((70, 200, 1010, 570), fill=bg)
    f = F("sans", 30)
    y = 225
    for ln in ["45 yaşında kadın; 4 aydır geçmeyen, çok ağrıyan ağız yaraları",
               "İki ayrı hekim, iki gargara, sonuç yok",
               "Yumuşak damak ve yanakta geniş, sığ erozyonlar",
               "Ağrıdan katı yiyemiyor; 4 kilo vermiş"]:
        for i, sub in enumerate(wrap(f, ln, 880)):
            d.text((86, y), ("•  " if i == 0 else "    ") + sub, font=f, fill=WHITE); y += 44
        y += 14
    d.rectangle((1448, 190, 1850, 590), fill=bg)
    rrect(d, (1459, 200, 1833, 576), 14, NAVY2)
    ctext(d, 1646, 290, "?", F("serif", 150), YELLOW)
    fb = F("bold", 24)
    for i, ln in enumerate(wrap(fb, "Devamı dersin sonunda", 330)):
        ctext(d, 1646, 490 + i * 32, ln, fb, SOFT)

def m1_s4_reveal(img):
    d = ImageDraw.Draw(img)
    for box in [(66, 376, 1004, 428), (66, 488, 1004, 540)]:
        d.rounded_rectangle(box, radius=10, outline=YELLOW, width=4)
    d.rounded_rectangle((1452, 194, 1840, 584), radius=10, outline=YELLOW, width=6)
    d.rectangle((1050, 600, 1850, 900), fill=bgcolor(img))
    rrect(d, (1062, 625, 1833, 890), 18, YELLOW)
    fb = F("serif", 36)
    y = 660
    for ln in wrap(fb, "İki bulgu daha: sırtta kabarcıklar, Nikolsky pozitif. Tahminin değişti mi?", 700):
        d.text((1100, y), ln, font=fb, fill=NAVY); y += 48
    top_right_tag(img, "VAKAYA DÖNÜŞ", PINK, WHITE)

def m1_s6_bridge(img):
    d = ImageDraw.Draw(img); bg = bgcolor(img)
    d.rectangle((70, 55, 1500, 170), fill=bg)
    d.text((86, 72), "3D: her lezyona üç soru", font=F("serif", 60), fill=NAVY)
    pill(d, 1832, 92, "Sırada telefon: iki fotoğraf, bir soru", F("bold", 24), YELLOW, NAVY, right=True, padx=20, pady=9)
    cards = [(86, 639), (672, 1229), (1271, 1826)]
    for (x0, x1), lab in zip(cards, ["1 · DAĞILIM", "2 · DÜZEY", "3 · DESEN"]):
        f = F("black", 26); w = tw(f, lab) + 40
        pill(d, (x0 + x1) / 2 - w / 2, 760, lab, f, PINK, WHITE, padx=20, pady=9)
    rrect(d, (86, 830, 1829, 965), 18, YELLOW)
    fb = F("serif", 34)
    lines = wrap(fb, "Bu üç soruyu sormayı öğrenen, DUS'un büllöz hastalık sorularının çoğunu ezberlemeden çözer.", 1650)
    y = 898 - len(lines) * 22
    for ln in lines:
        ctext(d, 957, y, ln, fb, NAVY); y += 44

def m1_roadmap_tag(img):
    top_right_tag(img, "Yol haritası", YELLOW, NAVY)

def m1_s8_map(img):
    """Liken planus belongs to the lining mucosa (cheek), not the tongue dorsum."""
    d = ImageDraw.Draw(img)
    for box, text in [((1218, 387, 1833, 567), "→ Aft, pemfigus, EM, liken planus"),
                      ((1218, 590, 1833, 724), "→ Coğrafik dil, median rhomboid glossit")]:
        col = img.getpixel((box[2] - 8, box[1] + 8))
        rows = text_rows(img, (box[0] + 20, box[1] + 10, box[2] - 10, box[3] - 8), 200)
        y0, y1 = rows[-1]
        d.rectangle((box[0] + 16, y0 - 4, box[2] - 6, y1 + 6), fill=col)
        d.text((box[0] + 24, y0 - 6), text, font=F("bold", 27), fill=PINK)

def m1_s23_isg(img):
    top_right_tag(img, "ISG 1990 ölçütleri", YELLOW, NAVY)

def m1_s34_promise(img):
    top_right_tag(img, "3D: Dağılım · Düzey · Desen", YELLOW, NAVY)

NEVILLE5 = "Neville BW, Damm DD, Allen CM, Chi AC. Oral and Maxillofacial Pathology. 5. baskı. Elsevier; 2023. (Klinik fotoğraflar)"

def refs_edit(img, neville_row, cta_box):
    d = ImageDraw.Draw(img); bg = bgcolor(img)
    rows = text_rows(img, (110, 200, 1860, 560), 150)
    y0, y1 = rows[neville_row]
    d.rectangle((112, y0 - 6, 1860, y1 + 8), fill=bg)
    f = F("sans", 30)
    d.text((118, y0 - 9), NEVILLE5, font=f, fill=NAVY)
    rrect(d, cta_box, 18, PINK)
    fb = F("serif", 34)
    lines = wrap(fb, "Evde tekrarı 3 Kasım'a kadar bir kez geçin. İlk üçü gelecek derste burada anarım.", cta_box[2] - cta_box[0] - 60)
    y = (cta_box[1] + cta_box[3]) / 2 - len(lines) * 22
    for ln in lines:
        d.text((cta_box[0] + 32, y), ln, font=fb, fill=WHITE); y += 44

def m1_s36_refs(img): refs_edit(img, 2, (86, 600, 1829, 700))
def m2_s39_refs(img): refs_edit(img, 0, (86, 560, 1829, 660))

# ================= M2 =================
def m2_s8_algo(img):
    d = ImageDraw.Draw(img); bg = bgcolor(img)
    d.rectangle((60, 55, 1860, 990), fill=bg)
    d.text((86, 72), "3G: beyaz lezyonda üç soru", font=F("serif", 60), fill=NAVY)
    # red flag first
    rrect(d, (86, 200, 1829, 292), 16, PINK)
    fb = F("bold", 28)
    rich_line(d, 112, 218, [("Önce şuna bak: ", F("black", 28), YELLOW),
                            ("dil kenarı ya da ağız tabanında, kırmızı alanı, sertliği ya da ülseri olan lezyon beklemez, biyopsiye gider.", fb, WHITE)])
    d.text((112, 254), "Gerisi için üç soru:", font=F("sans", 22), fill=ROSE)
    # question row
    xs = [86, 448, 810, 1172, 1534]; w = 292; y0, y1 = 330, 455
    qs = ["Gazlı bezle silinir mi?", "Germekle kaybolur mu?", "Tanınabilir bir tablo mu?",
          "Belirgin neden var mı? Sürtünme, ısırma, protez", "Klinik tanı: lökoplaki"]
    fq = F("bold", 24)
    for i, (x, q) in enumerate(zip(xs, qs)):
        col = PINK if i == 4 else PURPLE
        rrect(d, (x, y0, x + w, y1), 14, col)
        wrapped_center(d, (x, y0, x + w, y1), q, fq, WHITE)
        if i < 4:
            arrow(d, x + w + 6, (y0 + y1) / 2, x + w + 64, (y0 + y1) / 2, RED, 3, 10)
            ctext(d, x + w + 35, y0 + 22, "Hayır", F("bold", 20), RED)
    # yes answers
    ya0, ya1 = 520, 650
    ans = ["Psödomembran: kandida, nekroz, materia alba", "Lökoödem: varyasyon, tedavi yok",
           "Liken planus, süngerimsi nevüs, kıllı lökoplaki, nikotinik stomatit: kendi yolu",
           "Nedeni kaldır, 2–4 hafta izle"]
    fa = F("sans", 23)
    for x, a in zip(xs[:4], ans):
        arrow(d, x + w / 2, y1 + 4, x + w / 2, ya0 - 6, GREEN, 3, 10)
        d.text((x + w / 2 + 10, y1 + 18), "Evet", font=F("bold", 20), fill=GREEN)
        rrect(d, (x, ya0, x + w, ya1), 14, LILAC)
        wrapped_center(d, (x, ya0, x + w, ya1), a, fa, NAVY)
    # biopsy
    bx = (1172, 712, 1829, 800)
    arrow(d, xs[3] + w / 2, ya1 + 4, xs[3] + w / 2, bx[1] - 6, RED, 3, 10)
    d.text((xs[3] + w / 2 + 10, ya1 + 14), "Gerilemedi", font=F("bold", 20), fill=RED)
    arrow(d, xs[4] + w / 2, y1 + 4, xs[4] + w / 2, bx[1] - 6, RED, 3, 10)
    rrect(d, bx, 16, NAVY)
    ctext(d, (bx[0] + bx[2]) / 2, bx[1] + 18, "BİYOPSİ", F("serif", 44), YELLOW)
    rrect(d, (86, 712, 1100, 800), 16, YELLOW)
    d.text((116, 730), "Sırada telefon: yedi lezyon, üç kutu.", font=F("serif", 32), fill=NAVY)
    # frame legend
    rrect(d, (86, 830, 1829, 972), 16, NAVY2)
    rich_line(d, 116, 850, [("3G  ", F("black", 30), YELLOW), ("= Gazlı bezle gider mi?  ·  Gerince geçer mi?  ·  Gerekçesi var mı?", F("bold", 28), WHITE)])
    d.text((116, 900), "Gerekçe: tanınabilir bir tablo ya da belirgin bir neden. İkisi de yoksa buna lökoplaki diyoruz ve biyopsi alıyoruz.", font=F("sans", 24), fill=SOFT)

def m2_s10_cards(img):
    d = ImageDraw.Draw(img); bg = bgcolor(img)
    d.rectangle((70, 640, 1850, 985), fill=bg)
    cards = [(86, 655, 504, 815), (530, 655, 947, 815), (973, 655, 1391, 815), (1417, 655, 1835, 815)]
    content = [("Linea alba", "Oklüzal düzlemde beyaz çizgi; ısırma izi, varyasyon"),
               ("Yanak ısırma (morsicatio)", "Düzensiz, tüy gibi beyaz; alışkanlık, zararsız"),
               ("Fordyce granülleri", "Sarı-beyaz noktalar; ektopik sebase bez"),
               ("Nikotinik stomatit", "Damakta beyaz zemin, kırmızı noktalar; pipo, sıcak içecek")]
    for box, (title, body) in zip(cards, content):
        redraw_box(img, box, LILAC, title, [body], F("serif", 28), F("sans", 23), PURPLE, NAVY, pad=20, gap=4)
    rrect(d, (86, 835, 1835, 972), 16, (236, 228, 243))
    d.text((110, 846), "Fotoğrafsız üç tablo ve bir tuzak", font=F("black", 22), fill=PURPLE)
    cols = [(110, "Lökoödem", "gerince kaybolur; varyasyon", PURPLE),
            (545, "Beyaz süngerimsi nevüs", "kalıtsal (KRT4/13); çocukluktan beri", PURPLE),
            (990, "Tütün kesesi keratozu", "dumansız tütün; bırakınca geriler", PURPLE),
            (1435, "Tuzak", "ters sigara içimi: damakta yüksek risk", PINK)]
    for x, t, b, c in cols:
        d.text((x, 882), t, font=F("serif", 26), fill=c)
        for i, ln in enumerate(wrap(F("sans", 21), b, 380)):
            d.text((x, 918 + i * 26), ln, font=F("sans", 21), fill=NAVY)

def m2_s13_binary(img):
    d = ImageDraw.Draw(img)
    bar = (86, 871, 1829, 972)
    col = img.getpixel((100, 880))
    rrect(d, bar, 14, col)
    fb, fr = F("bold", 24), F("sans", 24)
    rich_line(d, 112, 884, [("Yerleşik sistem üç basamak: ", fb, NAVY), ("hafif · orta · ağır", fb, PURPLE),
                             (";  ağızda karsinoma in situ ağır displaziyle eş anlamlıdır.", fr, NAVY)])
    rich_line(d, 112, 920, [("İki basamaklı sistem (öneri): ", fb, NAVY), ("düşük", fb, PURPLE), (" = hafif, ", fr, NAVY), ("yüksek", fb, PINK),
                             (" = orta + ağır; kriter sayısına bakar, epitelin ne kadarına değil.  Ağır displazi izlenmez, çıkarılır.", fr, NAVY)])
    cols = {"hafif": (369, 627), "orta": (666, 924), "agir": (962, 1220), "cis": (1255, 1513)}
    fl = F("bold", 22)
    yb = 212
    for (x0, x1), lab, c in [((cols["hafif"][0], cols["agir"][1]), "Üç basamak (yerleşik)", PURPLE)]:
        d.line((x0, yb, x1, yb), fill=c, width=3); d.line((x0, yb, x0, yb + 12), fill=c, width=3); d.line((x1, yb, x1, yb + 12), fill=c, width=3)
        ctext(d, (x0 + x1) / 2, yb - 36, lab, fl, c)
    d.text((1255, 836), "= ağır displazi (ağız)", font=F("bold", 20), fill=PINK)

def m2_dysplasia_micro():
    base = Image.open(os.path.join(B.ORIG, "M2", "13.jpg")).convert("RGB")
    bg = bgcolor(base)
    img = Image.new("RGB", (1920, 1080), bg)
    # copy the footer strip from the original deck (title bar + footer look)
    img.paste(base.crop((0, 1000, 1920, 1080)), (0, 1000))
    d = ImageDraw.Draw(img)
    d.rectangle((1700, 1000, 1920, 1080), fill=bg)  # page number cleared; renumber() writes it
    d.text((86, 72), "Mikroskopta displazi: normal epitel ile ağır displazi", font=F("serif", 56), fill=NAVY)
    frames = [((86, 190, 940, 760), "displazi_normal.jpg", "Normal epitel", "Düzenli tabakalanma; bazalde tek sıra, yüzeye doğru olgunlaşma"),
              ((980, 190, 1834, 760), "displazi_agir.jpg", "Ağır displazi", "Atipi epitelin 2/3'ünden fazlasında; polarite kaybı, yüzeye yakın mitoz")]
    for box, fn, cap, sub in frames:
        path = os.path.join(IMG, fn)
        inner = (box[0], box[1], box[2], box[3] - 70)
        if os.path.exists(path):
            ph = Image.open(path).convert("RGB")
            w, h = inner[2] - inner[0], inner[3] - inner[1]
            r = max(w / ph.width, h / ph.height)
            ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1))
            ph = ph.crop(((ph.width - w) // 2, (ph.height - h) // 2, (ph.width - w) // 2 + w, (ph.height - h) // 2 + h))
            img.paste(ph, (inner[0], inner[1]))
        else:
            d.rectangle(inner, fill=(226, 218, 236))
            fp = F("italic", 26)
            for i, ln in enumerate(wrap(fp, "Fotoğraf yeri: kendi arşivinden H&E kesit. Dosya: canli/img/%s (bu slayt yeniden üretilince otomatik yerleşir)." % fn, inner[2] - inner[0] - 80)):
                ctext(d, (inner[0] + inner[2]) / 2, (inner[1] + inner[3]) / 2 - 40 + i * 34, ln, fp, GREY)
        d.rectangle((box[0], box[3] - 70, box[2], box[3]), fill=NAVY)
        d.text((box[0] + 18, box[3] - 62), cap, font=F("bold", 28), fill=WHITE)
        d.text((box[0] + 18, box[3] - 30), sub, font=F("sans", 19), fill=SOFT)
    rrect(d, (86, 790, 1834, 985), 16, NAVY)
    rich_line(d, 116, 806, [("DUS'un sorduğu kriterler", F("black", 26), YELLOW)])
    fb, fr = F("bold", 23), F("sans", 23)
    rich_line(d, 116, 846, [("Mimari: ", fb, YELLOW), ("bazal hücre hiperplazisi · damla biçimli rete · polarite kaybı · düzensiz tabakalanma · yüzeye yakın mitoz · diskeratoz · keratin incileri", fr, WHITE)])
    rich_line(d, 116, 884, [("Sitolojik: ", fb, YELLOW), ("anizonükleoz · nükleer pleomorfizm · hiperkromazi · N/S oranı artışı · atipik mitoz · belirgin nükleol", fr, WHITE)])
    d.text((116, 930), "Ağır: değişiklikler epitelin 2/3'ünü aşar; tam kat tutulum ağızda ağır displazi (= karsinoma in situ). Bazal membran aşıldıysa invaziv karsinom.", font=F("sans", 21), fill=SOFT)
    return img

def m2_s15_pvl(img):
    d = ImageDraw.Draw(img)
    col = img.getpixel((700, 955))
    d.rectangle((696, 760, 1232, 848), fill=col)
    d.text((704, 772), "%40–70", font=F("serif", 54), fill=YELLOW)

def m2_s27_tiroid(img):
    d = ImageDraw.Draw(img); bg = bgcolor(img)
    d.rectangle((1410, 640, 1850, 740), fill=bg)
    f = F("sans", 30)
    for i, ln in enumerate(wrap(f, "~%70'inde tek tiroid dokusu: önce sintigrafi", 418)):
        d.text((1417, 648 + i * 38), ln, font=f, fill=NAVY)

def m2_s37_line2(img):
    d = ImageDraw.Draw(img)
    d.rectangle((195, 400, 1900, 470), fill=NAVY)
    d.text((219, 408), "Silinmeyen, nedeni bulunmayan beyaz plak bekletilmez; tanıyı biyopsi koyar.", font=F("sans", 36), fill=WHITE)


# ================= generated "practical" slides (M1) =================
def _footer_from(lid, n):
    base = Image.open(os.path.join(B.ORIG, lid, "%02d.jpg" % n)).convert("RGB")
    bg = bgcolor(base)
    img = Image.new("RGB", (1920, 1080), bg)
    img.paste(base.crop((0, 1000, 1920, 1080)), (0, 1000))
    ImageDraw.Draw(img).rectangle((1700, 1000, 1920, 1080), fill=bg)
    return img

def photo_frame(img, box, fn, cap, sub=None, dark=False):
    d = ImageDraw.Draw(img)
    path = os.path.join(IMG, fn)
    inner = (box[0], box[1], box[2], box[3] - (72 if sub else 56))
    if os.path.exists(path):
        ph = Image.open(path).convert("RGB")
        w, h = inner[2] - inner[0], inner[3] - inner[1]
        r = max(w / ph.width, h / ph.height)
        ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1))
        ph = ph.crop(((ph.width - w) // 2, (ph.height - h) // 2, (ph.width - w) // 2 + w, (ph.height - h) // 2 + h))
        img.paste(ph, (inner[0], inner[1]))
    else:
        d.rectangle(inner, fill=(226, 218, 236) if not dark else (70, 58, 98))
        fp = F("italic", 24)
        for i, ln in enumerate(wrap(fp, "Fotoğraf yeri: %s. Dosya: canli/img/%s (slayt yeniden üretilince yerleşir)." % (cap, fn), inner[2] - inner[0] - 60)):
            ctext(d, (inner[0] + inner[2]) / 2, (inner[1] + inner[3]) / 2 - 30 + i * 32, ln, fp, GREY if not dark else SOFT)
    d.rectangle((box[0], inner[3], box[2], box[3]), fill=NAVY)
    d.text((box[0] + 18, inner[3] + 10), cap, font=F("bold", 26), fill=WHITE)
    if sub: d.text((box[0] + 18, inner[3] + 42), sub, font=F("sans", 18), fill=SOFT)

def make_cards(title, cards, photo=None, kicker=None, lid="M1"):
    """cards: list of (heading, lines, accent). photo: (file, caption, sub) on the left."""
    def build():
        img = _footer_from(lid, 13)
        d = ImageDraw.Draw(img)
        d.rectangle((880, 1000, 1700, 1080), fill=bgcolor(img))   # no photo credit on generated slides
        d.text((86, 72), title, font=F("serif", 54 if len(title) < 46 else 46), fill=NAVY)
        x0, y0, x1, y1 = 86, 190, 1834, 985
        if photo:
            photo_frame(img, (86, 190, 760, 985), *photo)
            x0 = 800
        if kicker:
            rrect(d, (x0, y0, x1, y0 + 70), 14, YELLOW)
            d.text((x0 + 24, y0 + 18), kicker, font=F("bold", 27), fill=NAVY)
            y0 += 90
        n = len(cards)
        cols = 1 if photo else (n if n <= 3 else 2)
        rows = (n + cols - 1) // cols
        gap = 22
        cw = (x1 - x0 - gap * (cols - 1)) / cols
        fh = F("serif", 34)
        pad = 26
        def layout(size):
            fb = F("sans", size)
            heights = []
            for head, lines, acc in cards:
                h = pad + 50
                for ln in lines:
                    h += len(wrap(fb, ln, cw - 2 * pad - 30)) * size * 1.32 + 8
                heights.append(h + pad - 8)
            return fb, heights
        for size in (31, 29, 27, 25, 23):
            fb, heights = layout(size)
            row_h = [max(heights[r * cols:(r + 1) * cols]) for r in range(rows)]
            if sum(row_h) + gap * (rows - 1) <= y1 - y0: break
        y = y0
        for r in range(rows):
            for c in range(cols):
                i = r * cols + c
                if i >= n: break
                head, lines, acc = cards[i]
                box = (int(x0 + c * (cw + gap)), int(y), int(x0 + c * (cw + gap) + cw), int(y + row_h[r]))
                rrect(d, box, 16, ROSE if acc == "pink" else LILAC)
                yy = box[1] + pad
                d.text((box[0] + pad, yy), head, font=fh, fill=PINK if acc == "pink" else PURPLE); yy += 50
                for ln in lines:
                    for j, sub in enumerate(wrap(fb, ln, cw - 2 * pad - 30)):
                        d.text((box[0] + pad, yy), ("•  " if j == 0 else "    ") + sub, font=fb, fill=NAVY); yy += fb.size * 1.32
                    yy += 8
            y += row_h[r] + gap
        return img
    return build

M1_PRACTICAL = {
 "pemfigus": make_cards("Pemfigus hastası koltukta: diş hekimi için pratik", [
    ("Uzun süre steroid alıyor", ["Adrenal supresyon: stres dozu gerekebilir, hekimine danışın", "Enfeksiyona yatkınlık; kandida sık, ağızda beyaz plağı yanlış okumayın"], ""),
    ("Koltukta", ["Randevular kısa, travma az; Nikolsky pozitif mukozayı çekiştirmeyin", "Dudakları kayganlaştırın; ekartör ve aspiratörü nazik kullanın"], ""),
    ("İyi haber", ["Dişeti lezyonları iyi ağız hijyeniyle belirgin azalır", "Plak kontrolü tedavinin parçasıdır; hastayı sık görün"], "pink")]),
 "mmp": make_cards("Pemfigoid yalnız ağızdaysa: tedavi diş hekimiyle başlar", [
    ("Güçlü topikal steroid", ["Klobetazol %0,05 merhem ya da jel, lezyona günde 2 kez", "Kandida için izleyin; gerekirse antifungal ekleyin"], ""),
    ("Dişeti için esnek plak (tray)", ["Steroidi plağın içine koyup dişetine oturtun: ilaç yerinde kalır", "Günde 2 kez 10–15 dakika"], ""),
    ("Hijyen tedavidir", ["İyi ağız hijyeni steroid ihtiyacını azaltır", "Göz, burun, genital tutulum ya da yaygın hastalıkta sistemik tedavi: dermatoloji ve göz"], "pink")]),
 "sjs": make_cards("Dudakta kanlı kabuk: SJS/TEN ve diş hekimi bağlantısı", [
    ("Trigeminal nevralji sizden geçer", ["Hastayı ilk gören çoğu zaman diş hekimidir; karbamazepini diş hekimi de yazabilir", "En sık tetikleyiciler: antiepileptikler, sülfonamidler, allopurinol"], ""),
    ("İlaçtan sonraki haftalarda", ["Ateş, boğaz ağrısı, göz yanması, dudakta kabuk", "= ilacı kes, hastaneye gönder; saatler önemli"], "pink"),
    ("SJS ve TEN", ["Eritema multiforme'nin ağır kuzenleri; deri soyulması <%10 SJS, >%30 TEN", "Ağız neredeyse her zaman tutulur: ilk belirti dudak ve ağızda olabilir"], "")]),
 "hsv_tx": make_cards("Herpes: tedavi", [
    ("Primer gingivostomatit", ["İlk 72 saatte asiklovir süspansiyon 15 mg/kg (en çok 200 mg/doz), günde 5 kez, 5–7 gün; 'çalkala-yut'", "Ateş ve ağrı: parasetamol/ibuprofen. Çocukta viskoz lidokain (nöbet) ve benzokain (methemoglobinemi) kullanılmaz"], ""),
    ("Herpes labialis", ["Prodromda valasiklovir 2 g, 12 saat sonra 2 g (tek gün); topikal pensiklovir iyileşmeyi yalnızca ~1 gün kısaltır", "Diş işleminin tetiklediği tekrarlarda işlem günü profilaksi"], ""),
    ("Sürekli baskılayıcı tedavi", ["Yılda 6'dan fazla atak, HSV'ye bağlı eritema multiforme, immünsupresyon"], "pink")],
    photo=("zoster_trigeminal.jpg", "Zona (VZV): trigeminal dermatom", "Tek taraflı, orta hatta durur; ağızda da aynı taraf")),
 "hsv_tx2": make_cards("Herpes bulaşır: hasta, hekim ve ekip", [
    ("Aktif uçukta elektif tedavi ertelenir", ["Kabuklanmaya kadar bekleyin: hastayı, ekibi ve aerosolle yayılmayı düşünün", "Acil işlem gerekiyorsa koruyucu ekipman ve lastik örtü"], "pink"),
    ("Herpetik dolama (whitlow)", ["Eldiven öncesi dönemde diş hekimlerinin parmağında meslek hastalığıydı", "Ağrılı, veziküler parmak; apse sanıp açmayın"], ""),
    ("Hastaya söyleyin", ["Dudak lezyonu varken göze dokunmasın; lens takanlar dikkat", "Bebeği öpmesin: neonatal herpes"], "")],
    photo=("herpetik_dolama.jpg", "Herpetik dolama (whitlow)", "Parmakta veziküller; diş hekiminin eski meslek hastalığı")),
 "behcet": make_cards("Behçet hastası diş hekiminde", [
    ("Ağız sağlığı hastalığı etkiler", ["Türk serilerinde (Mumcu ve ark.) kötü ağız sağlığı daha ağır hastalıkla ilişkili bulundu", "Periodontal bakım bir tedavi basamağıdır; hastayı düzenli görün"], ""),
    ("İşlemden sonra alevlenme", ["Diş çekimi ya da periodontal tedavi sonrası ağız ülserlerinde geçici alevlenme bildirildi", "Hastayı önceden uyarın; romatoloğuyla haberleşin (kolşisin, immünsupresyon)"], "pink")]),
 "mukozit": make_cards("Mukozit: kanıta dayalı önleme ve diş hekiminin rolü", [
    ("Önleme (MASCC/ISOO 2020)", ["Ağız bakım protokolü: yumuşak fırça, florlu macun, alkolsüz gargara", "Oral kriyoterapi (buz emme, 30 dk): bolus 5-FU ve yüksek doz melfalan", "Fotobiyomodülasyon (düşük düzeyli lazer): kök hücre nakli ve baş-boyun RT", "Benzidamin gargarası: orta doz (<50 Gy) baş-boyun RT", "Palifermin (KGF-1): tüm vücut ışınlamalı otolog nakil", "Radyoterapide önleme amacıyla klorheksidin önerilmez"], ""),
    ("Diş hekiminin rolü", ["Tedaviden önce enfeksiyon odaklarını temizleyin", "RT alanındaki umutsuz dişler RT'den en az 2 hafta önce çekilir: osteoradyonekroz riski RT sonrası çekimde en yüksek", "Kişiye özel flüor kaşıkları: radyasyon çürüğüne karşı", "Kemoterapide işlemi nötrofil ve trombosit sayısına göre zamanlayın"], "pink")],
    kicker="DSÖ derecesi: 0 yok · 1 ağrı ± eritem · 2 eritem + ülser, katı yiyebilir · 3 ülser, yalnız sıvı · 4 ağızdan beslenemez"),
}


def m2_s7_cannon(img):
    """Left photo on the white/red slide is a white sponge nevus: say so in the caption."""
    d = ImageDraw.Draw(img)
    bar = (86, 648, 695, 718)
    col = img.getpixel((100, 700))
    d.rectangle(bar, fill=col)
    d.text((104, 660), "Beyaz süngerimsi nevüs (Cannon): kalıtsal", font=F("bold", 26), fill=WHITE)

M2_PRACTICAL = {
 "neden": make_cards("Neden beyaz, neden kırmızı? Mekanizmalar", [
    ("Beyaz", ["Kalınlaşmış keratin tükürükle ıslanınca su emer ve opaklaşır: deride nasır, bulaşık suyunda kalan parmak ucu gibi", "Akantoz (kalın epitel) damar rengini örter", "Hücre içi ödem: lökoödem", "Yüzeyde psödomembran: kandida, nekroz", "Damarlanmanın azalması ve fibroz: submüköz fibroz"], ""),
    ("Kırmızı", ["Epitel atrofisi, keratin kaybı", "İltihap ve vazodilatasyon, damar artışı", "Eritroplakide epitel keratin yapamayacak kadar olgunlaşmamış ya da incelmiştir: displazinin kırmızı görünmesinin nedeni budur", "Bu yüzden ağızda kırmızı, beyazdan tehlikelidir"], "pink")], lid="M2"),
 "nikotin": make_cards("Neler neler var: pipo, sıcak çay ve ters sigara", [
    ("Suçlu duman değil, sıcak", ["Nikotinik stomatit: pipo ve sıcak içecek; dumandaki kanserojen değil, ısı yapar", "Damak beyaz zemin, üstünde kırmızı noktalar: iltihaplı küçük tükürük bezi kanal ağızları"], ""),
    ("Bırakınca geçer", ["Sigara ve sıcak bırakılınca geriler; premalign değil", "Çayını çok sıcak içen hastanın damağı korkutmasın; soğutmasını söyleyin"], ""),
    ("Bir de şu var", ["Ters sigara içimi: yanan uç ağzın içinde (Hindistan, Güney Amerika, bizde de rastlanır)", "Bu artık DSÖ 2020 potansiyel malign bozukluklar listesinde: damak lezyonu biyopsiye gider"], "pink")], lid="M2"),
 "kese": make_cards("Dumansız tütün keratozu ve Maraş otu", [
    ("Tütün kesesi keratozu", ["Tütünün tutulduğu vestibülde gri-beyaz, kırışık alan: 'cezir sonrası kum' gibi", "Verrüköz karsinomla ilişkili ('snuff dipper's cancer')"], ""),
    ("Bırakınca ne olur?", ["Yoğun beyaz olmayan lezyonların %98'i iki haftada düzelir", "6 haftada gerilemeyen lezyon gerçek lökoplaki sayılır: biyopsi"], ""),
    ("Yerel not: Maraş otu", ["Kahramanmaraş ve çevresi: Nicotiana rustica + odun külü, alt dudak vestibülünde tutulur", "Kullanıcılarda lökoplaki sık bildirilmiştir; ağız kanseriyle ilişkisi tartışmalı. Dudağı kaldırıp bakın"], "pink")], lid="M2"),
 "petesi": make_cards("Damakta peteşi: üç soru sor", [
    ("Mekanik", ["Öksürük, kusma, ıkınma: ani basınç artışı", "Yumuşak damakta emme travması"], ""),
    ("Enfeksiyöz mononükleoz", ["Sert-yumuşak damak birleşiminde peteşi: güzel bir klinik ipucu", "Boğaz ağrısı, lenfadenopati, halsizlik; EBV; ampisilin verme (döküntü)"], "pink"),
    ("Trombositopeni", ["Bas ve bak: solmayan nokta kanaması; dişeti kanaması, ekimoz", "Tam kan sayımı; lösemi, ITP, ilaç; kanamalı işlemden önce trombosit sayısı"], "")],
    photo=("petesi_damak.jpg", "Damakta peteşi", "Sert-yumuşak damak birleşimi; bas ve bak"), lid="M2"),
 "notropeni": make_cards("Nötropeni ve agranülositoz: metamizol uyarısı", [
    ("Nötropeni", ["ANC < 500/µL ağır nötropeni: iltihap belirtisi az, derin, kirli, nekrotik ülser; ağır periodontit", "Siklik nötropeni (ELANE): ~21 günlük döngüde ateş + aft benzeri ülser"], ""),
    ("Metamizol (Novalgin)", ["Yerel ve kritik: Türkiye'de çok kullanılır, agranülositoz yapabilir", "Metamizol alan hastada ateş, boğaz ağrısı, nekrotik ağız ülseri = acil hemogram", "Diş hekimi bu ilacı hem yazar hem de ilk komplikasyonu görür"], "pink"),
    ("Ortak kural", ["Açıklanamayan dişeti büyümesi, kanama, peteşi ya da iyileşmeyen ülser + halsizlik ya da ateş = hemogram"], "")], lid="M2"),
 "freud": make_cards("Freud'un damağı: 33 ameliyat ve alan kanserizasyonu", [
    ("1923: 'lökoplaki'", ["Freud'un damağındaki lezyona lökoplaki dendi; biyopsi karsinom çıktı", "Yirmi yıl günde 20 puro; damak ve çene kısmen çıkarıldı"], ""),
    ("Diş hekimi Hans Pichler", ["Sonraki 16 yılda onu 33 kez ameliyat etti ve bu protezi yaptı: Freud ona 'canavar' diyordu", "Yeni lezyonlar çıkmaya devam etti"], ""),
    ("Alan kanserizasyonu (Slaughter, 1953)", ["Kanser yalnız lezyonda değil, puroyla yanmış bütün mukozadaydı", "Bugünkü karşılığı: sigara içen hastada tek lezyonu çıkarmak yetmez, bütün ağız izlenir"], "pink")],
    photo=("freud_protez.jpg", "Freud'un obturatör protezi ('canavar')", "Pichler'in yaptığı damak protezi; konuşma ve yemeği zorlaştırıyordu"), lid="M2"),
 "uyari": make_cards("Yazarken üç uyarı", [
    ("Steroid yazmadan önce", ["Kandida ve herpesi dışlayın: herpese steroid, yangına benzin", "Gerekirse önce antifungal/antiviral, sonra steroid"], "pink"),
    ("Tanısız ülsere steroid yazmayın", ["Karsinomu maskeler ve iki hafta kuralını bozar", "Önce tanı, sonra ilaç"], "pink"),
    ("Etkileşim", ["Antifungal (azoller) ve antiviral ilaçları hastanın ilaç listesiyle karşılaştırın", "Statin, varfarin, bazı antiaritmikler ve immünsupresanlar azollerle etkileşir"], "")], lid="M2"),
 "hiv": make_cards("Kıllı lökoplaki gördüm: HIV testi isteyebilir miyim?", [
    ("Evet, ama", ["Hastayı bilgilendirip onamıyla test istenebilir", "Ya da enfeksiyon hastalıklarına yönlendirilir; yönlendirmenin nedenini açıkça söyleyin"], ""),
    ("Neden önemli", ["Ağız bulgusu HIV'in ilk ipucu olabilir: kıllı lökoplaki, tekrarlayan kandida, Kaposi, nekrotizan periodontit", "Bu farkındalık hayat kurtarır; erken tedavi bulaşı da keser"], "pink")], lid="M2"),
 "pj": make_cards("Dudakta çil gibi lekeler: Peutz-Jeghers", [
    ("Görünüm", ["Dudaklarda ve ağız içinde çok sayıda küçük kahverengi makül; çocuklukta başlar", "Otozomal dominant (STK11); dudaktaki lekeler yaşla solabilir, ağız içindekiler kalır"], ""),
    ("Gastroya gönder", ["Bağırsakta hamartomatöz polipler: invajinasyon, kanama; gastrointestinal ve diğer kanser riski yüksek", "Tanıyı koyan ağız olabilir: hastayı gastroenterolojiye yönlendirin, aile taraması"], "pink"),
    ("Ayırıcı", ["Addison: diffüz, yorgunluk, hipotansiyon", "Laugier-Hunziker: dudak ve tırnak, polip yok", "İlaç: hidroksiklorokin, minosiklin, imatinib"], "")],
    photo=("peutz_jeghers.jpg", "Peutz-Jeghers: perioral ve oral maküller", "Dudak, yanak, damak; çocuklukta başlar"), lid="M2"),
}

# ================= plans =================
def find(plan, **k):
    for i, it in enumerate(plan):
        if all(it.get(a) == b for a, b in k.items()): return i
    raise KeyError(k)

M1 = copy.deepcopy(B.M1_PLAN)
M1[find(M1, src=1)]["edits"] = [m1_s1_teaser]
M1[find(M1, src=1)]["dur"] = 150
M1[find(M1, src=1)]["notes"] += " Telefonu olmayan yanındakiyle ikili takım adıyla girebilir, örneğin 'Ayşe&Ali'; puan ikisinin olur."
i4 = find(M1, src=4); M1[i4]["edits"] = [m1_s4_hide]
M1[i4]["notes"] = "Hastamız 45 yaşında bir kadın. Dört aydır ağzındaki yaralar geçmiyor; iki diş hekimi gezmiş, iki gargara almış, sonuç yok. Ağrıdan katı yiyemiyor, dört kilo vermiş. Muayenede yumuşak damakta ve yanakta geniş, sığ erozyonlar var. Hastanın geri kalanına şimdilik bakmıyoruz; vakaya dönünce iki bulgu daha vereceğim. Şıklar şu an telefonlarda açık: fotoğrafa bakıp tahmininizi girin. Cevabı dersin sonunda açacağım; sonraki slaytta dağılımı göreceğiz."
M1[find(M1, src=6)]["edits"] = [m1_s6_bridge]
M1[find(M1, src=7)]["dur"] = 65
M1[find(M1, src=9)]["dur"] = 65
M1[find(M1, src=11)]["dur"] = 80
M1[find(M1, src=8)]["edits"] = [m1_s8_map]
M1.insert(find(M1, src=12) + 1, S(src=12, dur=35, q="W12", key="12Q", strip={2, 3}, title="İki kavanoz: cevap",
                                   notes="Kontrol sorusu: iki parça nereye konur? (Sonuç.) Doğru B: biri formaline, rutin boya için; diğeri Michel solüsyonuna, immünofloresan için. Formaline giren parçada floresan yapılamaz; Michel yoksa serum fizyolojikli gazlı bezle hemen gönderin."))
M1[find(M1, src=16)]["dur"] = 60
M1.insert(find(M1, src=16) + 1, S(src=None, dur=15, top=5, title="Ara liderlik: ilk 5",
                                   notes="On saniye: ilk beş. Takım adıyla girenler de burada. (B ile liderlik tablosu; → ile devam.)"))
M1[find(M1, src=21)]["dur"] = 50
M1[find(M1, src=22)]["dur"] = 90
M1[find(M1, src=23)]["edits"] = [m1_s23_isg]
M1.insert(find(M1, src=24) + 1, S(src=24, dur=35, q="W13", key="24Q", strip={1}, title="İki hafta kuralı: cevap",
                                   notes="Kontrol sorusu: protezi düzelttin, hasta ne zaman biyopsiye gider? (Sonuç.) Doğru B: nedeni kaldırdıktan sonra iki haftada iyileşmeyen ülser biyopsiye gider. 'Hemen' erken, 'altı hafta' geç; karsinom için her hafta önemli."))
M1[find(M1, src=29)].update(title="Biyopsiyi nereden alırsın?", notes="Fotoğrafta pemfigus şüpheli bir erozyon. Biyopsiyi nereden alırsınız? Telefonda fotoğrafa dokunun. (Isı haritası.) Doğru yer lezyonun kenarı: erozyonla sağlam görünen mukozanın sınırı, yani perilezyonel. Ortadan alınan parçada epitel yoktur, yarığın düzeyini göremem; uzaktan alınan parçada yarık yoktur. Kenar, iki kavanoz, hemen.")
M1[find(M1, src=29)]["strip"] = {1, 2, 3}
M1.insert(find(M1, src=30), S(src=4, dur=30, key="4R", edits=[m1_s4_reveal], title="Vakaya dönüş: hastanın geri kalanı",
                               notes="Başta sakladığım iki bulgu: son iki haftada sırtta kolay patlayan kabarcıklar; sağlam görünen mukozaya parmakla bastırıp kaydırınca epitel kayıyor, Nikolsky pozitif. Önce ağız, sonra deri. Şimdi tahmininizi yenileyin; sıradaki slaytta ilk tahminle karşılaştıracağız."))
M1[find(M1, src=31)]["dur"] = 50
M1[find(M1, src=30)]["dur"] = 45
M1[find(M1, src=34)]["edits"] = [m1_s34_promise]
M1[find(M1, src=25)]["dur"] = 45
M1[find(M1, src=33)]["dur"] = 45
M1[find(M1, src=35)]["dur"] = 50
M1[find(M1, src=36)]["edits"] = [m1_s36_refs]
M1[find(M1, src=36)]["dur"] = 30
M1[find(M1, src=36)]["title"] = "Kaynaklar ve evde tekrar"
M1[find(M1, src=6)]["title"] = "3D: her lezyona üç soru"
M1[find(M1, src=7)]["title"] = "1 Dağılım: Nerede?"
M1[find(M1, src=8)]["title"] = "1 Dağılım: mukoza haritası"
M1[find(M1, src=9)]["title"] = "2 Düzey: Hangi düzeyde?"
M1[find(M1, src=10)]["title"] = "2 Düzey: yarık nerede? Bütün konunun anahtarı"
M1[find(M1, src=14)]["title"] = "3 Desen: floresan ne diyor?"

M1_NOTES = dict(B.M1_NOTES)
M1_NOTES.pop(4)   # the opening-case note is rewritten in the plan
M1_NOTES[13] = rep("Ağızda pemfigoid tanısı koyduğunuz hastaların yarısına kadarında gözde de tutulum olabilir", "Ağızdan başlayan hastaların yaklaşık dörtte birinde zamanla göz de tutulur; tüm pemfigoid hastalarında oran daha yüksektir")
M1_NOTES[17] = rep("olguların yaklaşık yüzde 90'ı bir enfeksiyonla ilişkili.", "olguların yaklaşık yüzde 90'ı bir enfeksiyonla ilişkili, ama tetikleyici her zaman bulunamaz.")
M1_NOTES[21] = rep("Toplumun yaklaşık üçte birinde hayatı boyunca aft olur. Yani bu sınıfta en az 20 kişi şu an 'ben' diyor.", "Her beş kişiden birinde hayatı boyunca aft olur. Yani bu sınıfta en az 12 kişi şu an 'ben' diyor.")
M1_NOTES[15] = rep("Diğer şıkları da az önce gördük; her biri başka bir hastalığın adresi.",
                   "Floresan desenlerini birkaç slayt önce gördük; her biri başka bir hastalığın adresi. Bu ara büllöz bloğu kapatıyor; sırada aft.")
M1_NOTES[23] = rep("Uluslararası kriterlere göre tanı için", "1990 ISG ölçütlerine göre tanı için")
_old23 = M1_NOTES[23]
M1_NOTES[23] = lambda s: _old23(s) + " Daha yeni ICBD 2014 puanlamasında ağız ülseri zorunlu değil; sınavda sorulan hâlâ ISG."
M1_NOTES[34] = lambda s: "Dersin başında üç soru demiştim; bu beş cümle onların özeti. " + s
M1_NOTES[36] = lambda s: s + " Evde tekrarı 3 Kasım'a kadar bir kez geçin; ilk üçü gelecek derste burada anarım."


# --- practical slides for the dentist (M1)
M1.insert(find(M1, key="12Q") + 1, S(src=None, make=M1_PRACTICAL["pemfigus"], dur=35, strip={2, 3}, title="Pemfigus hastası koltukta: diş hekimi için pratik",
    notes="Bu hasta size kadar gelecek; üç şeyi aklınızda tutun. Uzun süre steroid alıyor: adrenal supresyon var, stres dozu gerekebilir, hekimine danışın; enfeksiyona yatkın, kandida sık. Koltukta randevu kısa, travma az; Nikolsky pozitif mukozayı çekiştirmeyin, dudakları kayganlaştırın. İyi haber: dişeti lezyonları iyi ağız hijyeniyle belirgin azalır; plak kontrolü tedavinin parçası."))
M1.insert(find(M1, src=13) + 1, S(src=None, make=M1_PRACTICAL["mmp"], dur=30, strip={2, 3}, title="Pemfigoid yalnız ağızdaysa: tedavi diş hekimiyle başlar",
    notes="Yalnız ağız tutulumunda tedavi sizin elinizde: güçlü topikal steroid, klobetazol yüzde 0,05. Dişeti için esnek plak, yani tray: steroidi plağın içine koyup dişetine oturtursunuz, ilaç yerinde kalır. İyi ağız hijyeni steroid ihtiyacını azaltır. Göz ya da yaygın tutulumda sistemik tedavi; dermatoloji ve göz hekimi."))
M1.insert(find(M1, src=17) + 1, S(src=None, make=M1_PRACTICAL["sjs"], dur=35, strip={1}, title="Dudakta kanlı kabuk: SJS/TEN ve diş hekimi bağlantısı",
    notes="Diş hekimi bağlantısı: trigeminal nevraljili hastayı ilk gören çoğu zaman diş hekimidir ve karbamazepini diş hekimi de yazabilir. Başladıktan sonraki haftalarda ateş, boğaz ağrısı, göz yanması, dudakta kabuk görürseniz ilacı kesin, hastaneye gönderin; SJS ve TEN'de saatler önemli. Deri soyulması yüzde 10'un altında SJS, yüzde 30'un üstünde TEN; ağız neredeyse her zaman tutulur."))
M1.insert(find(M1, src=20) + 1, S(src=None, make=M1_PRACTICAL["hsv_tx"], dur=40, strip={1}, title="Herpes: tedavi",
    notes="Tedavi. Primer gingivostomatit: ilk 72 saatte asiklovir süspansiyon, 15 mg/kg, en çok 200 mg/doz, günde 5 kez, 5–7 gün, çalkala-yut. Ateş ve ağrı için parasetamol ya da ibuprofen; çocukta viskoz lidokain nöbet, benzokain methemoglobinemi yapar, kullanmayın. Herpes labialis: prodromda valasiklovir 2 gram, 12 saat sonra 2 gram, tek gün; topikal pensiklovir yalnızca bir gün kazandırır. Diş işleminin tetiklediği tekrarlarda işlem günü profilaksi. Yılda altıdan fazla atak, HSV'ye bağlı eritema multiforme ve immünsupresyonda sürekli baskılayıcı tedavi. Soldaki fotoğraf zona: trigeminal dermatom, tek taraflı, orta hatta durur."))
M1.insert(find(M1, src=20) + 2, S(src=None, make=M1_PRACTICAL["hsv_tx2"], dur=30, strip={1}, title="Herpes bulaşır: hasta, hekim ve ekip",
    notes="Bulaş. Aktif veziküler uçuk varken elektif tedaviyi kabuklanmaya kadar erteleyin: hastayı ve ekibi korumak, aerosolle yayılmayı önlemek için. Eldiven öncesi dönemde diş hekimlerinin parmağında herpetik dolama, whitlow, bir meslek hastalığıydı; fotoğraf solda. Hastaya da söyleyin: göze dokunmasın, bebeği öpmesin."))
M1.insert(find(M1, src=23) + 1, S(src=None, make=M1_PRACTICAL["behcet"], dur=20, strip={1}, title="Behçet hastası diş hekiminde",
    notes="Diş hekimi için: Türk serilerinde, Mumcu ve arkadaşları, kötü ağız sağlığı daha ağır hastalıkla ilişkili bulundu. Diş çekimi ya da periodontal tedavi sonrası ağız ülserlerinde geçici alevlenme bildirildi; hastayı önceden uyarın, romatoloğuyla haberleşin."))
M1.insert(find(M1, src=25) + 1, S(src=None, make=M1_PRACTICAL["mukozit"], dur=45, optional=True, strip={1}, title="Mukozit: kanıta dayalı önleme ve diş hekiminin rolü",
    notes="DSÖ derecelendirmesi üstte; önceki slayttaki tablo bununla uyumlu. Kanıta dayalı önleme, MASCC/ISOO 2020: ağız bakım protokolü; oral kriyoterapi bolus 5-FU ve yüksek doz melfalanda; fotobiyomodülasyon kök hücre nakli ve baş-boyun radyoterapisinde; benzidamin orta doz radyoterapide; palifermin tüm vücut ışınlamalı otolog nakilde; radyoterapide önleme için klorheksidin önerilmez. Diş hekiminin rolü: enfeksiyon odaklarını tedaviden önce temizleyin; radyoterapi alanındaki umutsuz dişleri en az iki hafta önce çekin, osteoradyonekroz riski radyoterapi sonrası çekimde en yüksek; kişiye özel flüor kaşıkları; kemoterapide nötrofil ve trombosit sayısına göre zamanlama."))
# --- time trims to stay at 35:00
for key, dur in [(("src", 1), 120), (("src", 2), 40), (("src", 7), 55), (("src", 9), 55), (("src", 11), 70), (("src", 13), 50), (("src", 22), 75),
                 (("src", 14), 40), (("src", 17), 50), (("key", "18B"), 40), (("src", 20), 40), (("src", 21), 45), (("src", 23), 40), (("src", 16), 50),
                 (("src", 26), 50), (("src", 28), 40), (("src", 30), 40), (("src", 31), 45), (("key", "32B"), 35), (("src", 34), 40), (("src", 35), 45),
                 (("key", "27A"), 20), (("key", "27B"), 30), (("key", "12Q"), 30), (("key", "24Q"), 30), (("src", 33), 30), (("src", 25), 35), (("src", 36), 20)]:
    M1[find(M1, **{key[0]: key[1]})]["dur"] = dur
M1_NOTES[25] = lambda s: s + " DSÖ derecesi: 0 yok; 1 ağrı ve/veya eritem; 2 eritem ve ülser, katı yiyebilir; 3 ülser, yalnız sıvı; 4 ağızdan beslenemez. Tablo bununla uyumlu."

M1_QEDIT = {
    "W3": {"label": "1 Dağılım: Nerede?"},
    "W4": {"label": "2 Düzey: Hangi düzeyde?", "region": {"kind": "rect", "x0": 0, "x1": 1, "y0": 0.40, "y1": 0.60}},
    "W5": {"label": "3 Desen: DUS molası 1/2"},
    "W9": {"__replace__": True, "id": "W9", "type": "FINDIMG", "label": "Biyopsiyi nereden alırsın?", "scored": True,
           "q": "Pemfigus şüpheli erozyon. Biyopsiyi nereden alırsın? Fotoğrafta o noktaya dokun.",
           "img": "img/hn415_0.jpg",
           "answer": "Lezyonun kenarı: erozyon ile sağlam görünen mukozanın sınırı (perilezyonel)",
           "region": {"kind": "ring", "cx": 0.46, "cy": 0.40, "rx": 0.37, "ry": 0.34, "inner": 0.55},
           "exp": "Perilezyonel biyopsi: parça erozyonun kenarından, sağlam görünen mukozayı da içerecek şekilde alınır. Ortada epitel yoktur, yarığın düzeyi görülmez; uzakta yarık yoktur. İki kavanoz: formalin ve Michel."},
}
M1_QADD = [
    {"id": "W12", "type": "MCQ", "label": "İki kavanoz", "scored": True, "a": 1,
     "q": "Pemfigus şüphesiyle perilezyonel biyopsi aldın; iki parça var. Nereye koyarsın?",
     "opts": ["İkisi de formaline", "Biri formaline, biri Michel solüsyonuna (DIF için)", "İkisi de serum fizyolojiğe", "Biri formaline, biri alkole", "Dondurup gönderirim; kavanoz gerekmez"],
     "exp": "Formalin rutin boya (H&E) için; Michel solüsyonu immünofloresan için. Formaline giren parçada floresan yapılamaz. Michel yoksa serum fizyolojikli gazlı bezle hemen gönderilir."},
    {"id": "W13", "type": "MCQ", "label": "İki hafta kuralı", "scored": True, "a": 1,
     "q": "Protez kenarındaki ülser için protezi düzelttin. Hasta ne zaman biyopsiye gider?",
     "opts": ["Hemen, ilk görüşmede", "Nedeni kaldırdıktan sonra iki haftada iyileşmezse", "Altı hafta izledikten sonra", "Yalnızca ağrı artarsa", "Hiçbir zaman; travmatik ülser biyopsi gerektirmez"],
     "exp": "Nedeni kaldırıldığı hâlde iki haftada iyileşmeyen ülser biyopsiye gider: travmatik ülserle karsinom aynı yerde, aynı görünümde olabilir."},
]

M2 = copy.deepcopy(B.M2_PLAN)
M2[find(M2, src=1)]["edits"] = [m2_s1_teaser]
M2[find(M2, src=3)] = S(cloud={"q": "W11", "from": "prev"}, dur=45, title="Geçen dersin çıkış bileti",
                        notes="İlk dersin sonunda en çok kafa karıştıran konuyu sormuştum; en büyük kelime bu. (Buluta bak; en büyük kelimeyi iki cümleyle cevapla, ikinciyi de söyle.) Sonra beyaz lezyonlara geçiyoruz. Önceki oturum bulunamadıysa bu slaytı → ile atla.")
M2[find(M2, src=8)].update(edits=[m2_s8_algo], strip={1, 2, 3})
M2[find(M2, src=9)]["dur"] = 75
M2[find(M2, src=10)].update(edits=[m2_s10_cards], strip={1, 2})
M2[find(M2, src=12)]["strip"] = {3}
M2[find(M2, src=13)].update(edits=[m2_s13_binary], strip={3})
M2.insert(find(M2, src=13) + 1, S(src=None, make=m2_dysplasia_micro, dur=60, dus=True, title="Mikroskopta displazi: normal epitel ile ağır displazi",
                                   notes="Şema yetmez, mikroskop lazım. Solda normal epitel: düzenli tabakalanma, bazalde tek sıra, yüzeye doğru olgunlaşma. Sağda ağır displazi: atipi epitelin üçte ikisini aşmış, polarite kaybolmuş, yüzeye yakın mitoz, hiperkromatik ve pleomorfik çekirdekler. DUS tam bu kriterleri sorar; alttaki iki satırı okuyun. Bazal membran sağlamsa adı hâlâ displazi, aşıldıysa invaziv karsinom."))
M2[find(M2, src=14)].update(dur=75, title="Rapor geldi: ne yaparsın?")
M2[find(M2, src=15)].update(edits=[m2_s15_pvl], strip={3})
M2[find(M2, src=16)]["strip"] = {3}
M2.insert(find(M2, src=18) + 1, S(src=None, dur=15, top=5, title="Ara liderlik: ilk 5",
                                   notes="On saniye: ilk beş. Takım adıyla girenler de burada. (→ ile devam.)"))
M2[find(M2, src=20)]["dur"] = 60
M2[find(M2, src=26)]["dur"] = 75
M2[find(M2, src=27)]["edits"] = [m2_s27_tiroid]
M2[find(M2, src=32)]["dur"] = 90
M2[find(M2, src=33)]["dur"] = 45
M2[find(M2, src=37)]["edits"] = [m2_s37_line2]
M2[find(M2, src=39)]["edits"] = [m2_s39_refs]
M2[find(M2, src=39)]["dur"] = 30
M2[find(M2, src=39)]["title"] = "Kaynaklar ve evde tekrar"
M2[find(M2, src=6)]["title"] = "Açılış vakası: ne yaparsın?"
M2[find(M2, src=8)]["title"] = "3G: beyaz lezyonda üç soru"


# --- M2 additions
M2[find(M2, src=7)].update(edits=[m2_s7_cannon], dur=40)
M2.insert(find(M2, src=7) + 1, S(src=None, make=M2_PRACTICAL["neden"], dur=40, title="Neden beyaz, neden kırmızı? Mekanizmalar",
    notes="Mekanizmayı bir kez anlayın, listeyi ezberlemeyin. Beyaz: kalınlaşmış keratin tükürükle ıslanınca su emer ve opaklaşır; deride nasır, bulaşık suyunda kalan parmak ucu gibi. Akantoz damar rengini örter. Hücre içi ödem lökoödem yapar. Yüzeydeki psödomembran kandida ya da nekrozdur. Damarlanmanın azalması ve fibroz submüköz fibroz. Kırmızı: epitel atrofisi, keratin kaybı, iltihap ve vazodilatasyon, damar artışı. Eritroplakide epitel keratin yapamayacak kadar olgunlaşmamış ya da incelmiştir; displazinin kırmızı görünmesinin nedeni bu."))
M2.insert(find(M2, src=10) + 1, S(src=None, make=M2_PRACTICAL["nikotin"], dur=35, strip={1, 2}, title="Neler neler var: pipo, sıcak çay ve ters sigara",
    notes="Nikotinik stomatitte suçlu duman değil, sıcak: pipo ve sıcak içecek. Damak beyazlaşır, üstündeki kırmızı noktalar iltihaplı küçük tükürük bezi kanal ağızları. Bırakınca geriler, premalign değil; çayını çok sıcak içen hastaya soğutmasını söylemek yeter. Bir de şu var: ters sigara içimi, yanan uç ağzın içinde. O artık DSÖ 2020 potansiyel malign bozukluklar listesinde; damaktaki lezyon biyopsiye gider."))
M2.insert(find(M2, src=10) + 2, S(src=None, make=M2_PRACTICAL["kese"], dur=40, strip={1, 2, 3}, title="Dumansız tütün keratozu ve Maraş otu",
    notes="Tütün kesesi keratozu: tütünün tutulduğu vestibülde gri-beyaz, kırışık, cezir sonrası kum gibi bir alan; verrüköz karsinomla ilişkili. Tütün bırakılınca yoğun beyaz olmayan lezyonların yüzde 98'i iki haftada düzelir; altı haftada gerilemeyen lezyon gerçek lökoplaki sayılır, biyopsi. Yerel not: Kahramanmaraş ve çevresinde Maraş otu, Nicotiana rustica artı odun külü, alt dudak vestibülünde tutulur; kullanıcılarda lökoplaki sık bildirilmiş, ağız kanseriyle ilişkisi tartışmalı. Maraşlı hastanın dudağını kaldırıp bakın."))
M2.insert(find(M2, src=16) + 1, S(src=None, make=M2_PRACTICAL["freud"], dur=35, strip={3}, title="Freud'un damağı: 33 ameliyat ve alan kanserizasyonu",
    notes="Bir hikâye. Freud'un damağındaki lezyona 1923'te lökoplaki dendi; biyopsi karsinom çıktı. Sonraki 16 yılda bir diş hekimi, Hans Pichler, onu 33 kez ameliyat etti ve soldaki protezi yaptı; Freud ona canavar diyordu. Yeni lezyonlar çıkmaya devam etti, çünkü kanser yalnız lezyonda değil, puroyla yanmış bütün mukozadaydı. Slaughter buna 1953'te alan kanserizasyonu adını verdi. Bugünkü karşılığı: sigara içen hastada tek lezyonu çıkarmak yetmez, bütün ağız ömür boyu izlenir."))
M2.insert(find(M2, src=19) + 1, S(src=None, make=M2_PRACTICAL["hiv"], dur=20, title="Kıllı lökoplaki gördüm: HIV testi isteyebilir miyim?",
    notes="Bunu sormazlarsa ben soruyorum: kıllı lökoplaki görürsem HIV testi isteyebilir miyim? Evet: hastayı bilgilendirip onamıyla test istenebilir ya da enfeksiyon hastalıklarına yönlendirilir. Ağız bulgusu HIV'in ilk ipucu olabilir; bu farkındalık hayat kurtarır."))
M2.insert(find(M2, src=23) + 1, S(src=None, make=M2_PRACTICAL["notropeni"], dur=30, title="Nötropeni ve agranülositoz: metamizol uyarısı",
    notes="Nötropeni: ANC 500'ün altı ağır; iltihap belirtisi az, derin, kirli, nekrotik ülser ve ağır periodontit. Siklik nötropeni, ELANE mutasyonu, yaklaşık 21 günlük döngüde ateş ve aft benzeri ülser. Yerel ve kritik not: Türkiye'de çok kullanılan metamizol, Novalgin, agranülositoz yapabilir; metamizol alan hastada ateş, boğaz ağrısı ve nekrotik ağız ülseri acil hemogram demektir. Diş hekimi bu ilacı hem yazar hem de ilk komplikasyonu görür. Ortak kural slayttaki."))
M2.insert(find(M2, src=37), S(src=None, make=M2_PRACTICAL["uyari"], dur=30, title="Yazarken üç uyarı",
    notes="Reçete yazarken üç uyarı. Steroid yazmadan önce kandida ve herpesi dışlayın; herpese steroid, yangına benzin. Tanısız ülsere steroid yazmayın: karsinomu maskeler ve iki hafta kuralını bozar. Antifungal ve antiviral ilaç etkileşimlerini hastanın ilaç listesiyle karşılaştırın; azoller statin, varfarin ve immünsupresanlarla etkileşir."))
M2.insert(find(M2, key="22B") + 1, S(src=None, make=M2_PRACTICAL["petesi"], dur=25, title="Damakta peteşi: üç soru sor",
    notes="Damakta peteşi görünce üç soru. Mekanik mi: öksürük, kusma, ıkınma, yumuşak damakta emme travması (nedenini sözlü anlat). Enfeksiyöz mononükleoz mu: sert-yumuşak damak birleşiminde peteşi güzel bir klinik ipucudur; boğaz ağrısı, lenfadenopati, EBV; ampisilin verilirse döküntü. Trombositopeni mi: bas ve bak, solmaz; dişeti kanaması, ekimoz; tam kan sayımı, lösemi, ITP, ilaç. Kanamalı işlemden önce trombosit sayısı."))
M2.insert(find(M2, key="21B") + 1, S(src=None, make=M2_PRACTICAL["pj"], dur=25, title="Dudakta çil gibi lekeler: Peutz-Jeghers",
    notes="Dudaklarda ve ağız içinde çil gibi çok sayıda kahverengi makül: Peutz-Jeghers. Otozomal dominant, STK11. Bağırsakta hamartomatöz polipler, invajinasyon ve kanser riski. Tanıyı ağızdan koyan siz olabilirsiniz: gastroya gönderin, aileyi taratın. Ayırıcıda Addison, Laugier-Hunziker ve ilaç pigmentasyonu."))
for key, dur in [(("src", 1), 90), (("src", 9), 65), (("src", 14), 65), (("src", 17), 65), (("src", 18), 50), (("src", 20), 50), (("src", 26), 65), (("src", 23), 65),
                 (("src", 32), 75), (("src", 25), 30), (("src", 33), 35), (("src", 34), 40), (("src", 28), 35), (("src", 7), 35), (("src", 10), 55), (("src", 11), 65), (("src", 13), 40), (("src", 15), 55), (("src", 16), 40), (("src", 27), 65), (("src", 37), 40), (("src", 38), 40), (("src", 29), 35), (("src", 30), 60), (("src", 35), 40), (("src", 36), 40), (("src", 39), 20), (("key", "22B"), 35)]:
    M2[find(M2, **{key[0]: key[1]})]["dur"] = dur
M2[find(M2, cloud={"q": "W11", "from": "prev"})]["dur"] = 35
for key, dur in [(("src", 9), 60), (("src", 14), 60), (("src", 23), 55), (("src", 26), 60), (("src", 35), 35), (("src", 36), 35)]:
    M2[find(M2, **{key[0]: key[1]})]["dur"] = dur
M2[[i for i, it in enumerate(M2) if it.get("make") is M2_PRACTICAL["neden"]][0]]["dur"] = 35
M2[[i for i, it in enumerate(M2) if it.get("make") is m2_dysplasia_micro][0]]["dur"] = 50

M2_NOTES = dict(B.M2_NOTES)
_old21b = M2_NOTES["21B"]
M2_NOTES["21B"] = lambda s: _old21b(s).replace("yarısından fazlasında boyun metastazı var ve prognoz kötü", "önemli bir kısmında tanı anında boyun metastazı var; beş yıllık sağkalım yüzde 15–20 civarı")
M2_NOTES[7] = lambda s: s + " Sıradaki slaytta mekanizmaların listesi var."
M2_NOTES[8] = lambda s: "Çerçevemizin adı 3G: gazlı bezle gider mi, gerince geçer mi, gerekçesi var mı? Ama akışa girmeden önce şuna bakın: dil kenarı ya da ağız tabanında yerleşen, kırmızı alanı, sertliği ya da ülseri olan lezyon beklemez, doğrudan biyopsiye gider; açılış hastamız tam bu kutuda. Üçüncü soru da yeni: tanınabilir bir tablo mu? Liken planusun dantelini, süngerimsi nevüsü, kıllı lökoplakiyi tanırsanız lökoplaki demezsiniz. Tütünü nedenler kutusundan çıkardım: sigara içen hastanın plağına 'bırak, bekle' denmez. " + s
M2_NOTES[10] = lambda s: "Üstteki dört fotoğraf ile alttaki dört kart artık aynı tablolar: linea alba, yanak ısırma, Fordyce, nikotinik stomatit. Fotoğrafsız üç tablo ve tuzak alt şeritte. " + s
M2_NOTES[13] = rep("Güncel sınıflama bunları düşük ve yüksek dereceli diye ikiye de ayırıyor. Sizin için pratik karşılığı: rapor 'ağır displazi' diyorsa bu lezyon artık izlenmez, çıkarılır.",
                   "Yerleşik sistem hâlâ üç basamaklı: hafif, orta, ağır; ağızda karsinoma in situ ağır displaziyle eş anlamlı sayılıyor. İki basamaklı sistem bir öneri: düşük dereceli hafif displazi, yüksek dereceli orta ve ağır; epitelin ne kadarının tutulduğuna değil kriter sayısına bakıyor. Sizin için pratik karşılığı: rapor 'ağır displazi' diyorsa bu lezyon artık izlenmez, çıkarılır.")
M2_NOTES[14] = rep("Karsinoma in situ ile ağır displazinin yerini karıştıran çok olur: in situ tam kattır ama bazal membran hâlâ sağlam.",
                   "Rapor geldi, ne yaparsınız? Eşleştirin. (Sonuç.) Hafif displazi: nedeni kaldır, üç ila altı ayda kontrol, büyürse yeniden biyopsi. Ağır displazi ve karsinoma in situ: tam eksizyon. İnvaziv karsinom: baş-boyun cerrahisine sevk. Karsinoma in situ ağızda ağır displaziyle aynı kutuda; bazal membran hâlâ sağlam.")
M2_NOTES[15] = rep("uzun takipte hastaların yaklaşık yüzde 60'ında karsinoma dönüşüyor", "uzun takipte hastaların yüzde 40 ile 70'inde karsinoma dönüşüyor; son meta-analizde yüzde 44")
M2_NOTES[27] = rep("Hastaların dörtte üçünden fazlasında vücuttaki tek çalışan tiroid dokusu.", "Hastaların yaklaşık yüzde 70'inde vücuttaki tek tiroid dokusu.")
M2_NOTES[37] = rep("İki: lökoplaki bir kelime, tanıyı biyopsi koyar.", "İki: silinmeyen, nedeni bulunmayan beyaz plak bekletilmez; lökoplaki bir kelime, tanıyı biyopsi koyar.")
M2_NOTES[38] = lambda s: s.replace("en büyük kelimeyle bir sonraki derse başlayacağım", "en büyük kelimeyi bir sonraki dersin başında cevaplayacağım")
M2_NOTES[39] = lambda s: s + " Evde tekrarı 3 Kasım'a kadar bir kez geçin; ilk üçü gelecek derste burada anarım."

W3_OPTS = ["İki hafta antifungal verip izlerim", "En şüpheli alandan insizyonel biyopsi", "Lazerle buharlaştırırım, biyopsiye gerek yok", "Altı ay sonra kontrole çağırırım", "Fırça sitolojisi yeterli"]
M2_QEDIT = {
    "W3": {"label": "Açılış vakası: ne yaparsın?", "opts": W3_OPTS},
    "W14": {"opts": W3_OPTS},
    "W6": {"__replace__": True, "id": "W6", "type": "MATCH", "label": "Rapor geldi: ne yaparsın?", "scored": True,
           "q": "Biyopsi raporu geldi. Her sonuca uygun yönetimi eşleştir.",
           "left": ["Hafif displazi", "Ağır displazi", "İnvaziv skuamöz hücreli karsinom"],
           "right": ["Tam eksizyon", "Baş-boyun cerrahisine sevk", "İzlem: nedeni kaldır, 3–6 ayda kontrol"],
           "key": ["İzlem: nedeni kaldır, 3–6 ayda kontrol", "Tam eksizyon", "Baş-boyun cerrahisine sevk"],
           "exp": "Hafif displazi izlenir: nedeni kaldır, 3–6 ayda kontrol, büyürse yeniden biyopsi. Ağır displazi ve karsinoma in situ tam eksizyon. İnvaziv karsinom baş-boyun cerrahisine sevk."},
}


# ================= hızlı mod: çekirdek + "zaman kalırsa" bloğu =================
def ident(it):
    if it.get("key"): return it["key"]
    if it.get("make"):
        for d in (M1_PRACTICAL, M2_PRACTICAL):
            for k, v in d.items():
                if v is it["make"]: return "mk:" + k
        return "mk:micro" if it["make"] is m2_dysplasia_micro else "mk:?"
    if it.get("cloud"): return "cloud"
    if it.get("src") is None: return "board5" if it.get("top") else "board"
    return it["src"]

def fastify(plan, core, before_src):
    """core: {ident: dur}. Everything else becomes optional and moves in front of before_src (the five-sentence slide),
    keeping its original order. Items after before_src (closing block) stay where they are."""
    cut = next(i for i, it in enumerate(plan) if it.get("src") == before_src)
    head, tail = plan[:cut], plan[cut:]
    keep, opt = [], []
    for it in head:
        k = ident(it)
        if k in core:
            it["dur"] = core[k]; it.pop("optional", None); keep.append(it)
        else:
            it["optional"] = True; opt.append(it)
    for it in tail:
        k = ident(it)
        if k in core: it["dur"] = core[k]
    plan[:] = keep + opt + tail
    return sum(core.values())

M1_CORE = {1: 90, 2: 40, 4: 45, 5: 45, 6: 30, 7: 55, 8: 45, 9: 55, 10: 40, 11: 55, 12: 45, "12Q": 30, 13: 45, 14: 40,
           "18A": 30, "18B": 35, 15: 45, 16: 45, "board5": 15, 21: 45, 22: 60, 23: 40, 24: 45, "24Q": 30,
           26: 45, 29: 45, "4R": 30, 30: 40, 31: 45, "32A": 20, "32B": 35,
           34: 40, 35: 45, "board": 30, 36: 20}
M2_CORE = {1: 90, "cloud": 35, 4: 45, 6: 45, 7: 35, 8: 45, 9: 60, 19: 45, "mk:hiv": 20, 10: 50, "mk:kese": 35, 11: 60,
           12: 40, 13: 40, 14: 55, 15: 50, 16: 40, "mk:freud": 35, 17: 45, 18: 45, "board5": 15, 20: 50, "21A": 20, "21B": 35,
           "22A": 20, "22B": 35, 23: 40, 25: 30, 26: 55, 27: 40, 32: 45, 33: 35, 34: 40,
           37: 40, 38: 40, "board": 30, 39: 20}

if __name__ == "__main__":
    import shutil
    if os.path.exists(B.OUT): shutil.rmtree(B.OUT)
    print("M1 çekirdek", B.ts(fastify(M1, M1_CORE, 34)), "· M2 çekirdek", B.ts(fastify(M2, M2_CORE, 37)))
    B.build_lesson("M1", M1, qdrop={"W7"}, qedit=M1_QEDIT, note_edit=M1_NOTES, qadd=M1_QADD,
                   strip_cfg=(("1 Dağılım", "2 Düzey", "3 Desen"), "3D"),
                   cta="Evde tekrarı 3 Kasım'a kadar bir kez geçin. İlk üçü gelecek derste burada anarım.", frame="3D: Dağılım, Düzey, Desen")
    B.build_lesson("M2", M2, qdrop={"W1", "W2", "W10", "W12"}, qedit=M2_QEDIT, note_edit=M2_NOTES,
                   strip_cfg=(("1 Gider mi", "2 Geçer mi", "3 Gerekçe"), "3G"),
                   cta="Evde tekrarı 3 Kasım'a kadar bir kez geçin. İlk üçü gelecek derste burada anarım.", frame="3G: Gazlı bezle gider mi, gerince geçer mi, gerekçesi var mı?")
    idx = json.load(open(os.path.join(B.ORIG_JSON, "index.json"), encoding="utf-8"))
    for e in idx:
        L = json.load(open(os.path.join(B.ROOT, "dersler", e["id"] + ".json"), encoding="utf-8")); e["n"] = len(L["questions"])
    json.dump(idx, open(os.path.join(B.ROOT, "dersler", "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
