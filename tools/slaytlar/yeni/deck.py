# -*- coding: utf-8 -*-
"""HTML slide builder for new lessons (M3, M4).

Each slide is an HTML page in the M1/M2 look (Lora titles, Lato text, navy and
white themes). render.mjs turns the pages into 1920x1080 JPGs; this module also
writes the lesson JSON (notes with time stamps, CANLI blocks, questions).

Book figures are read from FOTO (see foto.py); fonts from ../fonts.
"""
import html, json, os, re, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CANLI = os.path.join(REPO, "canli")
FONTS = os.path.abspath(os.path.join(HERE, "..", "fonts"))
WORK = os.environ.get("DECK_WORK", os.path.join(HERE, "_work"))

C = dict(navy="#24163A", navy2="#392F54", purple="#442F67", pink="#BE285A", yellow="#F0B41E",
         lilac="#F4EEF8", rose="#FAE9EF", soft="#C8BED7", grey="#786E87", opt="#7C5BB6",
         green="#17744E", red="#AA2832")

E = html.escape

CSS = """
@font-face{font-family:Lora;src:url('file://%(f)s/Lora[wght].ttf');font-weight:400 700}
@font-face{font-family:Lora;font-style:italic;src:url('file://%(f)s/Lora-Italic[wght].ttf');font-weight:400 700}
@font-face{font-family:Lato;src:url('file://%(f)s/Lato-Regular.ttf');font-weight:400}
@font-face{font-family:Lato;src:url('file://%(f)s/Lato-Italic.ttf');font-weight:400;font-style:italic}
@font-face{font-family:Lato;src:url('file://%(f)s/Lato-Bold.ttf');font-weight:700}
@font-face{font-family:Lato;src:url('file://%(f)s/Lato-BoldItalic.ttf');font-weight:700;font-style:italic}
@font-face{font-family:Lato;src:url('file://%(f)s/Lato-Black.ttf');font-weight:900}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
.s{width:1920px;height:1080px;position:relative;overflow:hidden;font-family:Lato,sans-serif}
.dark{background:%(navy)s;color:#fff}
.light{background:#fff;color:%(navy)s}
.t{position:absolute;left:86px;top:78px;right:300px;margin:0;font:700 60px/1.12 Lora,serif;letter-spacing:-.2px}
.t.sm{font-size:52px;top:84px}
.t.xs{font-size:46px;top:90px}
.tag{position:absolute;right:70px;top:52px;border-radius:999px;padding:7px 16px 8px;font:700 22px Lato}
.tag.dus{background:%(yellow)s;color:%(navy)s;font-weight:900}
.tag.opt{background:%(grey)s;color:#fff;font-size:20px}
.tag.pink{background:%(pink)s;color:#fff}
.tag.yel{background:%(yellow)s;color:%(navy)s}
.body{position:absolute;left:86px;right:86px;top:192px;bottom:98px}
.foot{position:absolute;left:86px;top:1019px;font-size:18px;white-space:nowrap;display:flex;align-items:center;gap:10px}
.light .foot{color:#4a3f5a}.dark .foot{color:#d2ccd8}
.cred{position:absolute;right:178px;top:1009px;width:820px;text-align:right;font:italic 16px/1.35 Lato;color:%(grey)s}
.dark .cred{color:#a79cb8}
.num{position:absolute;right:106px;top:1019px;font-size:18px;color:#9a90a8}
.strip{display:flex;gap:8px;margin-left:18px}
.strip span{border-radius:999px;padding:5px 13px 6px;font:700 20px Lato;background:%(lilac)s;color:%(grey)s}
.dark .strip span{background:%(navy2)s;color:#aaa0be}
.strip span.on{background:%(yellow)s;color:%(navy)s}
.strip span.nm{background:%(pink)s;color:#fff;font-weight:900}
.row{display:flex;gap:22px}
.body>.row,.body>.col{height:100%%}
.col{display:flex;flex-direction:column;gap:22px}
.ph{position:relative;overflow:hidden;background:#ddd;border:4px solid #fff;box-shadow:0 2px 10px rgba(36,22,58,.22);flex:1 1 0}
.dark .ph{border-color:#fff}
.ph.hl{border-color:%(yellow)s;border-width:6px}
.ph img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.ph .cap{position:absolute;left:0;right:0;bottom:0;background:rgba(36,22,58,.84);color:#fff;padding:12px 18px 13px;font:700 28px/1.2 Lato}
.ph .cap small{display:block;font:400 19px/1.3 Lato;color:%(soft)s;margin-top:3px}
.ph .lab{position:absolute;left:14px;top:12px;background:%(yellow)s;color:%(navy)s;font:900 30px Lato;border-radius:10px;padding:4px 14px}
.box{border-radius:16px;padding:26px 30px}
.box h3{margin:0 0 12px;font:700 32px/1.2 Lora,serif}
.box.navy{background:%(navy)s;color:#fff}.box.navy h3{color:%(yellow)s}
.box.navy2{background:%(navy2)s;color:#fff}.box.navy2 h3{color:%(yellow)s}
.box.lilac{background:%(lilac)s;color:%(navy)s}.box.lilac h3{color:%(purple)s}
.box.rose{background:%(rose)s;color:%(navy)s}.box.rose h3{color:%(pink)s}
.box.yellow{background:%(yellow)s;color:%(navy)s}.box.yellow h3{color:%(navy)s}
.box.pink{background:%(pink)s;color:#fff}.box.pink h3{color:#fff}
.box p{margin:0 0 8px}
.box .k{font-weight:700}
.box.navy .k,.box.navy2 .k{color:%(yellow)s}
.box.lilac .k{color:%(purple)s}.box.rose .k{color:%(pink)s}
ul.b{margin:0;padding:0;list-style:none}
ul.b li{position:relative;padding-left:32px;margin:0 0 12px;line-height:1.3}
ul.b li:before{content:'';position:absolute;left:4px;top:.55em;width:9px;height:9px;border-radius:50%%;background:currentColor}
.light ul.b li:before{background:%(pink)s}
.box.navy ul.b li:before,.box.navy2 ul.b li:before{background:%(yellow)s}
.box.lilac ul.b li:before{background:%(purple)s}
.pato{border-radius:16px;background:%(navy)s;color:#fff;padding:24px 30px 24px 34px;border-left:12px solid %(yellow)s;position:relative}
.pato .pl{display:inline-block;background:%(pink)s;color:#fff;font:900 20px Lato;letter-spacing:1px;border-radius:999px;padding:6px 14px;margin-bottom:12px}
.pato h3{margin:0 0 8px;font:700 32px/1.2 Lora;color:%(yellow)s}
.live{display:inline-block;background:%(yellow)s;color:%(navy)s;font:700 30px Lato;border-radius:12px;padding:14px 22px;min-width:560px}
.qq{font:700 42px/1.25 Lora,serif;margin:34px 0 0}
.opts{margin-top:40px}
.opt{display:flex;align-items:center;gap:22px;margin-bottom:20px;font-size:31px;line-height:1.25}
.opt b{flex:0 0 64px;height:64px;border-radius:50%%;background:%(opt)s;color:#fff;display:flex;align-items:center;justify-content:center;font:700 30px Lato}
.big{font:700 40px/1.25 Lora,serif}
.num-circle{flex:0 0 100px;height:100px;border-radius:50%%;background:%(purple)s;color:#fff;display:flex;align-items:center;justify-content:center;font:700 46px Lora}
.mono{font-family:'DejaVu Sans Mono',monospace;font-weight:700}
.arrow{color:%(pink)s;font-weight:900}
table.t2{border-collapse:separate;border-spacing:0 10px;width:100%%;font-size:27px}
table.t2 td{padding:14px 20px;background:%(lilac)s;vertical-align:middle}
table.t2 td:first-child{border-radius:14px 0 0 14px;font-weight:700;color:%(purple)s}
table.t2 td:last-child{border-radius:0 14px 14px 0}
table.t2 tr.hot td{background:%(rose)s}
table.t2 tr.hot td:first-child{color:%(pink)s}
table.t2 th{font:700 22px Lato;color:%(grey)s;text-align:left;padding:0 20px}
""" % dict(C, f=FONTS)


