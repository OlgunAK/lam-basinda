# -*- coding: utf-8 -*-
"""Ders günü için flaş belleğe atılacak paket: indir/flas.zip.

İçinde tek tıkla açılan kısayollar (perde, öğrenci sayfası, slaytlar),
perdeyi tam ekran açan bir .bat, kumanda karekodlu BASLAT.html ve internet
yoksa diye dört dersin PowerPoint dosyası var. pptx_yap.py'den sonra çalıştır.
"""
import base64, html, io, json, os, zipfile
import qrcode
import qrcode.image.svg

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(REPO, "indir")
SITE = "https://olgunak.github.io/lam-basinda/"
U = {"perde": SITE + "canli/perde.html", "kumanda": SITE + "canli/kumanda.html",
     "ogrenci": SITE + "canli/", "ana": SITE, "quiz": SITE + "quiz/"}
D = "LamBasinda/"


def url_file(u):
    return ("[InternetShortcut]\r\nURL=%s\r\n" % u).encode()


def bat(u):
    s = r'''@echo off
rem Perdeyi tam ekran acar (Chrome, yoksa Edge, yoksa varsayilan tarayici).
set "U=%s"
for %%%%P in ("%%ProgramFiles%%\Google\Chrome\Application\chrome.exe" "%%ProgramFiles(x86)%%\Google\Chrome\Application\chrome.exe" "%%LocalAppData%%\Google\Chrome\Application\chrome.exe" "%%ProgramFiles(x86)%%\Microsoft\Edge\Application\msedge.exe" "%%ProgramFiles%%\Microsoft\Edge\Application\msedge.exe") do (
  if exist %%%%P ( start "" %%%%P --new-window --start-fullscreen "%%U%%" & exit /b )
)
start "" "%%U%%"
''' % u
    return s.replace("\n", "\r\n").encode()


