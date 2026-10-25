# -*- coding: utf-8 -*-
"""Book figures for the slides.

KITAP points to a folder with the PDFs (neville5.pdf, laskaris.pdf, who.pdf);
figures are cut out once into KITAP/fig and reused.

  F("n", "12.34")   Neville 5. baskı, Fig. 12.34
  F("l", "35.8")    Laskaris 4. baskı, Fig. 35.8
  crop=(x0, y0, x1, y1) as fractions keeps one panel of a combined figure.
"""
import json, os, re

KITAP = os.environ.get("KITAP", "/tmp/claude-0/-home-user-lam-basinda/066cc327-64ce-559a-a916-2b09d3ac6f46/scratchpad/kitap")
FIG = os.path.join(os.path.dirname(KITAP), "fig")
_idx = {}


def _index(book):
    if book in _idx:
        return _idx[book]
    import pymupdf
    pdf = {"n": "neville5.pdf", "l": "laskaris.pdf"}[book]
    cache = os.path.join(FIG, "idx_%s.json" % book)
    if os.path.exists(cache):
        _idx[book] = json.load(open(cache)); return _idx[book]
    d = pymupdf.open(os.path.join(KITAP, pdf))
    rng = range(470, 588) if book == "n" else range(1, d.page_count + 1)
    idx = {}
    for pn in rng:
        p = d[pn - 1]
        caps = []
        for b in p.get_text("blocks"):
            m = re.match(r"\s*•?\s*Fig\.\s*(\d+\.\d+)\s*(.*)", b[4], re.S)
            if m:
                caps.append((b, m.group(1), re.sub(r"\s+", " ", m.group(2)).strip()))
        for im in p.get_images(full=True):
            for r in p.get_image_rects(im[0]):
                if r.width < 60:
                    continue
                best = None
                for b, num, txt in caps:
                    if b[1] >= r.y1 - 5 and b[0] < r.x1 and b[2] > r.x0:
                        sc = b[1] - r.y1
                    elif b[0] >= r.x1 - 10 and r.y0 - 15 <= b[1] < r.y1:
                        sc = abs(b[1] - r.y0) + (0 if book == "l" else 500)
                    else:
                        continue
                    if best is None or sc < best[0]:
                        best = (sc, num, txt)
                if best:
                    k = best[1]; i = 1
                    while k in idx:
                        i += 1; k = "%s_%d" % (best[1], i)
                    idx[k] = {"page": pn, "xref": im[0], "cap": best[2]}
    os.makedirs(FIG, exist_ok=True)
    json.dump(idx, open(cache, "w"), ensure_ascii=False)
    _idx[book] = idx
    return idx


def F(book, key, crop=None):
    idx = _index(book)
    if key not in idx:
        raise KeyError("%s fig %s yok" % (book, key))
    out = os.path.join(FIG, "%s_%s%s.png" % (book, key, "" if not crop else "_" + "_".join("%g" % c for c in crop)))
    if not os.path.exists(out):
        import pymupdf
        from PIL import Image
        pdf = {"n": "neville5.pdf", "l": "laskaris.pdf"}[book]
        d = pymupdf.open(os.path.join(KITAP, pdf))
        pix = pymupdf.Pixmap(d, idx[key]["xref"])
        if pix.n - pix.alpha >= 4:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
        tmp = out + ".tmp.png"
        pix.save(tmp)
        im = Image.open(tmp).convert("RGB")
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        im.save(out); os.remove(tmp)
    return out


def cap(book, key):
    return _index(book)[key]["cap"]