# ---------------- small HTML helpers ----------------
def md(s):
    """Very small inline markup: **bold**, *italic*, ->, (lt) escapes everything else."""
    s = E(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<span class='k'>\1</span>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = s.replace("-&gt;", "<span class='arrow'>→</span>")
    return s


def bl(items, size=32, gap=12, cls=""):
    lis = "".join("<li style='margin-bottom:%dpx'>%s</li>" % (gap, md(i)) for i in items)
    return "<ul class='b %s' style='font-size:%dpx'>%s</ul>" % (cls, size, lis)


def box(kind, title=None, lines=None, size=28, html_=None, style="", gap=8):
    h = "<h3>%s</h3>" % md(title) if title else ""
    if html_ is not None:
        inner = html_
    elif isinstance(lines, str):
        inner = "<p style='font-size:%dpx;line-height:1.32'>%s</p>" % (size, md(lines))
    else:
        inner = "".join("<p style='font-size:%dpx;line-height:1.3;margin-bottom:%dpx'>%s</p>" % (size, gap, md(l)) for l in (lines or []))
    return "<div class='box %s' style='%s'>%s%s</div>" % (kind, style, h, inner)


def pato(title, text, size=27, style=""):
    t = text if isinstance(text, list) else [text]
    ps = "".join("<p style='margin:0 0 8px;font-size:%dpx;line-height:1.32'>%s</p>" % (size, md(x)) for x in t)
    return "<div class='pato' style='%s'><div class='pl'>PATOLOĞUN NOTU</div><h3>%s</h3>%s</div>" % (style, md(title), ps)


def ph(src, cap=None, sub=None, pos="50% 50%", style="", hl=False, label=None, fit="cover", bg=None):
    """Photo with the dark caption bar."""
    c = ""
    if cap:
        c = "<div class='cap'>%s%s</div>" % (md(cap), "<small>%s</small>" % md(sub) if sub else "")
    lab = "<div class='lab'>%s</div>" % E(label) if label else ""
    st = "object-position:%s;object-fit:%s" % (pos, fit)
    b = ";background:%s" % bg if bg else ""
    return "<div class='ph%s' style='%s%s'><img src='file://%s' style='%s'>%s%s</div>" % (
        " hl" if hl else "", style, b, src, st, lab, c)


def row(*kids, gap=22, style="", align="stretch"):
    return "<div class='row' style='gap:%dpx;align-items:%s;%s'>%s</div>" % (gap, align, style, "".join(kids))


def col(*kids, gap=22, style=""):
    return "<div class='col' style='gap:%dpx;%s'>%s</div>" % (gap, style, "".join(kids))


def div(inner, style=""):
    return "<div style='%s'>%s</div>" % (style, inner)


def numbered(items, size=36, numsize=None):
    """Five-sentences style list: yellow serif numbers."""
    out = []
    for i, t in enumerate(items, 1):
        out.append("<div style='display:flex;gap:60px;align-items:baseline;margin-bottom:46px'>"
                   "<span style='font:700 74px/1 Lora;color:%s;width:70px'>%d</span>"
                   "<span style='font-size:%dpx;line-height:1.3'>%s</span></div>" % (C["yellow"], i, size, md(t)))
    return "".join(out)


def steps(items, size=30):
    """Numbered circles with a pink label and a text column (diagnosis slide style)."""
    out = []
    for i, (lab, txt) in enumerate(items, 1):
        bg = C["pink"] if i == len(items) else C["purple"]
        out.append("<div style='display:flex;align-items:center;gap:32px;margin-bottom:26px'>"
                   "<div class='num-circle' style='background:%s'>%d</div>"
                   "<div style='flex:0 0 290px;font:700 36px Lora;color:%s'>%s</div>"
                   "<div style='font-size:%dpx;line-height:1.3'>%s</div></div>" % (bg, i, C["pink"], md(lab), size, md(txt)))
    return "".join(out)


# ---------------- slide shell ----------------
class Lesson:
    def __init__(self, lid, title, short, date, frame=None, strip=None, cta=None, ver="3", quiz=None):
        self.lid, self.title, self.short, self.date = lid, title, short, date
        self.frame, self.strip_cfg, self.cta, self.ver, self.quiz = frame, strip, cta, ver, quiz
        self.slides = []      # dicts
        self.questions = []
        self.qmap = {}

    def q(self, **q):
        q.setdefault("t", T_BY_TYPE[q["type"]])
        self.questions.append(q)
        self.qmap[q["id"]] = q
        return q["id"]

    def add(self, **s):
        self.slides.append(s)

    # one slide's html
    def page(self, s, n):
        theme = s.get("theme", "light")
        if s.get("raw"):
            inner = s["raw"]
        else:
            cls = "t" + ({"sm": " sm", "xs": " xs"}.get(s.get("tsize"), ""))
            inner = "<h1 class='%s'>%s</h1>" % (cls, md(s.get("heading", s["title"])))
            tag = None
            if s.get("optional"):
                tag = ("opt", "ZAMAN KALIRSA")
            elif s.get("tag"):
                tag = s["tag"]
            elif s.get("dus"):
                tag = ("dus", "DUS")
            if tag:
                inner += "<div class='tag %s'>%s</div>" % (tag[0], E(tag[1]))
            inner += "<div class='body' style='%s'>%s</div>" % (s.get("bstyle", ""), s.get("body", ""))
            strip = ""
            if s.get("strip") is not None and self.strip_cfg:
                name, labels = self.strip_cfg
                spans = "<span class='nm'>%s</span>" % E(name) + "".join(
                    "<span class='%s'>%s</span>" % ("on" if i in s["strip"] else "", E(l)) for i, l in enumerate(labels, 1))
                strip = "<div class='strip'>%s</div>" % spans
            inner += "<div class='foot'>%s  ·  4. Sınıf Patoloji%s</div>" % (E(self.short), strip)
            if s.get("cred"):
                inner += "<div class='cred'>Görseller: %s</div>" % md(s["cred"])
            if not s.get("nonum"):
                inner += "<div class='num'>%d</div>" % n
        return ("<!doctype html><html><head><meta charset='utf-8'><style>%s</style></head>"
                "<body><div class='s %s'>%s</div></body></html>") % (CSS, theme, inner)

    # ---------------- build ----------------
    def build(self, only=None):
        out_html = os.path.join(WORK, self.lid)
        if os.path.exists(out_html):
            shutil.rmtree(out_html)
        os.makedirs(out_html)
        out_img = os.path.join(CANLI, "slaytlar", self.lid)
        os.makedirs(out_img, exist_ok=True)
        jobs = []
        slides_json = []
        t = 0
        n = 0
        for s in self.slides:
            n += 1
            dur = s["dur"]
            stamp = "[%s–%s]" % (ts(t), ts(t + dur))
            if s.get("optional"):
                stamp += " ZAMAN KALIRSA; yoksa → ile atla."
            notes = stamp + "\n" + s.get("notes", "").strip()
            if s.get("board"):
                j = {"board": True, "title": s["title"], "notes": notes}
                if s.get("top"):
                    j["top"] = s["top"]
                slides_json.append(j); t += dur; continue
            if s.get("cloud"):
                slides_json.append({"cloud": s["cloud"], "title": s["title"], "notes": notes}); t += dur; continue
            title = s["title"]
            if s.get("optional"):
                title = "(Zaman kalırsa) " + title
            j = {"img": "slaytlar/%s/%02d.jpg?v=%s" % (self.lid, n, self.ver), "title": title}
            if s.get("lobby"):
                j["lobby"] = True
            if s.get("qopen"):
                j["qopen"] = s["qopen"]
                qq = self.qmap[s["qopen"]]
                notes += ("\n\nCANLI (%s, %s): Soru bu slayta gelince telefonlarda açılır; perde slaytı göstermeye devam eder. "
                          "Oylama bir sonraki slayta (dağılım) kadar açık kalır, geri gelsen de kapanmaz. → sonraki slayt. T: %d sn."
                          % (qq["id"], TYPE_TR[qq["type"]], qq["t"]))
            if s.get("q"):
                j["q"] = s["q"]
                qq = self.qmap[s["q"]]
                if s.get("cont"):
                    notes += "\n\nCANLI (%s, %s): Soru önceki slaytta açıldı, oylama hâlâ açık. → oylamayı kapatıp dağılımı gösterir, → sonraki slayt%s." % (
                        qq["id"], TYPE_TR[qq["type"]],
                        (" (tahmin anketi; cevap açılmaz). Doğru: " + "ABCDE"[qq["a"]]) if qq.get("a") is not None and qq.get("hide") else "")
                else:
                    notes += "\n\n" + live_block(qq, lobby=bool(s.get("lobby")))
            j["notes"] = notes
            slides_json.append(j)
            fn = os.path.join(out_html, "%02d.html" % n)
            open(fn, "w", encoding="utf-8").write(self.page(s, n))
            if only is None or n in only:
                jobs.append([fn, os.path.join(out_img, "%02d.jpg" % n)])
            t += dur
        # drop stale jpgs
        keep = {"%02d.jpg" % i for i in range(1, n + 1)}
        for f in os.listdir(out_img):
            if f not in keep:
                os.remove(os.path.join(out_img, f))
        json.dump(jobs, open(os.path.join(out_html, "jobs.json"), "w"))
        r = subprocess.run(["node", os.path.join(HERE, "render.mjs"), os.path.join(out_html, "jobs.json")],
                           capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode:
            print(r.stderr); raise SystemExit("render failed")
        L = {"id": self.lid, "title": self.title, "date": self.date, "questions": self.questions,
             "slides": slides_json, "duration": ts(t)}
        if self.cta:
            L["cta"] = self.cta
        if self.frame:
            L["frame"] = self.frame
        if self.quiz:
            L["quiz"] = self.quiz   # ders sonunda telefonda quiz bağlantısı
        json.dump(L, open(os.path.join(CANLI, "dersler", self.lid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        core = sum(s["dur"] for s in self.slides if not s.get("optional"))
        print("%s: %d slayt, %d soru, toplam %s (çekirdek %s)" % (self.lid, n, len(self.questions), ts(t), ts(core)))
        return L


def ts(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


T_BY_TYPE = {"WORDCLOUD": 45, "POLL": 45, "MCQ": 30, "IMGMCQ": 30, "FINDIMG": 30, "SCT": 45,
             "OPEN": 75, "SORTGROUP": 60, "SORTORDER": 60, "MATCH": 60}
TYPE_TR = {"WORDCLOUD": "Kelime bulutu", "POLL": "Anket", "MCQ": "Çoktan seçmeli", "IMGMCQ": "Görselli çoktan seçmeli",
           "FINDIMG": "Görüntüde bul", "SCT": "Senaryo uyum testi (SCT)", "OPEN": "Açık uçlu",
           "SORTGROUP": "Sıralama (gruplama)", "SORTORDER": "Sıralama", "MATCH": "Eşleştirme"}


def live_block(q, lobby=False):
    t = q["t"]; typ = q["type"]
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


# ---------------- ready-made bodies ----------------
TYPE_PILL = {"MCQ": "Çoktan seçmeli", "POLL": "Anket", "IMGMCQ": "Görselli çoktan seçmeli", "SCT": "Senaryo uyum testi",
             "MATCH": "Eşleştirme", "SORTGROUP": "Gruplama", "OPEN": "Açık uçlu", "WORDCLOUD": "Kelime bulutu", "FINDIMG": "Görüntüde bul"}


def qbody(q, photo=None, qsize=42, osize=31, extra=""):
    """MCQ/POLL slide body like M2/19: live pill, question, options; optional photo on the right."""
    pill = "<div class='live'>CANLI · %s · %s</div>" % (q["id"], TYPE_PILL[q["type"]])
    opts = ""
    if q.get("opts"):
        opts = "<div class='opts'>" + "".join("<div class='opt' style='font-size:%dpx'><b>%s</b><span>%s</span></div>" % (osize, "ABCDE"[i], md(o))
                                            for i, o in enumerate(q["opts"])) + "</div>"
    left = pill + "<div class='qq' style='font-size:%dpx'>%s</div>%s%s" % (qsize, md(q["q"]), extra, opts)
    if photo:
        return row(div(left, "flex:0 0 900px"), div(photo, "flex:1;display:flex;margin-top:0;height:793px"), gap=40)
    return left


def title_page(kicker, title, sub, date_author, teaser, img, cred, pos="50% 50%"):
    """Lobby slide: navy panel on the left, full-height picture on the right (M1/01 look)."""
    return ("<div style='position:absolute;left:0;top:0;width:1238px;height:1080px;background:%(navy)s'></div>"
            "<div style='position:absolute;left:1238px;top:0;right:0;height:1080px;overflow:hidden'>"
            "<img src='file://%(img)s' style='width:100%%;height:100%%;object-fit:cover;object-position:%(pos)s'></div>"
            "<div style='position:absolute;left:115px;top:100px;font:700 26px Lato;letter-spacing:3px;color:%(yellow)s'>%(kicker)s</div>"
            "<div style='position:absolute;left:115px;top:%(ttop)spx;width:1080px;font:700 %(tsz)spx/1.08 Lora;color:#fff'>%(title)s</div>"
            "<div style='position:absolute;left:115px;top:%(stop)spx;width:1060px;font:400 38px/1.3 Lato;color:#eee8f4'>%(sub)s</div>"
            "<div style='position:absolute;left:115px;top:808px;font:400 29px Lato;color:#fff'>%(da)s</div>"
            "<div style='position:absolute;left:112px;top:880px;width:1068px;background:%(yellow)s;border-radius:18px;padding:22px 28px;font:700 37px/1.25 Lora;color:%(navy)s'>%(teaser)s</div>"
            "<div style='position:absolute;left:1280px;right:30px;top:1006px;font:italic 16px/1.35 Lato;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.8)'>Görseller: %(cred)s</div>"
            ) % dict(C, tsz=92 if len(title) <= 28 else 80, ttop=380 if len(title) > 22 else 460, stop=610 if len(title) > 22 else 590, img=img, pos=pos, kicker=E(kicker), title=md(title), sub=md(sub), da=E(date_author), teaser=md(teaser), cred=md(cred))


def qmark(text="Devamı dersin sonunda", style=""):
    return ("<div style='flex:1 1 0;border-radius:14px;background:%s;display:flex;flex-direction:column;align-items:center;justify-content:center;%s'>"
            "<div style='font:700 150px/1 Lora;color:%s'>?</div><div style='font:700 24px Lato;color:%s;margin-top:28px'>%s</div></div>") % (
        C["navy2"], style, C["yellow"], C["soft"], E(text))


def grid_img(paths, out, labels="ABCD", cols=2, cell=(800, 560), crops=None):
    """Question picture for the phones: photos in a grid with A/B/C/D labels."""
    from PIL import Image, ImageDraw, ImageFont
    n = len(paths); rows = (n + cols - 1) // cols
    W, H = cell; g = 12
    im = Image.new("RGB", (cols * W + (cols + 1) * g, rows * H + (rows + 1) * g), (36, 22, 58))
    f = ImageFont.truetype(os.path.join(FONTS, "Lato-Black.ttf"), 64)
    d = ImageDraw.Draw(im)
    for i, p in enumerate(paths):
        ph = Image.open(p).convert("RGB")
        r = max(W / ph.width, H / ph.height)
        ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
        cx, cy = (crops[i] if crops else (0.5, 0.5))
        x0 = int((ph.width - W) * cx); y0 = int((ph.height - H) * cy)
        ph = ph.crop((x0, y0, x0 + W, y0 + H))
        x = g + (i % cols) * (W + g); y = g + (i // cols) * (H + g)
        im.paste(ph, (x, y))
        d.rounded_rectangle((x + 14, y + 14, x + 104, y + 104), 14, fill=(240, 180, 30))
        b = f.getbbox(labels[i])
        d.text((x + 59 - (b[2] - b[0]) / 2 - b[0], y + 59 - (b[3] - b[1]) / 2 - b[1]), labels[i], font=f, fill=(36, 22, 58))
    im.save(out, quality=86)
    return out