def qr_svg(u):
    img = qrcode.make(u, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
    b = io.BytesIO(); img.save(b)
    return "data:image/svg+xml;base64," + base64.b64encode(b.getvalue()).decode()


def page(info):
    cards = "\n".join(
        '<li><span class="d">%s</span> <b>%s</b> · %d slayt <a href="PowerPoint/%s">Aç</a></li>'
        % (html.escape(i["date"]), html.escape(i["title"]), i["slides"], i["file"]) for i in info)
    return """<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lam Başında · Başlat</title>
<style>
:root{--bg:#FBF8FC;--card:#fff;--ink:#24163A;--muted:#6B5D7B;--line:#E6DCEE;--hema:#4A2C82;--hema-soft:#EFE8FA;--eosin:#C2366A}
@media (prefers-color-scheme: dark){:root{--bg:#150E1E;--card:#20172C;--ink:#F2EBF7;--muted:#A898B9;--line:#382A49;--hema:#B9A0EE;--hema-soft:#2C2142;--eosin:#F27CA3;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:24px 16px 48px;display:flex;flex-direction:column;gap:18px}
h1{margin:0;font:700 1.7rem Georgia,serif}h2{margin:0 0 8px;font:700 1.15rem Georgia,serif}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
.big{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.btn{display:block;text-decoration:none;text-align:center;border-radius:12px;padding:18px 14px;font-weight:700;font-size:1.15rem;background:var(--hema);color:var(--bg)}
.btn.g{background:var(--hema-soft);color:var(--hema);border:1px solid var(--line)}
.btn small{display:block;font-weight:500;font-size:.8rem;opacity:.85}
.row{display:flex;gap:18px;align-items:center;flex-wrap:wrap}.row img{width:170px;height:170px;background:#fff;border-radius:10px;padding:6px}
.m{color:var(--muted);font-size:.9rem}ul{margin:0;padding-left:20px}li{margin:4px 0}.d{color:var(--eosin);font-weight:700;font-size:.85rem}
a{color:var(--hema)}code{background:var(--hema-soft);padding:1px 6px;border-radius:6px}
</style></head><body><main class="wrap">
<h1>Lam Başında · Ders günü</h1>
<section class="card"><h2>1 · Sınıf bilgisayarında</h2><div class="big">
<a class="btn" href="%(perde)s">Perdeyi aç<small>açılınca F11 ile tam ekran</small></a>
<a class="btn g" href="%(ogrenci)s">Öğrenci sayfası<small>öğrencilerin gördüğü</small></a>
<a class="btn g" href="%(ana)s">Slaytlar ve quizler<small>ana sayfa</small></a>
</div></section>
<section class="card"><h2>2 · Telefonunda kumanda</h2><div class="row">
<img alt="Kumanda karekodu" src="%(qr)s">
<div><p>Telefonun kamerasıyla okut, kumanda açılır. Google hesabınla gir, dersi seç.</p>
<p class="m">Adres: <a href="%(kumanda)s">%(kumanda)s</a></p></div></div></section>
<section class="card"><h2>İnternet yoksa: PowerPoint</h2>
<p class="m">Canlı ders (sorular, karekod, liderlik) internetsiz çalışmaz. Bu durumda dersi PowerPoint'ten anlat; sorular ve doğru cevaplar not bölümünde.</p>
<ul>%(cards)s</ul></section>
<section class="card"><h2>Kontrol listesi</h2><ul>
<li>Perde ilk kez açılıyorsa <b>Perde hesabıyla gir</b> kutusuna perde şifresini yaz (tarayıcı sonra hatırlar).</li>
<li>Telefonda kumanda Google hesabıyla girişli olsun; şarj ve internet (mobil veri yedek).</li>
<li>Perdede <code>F11</code> tam ekran, <code>→</code> <code>←</code> slayt, <code>L</code> katılım ekranı, <code>.</code> karartma.</li>
<li>Blok derste birinci ders bitince ikinci dersin oturumunu aç; öğrenciler tek dokunuşla geçer.</li>
<li>HDMI adaptörü ve tıklayıcı.</li>
</ul></section>
</main></body></html>""" % dict(U, qr=qr_svg(U["kumanda"]), cards=cards)


def oku():
    s = """LAM BASINDA - DERS GUNU FLASI

Bu klasoru flasa oldugu gibi kopyala.

  BASLAT.html              Cift tikla: perde, ogrenci sayfasi, kumanda karekodu, kontrol listesi
  1 - Perde (tam ekran).bat  Cift tikla: perdeyi Chrome/Edge'de tam ekran acar
  1 - Perde.url            Ayni sayfa, normal pencere (sonra F11)
  2 - Kumanda.url          Kumanda (telefonda acmak icin BASLAT.html'deki karekodu okut)
  3 - Ogrenci sayfasi.url  Ogrencilerin gordugu sayfa
  4 - Slaytlar ve quizler.url  Ana sayfa
  PowerPoint/              Internet yoksa: dort dersin slaytlari (notlar ve cevaplar ici)

Windows .bat dosyasi icin uyari verirse "Yine de calistir" de; istemezsen 1 - Perde.url kullan.

Adresler:
  Perde    %(perde)s
  Kumanda  %(kumanda)s
  Ogrenci  %(ogrenci)s
  Ana      %(ana)s
""" % U
    return s.replace("\n", "\r\n").encode()


def main():
    info = json.load(open(os.path.join(OUT, "dersler.json"), encoding="utf-8"))
    path = os.path.join(OUT, "flas.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(D + "BASLAT.html", page(info).encode())
        z.writestr(D + "OKU.txt", oku())
        z.writestr(D + "1 - Perde (tam ekran).bat", bat(U["perde"]))
        z.writestr(D + "1 - Perde.url", url_file(U["perde"]))
        z.writestr(D + "2 - Kumanda.url", url_file(U["kumanda"]))
        z.writestr(D + "3 - Ogrenci sayfasi.url", url_file(U["ogrenci"]))
        z.writestr(D + "4 - Slaytlar ve quizler.url", url_file(U["ana"]))
        for i in info:
            z.write(os.path.join(OUT, i["file"]), D + "PowerPoint/" + i["file"])
    print(path, round(os.path.getsize(path) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
