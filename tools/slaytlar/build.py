# -*- coding: utf-8 -*-
"""Rebuilds the M1/M2 slide decks (JPG + JSON) from the originals in git.

Originals are read from ORIG (a pristine copy of canli/slaytlar), outputs go
to OUT/<lesson>/NN.jpg and the lesson JSON files are rewritten.
"""
import json, os, shutil, copy, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/user/lam-basinda/canli"
SCR = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(SCR, "orig")          # pristine copy of slaytlar
ORIG_JSON = os.path.join(SCR, "orig_json")
OUT = os.path.join(SCR, "out")            # new slaytlar
FONTS = os.path.join(SCR, "fonts")
VER = sys.argv[1] if len(sys.argv) > 1 else "2"

# ---------- palette (sampled from the originals) ----------
NAVY = (36, 22, 58)
NAVY2 = (57, 47, 84)
PURPLE = (68, 47, 103)
PINK = (190, 40, 90)
YELLOW = (240, 180, 30)
LILAC = (244, 238, 248)
ROSE = (250, 233, 239)
WHITE = (255, 255, 255)
SOFT = (200, 190, 215)
GREY = (120, 110, 135)

# ---------- fonts ----------
def F(kind, size, wght=700):
    if kind == "serif":
        f = ImageFont.truetype(os.path.join(FONTS, "Lora[wght].ttf"), size)
        f.set_variation_by_axes([wght])
        return f
    name = {"sans": "Lato-Regular.ttf", "bold": "Lato-Bold.ttf",
            "italic": "Lato-Italic.ttf", "black": "Lato-Black.ttf"}[kind]
    return ImageFont.truetype(os.path.join(FONTS, name), size)

# ---------- drawing helpers ----------
def rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

def tw(font, s):
    b = font.getbbox(s)
    return b[2] - b[0]

