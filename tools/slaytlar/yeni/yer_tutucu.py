# -*- coding: utf-8 -*-
"""Fills the empty photo frames left in the M1/M2 decks (build2.py placeholders).

Each frame is found by its placeholder colour inside a search box, the book
figure is cover-fitted into it, and the same picture is saved under the file
name build2.py expects (canli/img/...), so a later rebuild keeps it.
"""
import json, os, re, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import CANLI
from foto import F

PH = np.array([226, 218, 236])
VER = "5"
# (lesson, slide title start, search box, figure, file name in canli/img)
JOBS = [
    ("M1", "(Zaman kalırsa) Herpes: tedavi", (60, 170, 800, 1000), ("n", "7.18"), "zoster_trigeminal.jpg"),
    ("M1", "(Zaman kalırsa) Herpes bulaşır", (60, 170, 800, 1000), ("n", "7.9"), "herpetik_dolama.jpg"),
    ("M2", "(Zaman kalırsa) Mikroskopta displazi", (60, 170, 960, 780), ("n", "16.102"), "displazi_normal.jpg"),
    ("M2", "(Zaman kalırsa) Mikroskopta displazi", (960, 170, 1860, 780), ("n", "10.74"), "displazi_agir.jpg"),
    ("M2", "(Zaman kalırsa) Dudakta çil gibi lekeler", (60, 170, 800, 1000), ("l", "28.16"), "peutz_jeghers.jpg"),
    ("M2", "(Zaman kalırsa) Damakta peteşi", (60, 170, 800, 1000), ("n", "7.22"), "petesi_damak.jpg"),
]


def frame(img, search):
    a = np.array(img.crop(search).convert("RGB")).astype(int)
    m = np.abs(a - PH).sum(axis=2) < 10
    rows = np.where(m.mean(axis=1) > 0.5)[0]
    cols = np.where(m.mean(axis=0) > 0.5)[0]
    if not len(rows):
        return None
    return (search[0] + cols[0], search[1] + rows[0], search[0] + cols[-1] + 1, search[1] + rows[-1] + 1)


def cover(ph, w, h):
    r = max(w / ph.width, h / ph.height)
    ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
    x0 = (ph.width - w) // 2; y0 = (ph.height - h) // 2
    return ph.crop((x0, y0, x0 + w, y0 + h))


def main():
    jsons = {}
    for lid, title, search, fig, name in JOBS:
        L = jsons.setdefault(lid, json.load(open(os.path.join(CANLI, "dersler", lid + ".json"), encoding="utf-8")))
        s = next(x for x in L["slides"] if x["title"].startswith(title))
        path = os.path.join(CANLI, s["img"].split("?")[0])
        img = Image.open(path).convert("RGB")
        box = frame(img, search)
        src = Image.open(F(*fig)).convert("RGB")
        src.save(os.path.join(CANLI, "img", name), quality=88)
        if box is None:
            print("zaten dolu:", lid, title, name); continue
        img.paste(cover(src, box[2] - box[0], box[3] - box[1]), box[:2])
        img.save(path, quality=92, subsampling=0)
        s["img"] = re.sub(r"\?v=\w+", "?v=" + VER, s["img"])
        print(lid, os.path.basename(path), name, box)
    for lid, L in jsons.items():
        json.dump(L, open(os.path.join(CANLI, "dersler", lid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
