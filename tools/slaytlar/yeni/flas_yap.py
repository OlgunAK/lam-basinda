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
    # Flaştaki zip'ten internetsiz açılır: site dosyalarına (ortak/tasarim.css, fontlar)
    # bağlanmaz. Rol token'ları ortak/tasarim.css'teki değerlerin kopyası; yazı sistem yazıları.
    cards = "\n".join(
        '<li><span class="b"><b>%s</b><span class="meta">%s · %d slayt</span></span><a class="btn q sm" href="PowerPoint/%s">Aç</a></li>'
        % (html.escape(i["title"]), html.escape(i["date"]), i["slides"], i["file"]) for i in info)
    return """<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lam Başında · Başlat</title>
<style>
:root{--c-bg:#FAF7FB;--c-surface:#FFFFFF;--c-surface-2:#F1ECF6;--c-text:#22163A;--c-text-2:#5E5070;--c-line:#E4DAEC;--c-line-strong:#8F80A3;
--c-accent:#4A2C82;--c-accent-soft:#EEE7F8;--c-on-accent:#FFFFFF;--c-now:#B0275B;--c-qr-bg:#FFFFFF;
--f-display:Georgia,"Times New Roman",serif;--f-body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
--s-1:4px;--s-2:8px;--s-3:12px;--s-4:16px;--s-5:24px;--s-6:32px;--s-7:48px;--r-sm:8px;--r-md:12px;--r-lg:16px;color-scheme:light}
@media (prefers-color-scheme: dark){:root{--c-bg:#160F21;--c-surface:#211830;--c-surface-2:#2D2243;--c-text:#F3EDF8;--c-text-2:#AFA1C2;--c-line:#4A3D60;--c-line-strong:#6E5F84;
--c-accent:#BBA3F0;--c-accent-soft:#2D2243;--c-on-accent:#160F21;--c-now:#F283AA;color-scheme:dark}}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--c-bg);color:var(--c-text);font:16px/1.5 var(--f-body);-webkit-font-smoothing:antialiased}
.wrap{max-width:880px;margin:0 auto;padding:var(--s-6) var(--s-4) var(--s-7);display:flex;flex-direction:column;gap:var(--s-4)}
h1,h2{margin:0;font-family:var(--f-display);font-weight:700;line-height:1.2;letter-spacing:-.01em;text-wrap:balance}
h1{font-size:1.75rem;margin-bottom:var(--s-2)}h2{font-size:1.125rem;margin-bottom:var(--s-3)}
p{margin:0;text-wrap:pretty;max-width:65ch}
.card{background:var(--c-surface);border:1px solid var(--c-line);border-radius:var(--r-lg);padding:var(--s-5)}
.big{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:var(--s-2)}
.btn{display:flex;flex-direction:column;justify-content:center;gap:2px;min-height:44px;text-decoration:none;text-align:center;border-radius:var(--r-md);border:1px solid transparent;padding:var(--s-4) var(--s-3);font-weight:700;font-size:1.125rem;line-height:1.25;background:var(--c-accent);color:var(--c-on-accent);transition-property:background-color,border-color,scale;transition-duration:150ms;transition-timing-function:ease-out}
.btn.q{background:var(--c-surface);color:var(--c-text);border-color:var(--c-line-strong)}
.btn:active{scale:.96}
@media (hover:hover){.btn:hover{background:color-mix(in oklab,var(--c-accent) 88%%,var(--c-text))}.btn.q:hover{background:var(--c-surface-2);border-color:var(--c-accent)}}
.btn small{font-weight:500;font-size:.8125rem;opacity:.85}
.btn.sm{flex:none;padding:0 var(--s-4);font-size:.875rem}
.row{display:flex;gap:var(--s-5);align-items:center;flex-wrap:wrap}
.row img{width:170px;height:170px;background:var(--c-qr-bg);border-radius:var(--r-md);padding:6px}
.row div{display:flex;flex-direction:column;gap:var(--s-2)}
.m,.meta{color:var(--c-text-2);font-size:.875rem}.meta{font-variant-numeric:tabular-nums}
ul{margin:0;padding-left:20px}li{margin:var(--s-1) 0}li::marker{color:var(--c-text-2)}
ul.decks{list-style:none;padding:0;margin-top:var(--s-3);display:flex;flex-direction:column}
ul.decks li{display:flex;align-items:center;gap:var(--s-3);margin:0;padding:var(--s-3) 0;border-top:1px solid var(--c-line)}
ul.decks .b{flex:1;display:flex;flex-direction:column}
a{color:var(--c-accent);text-underline-offset:.18em}
a:focus-visible{outline:3px solid var(--c-accent);outline-offset:2px}
::selection{background:var(--c-now);color:var(--c-on-accent)}
kbd{font:inherit;font-size:.875rem;font-weight:650;background:var(--c-surface-2);border:1px solid var(--c-line);border-radius:6px;padding:0 6px;font-variant-numeric:tabular-nums}
@media (prefers-reduced-motion:reduce){*{transition-duration:1ms!important}}
</style></head><body><main class="wrap">
<h1>Lam Başında · Ders günü</h1>
<section class="card"><h2>1 · Sınıf bilgisayarında</h2><div class="big">
<a class="btn" href="%(perde)s">Perdeyi aç<small>açılınca F11 ile tam ekran</small></a>
<a class="btn q" href="%(ogrenci)s">Öğrenci sayfası<small>öğrencilerin gördüğü</small></a>
<a class="btn q" href="%(ana)s">Slaytlar ve quizler<small>ana sayfa</small></a>
</div></section>
<section class="card"><h2>2 · Telefonunda kumanda</h2><div class="row">
<img alt="Kumanda karekodu" src="%(qr)s">
<div><p>Telefonun kamerasıyla okut, kumanda açılır. Google hesabınla gir, dersi seç.</p>
<p class="m">Adres: <a href="%(kumanda)s">%(kumanda)s</a></p></div></div></section>
<section class="card"><h2>İnternet yoksa: PowerPoint</h2>
<p class="m">Canlı ders (sorular, karekod, liderlik) internetsiz çalışmaz. Bu durumda dersi PowerPoint'ten anlat; sorular ve doğru cevaplar not bölümünde.</p>
<ul class="decks">%(cards)s</ul></section>
<section class="card"><h2>Kontrol listesi</h2><ul>
<li>Perde ilk kez açılıyorsa <b>Perde hesabıyla gir</b> kutusuna perde şifresini yaz (tarayıcı sonra hatırlar).</li>
<li>Telefonda kumanda Google hesabıyla girişli olsun; şarj ve internet (mobil veri yedek).</li>
<li>Perdede <kbd>F11</kbd> tam ekran, <kbd>→</kbd> <kbd>←</kbd> slayt, <kbd>L</kbd> katılım ekranı, <kbd>.</kbd> karartma.</li>
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
