/* Slaytı tarayıcıda 1920×1080 JPG'ye çevirir.
   Kare önce görünmez bir sahnede çizilir (yazı sığdırma için gerçek ölçüm gerekir),
   sonra fontlar ve görseller gömülü bir SVG foreignObject içinde tuvale basılır. */
(function () {
  "use strict";
  var FONT_KOK = "../ortak/fontlar/";
  var cssGomulu = null;
  var gorselOnbellek = new Map();

  function blobToDataURL(b) {
    return new Promise(function (ok, hata) { var r = new FileReader(); r.onload = function () { ok(r.result); }; r.onerror = hata; r.readAsDataURL(b); });
  }
  async function urlToDataURL(url) {
    if (url.startsWith("data:")) return url;
    if (gorselOnbellek.has(url)) return gorselOnbellek.get(url);
    var p = fetch(url).then(function (r) { if (!r.ok) throw new Error("Görsel yüklenemedi: " + url); return r.blob(); }).then(blobToDataURL);
    gorselOnbellek.set(url, p);
    return p;
  }
  async function gomuluCSS() {
    if (cssGomulu) return cssGomulu;
    var css = Slayt.css(FONT_KOK);
    var urller = Array.from(new Set((css.match(/url\('([^']+)'\)/g) || []).map(function (m) { return m.slice(5, -2); })));
    for (var i = 0; i < urller.length; i++) {
      var d = await urlToDataURL(urller[i]);
      css = css.split("url('" + urller[i] + "')").join("url('" + d + "')");
    }
    cssGomulu = css;
    return css;
  }

  /* sahne: görünür olmayan ama yerleşimi yapılan 1920×1080 kutu; coz: görsel yolu → URL */
  async function kareJPEG(ders, f, sahne, coz, kalite) {
    sahne.innerHTML = Slayt.html(ders, f, { coz: coz });
    var imgs = Array.from(sahne.querySelectorAll("img"));
    await Promise.all(imgs.map(function (im) { return im.complete ? 0 : new Promise(function (r) { im.onload = im.onerror = r; }); }));
    await document.fonts.ready;
    Slayt.sigdir(sahne.firstChild);
    var kopya = sahne.firstChild.cloneNode(true);
    var kimg = Array.from(kopya.querySelectorAll("img"));
    for (var i = 0; i < kimg.length; i++) kimg[i].setAttribute("src", await urlToDataURL(kimg[i].src));
    var css = await gomuluCSS();
    var xml = new XMLSerializer().serializeToString(kopya);
    var svg = "<svg xmlns='http://www.w3.org/2000/svg' width='1920' height='1080'><foreignObject x='0' y='0' width='1920' height='1080'>" +
      "<div xmlns='http://www.w3.org/1999/xhtml'><style>" + css.replace(/</g, "\\3c ") + "</style>" + xml + "</div></foreignObject></svg>";
    var img = new Image();
    img.decoding = "sync";
    try {
      img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
      await img.decode();
      await new Promise(function (r) { setTimeout(r, 30); });
      var cv = document.createElement("canvas"); cv.width = 1920; cv.height = 1080;
      var cx = cv.getContext("2d");
      cx.fillStyle = "#000"; cx.fillRect(0, 0, 1920, 1080);
      cx.drawImage(img, 0, 0);
      return await new Promise(function (ok, hata) { cv.toBlob(function (b) { b ? ok(b) : hata(new Error("JPG üretilemedi")); }, "image/jpeg", kalite || 0.88); });
    } finally { img.src = ""; }
  }

  /* Yüklenen fotoğrafı en çok 1800 px kenarlı JPG'ye küçültür. */
  async function fotoKucult(dosya, enCok) {
    enCok = enCok || 1800;
    var bmp = await createImageBitmap(dosya);
    var o = Math.min(1, enCok / Math.max(bmp.width, bmp.height));
    var cv = document.createElement("canvas"); cv.width = Math.round(bmp.width * o); cv.height = Math.round(bmp.height * o);
    cv.getContext("2d").drawImage(bmp, 0, 0, cv.width, cv.height);
    return new Promise(function (ok) { cv.toBlob(ok, "image/jpeg", 0.9); });
  }

  window.Disa = { kareJPEG: kareJPEG, fotoKucult: fotoKucult, blobToDataURL: blobToDataURL };
})();
