# -*- coding: utf-8 -*-
"""Adds new slides into the existing M1/M2 decks (built earlier by build.py/build2.py).

Each added slide is marked "ek": true in the lesson JSON. On every run the
previous additions are removed, the new ones are inserted before the anchor
slide, existing JPGs are renamed to their new position with the page number
redrawn, and the time stamps in the notes are recomputed.

  python3 ek.py M1      (contents in ek_m1.py)
  python3 ek.py M2      (contents in ek_m2.py)
"""
import importlib, json, os, re, shutil, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import deck as D
import build as B   # renumber() for the old slide images

STAMP = re.compile(r"^\[(\d+):(\d\d)–(\d+):(\d\d)\]")


def secs(m, i):
    return int(m.group(i)) * 60 + int(m.group(i + 1))


def run(lid):
    mod = importlib.import_module("ek_" + lid.lower())
    jpath = os.path.join(D.CANLI, "dersler", lid + ".json")
    L = json.load(open(jpath, encoding="utf-8"))
    imgdir = os.path.join(D.CANLI, "slaytlar", lid)
    ver = mod.VER

    # 1. base slides with their current pictures and durations
    base = []
    for s in L["slides"]:
        if s.get("ek"):
            continue
        m = STAMP.match(s.get("notes", ""))
        dur = secs(m, 3) - secs(m, 1) if m else 30
        body = STAMP.sub("", s.get("notes", ""), count=1)
        pic = None
        if s.get("img"):
            pic = Image.open(os.path.join(D.CANLI, s["img"].split("?")[0])).convert("RGB")
        base.append({"json": s, "dur": dur, "rest": body, "pic": pic})

    # 2. insert the new slides before their anchors
    lesson = D.Lesson(lid, L["title"], mod.SHORT, L["date"], strip=getattr(mod, "STRIP", None))
    order = []
    adds = {}
    for spec in mod.SLIDES:
        adds.setdefault(spec["before"], []).append(spec)
    for b in base:
        for spec in adds.pop(b["json"]["title"], []):
            order.append({"new": spec})
        order.append(b)
    assert not adds, "anchor not found: %s" % list(adds)

    # 3. write pictures and JSON
    work = os.path.join(D.WORK, lid + "_ek")
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    tmp = os.path.join(work, "img")
    os.makedirs(tmp)
    jobs, slides, t = [], [], 0
    for n, it in enumerate(order, 1):
        if "new" in it:
            spec = dict(it["new"]); spec.setdefault("optional", True)
            dur = spec["dur"]
            stamp = "[%s–%s]" % (D.ts(t), D.ts(t + dur)) + (" ZAMAN KALIRSA; yoksa → ile atla." if spec.get("optional") else "")
            fn = os.path.join(work, "%02d.html" % n)
            open(fn, "w", encoding="utf-8").write(lesson.page(spec, n))
            jobs.append([fn, os.path.join(tmp, "%02d.jpg" % n)])
            title = ("(Zaman kalırsa) " if spec.get("optional") else "") + spec["title"]
            slides.append({"img": "slaytlar/%s/%02d.jpg?v=%s" % (lid, n, ver), "title": title,
                           "notes": stamp + "\n" + spec["notes"].strip(), "ek": True})
        else:
            s = dict(it["json"]); dur = it["dur"]
            rest = it["rest"]
            # keep "ZAMAN KALIRSA" marker that followed the old stamp
            s["notes"] = "[%s–%s]" % (D.ts(t), D.ts(t + dur)) + rest
            if it["pic"] is not None:
                pic = it["pic"].copy()
                old = int(re.search(r"/(\d+)\.jpg", s["img"]).group(1))
                if old != n and not s.get("lobby"):
                    B.renumber(pic, n)
                pic.save(os.path.join(tmp, "%02d.jpg" % n), quality=92, subsampling=0)
                s["img"] = "slaytlar/%s/%02d.jpg?v=%s" % (lid, n, ver)
            slides.append(s)
        t += dur
    json.dump(jobs, open(os.path.join(work, "jobs.json"), "w"))
    r = subprocess.run(["node", os.path.join(HERE, "render.mjs"), os.path.join(work, "jobs.json")], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr); raise SystemExit("render failed")
    for f in os.listdir(imgdir):
        os.remove(os.path.join(imgdir, f))
    for f in os.listdir(tmp):
        shutil.move(os.path.join(tmp, f), os.path.join(imgdir, f))
    L["slides"] = slides
    L["duration"] = D.ts(t)
    json.dump(L, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    core = sum(x["dur"] if "dur" in x else 0 for x in order if "new" not in x and "ZAMAN KALIRSA" not in x["rest"][:40])
    print("%s: %d slayt (%d yeni), toplam %s" % (lid, len(slides), len(mod.SLIDES), D.ts(t)))


if __name__ == "__main__":
    for lid in sys.argv[1:]:
        run(lid)
