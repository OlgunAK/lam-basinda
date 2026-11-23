# -*- coding: utf-8 -*-
"""Tükürük bezlerinin yerini gösteren yandan baş çizimi (canli/img/M4/bezler_*.svg).
Her dosyada sözü edilen bez eozin pembesiyle vurgulanır."""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "canli", "img", "M4")
ON, OFF, CIZGI, DERI, YAZI, YAZI2 = "#B0275B", "#D8CCEA", "#4A2C82", "#6B5D7B", "#24163A", "#6B5D7B"
F = "font-family='Figtree, Arial, sans-serif'"


def svg(aktif):
    a = lambda k: ON if k in aktif else OFF
    y = lambda k: (ON, 700) if k in aktif else (YAZI2, 500)
    p = ["<svg xmlns='http://www.w3.org/2000/svg' viewBox='15 45 560 600' width='560' height='600'>",
         "<rect x='15' y='45' width='560' height='600' fill='#F7F3FB'/>",
         # baş ve boyun
         "<path d='M330 60 C230 60 168 120 162 205 C160 232 152 252 142 270 L104 322 L136 336 L130 362 C120 372 121 386 129 393 "
         "L121 405 L133 414 C126 428 129 441 141 452 C152 472 165 486 195 494 C245 503 305 497 362 472 L392 455 "
         "C420 440 470 430 505 400 C548 350 562 260 544 175 C524 100 445 60 330 60 Z' fill='#FBEFEA' stroke='%s' stroke-width='3'/>" % DERI,
         "<path d='M252 497 C255 580 262 660 266 750' fill='none' stroke='%s' stroke-width='3'/>" % DERI,
         "<path d='M470 425 C478 540 492 650 505 750' fill='none' stroke='%s' stroke-width='3'/>" % DERI,
         # kulak
         "<ellipse cx='462' cy='292' rx='22' ry='42' fill='#F6E2DA' stroke='%s' stroke-width='3'/>" % DERI,
         # mandibula (kesikli)
         "<path d='M150 462 C210 488 310 486 388 458 L410 300' fill='none' stroke='%s' stroke-width='3' stroke-dasharray='9 7'/>" % DERI,
         # ağız boşluğu: damak ve dil
         "<path d='M138 396 C200 380 285 376 345 392 L345 404 C290 392 200 396 138 404 Z' fill='#F1D7DF' stroke='%s' stroke-width='2'/>" % DERI,
         "<path d='M150 414 C205 402 292 402 340 420 C312 448 205 452 152 432 Z' fill='#E9B7C3' stroke='%s' stroke-width='2'/>" % DERI,
        ]
    # küçük bezler: damak boyunca, dudakta ve yanakta noktalar
    for x in range(168, 336, 20):
        p.append("<circle cx='%d' cy='%d' r='6' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, 386 if x < 300 else 389, a("kucuk"), CIZGI))
    for cx, cy in ((134, 384), (138, 420), (262, 360)):
        p.append("<circle cx='%d' cy='%d' r='6' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, a("kucuk"), CIZGI))
    # sublingual: ağız tabanında, dilin altında
    p.append("<ellipse cx='228' cy='458' rx='52' ry='13' fill='%s' stroke='%s' stroke-width='2.5'/>" % (a("sublingual"), CIZGI))
    # submandibuler ve Wharton kanalı
    p.append("<ellipse cx='332' cy='506' rx='58' ry='32' fill='%s' stroke='%s' stroke-width='2.5'/>" % (a("submandibuler"), CIZGI))
    p.append("<path d='M300 494 C262 478 220 466 182 448' fill='none' stroke='%s' stroke-width='3' stroke-dasharray='6 5'/>" % CIZGI)
    # parotis ve Stensen kanalı
    p.append("<path d='M412 268 C446 312 458 372 438 436 C410 450 384 440 374 410 C364 368 378 312 412 268 Z' fill='%s' stroke='%s' stroke-width='2.5'/>" % (a("parotis"), CIZGI))
    p.append("<path d='M384 360 C350 368 322 376 300 384' fill='none' stroke='%s' stroke-width='3' stroke-dasharray='6 5'/>" % CIZGI)

    def etiket(x, y0, metin, alt, hx, hy, k):
        c, w = y(k)
        p.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 8, hx, hy, c))
        p.append("<text x='%d' y='%d' %s font-size='36' font-weight='%d' fill='%s'>%s</text>" % (x - (0 if x > hx else 0), y0, F, w, c if k in aktif else YAZI, metin))
        if alt:
            p.append("<text x='%d' y='%d' %s font-size='25' fill='%s'>%s</text>" % (x, y0 + 26, F, YAZI2, alt))
    etiket(412, 500, "Parotis", "Stensen kanalı", 430, 420, "parotis")
    etiket(300, 600, "Submandibuler", "Wharton kanalı", 350, 535, "submandibuler")
    etiket(30, 560, "Sublingual", "ağız tabanı", 200, 468, "sublingual")
    etiket(20, 200, "Küçük bezler", "damak, dudak, yanak", 180, 380, "kucuk")
    p.append("</svg>")
    return "".join(p)


for ad, aktif in (("parotis", {"parotis"}), ("submandibuler_kucuk", {"submandibuler", "kucuk"}), ("sublingual", {"sublingual"}),
                  ("hepsi", {"parotis", "submandibuler", "sublingual", "kucuk"})):
    open(os.path.join(OUT, "bezler_%s.svg" % ad), "w", encoding="utf-8").write(svg(aktif))
print("ok")