def wrap(font, s, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(font, t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def pill(d, x, y, text, font, fill, fg, padx=16, pady=7, right=False, outline=None):
    w = tw(font, text) + 2 * padx
    h = font.size + 2 * pady
    if right:
        x = x - w
    rrect(d, (x, y, x + w, y + h), h // 2, fill)
    if outline:
        d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, outline=outline, width=2)
    d.text((x + padx, y + pady - font.size * 0.12), text, font=font, fill=fg)
    return (x, y, x + w, y + h)

def uniform(img, box, tol=12):
    a = np.array(img.crop(box)).astype(int)
    c = a[a.shape[0] // 2, a.shape[1] // 2]
    return (np.abs(a - c).sum(axis=2) > tol).mean() < 0.002

def is_dark(img):
    return sum(img.getpixel((20, 20))) < 300

def bgcolor(img):
    return img.getpixel((20, 20))

def exact_box(img, approx, bg, tol=30):
    """Shrink an approximate box to the exact bounds of the non-bg object inside."""
    x0, y0, x1, y1 = approx
    a = np.array(img.crop(approx)).astype(int)
    m = np.abs(a - np.array(bg)).sum(axis=2) > tol
    ys = np.where(m.any(axis=1))[0]; xs = np.where(m.any(axis=0))[0]
    return (x0 + xs[0], y0 + ys[0], x0 + xs[-1] + 1, y0 + ys[-1] + 1)

# ---------- per-slide element edits ----------
def renumber(img, n):
    """Replace the page number in the bottom-right footer."""
    d = ImageDraw.Draw(img)
    region = (1760, 1005, 1900, 1070)
    bg = img.getpixel((1899, 1069))
    a = np.array(img.crop(region)).astype(int)
    m = np.abs(a - np.array(bg)).sum(axis=2) > 60
    if m.any():
        ys = np.where(m.any(axis=1))[0]; xs = np.where(m.any(axis=0))[0]
        right = region[0] + xs[-1] + 1
        top = region[1] + ys[0]
        h = ys[-1] - ys[0] + 1
        # average colour of the digits
        col = tuple(int(v) for v in a[m].mean(axis=0))
        d.rectangle((region[0] + xs[0] - 2, region[1] + ys[0] - 2, right + 2, region[1] + ys[-1] + 3), fill=bg)
    else:
        right, top, h, col = 1880, 1028, 13, (150, 140, 170)
    f = F("sans", int(round(h / 0.72)))
    s = str(n)
    b = f.getbbox(s)
    d.text((right - (b[2] - b[0]) - b[0], top - b[1]), s, font=f, fill=col)

def top_right_tag(img, text, fill, fg, font=None):
    """Put a pill at the top-right where the title leaves room."""
    font = font or F("bold", 22)
    d = ImageDraw.Draw(img)
    w = tw(font, text) + 32; h = font.size + 14
    for y in (52, 128, 150):
        box = (1850 - w - 10, y - 6, 1860, y + h + 6)
        if uniform(img, box):
            return pill(d, 1850, y, text, font, fill, fg, right=True)
    return pill(d, 1850, 128, text, font, fill, fg, right=True)

def dus_badge(img):
    return top_right_tag(img, "DUS", YELLOW, NAVY, F("black", 22))

def optional_tag(img):
    return top_right_tag(img, "ZAMAN KALIRSA", (120, 110, 135) if not is_dark(img) else (90, 80, 110), WHITE, F("bold", 20))

def strip(img, active, labels=("1 Dağılım", "2 Düzey", "3 Desen"), name="3D"):
    """Breadcrumb in the footer centre, with the frame name in front."""
    d = ImageDraw.Draw(img)
    dark = is_dark(img)
    f = F("bold", 20)
    y = 1017
    # start right after the footer text, whatever its width
    bg = img.getpixel((60, 1025))
    a = np.array(img.crop((80, 1012, 900, 1045))).astype(int)
    m = (np.abs(a - np.array(bg)).sum(axis=2) > 60).any(axis=0)
    xs = np.where(m)[0]
    x = 80 + (xs[-1] if len(xs) else 340) + 28
    box = pill(d, x, y, name, F("black", 20), PINK, WHITE, padx=12, pady=6)
    x = box[2] + 10
    for i, lab in enumerate(labels, 1):
        on = i in active
        fill = YELLOW if on else ((57, 47, 84) if dark else LILAC)
        fg = NAVY if on else ((170, 160, 190) if dark else GREY)
        box = pill(d, x, y, lab, f, fill, fg, padx=14, pady=6)
        x = box[2] + 8

def cover_rect(img, box, color):
    ImageDraw.Draw(img).rectangle(box, fill=color)

def recolor_sct(img, labels):
    """Neutralise the five coloured SCT boxes and rewrite their labels."""
    d = ImageDraw.Draw(img)
    bg = bgcolor(img)
    approx = [(80, 684, 423, 858), (429, 684, 775, 858), (785, 684, 1124, 858), (1133, 684, 1477, 858), (1484, 684, 1829, 858)]
    f = F("bold", 26)
    for box, lab in zip(approx, labels):
        ex = exact_box(img, box, bg)
        d.rectangle(box, fill=bg)
        rrect(d, ex, 14, NAVY2)
        w = tw(f, lab)
        d.text(((ex[0] + ex[2]) / 2 - w / 2, (ex[1] + ex[3]) / 2 - f.size * 0.62), lab, font=f, fill=WHITE)

def caption_append(img, bar, extra):
    """Append text after the white caption inside a dark caption bar."""
    a = np.array(img.crop(bar)).astype(int)
    m = (a.min(axis=2) > 200)
    xs = np.where(m.any(axis=0))[0]; ys = np.where(m.any(axis=1))[0]
    right = bar[0] + xs[-1] + 1; top = bar[1] + ys[0]; h = ys[-1] - ys[0] + 1
    f = F("bold", int(round(h / 0.74)))
    b = f.getbbox(extra)
    ImageDraw.Draw(img).text((right + 2, top - b[1]), extra, font=f, fill=WHITE)

def redraw_box(img, box, color, title, lines, tfont, bfont, tcolor, bcolor, pad=28, gap=10, radius=16):
    d = ImageDraw.Draw(img)
    rrect(d, box, radius, color)
    x = box[0] + pad; y = box[1] + pad
    if title:
        d.text((x, y), title, font=tfont, fill=tcolor)
        y += tfont.size * 1.35 + gap
    maxw = box[2] - box[0] - 2 * pad
    for ln in lines:
        for sub in wrap(bfont, ln, maxw):
            d.text((x, y), sub, font=bfont, fill=bcolor)
            y += bfont.size * 1.3
    return y

def rich_line(d, x, y, parts, maxw=None):
    """parts: list of (text, font, color)."""
    for text, font, color in parts:
        d.text((x, y), text, font=font, fill=color)
        x += tw(font, text)
    return x

# ---------- lessons ----------
def load(l):
    return json.load(open(os.path.join(ORIG_JSON, l + ".json"), encoding="utf-8"))

def ts(sec):
    return "%d:%02d" % (sec // 60, sec % 60)

T_BY_TYPE = {"WORDCLOUD": 45, "POLL": 45, "MCQ": 30, "IMGMCQ": 30, "FINDIMG": 30, "SCT": 45,
             "OPEN": 75, "SORTGROUP": 60, "SORTORDER": 60, "MATCH": 60}
TYPE_TR = {"WORDCLOUD": "Kelime bulutu", "POLL": "Anket", "MCQ": "Çoktan seçmeli", "IMGMCQ": "Görselli çoktan seçmeli",
           "FINDIMG": "Görüntüde bul", "SCT": "Senaryo uyum testi (SCT)", "OPEN": "Açık uçlu",
           "SORTGROUP": "Sıralama (gruplama)", "SORTORDER": "Sıralama", "MATCH": "Eşleştirme"}

def live_block(q, lobby=False):
    t = q["t"]
    typ = q["type"]
    s = "CANLI (%s, %s): " % (q["id"], TYPE_TR[typ])
    if lobby:
        s += "Katılım ekranı açıkken soru telefonlarda açık; girenler hemen yazabilir. L ile katılım ekranını kapatınca bulut perdeye düşer. → kapatır, → sonraki slayt."
    elif typ == "WORDCLOUD":
        s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. Bulut canlı akar. → kapatır, → sonraki slayt."
    elif typ == "POLL" and q.get("hide"):
        s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. → oylamayı kapatıp dağılımı gösterir, → sonraki slayt (tahmin anketi; cevap açılmaz)."
    elif typ == "OPEN":
        s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. Cevaplar gizli gelir; H ile göster. → kapatır, → beklenen cevabı açar, → sonraki slayt."
    else:
        s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. → oylamayı kapatıp sonuçları gösterir, → doğru cevabı ve açıklamayı açar, → sonraki slayt."
    if q.get("a") is not None and typ in ("MCQ", "IMGMCQ", "POLL"):
        s += " Doğru: %s." % "ABCDE"[q["a"]]
    if typ == "FINDIMG":
        s += " Doğru alan: %s." % q["answer"]
    s += " T: %d sn (perdede T düğmesi bu soruda %d sn sayar)." % (t, t)
    return s

STAMP = re.compile(r"^\[[^\]]*\]\s*\n?")

def strip_old(notes):
    notes = STAMP.sub("", notes.strip())
    return re.sub(r"\n\nCANLI \(.*$", "", notes, flags=re.S).strip()

def build_lesson(lid, plan, qdrop, qedit, note_edit, qadd=(), strip_cfg=None, cta=None, frame=None):
    L = load(lid)
    orig_slides = L["slides"]
    questions = [q for q in L["questions"] if q["id"] not in qdrop] + [copy.deepcopy(q) for q in qadd]
    for i, q in enumerate(questions):
        e = qedit.get(q["id"])
        if e and e.get("__replace__"):
            e = dict(e); e.pop("__replace__"); questions[i] = e
    qmap = {q["id"]: q for q in questions}
    for q in questions:
        q["t"] = T_BY_TYPE[q["type"]]
        e = qedit.get(q["id"])
        if e and not e.get("__replace__"):
            q.update(e)
    os.makedirs(os.path.join(OUT, lid), exist_ok=True)
    new_slides = []
    t = 0
    n = 0
    for item in plan:
        n += 1
        src = item.get("src")          # original slide number (1-based) or None for board
        dur = item["dur"]
        if src is None and not item.get("make"):
            if item.get("cloud"):
                s = {"cloud": item["cloud"], "title": item["title"], "notes": "[%s–%s]\n%s" % (ts(t), ts(t + dur), item.get("notes", ""))}
            else:
                s = {"board": True, "title": item.get("title", "Liderlik tablosu"), "notes": "[%s–%s]\n%s" % (ts(t), ts(t + dur), item.get("notes", "Liderlik tablosu. İlk üçü alkışlayalım. Eşit puanda hızlı olan önde."))}
                if item.get("top"): s["top"] = item["top"]
            new_slides.append(s); t += dur; continue
        o = copy.deepcopy(orig_slides[src - 1]) if src else {"title": item["title"], "notes": item.get("notes", "")}
        s = {"img": "slaytlar/%s/%02d.jpg?v=%s" % (lid, n, VER), "title": o["title"]}
        if item.get("title"): s["title"] = item["title"]
        if item.get("optional"): s["title"] = "(Zaman kalırsa) " + s["title"]
        if item.get("lobby"): s["lobby"] = True
        if item.get("qopen"): s["qopen"] = item["qopen"]
        qid = item.get("q", o.get("q"))
        if item.get("noq"): qid = None
        if qid and qid in qmap: s["q"] = qid
        body = strip_old(o.get("notes", ""))
        if item.get("notes") is not None:
            body = item["notes"]
        key = item.get("key", src)
        if key in note_edit:
            body = note_edit[key](body)
        stamp = "[%s–%s]" % (ts(t), ts(t + dur))
        if item.get("optional"):
            stamp += " ZAMAN KALIRSA; yoksa → ile atla."
        notes = stamp + "\n" + body
        if s.get("qopen") and s["qopen"] in qmap:
            qq = qmap[s["qopen"]]
            notes += "\n\nCANLI (%s, %s): Soru bu slayta gelince telefonlarda açılır; perde slaytı göstermeye devam eder. Oylama bir sonraki slayta (dağılım) kadar açık kalır, geri gelsen de kapanmaz. → sonraki slayt. T: %d sn." % (qq["id"], TYPE_TR[qq["type"]], qq["t"])
        elif item.get("cont") and s.get("q"):
            qq = qmap[s["q"]]
            notes += "\n\nCANLI (%s, %s): Soru önceki slaytta açıldı, oylama hâlâ açık. → oylamayı kapatıp dağılımı gösterir, → sonraki slayt%s." % (qq["id"], TYPE_TR[qq["type"]], (" (tahmin anketi; cevap açılmaz). Doğru: " + "ABCDE"[qq["a"]]) if qq.get("a") is not None and qq.get("hide") else "")
        elif s.get("q"):
            notes += "\n\n" + live_block(qmap[s["q"]], lobby=bool(s.get("lobby")))
        s["notes"] = notes
        new_slides.append(s)
        # image
        img = item["make"]() if item.get("make") else Image.open(os.path.join(ORIG, lid, "%02d.jpg" % src)).convert("RGB")
        for fn in item.get("edits", []):
            fn(img)
        if item.get("optional"): optional_tag(img)
        elif item.get("dus"): dus_badge(img)
        if "strip" in item: strip(img, item["strip"], *(strip_cfg or ()))
        if not item.get("nonum"): renumber(img, n)
        img.save(os.path.join(OUT, lid, "%02d.jpg" % n), quality=92, subsampling=0)
        t += dur
    L["questions"] = questions
    L["slides"] = new_slides
    L["duration"] = ts(t)
    if cta: L["cta"] = cta
    if frame: L["frame"] = frame
    json.dump(L, open(os.path.join(ROOT, "dersler", lid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(lid, "slides", len(new_slides), "questions", len(questions), "total", ts(t))
    return L

# ============ M1 edits ============
def m1_s6_bridge(img):
    d = ImageDraw.Draw(img)
    pill(d, 1832, 92, "Sırada telefon: iki fotoğraf, bir soru", F("bold", 24), YELLOW, NAVY, right=True, padx=20, pady=9)

def m1_s11_desmoglein(img):
    box = (80, 665, 983, 976)
    redraw_box(img, box, NAVY, "Desmoglein kuralı",
               ["Anti-DSG3  →  yalnızca ağız", "Anti-DSG3 + DSG1  →  ağız + deri", "Anti-DSG1  →  pemfigus foliaseus, ağız korunur"],
               F("serif", 32), F("sans", 28), YELLOW, WHITE, pad=30, gap=14)

def m1_s24_tugse(img):
    caption_append(img, (700, 722, 1240, 770), " (TUGSE)")

def m1_s25_grades(img):
    d = ImageDraw.Draw(img)
    rows = [(1368, 266, 1829, 347), (1368, 361, 1829, 442), (1368, 456, 1829, 537), (1368, 551, 1829, 632)]
    texts = ["Eritem, ağrı", "Ülser; katı yiyebilir", "Ülser; yalnızca sıvı", "Ağızdan beslenemez"]
    f = F("sans", 30)
    for (x0, y0, x1, y1), s in zip(rows, texts):
        col = img.getpixel((x1 - 12, (y0 + y1) // 2))
        d.rectangle((x0 + 8, y0 + 6, x1 - 6, y1 - 6), fill=col)
        d.text((x0 + 14, (y0 + y1) / 2 - f.size * 0.62), s, font=f, fill=NAVY)

def m1_s29_sct(img):
    recolor_sct(img, ["−2 Çok zayıflatır", "−1 Zayıflatır", "0 Etkilemez", "+1 Güçlendirir", "+2 Çok güçlendirir"])

def m1_s18_A(img):
    cover_rect(img, (80, 600, 1840, 985), WHITE)

def m1_s27_A(img):
    cover_rect(img, (70, 590, 665, 995), WHITE)       # lupus photo
    cover_rect(img, (678, 540, 1836, 985), WHITE)     # rows 3-4 + rule box

def m1_s32_A(img):
    d = ImageDraw.Draw(img)
    cols = [(86, 187, 504, 979), (529, 187, 947, 979), (972, 187, 1390, 979), (1415, 187, 1832, 979)]
    for x0, y0, x1, y1 in cols:
        col = img.getpixel((x0 + 12, 850))
        d.rectangle((x0 + 4, 545, x1 - 4, 840), fill=col)

# ============ M2 edits ============
def m2_s10_cards(img):
    cards = [(86, 655, 504, 972), (530, 655, 947, 972), (973, 655, 1391, 972), (1417, 655, 1835, 972)]
    content = [("Lökoödem", "Gerince kaybolur; varyasyon", PURPLE),
               ("Beyaz süngerimsi nevüs", "Kalıtsal (KRT4/13); çocukluktan beri", PURPLE),
               ("Tütün kesesi keratozu", "Dumansız tütün; bırakınca geriler", PURPLE),
               ("Tuzak", "Ters sigara içimi damakta yüksek risk", PINK)]
    for box, (title, body, tc) in zip(cards, content):
        col = img.getpixel((box[2] - 10, box[3] - 10))
        redraw_box(img, box, col, title, [body], F("serif", 30), F("sans", 26), tc, NAVY, pad=24, gap=8)

def m2_s11_sct(img):
    m1_s29_sct(img)

def m2_s13_binary(img):
    d = ImageDraw.Draw(img)
    # bottom bar
    bar = (86, 871, 1829, 972)
    col = img.getpixel((100, 880))
    rrect(d, bar, 14, col)
    fb, fr = F("bold", 27), F("sans", 27)
    y = 892
    x = rich_line(d, 112, y, [("İki basamaklı sınıflama:  ", fb, NAVY), ("Düşük dereceli", fb, PURPLE), (" = hafif displazi   ·   ", fr, NAVY),
                               ("Yüksek dereceli", fb, PINK), (" = orta, ağır displazi ve karsinoma in situ", fr, NAVY)])
    d.text((112, y + 38), "Yüksek dereceli lezyon izlenmez, çıkarılır.", font=fb, fill=NAVY)
    # brackets above columns
    cols = {"hafif": (369, 627), "orta": (666, 924), "cis": (1255, 1513)}
    fl = F("bold", 24)
    for (x0, x1), lab, c in [((cols["hafif"][0], cols["hafif"][1]), "Düşük dereceli", PURPLE),
                             ((cols["orta"][0], cols["cis"][1]), "Yüksek dereceli", PINK)]:
        yb = 212
        d.line((x0, yb, x1, yb), fill=c, width=3)
        d.line((x0, yb, x0, yb + 12), fill=c, width=3)
        d.line((x1, yb, x1, yb + 12), fill=c, width=3)
        w = tw(fl, lab)
        d.text(((x0 + x1) / 2 - w / 2, yb - 38), lab, font=fl, fill=c)

def m2_s16_rule(img):
    d = ImageDraw.Draw(img)
    box = (86, 806, 1829, 972)
    rrect(d, box, 16, NAVY)
    fb, fr = F("bold", 28), F("sans", 24)
    rich_line(d, 116, 836, [("Bugünün kuralı: ", fb, YELLOW), ("iki haftada iyileşmeyen ülser ve silinmeyen kırmızı-beyaz alan biyopsiye gider.", fb, WHITE)])
    d.text((116, 886), "Ayrıntısı 3 Kasım'daki epitelyal tümörler dersinde.", font=fr, fill=SOFT)

def m2_s37_line2(img):
    d = ImageDraw.Draw(img)
    d.rectangle((195, 400, 1900, 470), fill=NAVY)
    f = F("sans", 36)
    d.text((206, 408), "Altı ay bekleyen plak = ağır displazi: lökoplaki bir kelimedir, tanıyı biyopsi koyar.", font=f, fill=WHITE)

def m2_s21_A(img):
    cover_rect(img, (995, 192, 1845, 995), WHITE)

def m2_s22_A(img):
    cover_rect(img, (630, 180, 1870, 985), WHITE)

# ============ note edits ============
def rep(old, new):
    def f(s):
        assert old in s, ("note text not found", old)
        return s.replace(old, new)
    return f

DIKKAT = re.compile(r"\s*Dikkat: diş çekimi[^.]*\.")

M1_NOTES = {
    4: rep("Şimdi tahmininizi alalım; cevabı dersin sonunda açacağım.", "Şıklar şu an telefonlarda açık; fotoğrafa bakıp tahmininizi girin. Cevabı dersin sonunda açacağım. Sonraki slaytta dağılımı göreceğiz."),
    6: lambda s: s + " Sırada telefon: iki fotoğraf, bir soru.",
    15: rep("Diğer şıkları da az önce gördük; her biri başka bir hastalığın adresi.",
            "Floresan desenlerini birkaç slayt önce gördük; her biri başka bir hastalığın adresi. Bu ara aynı zamanda virüs bloğunu kapatıyor; sırada aft."),
    20: rep("Neden B? Klinik şüpheyi patolog şöyle doğrular:", "Kliniği gördük; şimdi patolog gözüyle bakalım. Klinik şüpheyi patolog şöyle doğrular:"),
    24: rep("Sağdaki dil ülseri ise travmatik eozinofilik ülser:", "Sağdaki dil ülseri ise travmatik eozinofilik ülser, kısaltması TUGSE:"),
    28: lambda s: s + " Sırada telefon: patolog gibi düşüneceksiniz.",
    "18A": lambda s: DIKKAT.sub(" ", s).strip() + " (İleri: aftla ayırım ve tuzak.)",
    "18B": lambda s: "Aftla karıştırmayın: virüs önce vezikül, sonra küme hâlinde küçük ülserler; aftta vezikül yoktur, sarı tabanlı, kırmızı haleli tek ya da birkaç ülser. Dişeti yaygın ve ateş varsa primer herpes; dişeti sağlam, arka ağızsa herpangina. " + DIKKAT.search(s).group(0).strip(),
    "27A": lambda s: s.split("Yeni bir ilaçtan")[0].strip() + " (İleri: ilaç, lupus, nakil.)",
    "27B": lambda s: "Yeni bir ilaçtan" + s.split("Yeni bir ilaçtan")[1],
    "32A": lambda s: "Bugün gördüklerimizi tek tabloya koyalım. Ağızda yara gören hekim iki soru sorar: ne zamandır ve kaç tane? Dört kolon, dört kural; alt satırdaki kırmızı cümleleri okuyun. (İleri: kolonlar doluyor.)",
    "32B": lambda s: s.replace("Bugün gördüklerimizi tek tabloya koyalım. Ağızda yara gören hekim iki soru sorar: ne zamandır ve kaç tane? ", "Şimdi hastalıkları yerleştirelim. "),
}

M2_NOTES = {
    1: lambda s: s + "\n\nKatılım ekranı bu slaytta açık. İlk dersten gelenler telefondaki 'Sıradaki derse geç' düğmesine dokunur; tekrar kod okutmak gerekmez. Yeni gelenler için kod perdede. Herkes girince L ile kapatıp başlıyoruz.",
    3: rep("Tek kelime. (Bulut.)", "Tek kelime, 45 saniye. (Bulut.)"),
    4: rep("Fotoğrafa bakın ve iki soruya cevap verin: bu ne, ve şimdi ne yaparsınız? Cevabı dersin sonunda açacağım.",
           "Fotoğrafa bakın. Önce yüksek sesle: bu ne? (İki üç tahmin al, yorum yapma.) Şıklar şu an telefonlarda açık: şimdi ne yaparsınız? Cevabı dersin sonunda açacağım; sonraki slaytta dağılımı göreceğiz."),
    9: rep("Bir dakika. (Sonuç.)", "Bir dakika; yedi kutu, üç grup. (Sonuç.)"),
    19: rep("Kısa bir köprü; ayrıntısı 24 Kasım'da.", "Algoritmanın ilk kutusu 'silinir mi' demişti; işte silinenler ve silinmeyen bir virüs. Ayrıntısı 24 Kasım'da."),
    13: rep("Güncel sınıflama bunları düşük ve yüksek dereceli diye ikiye de ayırıyor. Sizin için pratik karşılığı: rapor 'ağır displazi' diyorsa bu lezyon artık izlenmez, çıkarılır.",
            "Güncel sınıflama iki basamağa indi: düşük dereceli, yani hafif displazi; yüksek dereceli, yani orta ve ağır displazi ile karsinoma in situ. Şemanın üstündeki iki parantez bunu gösteriyor. Sizin için pratik karşılığı: rapor 'yüksek dereceli' ya da 'ağır displazi' diyorsa bu lezyon artık izlenmez, çıkarılır."),
    14: rep("Karsinoma in situ ile ağır displazinin yerini karıştıran çok olur: in situ tam kattır ama bazal membran hâlâ sağlam.",
            "Karsinoma in situ ile ağır displazinin yerini karıştıran çok olur: in situ tam kattır ama bazal membran hâlâ sağlam. İki basamaklı sistemde orta displaziden itibaren hepsi yüksek dereceli."),
    "21A": lambda s: s.split("Ama damakta ya da maksiller")[0].strip() + " (İleri: melanom alarmı ve yaygın pigment.)",
    "21B": lambda s: "Ama damakta ya da maksiller" + s.split("Ama damakta ya da maksiller")[1],
    "22A": lambda s: s.split("Birinci fotoğraf")[0].strip() + " (İleri: beş fotoğraf.)",
    "22B": lambda s: "Birinci fotoğraf" + s.split("Birinci fotoğraf")[1],
    37: rep("İki: lökoplaki bir kelime, tanıyı biyopsi koyar.", "İki: altı ay bekleyen plak ağır displazi çıktı; lökoplaki bir kelime, tanıyı biyopsi koyar."),
}

W6_EXP = "Karsinoma in situ tam kat atipidir ama bazal membran sağlamdır; bazal membran aşılınca invaziv karsinom. İki basamaklı sistem: düşük dereceli = hafif; yüksek dereceli = orta, ağır ve karsinoma in situ."

# ============ plans ============
S = lambda **k: k
M1_PLAN = [
    S(src=1, dur=165, nonum=True, lobby=True, notes="Günaydın. Bugün ağızdaki yaraların ve kabarcıkların peşine düşeceğiz. Sağdaki yeşil ağı görüyorsunuz; bunun ne olduğunu birkaç dakika sonra söyleyeceğim, şimdilik güzel bir balık ağı gibi dursun. Karekod perdede, başlığın yanında: okutun; hesap yok, uygulama yok. Takma ad isterseniz yazın; dersin sonunda liderlik tablosu var, doğru ve hızlı olan kazanıyor. Katılımcı sayısı sağda akıyor; herkes girince → ile ısınma sorusuna geçiyoruz. (L: katılım ekranını gizle/göster.)"),
    S(src=2, dur=45, q="W1", notes="Telefondan tek kelime yazın: ağızda yara deyince aklınıza ilk ne geliyor? (Bulut oluşurken yorumla.) Büyük ihtimalle 'aft' kocaman çıktı. Çok normal; toplumda en sık oral ülser o. Ama bugünün sonunda bu buluta en az beş yeni kelime ekleyeceğiz, bir tanesi de hayat kurtaracak."),
    S(src=4, dur=45, qopen="W2"),
    S(src=5, dur=60, cont=True),
    S(src=6, dur=30, edits=[m1_s6_bridge]),
    S(src=7, dur=75, strip={1}),
    S(src=8, dur=45, strip={1}, dus=True),
    S(src=9, dur=75, strip={2}),
    S(src=10, dur=45, strip={2}, dus=True),
    S(src=11, dur=90, strip={1, 2, 3}, dus=True, edits=[m1_s11_desmoglein]),
    S(src=12, dur=45, strip={2, 3}),
    S(src=13, dur=60, strip={1, 2, 3}, dus=True),
    S(src=14, dur=45, strip={3}, dus=True),
    S(src=17, dur=60, strip={1}, dus=True),
    S(src=18, dur=30, strip={1, 2}, dus=True, key="18A", edits=[m1_s18_A], title="Vezikül kümesi görürsen virüsü düşün (1/2)"),
    S(src=18, dur=45, strip={1, 2}, key="18B", title="Vezikül kümesi görürsen virüsü düşün (2/2)"),
    S(src=20, dur=45, strip={2}, dus=True),
    S(src=15, dur=75),
    S(src=16, dur=75),
    S(src=21, dur=60, strip={1}, dus=True),
    S(src=22, dur=105),
    S(src=23, dur=45, strip={1}, dus=True),
    S(src=24, dur=45, strip={1}, edits=[m1_s24_tugse]),
    S(src=26, dur=60, strip={2, 3}, dus=True),
    S(src=27, dur=25, strip={1, 3}, dus=True, key="27A", edits=[m1_s27_A], title="Liken planus mu, taklitçisi mi? (1/2)"),
    S(src=27, dur=35, strip={1, 3}, key="27B", title="Liken planus mu, taklitçisi mi? (2/2)"),
    S(src=28, dur=45, strip={1, 2, 3}),
    S(src=29, dur=75, edits=[m1_s29_sct]),
    S(src=30, dur=60),
    S(src=31, dur=60, strip={1, 2, 3}),
    S(src=32, dur=20, strip={1, 2, 3}, key="32A", edits=[m1_s32_A], title="Ülsere ilk bakış: zaman ve sayı yolu gösterir (1/2)"),
    S(src=32, dur=40, strip={1, 2, 3}, key="32B", title="Ülsere ilk bakış: zaman ve sayı yolu gösterir (2/2)"),
    S(src=25, dur=60, optional=True, strip={1}, edits=[m1_s25_grades]),
    S(src=33, dur=60, optional=True, strip={1, 3}),
    S(src=34, dur=45),
    S(src=35, dur=60),
    S(src=None, dur=30),
    S(src=36, dur=15),
]

M2_PLAN = [
    S(src=1, dur=90, lobby=True, nonum=True),
    S(src=3, dur=45),
    S(src=4, dur=45, qopen="W3"),
    S(src=6, dur=60, cont=True),
    S(src=7, dur=45),
    S(src=8, dur=45),
    S(src=9, dur=90),
    S(src=19, dur=45, dus=True),
    S(src=10, dur=60, edits=[m2_s10_cards]),
    S(src=11, dur=75, edits=[m2_s11_sct]),
    S(src=12, dur=60, dus=True),
    S(src=13, dur=45, dus=True, edits=[m2_s13_binary]),
    S(src=14, dur=90),
    S(src=15, dur=60, dus=True),
    S(src=16, dur=45, dus=True, edits=[m2_s16_rule]),
    S(src=17, dur=75),
    S(src=18, dur=60),
    S(src=20, dur=75),
    S(src=21, dur=25, dus=True, key="21A", edits=[m2_s21_A], title="Kahverengi, mavi, siyah: pigment nereden geliyor? (1/2)"),
    S(src=21, dur=35, key="21B", title="Kahverengi, mavi, siyah: pigment nereden geliyor? (2/2)"),
    S(src=22, dur=20, key="22A", edits=[m2_s22_A], title="Kırmızı ve mor lezyonlar: bas ve bak (1/2)"),
    S(src=22, dur=40, key="22B", title="Kırmızı ve mor lezyonlar: bas ve bak (2/2)"),
    S(src=23, dur=75, dus=True),
    S(src=25, dur=45),
    S(src=26, dur=90),
    S(src=27, dur=75, dus=True),
    S(src=32, dur=105),
    S(src=33, dur=60),
    S(src=34, dur=45),
    S(src=28, dur=45, optional=True),
    S(src=29, dur=45, optional=True),
    S(src=30, dur=60, optional=True),
    S(src=35, dur=45, optional=True),
    S(src=36, dur=45, optional=True),
    S(src=37, dur=45, edits=[m2_s37_line2]),
    S(src=38, dur=45),
    S(src=None, dur=30),
    S(src=39, dur=15),
]

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    build_lesson("M1", M1_PLAN, qdrop={"W7"},
                 qedit={"W4": {"region": {"kind": "rect", "x0": 0, "x1": 1, "y0": 0.40, "y1": 0.60}}},
                 note_edit=M1_NOTES)
    build_lesson("M2", M2_PLAN, qdrop={"W2", "W10", "W12"},
                 qedit={"W6": {"exp": W6_EXP}},
                 note_edit=M2_NOTES)
    idx = json.load(open(os.path.join(ORIG_JSON, "index.json"), encoding="utf-8"))
    for e in idx:
        L = json.load(open(os.path.join(ROOT, "dersler", e["id"] + ".json"), encoding="utf-8")); e["n"] = len(L["questions"])
    json.dump(idx, open(os.path.join(ROOT, "dersler", "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
