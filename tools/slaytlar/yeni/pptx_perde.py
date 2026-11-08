# -*- coding: utf-8 -*-
"""Perdedeki akışla PowerPoint (indir/M3.pptx, M4.pptx).

Her adım ayrı slayt; her sorudan sonra cevap slaytı; "Tamam mı, devam mı?"
slaytında tıklanabilir iki düğme (Tamam → çıkış bileti, Devam → ayrıntılar);
liderlik ve kelime bulutu yerine yer tutucu. pptx_yap.py çağırır.
"""
import os, json, re
import pptx_yap as P
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

BG, INK, PUR, PINK, LIL = RGBColor(0xF8,0xF5,0xFA), RGBColor(0x24,0x16,0x3A), RGBColor(0x4A,0x2C,0x82), RGBColor(0xC2,0x36,0x6A), RGBColor(0xEF,0xE8,0xFA)
W, H = P.W, P.H
X = lambda f: Emu(int(W * f)); Y = lambda f: Emu(int(H * f))

def clean(n):
    n = re.sub(r"\n\nCANLI \(.*$", "", n or "", flags=re.S).strip()
    return re.sub(r"^\[[^\]]*\]\s*", "", n).replace("ZAMAN KALIRSA; yoksa → ile atla.", "Zaman kalırsa.").strip()

def box(sl, x, y, w, h, fill, lines, size=22, color=INK, bold_first=False, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = sl.shapes.add_shape(shape, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill; s.line.fill.background(); s.shadow.inherit = False
    try: s.adjustments[0] = 0.08
    except Exception: pass
    tf = s.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Emu(int(W * 0.018)); tf.margin_top = tf.margin_bottom = Emu(int(H * 0.02))
    for i, t in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = t; r.font.size = Pt(size if i else size + (4 if bold_first else 0)); r.font.color.rgb = color
        r.font.bold = bool(bold_first and i == 0); r.font.name = "Calibri"
        p.space_after = Pt(6)
    return s

def plain(prs, title, sub, notes):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid(); sl.background.fill.fore_color.rgb = BG
    box(sl, X(.05), Y(.07), X(.9), Y(.14), BG, [title], 40, INK, shape=MSO_SHAPE.RECTANGLE)
    box(sl, X(.05), Y(.35), X(.9), Y(.3), LIL, [sub], 28, PUR)
    sl.notes_slide.notes_text_frame.text = notes
    return sl

def answer_text(q):
    t = q["type"]
    if t in ("MCQ", "IMGMCQ") and q.get("a") is not None:
        L, o = "ABCDE"[q["a"]], q["opts"][q["a"]]
        return "Doğru cevap: %s" % (L if o.strip() == L else "%s) %s" % (L, o))
    if t == "MATCH":
        return "Doğru eşleşme: " + " · ".join("%s → %s" % (a, b) for a, b in zip(q["left"], q["key"]))
    if t == "SCT" and q.get("scale"):
        return "Uzman cevabı: %s" % q["scale"][q["a"]]
    return None

def build(lid, out):
    L = json.load(open(os.path.join(P.CANLI, "dersler", lid + ".json"), encoding="utf-8"))
    qmap = {q["id"]: q for q in L["questions"]}
    prs = Presentation(); prs.slide_width, prs.slide_height = W, H
    k1 = cikis = None; after_k1 = None
    for s in L["slides"]:
        notes = s["title"] + "\n\n" + clean(s.get("notes"))
        if s.get("board"):
            plain(prs, s["title"], "Canlı derste perdede liderlik tablosu açılır (ilk %s)." % s.get("top", 10) if s.get("top") else "Canlı derste perdede liderlik tablosu açılır.", notes); continue
        if s.get("cloud"):
            plain(prs, s["title"], "Canlı derste perdede önceki dersin kelime bulutu açılır.", notes); continue
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        sl.shapes.add_picture(os.path.join(P.CANLI, s["img"].split("?")[0]), 0, 0, W, H)
        sl.notes_slide.notes_text_frame.text = notes
        if k1 is not None and after_k1 is None:
            after_k1 = sl
        if s["title"].startswith("Çıkış bileti"):
            cikis = sl
        qid = s.get("q")
        if not qid:
            continue
        q = qmap[qid]
        if qid == "K1":
            k1 = sl; continue
        a = answer_text(q)
        if not a or q.get("hide"):
            continue                                   # tahmin anketi: cevap açılmaz
        # perdede → ile cevap açılır: aynı slayt + cevap kutusu
        sl2 = prs.slides.add_slide(prs.slide_layouts[6])
        sl2.shapes.add_picture(os.path.join(P.CANLI, s["img"].split("?")[0]), 0, 0, W, H)
        lines = [a] + ([q["exp"]] if q.get("exp") else [])
        box(sl2, X(.53), Y(.50), X(.43), Y(.38), PUR, lines, 18, RGBColor(255, 255, 255), bold_first=True)
        sl2.notes_slide.notes_text_frame.text = s["title"] + " · cevap\n\n" + "\n\n".join(lines)
    if k1 is not None:
        b1 = box(k1, X(.05), Y(.66), X(.36), Y(.12), PINK, ["Tamam → çıkış biletine git"], 24, RGBColor(255, 255, 255), bold_first=True)
        b2 = box(k1, X(.44), Y(.66), X(.36), Y(.12), PUR, ["Devam → ayrıntılara geç"], 24, RGBColor(255, 255, 255), bold_first=True)
        if cikis is not None: b1.click_action.target_slide = cikis
        if after_k1 is not None: b2.click_action.target_slide = after_k1
    prs.core_properties.title = L["title"]; prs.core_properties.author = "Uzm. Dr. M. Olgun Ak"
    prs.save(out)
    return len(prs.slides)



def build_perde(lid):
    os.makedirs(P.OUT, exist_ok=True)
    path = os.path.join(P.OUT, lid + ".pptx")
    n = build(lid, path)
    L = json.load(open(os.path.join(P.CANLI, "dersler", lid + ".json"), encoding="utf-8"))
    return {"id": lid, "title": L["title"], "date": L["date"], "slides": n, "mb": round(os.path.getsize(path) / 1e6, 1),
            "file": lid + ".pptx", "quiz": L.get("quiz", "")}
