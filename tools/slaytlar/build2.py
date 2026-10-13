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
    d.text((140, 902), "Açılış vakası: 4 ay, 2 diş hekimi, tanı yok.", font=F("serif", 40), fill=NAVY)

def m2_s1_teaser(img):
    d = ImageDraw.Draw(img)
    rrect(d, (112, 880, 1215, 985), 18, YELLOW)
    d.text((140, 902), "Açılış vakası: 6 ay, dil kenarında plak, 40 paket-yıl.", font=F("serif", 40), fill=NAVY)

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
    for i, ln in enumerate(wrap(fb, "Hastanın geri kalanı: vakaya dönüşte", 330)):
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
    for ln in wrap(fb, "Vakaya dönüş: iki yeni bulgu. Sırtta kabarcıklar ve Nikolsky pozitif. Şimdi tahminini yenile.", 700):
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
    lines = wrap(fb, "Söz: bu üç soruyu soran öğrenci, DUS'taki büllöz hastalık sorularının çoğunu ezberlemeden çözer.", 1650)
    y = 898 - len(lines) * 22
    for ln in lines:
        ctext(d, 957, y, ln, fb, NAVY); y += 44

def m1_roadmap_tag(img):
    top_right_tag(img, "YOL HARİTASI · SONDA DOLACAK", YELLOW, NAVY)

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
    top_right_tag(img, "SÖZ VERMİŞTİM: 3D, DUS'U ÇÖZER", YELLOW, NAVY)

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
    lines = wrap(fb, "Ödev: evde tekrarı 3 Kasım'a kadar bitir. İlk üç isim bir sonraki derste perdede.", cta_box[2] - cta_box[0] - 60)
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
    rich_line(d, 112, 218, [("Önce kırmızı bayrak: ", F("black", 28), YELLOW),
                            ("dil kenarı ya da ağız tabanı, kırmızı alan, sertlik ya da ülser → beklemeden biyopsi.", fb, WHITE)])
    d.text((112, 254), "Bu lezyon aşağıdaki akışa girmez.", font=F("sans", 22), fill=ROSE)
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
    d.text((116, 900), "Gerekçe: tanınabilir bir tablo ya da belirgin bir neden. İkisi de yoksa adı lökoplaki, yolu biyopsi.", font=F("sans", 24), fill=SOFT)

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
M1.insert(find(M1, src=6) + 1, S(src=32, dur=20, strip={1, 2, 3}, key="32R", edits=[B.m1_s32_A, m1_roadmap_tag],
                                 title="Yol haritası: ülserde zaman ve sayı (sonda dolacak)",
                                 notes="Yol haritamız bu tablo. Ülser gören hekim iki soru sorar: ne zamandır ve kaç tane? Dört kolon şimdilik boş; dersin sonunda bugünkü hastalıkları buraya yerleştireceğiz. Üç soru (3D) her kolonun içinde çalışır."))
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
                               notes="Söz verdiğim iki bulgu: son iki haftada sırtta kolay patlayan kabarcıklar; sağlam görünen mukozaya parmakla bastırıp kaydırınca epitel kayıyor, Nikolsky pozitif. Önce ağız, sonra deri. Şimdi tahmininizi yenileyin; sıradaki slaytta ilk tahminle karşılaştıracağız."))
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
M1_NOTES[15] = rep("Diğer şıkları da az önce gördük; her biri başka bir hastalığın adresi.",
                   "Floresan desenlerini birkaç slayt önce gördük; her biri başka bir hastalığın adresi. Bu ara büllöz bloğu kapatıyor; sırada aft.")
M1_NOTES[23] = rep("Uluslararası kriterlere göre tanı için", "1990 ISG ölçütlerine göre tanı için")
_old23 = M1_NOTES[23]
M1_NOTES[23] = lambda s: _old23(s) + " Daha yeni ICBD 2014 puanlamasında ağız ülseri zorunlu değil; sınavda sorulan hâlâ ISG."
M1_NOTES[34] = lambda s: "Söz vermiştim: üç soru, yani 3D, DUS'un büllöz sorularını çözer; beş cümle bunun özeti. " + s
M1_NOTES[36] = lambda s: s + " Ödev: evde tekrar modülünü 3 Kasım'a kadar bitirin; ilk üç ismi bir sonraki derste perdede göstereceğim."
M1_NOTES["32B"] = lambda s: B.M1_NOTES["32B"](s).replace("Şimdi hastalıkları yerleştirelim. ", "Dersin başındaki boş tabloya döndük; şimdi hastalıkları yerleştirelim. ")

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
                        notes="Söz vermiştim: ilk dersin çıkış biletindeki en büyük kelime bu. (Buluta bak; en büyük kelimeyi iki cümleyle cevapla, ikinciyi de söyle.) Sonra beyaz lezyonlara geçiyoruz. Önceki oturum bulunamadıysa bu slaytı → ile atla.")
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

M2_NOTES = dict(B.M2_NOTES)
M2_NOTES[8] = lambda s: "Çerçevemizin adı 3G: gazlı bezle gider mi, gerince geçer mi, gerekçesi var mı? Ama akışa girmeden önce kırmızı bayrak: dil kenarı ya da ağız tabanında yerleşen, kırmızı alanı, sertliği ya da ülseri olan lezyon beklemez, doğrudan biyopsiye gider; açılış hastamız tam bu kutuda. Üçüncü soru da yeni: tanınabilir bir tablo mu? Liken planusun dantelini, süngerimsi nevüsü, kıllı lökoplakiyi tanırsanız lökoplaki demezsiniz. Tütünü nedenler kutusundan çıkardım: sigara içen hastanın plağına 'bırak, bekle' denmez. " + s
M2_NOTES[10] = lambda s: "Üstteki dört fotoğraf ile alttaki dört kart artık aynı tablolar: linea alba, yanak ısırma, Fordyce, nikotinik stomatit. Fotoğrafsız üç tablo ve tuzak alt şeritte. " + s
M2_NOTES[13] = rep("Güncel sınıflama bunları düşük ve yüksek dereceli diye ikiye de ayırıyor. Sizin için pratik karşılığı: rapor 'ağır displazi' diyorsa bu lezyon artık izlenmez, çıkarılır.",
                   "Yerleşik sistem hâlâ üç basamaklı: hafif, orta, ağır; ağızda karsinoma in situ ağır displaziyle eş anlamlı sayılıyor. İki basamaklı sistem bir öneri: düşük dereceli hafif displazi, yüksek dereceli orta ve ağır; epitelin ne kadarının tutulduğuna değil kriter sayısına bakıyor. Sizin için pratik karşılığı: rapor 'ağır displazi' diyorsa bu lezyon artık izlenmez, çıkarılır.")
M2_NOTES[14] = rep("Karsinoma in situ ile ağır displazinin yerini karıştıran çok olur: in situ tam kattır ama bazal membran hâlâ sağlam.",
                   "Rapor geldi, ne yaparsınız? Eşleştirin. (Sonuç.) Hafif displazi: nedeni kaldır, üç ila altı ayda kontrol, büyürse yeniden biyopsi. Ağır displazi ve karsinoma in situ: tam eksizyon. İnvaziv karsinom: baş-boyun cerrahisine sevk. Karsinoma in situ ağızda ağır displaziyle aynı kutuda; bazal membran hâlâ sağlam.")
M2_NOTES[15] = rep("uzun takipte hastaların yaklaşık yüzde 60'ında karsinoma dönüşüyor", "uzun takipte hastaların yüzde 40 ile 70'inde karsinoma dönüşüyor; son meta-analizde yüzde 44")
M2_NOTES[27] = rep("Hastaların dörtte üçünden fazlasında vücuttaki tek çalışan tiroid dokusu.", "Hastaların yaklaşık yüzde 70'inde vücuttaki tek tiroid dokusu.")
M2_NOTES[37] = rep("İki: lökoplaki bir kelime, tanıyı biyopsi koyar.", "İki: silinmeyen, nedeni bulunmayan beyaz plak bekletilmez; lökoplaki bir kelime, tanıyı biyopsi koyar.")
M2_NOTES[38] = lambda s: s.replace("en büyük kelimeyle bir sonraki derse başlayacağım", "en büyük kelimeyi bir sonraki dersin başında cevaplayacağım")
M2_NOTES[39] = lambda s: s + " Ödev: evde tekrar modülünü 3 Kasım'a kadar bitirin; ilk üç ismi bir sonraki derste perdede göstereceğim."

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

if __name__ == "__main__":
    import shutil
    if os.path.exists(B.OUT): shutil.rmtree(B.OUT)
    B.build_lesson("M1", M1, qdrop={"W7"}, qedit=M1_QEDIT, note_edit=M1_NOTES, qadd=M1_QADD,
                   strip_cfg=(("1 Dağılım", "2 Düzey", "3 Desen"), "3D"),
                   cta="Evde tekrarı 3 Kasım'a kadar bitir; ilk üç isim bir sonraki derste perdede.", frame="3D: Dağılım, Düzey, Desen")
    B.build_lesson("M2", M2, qdrop={"W1", "W2", "W10", "W12"}, qedit=M2_QEDIT, note_edit=M2_NOTES,
                   strip_cfg=(("1 Gider mi", "2 Geçer mi", "3 Gerekçe"), "3G"),
                   cta="Evde tekrarı 3 Kasım'a kadar bitir; ilk üç isim bir sonraki derste perdede.", frame="3G: Gazlı bezle gider mi, gerince geçer mi, gerekçesi var mı?")
    idx = json.load(open(os.path.join(B.ORIG_JSON, "index.json"), encoding="utf-8"))
    for e in idx:
        L = json.load(open(os.path.join(B.ROOT, "dersler", e["id"] + ".json"), encoding="utf-8")); e["n"] = len(L["questions"])
    json.dump(idx, open(os.path.join(B.ROOT, "dersler", "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
