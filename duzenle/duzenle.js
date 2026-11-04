/* Lam Başında düzenleyici.
   İki çeşit ders var:
   - kaynaklı ders (canli/dersler/kaynak/<ID>.json): slaytın metni, görseli, sorusu, notu düzenlenir;
     kaydedince değişen slaytlar yeniden çizilir, canlı ders dosyası yeniden yazılır.
   - hazır ders (yalnız canli/dersler/<ID>.json, M1 ve M2 gibi): slayt resmi değiştirilir, başlık,
     konuşma notu ve sorular düzenlenir. */
(function () {
  "use strict";
  var $ = function (s, k) { return (k || document).querySelector(s); };
  var KOK = "../canli/";
  var TIPLER = { adim: "Adım adım", soru: "Soru", kutular: "Plan / kutular", tablo: "Tablo", kaynaklar: "Kaynaklar", kapak: "Kapak", ozet: "Özet (sentez)",
    liderlik: "Liderlik", bulut: "Kelime bulutu", resim: "Resim" };
  var SORU_TUR = ["MCQ", "POLL", "IMGMCQ", "WORDCLOUD", "OPEN", "MATCH", "SCT", "FINDIMG", "SORTGROUP", "SORTORDER"];
  var TONLAR = [["mor", "Mor (açık)"], ["pembe", "Pembe (açık)"], ["koyu", "Koyu mor"], ["vurgu", "Vurgu (pembe dolu)"]];
  var KONUM = [["", "Orta"], ["50% 0%", "Üst"], ["50% 100%", "Alt"], ["0% 50%", "Sol"], ["100% 50%", "Sağ"]];

  var S = {
    index: [], id: null, mod: "kaynak", D: null, D0: null, secili: 0, adim: 0, sekme: "slayt", soru: 0,
    kirli: new Set(), hepsi: false, yeni: new Map(), gecmis: [], galeriCb: null
  };

  /* ---------------- yardımcılar ---------------- */
  function kopya(x) { return JSON.parse(JSON.stringify(x)); }
  function h(tag, at, cocuk) {
    var e = document.createElement(tag);
    if (at) Object.keys(at).forEach(function (k) {
      if (k === "on") Object.keys(at.on).forEach(function (o) { e.addEventListener(o, at.on[o]); });
      else if (k === "text") e.textContent = at.text;
      else if (k === "html") e.innerHTML = at.html;
      else if (at[k] === true) e.setAttribute(k, "");
      else if (at[k] !== false && at[k] != null) e.setAttribute(k, at[k]);
    });
    (cocuk || []).forEach(function (c) { if (c != null) e.append(c); });
    return e;
  }
  function ikon(ad) { var s = document.createElementNS("http://www.w3.org/2000/svg", "svg"); var u = document.createElementNS("http://www.w3.org/2000/svg", "use"); u.setAttribute("href", "#i-" + ad); s.append(u); return s; }
  function ikonBtn(ad, baslik, fn, cls) {
    return h("button", { type: "button", class: "ikon-btn " + (cls || ""), title: baslik, "aria-label": baslik, on: { click: fn } }, [ikon(ad)]);
  }
  function kucukBtn(ad, yazi, fn) { return h("button", { type: "button", class: "kucuk-btn", on: { click: fn } }, [ad ? ikon(ad) : null, yazi]); }
  function coz(src) {
    if (!src) return "";
    if (S.yeni.has(src)) return S.yeni.get(src).url;
    return KOK + src;
  }
  function slaytlar() { return S.mod === "kaynak" ? S.D.slaytlar : S.D.slides; }
  function sorular() { return S.mod === "kaynak" ? (S.D.sorular = S.D.sorular || []) : (S.D.questions = S.D.questions || []); }

  /* ---------------- taslak (bu tarayıcıda) ---------------- */
  var IDB = null;
  function idb() {
    if (IDB) return IDB;
    IDB = new Promise(function (ok, hata) {
      var r = indexedDB.open("lb-duzenle", 1);
      r.onupgradeneeded = function () { r.result.createObjectStore("dosya"); };
      r.onsuccess = function () { ok(r.result); }; r.onerror = function () { hata(r.error); };
    });
    return IDB;
  }
  async function idbYaz(k, v) { try { var db = await idb(); db.transaction("dosya", "readwrite").objectStore("dosya").put(v, k); } catch (e) {} }
  async function idbOku(k) { try { var db = await idb(); return await new Promise(function (ok) { var r = db.transaction("dosya").objectStore("dosya").get(k); r.onsuccess = function () { ok(r.result); }; r.onerror = function () { ok(null); }; }); } catch (e) { return null; } }
  async function idbSil(k) { try { var db = await idb(); db.transaction("dosya", "readwrite").objectStore("dosya").delete(k); } catch (e) {} }

  var taslakZaman = null;
  function taslakSakla() {
    clearTimeout(taslakZaman);
    taslakZaman = setTimeout(function () {
      var yeni = {}; S.yeni.forEach(function (v, k) { yeni[k] = v.blob; });
      idbYaz("taslak-" + S.id, { D: S.D, D0: S.D0, mod: S.mod, kirli: Array.from(S.kirli), hepsi: S.hepsi, yeni: yeni, zaman: Date.now() });
    }, 400);
  }

  /* ---------------- değişiklik ---------------- */
  function degisti(etki) {
    // etki: sayı (slayt sırası), "hepsi", "sonrasi:<i>", "yok"
    if (etki === "hepsi") S.hepsi = true;
    else if (typeof etki === "string" && etki.indexOf("sonrasi:") === 0) { var i = +etki.slice(8); for (var j = i; j < slaytlar().length; j++) S.kirli.add(j); }
    else if (typeof etki === "number") S.kirli.add(etki);
    durumYaz(); taslakSakla(); onizleGecikmeli();
  }
  function gecmiseYaz() {
    S.gecmis.push(JSON.stringify({ D: S.D, kirli: Array.from(S.kirli), hepsi: S.hepsi, secili: S.secili }));
    if (S.gecmis.length > 80) S.gecmis.shift();
    $("#geriAl").disabled = false;
  }
  function geriAl() {
    var g = S.gecmis.pop(); if (!g) return;
    g = JSON.parse(g); S.D = g.D; S.kirli = new Set(g.kirli); S.hepsi = g.hepsi; S.secili = Math.min(g.secili, slaytlar().length - 1);
    $("#geriAl").disabled = !S.gecmis.length;
    hepsiniCiz(); taslakSakla();
  }
  function degisiklikVar() { return JSON.stringify(S.D) !== JSON.stringify(S.D0) || S.yeni.size > 0; }
  function durumYaz() {
    var d = $("#durum"), var_ = degisiklikVar();
    $("#kaydet").disabled = !var_; $("#zipIndir").disabled = !var_;
    if (!S.D) { d.textContent = ""; return; }
    var n = S.hepsi ? slaytlar().length : S.kirli.size;
    d.innerHTML = var_ ? "<b>Kaydedilmemiş değişiklik</b> · " + (S.mod === "kaynak" ? n + " slayt yeniden çizilecek" : "yayınlanmadı") +
      (GH.ayar().anahtar ? "" : " · GitHub anahtarı girilmedi") : (S.mod === "kaynak" ? "Kayıtlı. " : "Hazır ders: slayt resimleri sabit; resim, başlık, not ve sorular değiştirilebilir. ");
  }

  /* bağlama: alan değişince yaz */
  function bagla(nesne, anahtar, etki, donustur) {
    return function (e) {
      var el = e.target, v;
      if (el.type === "checkbox") v = el.checked;
      else if (el.type === "number") v = el.value === "" ? undefined : +el.value;
      else v = el.value;
      if (donustur) v = donustur(v);
      if (!S._yazdi) { gecmiseYaz(); S._yazdi = true; setTimeout(function () { S._yazdi = false; }, 1200); }
      if (v === undefined || v === "" || v === false) delete nesne[anahtar]; else nesne[anahtar] = v;
      degisti(etki);
      if (anahtar === "baslik" || anahtar === "title" || anahtar === "metin") listeCiz();
    };
  }
  function metin(et, nesne, anahtar, etki, ek) {
    ek = ek || {};
    var el = ek.cok ? h("textarea", { rows: ek.satir || 3, class: ek.kod ? "kod" : null, spellcheck: ek.kod ? "false" : "true" }) : h("input", { type: ek.sayi ? "number" : "text", min: ek.sayi ? 0 : null });
    el.value = nesne[anahtar] == null ? "" : nesne[anahtar];
    if (ek.yer) el.placeholder = ek.yer;
    el.addEventListener("input", bagla(nesne, anahtar, etki, ek.sayi ? null : ek.donustur));
    return h("label", { class: "alan" }, [h("span", { text: et }), ek.not ? h("small", { text: ek.not }) : null, el]);
  }
  function satirlar(et, nesne, anahtar, etki, not) {
    var el = h("textarea", { rows: Math.max(3, (nesne[anahtar] || []).length + 1) });
    el.value = (nesne[anahtar] || []).join("\n");
    el.addEventListener("input", function () {
      if (!S._yazdi) { gecmiseYaz(); S._yazdi = true; setTimeout(function () { S._yazdi = false; }, 1200); }
      nesne[anahtar] = el.value.split("\n").map(function (x) { return x.trim(); }).filter(Boolean); degisti(etki);
    });
    return h("label", { class: "alan" }, [h("span", { text: et }), h("small", { text: not || "Her satır bir madde." }), el]);
  }
  function kutucuk(et, nesne, anahtar, etki) {
    var el = h("input", { type: "checkbox" }); el.checked = !!nesne[anahtar];
    el.addEventListener("change", bagla(nesne, anahtar, etki));
    return h("label", { class: "secim" }, [el, et]);
  }
  function secim(et, nesne, anahtar, secenekler, etki, bos) {
    var el = h("select");
    if (bos != null) el.append(h("option", { value: "", text: bos }));
    secenekler.forEach(function (o) { el.append(h("option", { value: o[0], text: o[1] })); });
    el.value = nesne[anahtar] == null ? "" : nesne[anahtar];
    el.addEventListener("change", bagla(nesne, anahtar, etki));
    return h("label", { class: "alan" }, [h("span", { text: et }), el]);
  }
  function soruSecenekleri() { return sorular().map(function (q) { return [q.id, q.id + " · " + (q.label || q.q || "").slice(0, 50)]; }); }

  /* ---------------- yükleme ---------------- */
  async function getJSON(yol) {
    var a = GH.ayar();
    if (a.anahtar) {
      try { var t = await GH.dosyaOku(a, yol); return t == null ? null : JSON.parse(t); } catch (e) { console.warn(e); }
    }
    var r = await fetch("../" + yol + "?t=" + Date.now(), { cache: "no-store" });
    if (r.status === 404) return null;
    if (!r.ok) throw new Error(yol + " okunamadı (" + r.status + ")");
    return r.json();
  }

  async function basla() {
    var a = GH.ayar();
    if (!a.depo) GH.ayarYaz(Object.assign({ depo: "olgunak/lam-basinda", dal: "main" }, a));
    S.index = await getJSON("canli/dersler/index.json") || [];
    dersListesi();
    var son = null; try { son = localStorage.getItem("lb_son_ders"); } catch (e) {}
    var id = (location.hash.slice(1) || son || (S.index[S.index.length - 1] || {}).id);
    if (id && S.index.some(function (x) { return x.id === id; })) await dersAc(id); else if (S.index.length) await dersAc(S.index[0].id);
  }
  function dersListesi() {
    var sel = $("#ders"); sel.innerHTML = "";
    S.index.forEach(function (x) { sel.append(h("option", { value: x.id, text: x.id + " · " + x.title })); });
    sel.append(h("option", { value: "__yeni", text: "+ Yeni ders oluştur" }));
    if (S.id) sel.value = S.id;
  }

  async function dersAc(id) {
    if (S.D && degisiklikVar() && S.id !== id) {
      if (!confirm("Bu dersteki değişiklikler yayınlanmadı. Taslak bu bilgisayarda saklı kalır. Başka derse geçilsin mi?")) { $("#ders").value = S.id; return; }
    }
    $("#durum").textContent = "Yükleniyor…";
    S.id = id; S.secili = 0; S.adim = 0; S.soru = 0; S.kirli = new Set(); S.hepsi = false; S.gecmis = []; S.yeni = new Map();
    $("#geriAl").disabled = true;
    try { localStorage.setItem("lb_son_ders", id); } catch (e) {}
    history.replaceState(null, "", "#" + id);
    var kaynak = await getJSON("canli/dersler/kaynak/" + id + ".json");
    if (kaynak) { S.mod = "kaynak"; S.D = kaynak; }
    else { S.mod = "hazir"; S.D = await getJSON("canli/dersler/" + id + ".json"); }
    if (!S.D) throw new Error(id + " dersi bulunamadı");
    S.D0 = kopya(S.D);
    var t = await idbOku("taslak-" + id);
    if (t && t.mod === S.mod && JSON.stringify(t.D) !== JSON.stringify(S.D)) {
      var tarih = new Date(t.zaman).toLocaleString("tr-TR");
      var ayni = JSON.stringify(t.D0) === JSON.stringify(S.D0);
      if (confirm("Bu ders için " + tarih + " tarihli yayınlanmamış bir taslak var." + (ayni ? "" : " (Bu arada sitedeki ders de değişmiş.)") + "\n\nTaslağı açmak için Tamam, sitedeki sürümle başlamak için İptal.")) {
        S.D = t.D; S.kirli = new Set(t.kirli || []); S.hepsi = !!t.hepsi;
        Object.keys(t.yeni || {}).forEach(function (k) { S.yeni.set(k, { blob: t.yeni[k], url: URL.createObjectURL(t.yeni[k]) }); });
      } else idbSil("taslak-" + id);
    }
    $("#ders").value = id;
    hepsiniCiz();
  }

  function yeniDers() {
    var ids = S.index.map(function (x) { return x.id; });
    var n = 1; while (ids.indexOf("M" + n) >= 0) n++;
    var id = prompt("Yeni dersin kodu (ör. M" + n + "):", "M" + n);
    if (!id) { $("#ders").value = S.id; return; }
    id = id.trim().toUpperCase().replace(/[^A-Z0-9]/g, "");
    if (!id || ids.indexOf(id) >= 0) { alert("Bu kod kullanılıyor ya da geçersiz."); $("#ders").value = S.id; return; }
    var ad = prompt("Dersin adı:", "Yeni ders") || "Yeni ders";
    S.index.push({ id: id, title: ad, date: "", n: 0 });
    S.id = id; S.mod = "kaynak"; S.secili = 0; S.adim = 0; S.kirli = new Set(); S.hepsi = true; S.gecmis = []; S.yeni = new Map();
    S.D = { id: id, baslik: ad, kisa: ad, tarih: "", surum: "1", cerceve: "", serit: { ad: "", gruplar: [] }, cta: "", quiz: "", sorular: [],
      slaytlar: [Object.assign(Slayt.SABLON.kapak(), { baslik: ad }), Slayt.SABLON.adim()] };
    S.D0 = { yeni: true };
    dersListesi(); hepsiniCiz(); taslakSakla();
  }

  /* ---------------- çizim ---------------- */
  function hepsiniCiz() { $(".ekle").style.display = S.mod === "kaynak" ? "" : "none"; listeCiz(); formCiz(); onizle(); durumYaz(); }

  function listeCiz() {
    var ol = $("#slaytlar"); ol.innerHTML = "";
    var no = 0;
    slaytlar().forEach(function (s, i) {
      no++;
      var k = S.mod === "kaynak";
      var tip = k ? s.tip : (s.board ? "liderlik" : s.cloud ? "bulut" : "resim");
      var ad = k ? s.baslik : s.title;
      var bilgi = [h("span", { text: TIPLER[tip] || tip })];
      if (k && (s.tip === "adim" || s.tip === "kutular")) bilgi.push(h("span", { class: "tnum", text: Slayt.adimSayisi(s) + " adım" }));
      var q = k ? (s.soru || s.soruAc) : (s.q || s.qopen);
      if (q) bilgi.push(h("span", { text: "soru " + q }));
      if (k && s.dus) bilgi.push(h("span", { text: "DUS" }));
      if (k && s.opsiyonel) bilgi.push(h("span", { text: "zaman kalırsa" }));
      if (S.kirli.has(i) || (S.hepsi && k)) bilgi.push(h("span", { class: "k", text: "değişti" }));
      var b = h("button", { type: "button", class: "sl-btn", "aria-current": i === S.secili ? "true" : "false",
        on: { click: function () { S.secili = i; S.adim = 0; listeCiz(); formCiz(); onizle(); } } },
        [h("span", { class: "no", text: String(no) }), h("span", { class: "ad", text: ad || "(başlıksız)" }), h("span", { class: "bilgi" }, bilgi)]);
      var li = h("li", null, [b]);
      if (i === S.secili && k) {
        li.append(h("div", { class: "sl-islem" }, [
          ikonBtn("yukari", "Yukarı taşı", function () { tasi(i, -1); }), ikonBtn("asagi", "Aşağı taşı", function () { tasi(i, 1); }),
          ikonBtn("kopya", "Çoğalt", function () { cogalt(i); }), ikonBtn("sil", "Sil", function () { sil(i); }, "tehlike")]));
      }
      ol.append(li);
    });
    var cur = ol.querySelector("[aria-current=true]"); if (cur) cur.scrollIntoView({ block: "nearest" });
  }
  function tasi(i, d) {
    var a = slaytlar(), j = i + d; if (j < 0 || j >= a.length) return;
    gecmiseYaz(); var t = a[i]; a[i] = a[j]; a[j] = t; S.secili = j; degisti("sonrasi:" + Math.min(i, j)); listeCiz(); formCiz();
  }
  function cogalt(i) { gecmiseYaz(); slaytlar().splice(i + 1, 0, kopya(slaytlar()[i])); S.secili = i + 1; degisti("sonrasi:" + i); listeCiz(); formCiz(); }
  function sil(i) {
    if (!confirm("“" + (slaytlar()[i].baslik || "") + "” slaytı silinsin mi?")) return;
    gecmiseYaz(); slaytlar().splice(i, 1); S.secili = Math.max(0, Math.min(i, slaytlar().length - 1)); degisti("sonrasi:" + i); listeCiz(); formCiz();
  }
  function ekle() {
    if (S.mod !== "kaynak") { alert("Hazır derslere (M1, M2) slayt eklenemez; yalnız var olan slaytlar düzenlenir."); return; }
    var tip = $("#yeniTip").value, s = Slayt.SABLON[tip]();
    gecmiseYaz(); slaytlar().splice(S.secili + 1, 0, s); S.secili += 1; S.adim = 0; degisti("sonrasi:" + S.secili); listeCiz(); formCiz();
  }

  /* önizleme */
  var onizZaman = null;
  function onizleGecikmeli() { clearTimeout(onizZaman); onizZaman = setTimeout(onizle, 150); }
  function olcekle() {
    var c = $("#cerceve"), s = $("#sahne"); s.style.transform = "scale(" + (c.clientWidth / 1920) + ")";
  }
  async function onizle() {
    var sahne = $("#sahne");
    if (!S.D || !slaytlar().length) { sahne.innerHTML = ""; $("#adimYazi").textContent = ""; return; }
    var s = slaytlar()[S.secili];
    if (S.mod === "hazir") {
      var src = s.img ? s.img.split("?")[0] : null;
      sahne.innerHTML = src ? "<img alt='' style='width:1920px;height:1080px;object-fit:contain;background:#000' src='" + Slayt.esc(coz(src)) + "'>"
        : "<div class='sl koyu' style='display:grid;place-items:center;font-size:48px;color:#AFA1C2'>" + (s.board ? "Liderlik tablosu: perde canlı çizer" : "Kelime bulutu: perde canlı çizer") + "</div>";
      $("#adimYazi").textContent = "Slayt " + (S.secili + 1) + "/" + slaytlar().length;
      olcekle(); return;
    }
    var kar = Slayt.kareler(S.D).filter(function (f) { return f.si === S.secili; });
    if (S.adim >= kar.length) S.adim = kar.length - 1;
    var f = kar[Math.max(0, S.adim)];
    sahne.innerHTML = Slayt.html(S.D, f, { coz: coz });
    olcekle();
    await Promise.all(Array.from(sahne.querySelectorAll("img")).map(function (im) { return im.complete ? 0 : new Promise(function (r) { im.onload = im.onerror = r; }); }));
    await document.fonts.ready;
    if (sahne.firstChild) Slayt.sigdir(sahne.firstChild);
    $("#adimYazi").textContent = f.N ? "Adım " + (S.adim + 1) + "/" + f.N : "Tek kare";
    $("#oncekiAdim").disabled = !f.N || S.adim === 0;
    $("#sonrakiAdim").disabled = !f.N || S.adim >= f.N - 1;
    document.querySelectorAll(".blok[data-madde]").forEach(function (b) { b.classList.toggle("su", +b.dataset.madde === S.adim); });
  }

  /* ---------------- formlar ---------------- */
  function formCiz() {
    ["slayt", "soru", "ders"].forEach(function (t) { $("#sk-" + t).setAttribute("aria-selected", String(S.sekme === t)); });
    var f = $("#form"), kay = f.scrollTop, anahtar = S.sekme + ":" + S.secili + ":" + S.soru;
    if (S._formAnahtar !== anahtar) kay = 0;
    S._formAnahtar = anahtar;
    f.innerHTML = "";
    if (!S.D) return;
    requestAnimationFrame(function () { f.scrollTop = kay; });
    if (S.sekme === "slayt") (S.mod === "kaynak" ? slaytFormu : hazirSlaytFormu)(f);
    else if (S.sekme === "soru") soruFormu(f);
    else dersFormu(f);
  }

  function hazirSlaytFormu(f) {
    var s = slaytlar()[S.secili], i = S.secili; if (!s) return;
    f.append(metin("Başlık (kumandada görünür)", s, "title", "yok"));
    if (s.img) {
      var src = s.img.split("?")[0];
      f.append(h("div", { class: "panel" }, [h("div", { class: "panel-foto" }, [h("img", { src: coz(src), alt: "" }),
        h("div", { class: "alanlar" }, [h("p", { class: "aciklama", text: "Bu slayt hazır bir resim. Değiştirmek için 1920×1080 (16:9) bir JPG ya da PNG seçin; PowerPoint'ten “Farklı kaydet → JPEG” ile alabilirsiniz." }),
          h("label", { class: "kucuk-btn" }, [ikon("yukle"), "Resmi değiştir", h("input", { type: "file", accept: "image/*", class: "sr", on: { change: async function (e) {
            var dosya = e.target.files[0]; if (!dosya) return;
            var blob = await Disa.fotoKucult(dosya, 1920);
            gecmiseYaz();
            S.yeni.set(src, { blob: blob, url: URL.createObjectURL(blob) });
            s.img = src + "?v=" + Date.now().toString(36);
            degisti(i); formCiz(); listeCiz();
          } } })])])])]));
    }
    if (s.q || s.qopen) f.append(h("p", { class: "bilgi-kutu", text: "Bu slaytta soru " + (s.q || s.qopen) + " açılır. Sorunun metni Sorular sekmesinde." }));
    f.append(metin("Konuşma notu (kumandada görünür)", s, "notes", "yok", { cok: true, satir: 10, not: "Baştaki [dakika] damgası ve CANLI satırı kumanda içindir; silmeyin." }));
  }

  function ortakAlanlar(f, s, i) {
    f.append(metin("Başlık", s, "baslik", i));
    if (s.tip !== "kapak" && s.tip !== "liderlik" && s.tip !== "bulut") {
      f.append(h("div", { class: "iki" }, [secim("Zemin", s, "tema", [["koyu", "Koyu (karanlık sınıf)"]], i, "Açık")]));
      f.append(h("div", { class: "satir" }, [kutucuk("DUS etiketi", s, "dus", i), kutucuk("Zaman kalırsa (isteğe bağlı slayt)", s, "opsiyonel", i),
        kutucuk("Renk alanı zemini (dikkat çeken slayt)", s, "alan", i)]));
      var gr = (S.D.serit && S.D.serit.gruplar) || [];
      if (gr.length) {
        var kut = gr.map(function (g, gi) {
          var el = h("input", { type: "checkbox" }); el.checked = (s.serit || []).indexOf(gi + 1) >= 0;
          el.addEventListener("change", function () {
            gecmiseYaz(); var a = (s.serit || []).filter(function (x) { return x !== gi + 1; }); if (el.checked) a.push(gi + 1); a.sort();
            if (a.length) s.serit = a; else delete s.serit; degisti(i);
          });
          return h("label", { class: "secim" }, [el, g]);
        });
        f.append(h("div", null, [h("span", { class: "alan", text: "Alt şeritte yanan grup" }), h("div", { class: "satir" }, kut)]));
      }
      f.append(metin("Görsel kaynağı (alt satırda)", s, "kaynak", i, { yer: "ör. Neville 5. baskı" }));
    }
  }

  function sureNot(f, nesne, i) {
    f.append(h("div", { class: "iki" }, [metin("Süre (saniye)", nesne, "sure", i, { sayi: true })]));
    f.append(metin("Konuşma notu (kumandada görünür)", nesne, "not", i, { cok: true, satir: 4 }));
  }

  function slaytFormu(f) {
    var s = slaytlar()[S.secili], i = S.secili; if (!s) { f.append(h("p", { class: "aciklama", text: "Slayt yok. Soldan ekleyin." })); return; }
    f.append(h("p", { class: "aciklama", text: TIPLER[s.tip] + " slaytı" }));
    ortakAlanlar(f, s, i);
    if (s.tip === "adim") {
      f.append(secim("Bu slaytta soru telefonlarda açılsın (son adımda)", s, "soruAc", soruSecenekleri(), i, "Hayır"));
      f.append(h("h3", { text: "Maddeler" }));
      f.append(h("p", { class: "aciklama", text: "Her madde perdede ayrı bir adımda açılır. Görseli olmayan madde bir önceki maddenin görselini gösterir." }));
      (s.maddeler || []).forEach(function (m, mi) { f.append(maddeBlok(s, m, mi, i)); });
      f.append(kucukBtn("arti", "Madde ekle", function () { gecmiseYaz(); s.maddeler.push({ metin: "Yeni madde", sure: 8, not: "" }); S.adim = s.maddeler.length - 1; degisti(i); formCiz(); }));
    } else if (s.tip === "soru") {
      f.append(secim("Soru", s, "soru", soruSecenekleri(), i, "Seçin"));
      f.append(kutucuk("Soru önceki slaytta açıldı (bu slayt dağılımı gösterir)", s, "devam", i));
      f.append(metin("Sorunun altındaki açıklama", s, "aciklama", i, { cok: true, satir: 2 }));
      f.append(h("h3", { text: "Görseller (sağda)" }));
      s.gorsel = s.gorsel || [];
      panelListesi(f, s.gorsel, i);
      sureNot(f, s, i);
    } else if (s.tip === "kutular") {
      f.append(h("p", { class: "aciklama", text: "Her adımda bir kutu daha açılır. “Vurgu” tonlu kutu alta tam genişlikte yerleşir." }));
      (s.kutular || []).forEach(function (k, ki) {
        var b = h("div", { class: "blok", "data-madde": ki }, [h("div", { class: "blok-ust" }, [h("b", { text: "Kutu " + (ki + 1) }),
          ikonBtn("sil", "Kutuyu sil", function () { gecmiseYaz(); s.kutular.splice(ki, 1); s.adimlar.splice(ki, 1); degisti(i); formCiz(); }, "tehlike")])]);
        b.append(metin("Kutu başlığı", k, "baslik", i));
        b.append(secim("Ton", k, "ton", TONLAR, i));
        if (k.tablo) b.append(tabloAlan("İçerik (tablo)", k, "tablo", i));
        else b.append(satirlar("Maddeler", k, "maddeler", i));
        var ad = s.adimlar[ki] = s.adimlar[ki] || { sure: 10, not: "" };
        b.append(h("div", { class: "iki" }, [metin("Bu adımın süresi (sn)", ad, "sure", i, { sayi: true })]));
        b.append(metin("Bu adımın notu", ad, "not", i, { cok: true, satir: 2 }));
        f.append(b);
      });
      f.append(kucukBtn("arti", "Kutu ekle", function () { gecmiseYaz(); s.kutular.push({ baslik: "Yeni grup", ton: "mor", maddeler: ["Konu"] }); s.adimlar.push({ sure: 10, not: "" }); degisti(i); formCiz(); }));
    } else if (s.tip === "ozet") {
      f.append(h("p", { class: "aciklama", text: "İki sütunlu numaralı liste: her satır bir konu ve akılda kalacak cümlesi." }));
      (s.maddeler = s.maddeler || []).forEach(function (m, mi) {
        var b = h("div", { class: "blok" }, [h("div", { class: "blok-ust" }, [h("b", { text: String(mi + 1) }),
          ikonBtn("sil", "Satırı sil", function () { gecmiseYaz(); s.maddeler.splice(mi, 1); degisti(i); formCiz(); }, "tehlike")])]);
        b.append(metin("Konu", m, "ust", i)); b.append(metin("Akılda kalacak cümle", m, "metin", i, { cok: true, satir: 2 }));
        f.append(b);
      });
      f.append(kucukBtn("arti", "Satır ekle", function () { gecmiseYaz(); s.maddeler.push({ ust: "Konu", metin: "" }); degisti(i); formCiz(); }));
      sureNot(f, s, i);
    } else if (s.tip === "tablo") {
      f.append(metin("Sütun başlıkları", s, "tabloBaslik", i, { not: "İki başlığı → ile ayırın: Eski ad → Güncel ad" }));
      f.append(tabloAlan("Satırlar", s, "satirlar", i));
      sureNot(f, s, i);
    } else if (s.tip === "kaynaklar") {
      f.append(satirlar("Kaynaklar", s, "maddeler", i, "Her satır bir kaynak."));
      f.append(metin("Quiz açıklaması", s, "quizMetni", i));
      f.append(metin("Quiz adresi", s, "quizAdres", i));
      f.append(metin("Alttaki çağrı", s, "cagri", i));
      sureNot(f, s, i);
    } else if (s.tip === "kapak") {
      f.append(metin("Alt başlık", s, "alt", i));
      f.append(metin("Tarih ve hoca", s, "tarih", i));
      f.append(metin("Üst satır", s, "ust", i));
      f.append(metin("Açılış vakası (pembe kutu)", s, "vaka", i, { cok: true, satir: 2 }));
      f.append(kutucuk("Katılım ekranı bu slaytta (karekod)", s, "katilim", i));
      s.gorsel = s.gorsel || {};
      f.append(h("h3", { text: "Sağdaki görsel" }));
      f.append(fotoAlan(s.gorsel, i, true));
      f.append(metin("Görsel kaynağı", s, "kaynak", i));
      sureNot(f, s, i);
    } else if (s.tip === "liderlik") {
      f.append(metin("Kaç kişi gösterilsin (boşsa hepsi)", s, "ilk", i, { sayi: true }));
      sureNot(f, s, i);
    } else if (s.tip === "bulut") {
      s.bulut = s.bulut || { q: "", from: "prev" };
      f.append(metin("Önceki dersin kelime bulutu sorusu", s.bulut, "q", i, { yer: "ör. W7" }));
      sureNot(f, s, i);
    }
  }

  function tabloAlan(et, nesne, anahtar, i) {
    var el = h("textarea", { rows: Math.max(4, (nesne[anahtar] || []).length + 1) });
    el.value = (nesne[anahtar] || []).map(function (r) { return r.join(" | "); }).join("\n");
    el.addEventListener("input", function () {
      if (!S._yazdi) { gecmiseYaz(); S._yazdi = true; setTimeout(function () { S._yazdi = false; }, 1200); }
      nesne[anahtar] = el.value.split("\n").filter(function (x) { return x.trim(); }).map(function (r) { return r.split("|").map(function (c) { return c.trim(); }); });
      degisti(i);
    });
    return h("label", { class: "alan" }, [h("span", { text: et }), h("small", { text: "Her satır bir tablo satırı; sütunları | ile ayırın." }), el]);
  }

  function maddeBlok(s, m, mi, i) {
    var b = h("div", { class: "blok" + (mi === S.adim ? " su" : ""), "data-madde": mi });
    b.append(h("div", { class: "blok-ust" }, [
      h("b", { text: "Adım " + (mi + 1) }),
      kucukBtn(null, "Önizle", function () { S.adim = mi; onizle(); }),
      ikonBtn("yukari", "Yukarı", function () { if (!mi) return; gecmiseYaz(); var a = s.maddeler; a.splice(mi - 1, 0, a.splice(mi, 1)[0]); degisti(i); formCiz(); }),
      ikonBtn("asagi", "Aşağı", function () { var a = s.maddeler; if (mi >= a.length - 1) return; gecmiseYaz(); a.splice(mi + 1, 0, a.splice(mi, 1)[0]); degisti(i); formCiz(); }),
      ikonBtn("sil", "Maddeyi sil", function () { if (s.maddeler.length < 2) return; gecmiseYaz(); s.maddeler.splice(mi, 1); S.adim = Math.max(0, mi - 1); degisti(i); formCiz(); }, "tehlike")]));
    b.append(metin("Üst başlık (isteğe bağlı)", m, "ust", i));
    b.append(metin("Metin", m, "metin", i, { cok: true, satir: 2 }));
    b.append(h("div", { class: "iki" }, [metin("Süre (sn)", m, "sure", i, { sayi: true })]));
    b.append(metin("Konuşma notu", m, "not", i, { cok: true, satir: 2 }));
    var g = h("div", { class: "alan" }, [h("span", { text: "Bu adımda soldaki görsel" })]);
    b.append(g);
    if (m.gorsel && m.gorsel.length) panelListesi(b, m.gorsel, i, function () { delete m.gorsel; });
    else b.append(h("div", { class: "satir" }, [kucukBtn("gorsel", "Görsel ekle", function () {
      galeriAc(function (src) { gecmiseYaz(); m.gorsel = [{ foto: src }]; degisti(i); formCiz(); });
    }), h("span", { class: "aciklama", text: "Yoksa önceki adımın görseli kalır." })]));
    return b;
  }

  function fotoAlan(p, i, tek) {
    var img = h("img", { src: coz(p.foto), alt: "" });
    var alanlar = h("div", { class: "alanlar" }, [h("div", { class: "satir" }, [kucukBtn("gorsel", p.foto ? "Değiştir" : "Görsel seç", function () {
      galeriAc(function (src) { gecmiseYaz(); p.foto = src; degisti(i); formCiz(); });
    })])]);
    if (!tek) {
      alanlar.append(metin("Alt yazı", p, "yazi", i));
      alanlar.append(metin("İkinci satır", p, "alt", i));
      alanlar.append(h("div", { class: "iki" }, [secim("Kırpma", p, "konum", KONUM.slice(1), i, "Orta"), metin("Köşe harfi", p, "etiket", i, { yer: "A" })]));
      alanlar.append(kutucuk("Kırpmadan sığdır", p, "sigdir", i));
    } else alanlar.append(secim("Kırpma", p, "konum", KONUM.slice(1), i, "Orta"));
    return h("div", { class: "panel" }, [h("div", { class: "panel-foto" }, [img, alanlar])]);
  }

  function panelListesi(kap, dizi, i, bosalinca) {
    dizi.forEach(function (p, pi) {
      var ust = h("div", { class: "blok-ust" }, [h("b", { text: p.foto != null ? "Fotoğraf" : p.rakam != null ? "Büyük rakam" : p.kutu != null ? "Kutu" : p.not ? "Patoloğun notu" : p.soruIsareti != null ? "Soru işareti" : p.cubuklar ? "Çubuk grafik" : p.cizim ? "Çizim" : "Görsel" }),
        ikonBtn("sil", "Kaldır", function () { gecmiseYaz(); dizi.splice(pi, 1); if (!dizi.length && bosalinca) bosalinca(); degisti(i); formCiz(); }, "tehlike")]);
      var pan;
      if (p.foto != null) { pan = fotoAlan(p, i); pan.prepend(ust); }
      else {
        pan = h("div", { class: "panel" }, [ust]);
        if (p.rakam != null) { pan.append(metin("Rakam", p, "rakam", i)); pan.append(metin("Açıklama", p, "aciklama", i)); }
        else if (p.kutu != null) { pan.append(metin("Metin", p, "kutu", i, { cok: true, satir: 2 })); pan.append(secim("Ton", p, "ton", TONLAR, i)); }
        else if (p.not) { pan.append(metin("Başlık", p.not, "baslik", i)); pan.append(metin("Metin", p.not, "metin", i, { cok: true, satir: 3 })); }
        else if (p.soruIsareti != null) pan.append(metin("Yazı", p, "soruIsareti", i));
        else if (p.cubuklar) {
          pan.append(metin("Grafik başlığı", p, "baslik", i));
          pan.append(metin("Kaçıncı satıra kadar görünsün (0'dan)", p, "kadar", i, { sayi: true }));
          var ta = h("textarea", { rows: 5, class: "kod" }); ta.value = p.cubuklar.map(function (c) { return [c.ad, c.alt, c.ust, c.not || "", c.vurgu ? "vurgu" : ""].join(" | "); }).join("\n");
          ta.addEventListener("change", function () {
            gecmiseYaz();
            p.cubuklar = ta.value.split("\n").filter(function (x) { return x.trim(); }).map(function (r) { var c = r.split("|").map(function (x) { return x.trim(); }); return { ad: c[0], alt: +c[1] || 0, ust: +c[2] || 0, not: c[3] || "", vurgu: c[4] === "vurgu" }; });
            degisti(i);
          });
          pan.append(h("label", { class: "alan" }, [h("span", { text: "Satırlar" }), h("small", { text: "ad | alt % | üst % | not | vurgu" }), ta]));
        } else pan.append(h("p", { class: "aciklama", text: "Bu çizim düzenleyicide değiştirilemez; kaldırıp yerine fotoğraf koyabilirsiniz." }));
      }
      kap.append(pan);
    });
    kap.append(h("div", { class: "satir" }, [
      kucukBtn("gorsel", "Fotoğraf", function () { galeriAc(function (src) { gecmiseYaz(); dizi.push({ foto: src }); degisti(i); formCiz(); }); }),
      kucukBtn("arti", "Büyük rakam", function () { gecmiseYaz(); dizi.push({ rakam: "%10", aciklama: "Açıklama" }); degisti(i); formCiz(); }),
      kucukBtn("arti", "Kutu", function () { gecmiseYaz(); dizi.push({ kutu: "Metin", ton: "mor" }); degisti(i); formCiz(); }),
      kucukBtn("arti", "Patoloğun notu", function () { gecmiseYaz(); dizi.push({ not: { baslik: "Başlık", metin: "Metin" } }); degisti(i); formCiz(); })]));
  }

  /* sorular */
  function soruEtkisi(id) {
    if (S.mod !== "kaynak") return "yok";
    slaytlar().forEach(function (s, i) { if (s.soru === id) S.kirli.add(i); });
    return "yok";
  }
  function soruFormu(f) {
    var qs = sorular();
    var liste = h("div", { class: "soru-liste" });
    qs.forEach(function (q, qi) {
      liste.append(h("button", { type: "button", "aria-current": qi === S.soru ? "true" : "false", on: { click: function () { S.soru = qi; formCiz(); } } },
        [h("b", { text: q.id }), h("span", { text: q.label || q.q || "" })]));
    });
    f.append(liste);
    f.append(h("div", { class: "satir" }, [kucukBtn("arti", "Yeni soru", function () {
      gecmiseYaz(); var n = 1; while (qs.some(function (q) { return q.id === "W" + n; })) n++;
      qs.push({ id: "W" + n, type: "MCQ", label: "Yeni soru", q: "Soru metni?", scored: true, opts: ["A şıkkı", "B şıkkı", "C şıkkı", "D şıkkı"], a: 0, exp: "", t: 30 });
      S.soru = qs.length - 1; degisti("yok"); formCiz();
    })]));
    var q = qs[S.soru]; if (!q) return;
    var ek = function () { soruEtkisi(q.id); degisti("yok"); };
    var etki = "yok";
    f.append(h("h3", { text: "Soru " + q.id }));
    var kullanan = slaytlar().filter(function (s) { return (s.soru || s.soruAc || s.q || s.qopen) === q.id; }).length;
    var b = h("div", { class: "blok" });
    b.append(h("div", { class: "iki" }, [secim("Tür", q, "type", SORU_TUR.map(function (t) { return [t, Slayt.TUR_TR[t]]; }), etki),
      metin("Süre (sn)", q, "t", etki, { sayi: true })]));
    b.append(metin("Kısa ad (kumanda ve listede)", q, "label", etki));
    var qt = metin("Soru metni", q, "q", etki, { cok: true, satir: 3 }); qt.querySelector("textarea").addEventListener("input", ek); b.append(qt);
    b.append(kutucuk("Puanlı (liderlik tablosuna sayılır)", q, "scored", etki));
    if (["MCQ", "POLL", "IMGMCQ"].indexOf(q.type) >= 0) {
      var op = satirlar("Şıklar", q, "opts", etki, "Her satır bir şık (en çok 5)."); op.querySelector("textarea").addEventListener("input", function () { ek(); dogruSec(); }); b.append(op);
      var dogru = h("div"); b.append(dogru);
      var dogruSec = function () {
        dogru.innerHTML = "";
        dogru.append(secim("Doğru cevap", q, "a", (q.opts || []).map(function (o, oi) { return [String(oi), "ABCDE"[oi] + " · " + o]; }), etki, "Yok (anket)"));
        dogru.querySelector("select").addEventListener("change", function (e) { if (e.target.value === "") delete q.a; else q.a = +e.target.value; degisti("yok"); });
      };
      dogruSec();
      if (q.type === "POLL") {
        b.append(kutucuk("Tahmin anketi: sonuçta doğru cevap açılmaz", q, "hide", etki));
        b.append(secim("Dersin başındaki şu soruyla karşılaştır", q, "compare", soruSecenekleri().filter(function (x) { return x[0] !== q.id; }), etki, "Yok"));
      }
    }
    if (q.type === "MATCH") {
      b.append(satirlar("Sol sütun", q, "left", etki));
      b.append(satirlar("Sağ sütun (karışık sırayla)", q, "right", etki));
      b.append(satirlar("Doğru eşleşme", q, "key", etki, "Sol sütunun her satırına karşılık gelen sağ öğe, aynı sırayla."));
    }
    var ex = metin("Açıklama (cevaptan sonra)", q, "exp", etki, { cok: true, satir: 3 }); b.append(ex);
    var gor = h("div", { class: "panel" });
    var resim = h("div", { class: "panel-foto" }, [h("img", { src: q.img ? coz(q.img) : "", alt: "" }), h("div", { class: "alanlar" }, [
      h("p", { class: "aciklama", text: "Telefonda sorunun üstünde görünen görsel (isteğe bağlı)." }),
      h("div", { class: "satir" }, [kucukBtn("gorsel", q.img ? "Değiştir" : "Görsel seç", function () { galeriAc(function (src) { gecmiseYaz(); q.img = src; degisti("yok"); formCiz(); }); }),
        q.img ? kucukBtn("sil", "Kaldır", function () { gecmiseYaz(); delete q.img; degisti("yok"); formCiz(); }) : null])])]);
    gor.append(resim); b.append(gor);
    f.append(b);
    var ileri = h("details", null, [h("summary", { text: "Gelişmiş: sorunun tamamı (JSON)" })]);
    var ta = h("textarea", { rows: 12, class: "kod", spellcheck: "false" }); ta.value = JSON.stringify(q, null, 1);
    var hata = h("p", { class: "aciklama" });
    ta.addEventListener("change", function () {
      try { var y = JSON.parse(ta.value); gecmiseYaz(); qs[S.soru] = y; ek(); formCiz(); } catch (e) { hata.textContent = "JSON hatalı: " + e.message; hata.className = "uyari"; }
    });
    ileri.append(h("label", { class: "alan" }, [h("small", { text: "Görüntüde bul, sıralama, SCT gibi türlerin ayrıntıları burada." }), ta]), hata);
    f.append(ileri);
    f.append(h("div", { class: "satir" }, [kucukBtn("sil", "Soruyu sil", function () {
      if (kullanan && !confirm(q.id + " " + kullanan + " slaytta kullanılıyor. Yine de silinsin mi?")) return;
      if (!kullanan && !confirm(q.id + " silinsin mi?")) return;
      gecmiseYaz(); qs.splice(S.soru, 1); S.soru = 0; degisti("yok"); formCiz();
    })]));
  }

  function dersFormu(f) {
    var D = S.D;
    if (S.mod === "kaynak") {
      f.append(metin("Ders adı", D, "baslik", "yok"));
      f.append(metin("Kısa ad (slayt altında)", D, "kisa", "hepsi"));
      f.append(metin("Tarih", D, "tarih", "yok"));
      f.append(metin("Çerçeve (kumandada)", D, "cerceve", "yok"));
      D.serit = D.serit || { ad: "", gruplar: [] };
      f.append(satirlar("Alt şerit grupları", D.serit, "gruplar", "hepsi", "Her satır bir grup, ör. “1 Neoplastik olmayan”."));
      f.append(metin("Ders sonu çağrısı (perdede)", D, "cta", "yok", { cok: true, satir: 2 }));
      f.append(metin("Quiz bağlantısı", D, "quiz", "yok", { yer: "../quiz/#yd" }));
      f.append(h("p", { class: "aciklama", text: "Sürüm: " + (D.surum || "") + " · Her kayıtta artar; telefonlar slaytları yeniden indirir." }));
    } else {
      f.append(metin("Ders adı", D, "title", "yok"));
      f.append(metin("Tarih", D, "date", "yok"));
      f.append(metin("Çerçeve", D, "frame", "yok"));
      f.append(metin("Ders sonu çağrısı", D, "cta", "yok", { cok: true, satir: 2 }));
      f.append(metin("Quiz bağlantısı", D, "quiz", "yok"));
    }
    f.append(h("h3", { text: "Yayın" }));
    var a = GH.ayar();
    f.append(h("p", { class: "aciklama", text: a.anahtar ? "Kayıt yeri: " + a.depo + " · " + a.dal + " dalı. Kayıttan sonra PowerPoint dosyaları birkaç dakika içinde GitHub'da kendiliğinden yenilenir." : "GitHub anahtarı girilmedi; şimdilik yalnız “Bilgisayara indir” çalışır." }));
  }

  /* ---------------- galeri ---------------- */
  function dersGorselleri() {
    var set = new Set();
    function ekle(x) { if (x && typeof x === "string" && /\.(jpe?g|png|webp|gif)$/i.test(x.split("?")[0])) set.add(x.split("?")[0]); }
    (function gez(o) {
      if (Array.isArray(o)) o.forEach(gez);
      else if (o && typeof o === "object") Object.keys(o).forEach(function (k) { if (k === "foto" || k === "img" || k === "src") ekle(o[k]); else gez(o[k]); });
    })(S.D);
    S.yeni.forEach(function (v, k) { set.add(k); });
    return Array.from(set).filter(function (x) { return x.indexOf("slaytlar/") !== 0; });
  }
  function galeriAc(cb) {
    S.galeriCb = cb;
    var iz = $("#galeriIzgara"); iz.innerHTML = "";
    dersGorselleri().forEach(function (src) {
      iz.append(h("button", { type: "button", on: { click: function () { $("#galeri").close(); cb(src); } } }, [h("img", { src: coz(src), alt: "", loading: "lazy" }), h("span", { text: src.split("/").pop() })]));
    });
    $("#galeri").showModal();
  }
  async function galeriYukle(e) {
    var dosya = e.target.files[0]; e.target.value = ""; if (!dosya) return;
    var blob = await Disa.fotoKucult(dosya, 1800);
    var ad = (dosya.name.replace(/\.[^.]+$/, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").slice(0, 30) || "gorsel") + "-" + Date.now().toString(36) + ".jpg";
    var src = "img/" + S.id + "/" + ad;
    S.yeni.set(src, { blob: blob, url: URL.createObjectURL(blob) });
    $("#galeri").close();
    if (S.galeriCb) S.galeriCb(src);
  }

  /* ---------------- kaydetme ---------------- */
  function kayitPenceresi(baslik) {
    $("#kayitBaslik").textContent = baslik; $("#kayitYazi").textContent = ""; $("#kayitCubuk").value = 0; $("#kayitCubuk").hidden = false;
    $("#kayitKapat").hidden = true; $("#kayit").showModal();
  }
  function kayitIlerle(oran, yazi) { if (oran != null) $("#kayitCubuk").value = oran; if (yazi) $("#kayitYazi").textContent = yazi; }
  function kayitBitti(baslik, yazi, html) {
    $("#kayitBaslik").textContent = baslik; $("#kayitCubuk").hidden = true;
    if (html) $("#kayitYazi").innerHTML = html; else $("#kayitYazi").textContent = yazi;
    $("#kayitKapat").hidden = false; $("#kayitKapat").focus();
  }

  function zamanSurum() { var d = new Date(); return d.getFullYear().toString().slice(2) + String(d.getMonth() + 1).padStart(2, "0") + String(d.getDate()).padStart(2, "0") + String(d.getHours()).padStart(2, "0") + String(d.getMinutes()).padStart(2, "0"); }

  /* Kaydedilecek bütün dosyaları hazırlar: [{yol, icerik}], sil: [yol] */
  async function dosyalariHazirla() {
    var dosyalar = [], sil = [], id = S.id;
    S.yeni.forEach(function (v, k) { dosyalar.push({ yol: "canli/" + k, icerik: v.blob }); });
    var idx = kopya(S.index);
    if (S.mod === "kaynak") {
      S.D.surum = zamanSurum();
      var kar = Slayt.kareler(S.D);
      var cizilecek = kar.filter(function (f) { return Slayt.gorselVar(f) && (S.hepsi || S.kirli.has(f.si)); });
      var sahne = $("#cizimSahne");
      if (!$("#cizimCSS")) { var st = h("style", { id: "cizimCSS" }); st.textContent = Slayt.css("../ortak/fontlar/"); document.head.append(st); }
      for (var i = 0; i < cizilecek.length; i++) {
        kayitIlerle(i / Math.max(1, cizilecek.length) * 0.8, "Slayt çiziliyor " + (i + 1) + "/" + cizilecek.length);
        var blob = await Disa.kareJPEG(S.D, cizilecek[i], sahne, coz);
        dosyalar.push({ yol: "canli/slaytlar/" + id + "/" + Slayt.dosyaAdi(cizilecek[i]), icerik: blob });
      }
      sahne.innerHTML = "";
      var yeniAd = new Set(kar.filter(Slayt.gorselVar).map(Slayt.dosyaAdi));
      if (S.D0 && S.D0.slaytlar) Slayt.kareler(S.D0).filter(Slayt.gorselVar).map(Slayt.dosyaAdi).forEach(function (a) { if (!yeniAd.has(a)) sil.push("canli/slaytlar/" + id + "/" + a); });
      var L = Slayt.canli(kopya(S.D));
      dosyalar.push({ yol: "canli/dersler/kaynak/" + id + ".json", icerik: JSON.stringify(S.D, null, 1) + "\n" });
      dosyalar.push({ yol: "canli/dersler/" + id + ".json", icerik: JSON.stringify(L, null, 1) });
      var e = idx.find(function (x) { return x.id === id; }); var rec = { id: id, title: L.title, date: L.date, n: L.questions.length };
      if (e) Object.assign(e, rec); else idx.push(rec);
    } else {
      dosyalar.push({ yol: "canli/dersler/" + id + ".json", icerik: JSON.stringify(S.D, null, 1) });
      var e2 = idx.find(function (x) { return x.id === id; }); if (e2) Object.assign(e2, { title: S.D.title, date: S.D.date, n: (S.D.questions || []).length });
    }
    dosyalar.push({ yol: "canli/dersler/index.json", icerik: JSON.stringify(idx, null, 1) });
    return { dosyalar: dosyalar, sil: sil, idx: idx };
  }

  async function kaydet() {
    if (!GH.ayar().anahtar) { ayarlarAc(); return; }
    kayitPenceresi("Kaydediliyor");
    var yedek = kopya(S.D);
    try {
      var h_ = await dosyalariHazirla();
      var sonuc = await GH.kaydet(h_.dosyalar, h_.sil, "Düzenleyici: " + S.id + " güncellendi", function (y) { kayitIlerle(null, y); });
      kayitIlerle(1);
      S.index = h_.idx; S.D0 = kopya(S.D); S.kirli = new Set(); S.hepsi = false; S.gecmis = []; $("#geriAl").disabled = true;
      S.yeni.forEach(function (v, k) { /* artık sitede */ }); S.yeni = new Map();
      await idbSil("taslak-" + S.id);
      dersListesi(); hepsiniCiz();
      kayitBitti("Yayınlandı", null, sonuc.degisen ? "Değişen " + sonuc.degisen + " dosya GitHub'a yazıldı. Site 1–2 dakika içinde güncellenir. <a href='" + sonuc.url + "' target='_blank' rel='noopener'>Commit'i gör</a>" : "Değişen dosya yoktu; site zaten güncel.");
    } catch (e) {
      S.D = yedek;
      kayitBitti("Kaydedilemedi", e.message + " Değişiklikler taslak olarak bu bilgisayarda duruyor.");
    }
  }

  async function zipIndir() {
    kayitPenceresi("Dosyalar hazırlanıyor");
    var yedek = kopya(S.D);
    try {
      if (!window.JSZip) await new Promise(function (ok, hata) { var sc = h("script", { src: "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js" }); sc.onload = ok; sc.onerror = function () { hata(new Error("Zip kütüphanesi yüklenemedi (internet?)")); }; document.head.append(sc); });
      var h_ = await dosyalariHazirla();
      var z = new JSZip();
      h_.dosyalar.forEach(function (d) { z.file(d.yol, d.icerik); });
      z.file("BENIOKU.txt", "Bu klasördeki dosyaları depo köküne aynı yollarla kopyalayın (GitHub'da: Add file > Upload files, klasörleri sürükleyin).\n" +
        (h_.sil.length ? "\nSilinmesi gereken eski dosyalar:\n" + h_.sil.join("\n") + "\n" : ""));
      var blob = await z.generateAsync({ type: "blob" });
      var a = h("a", { href: URL.createObjectURL(blob), download: "lam-basinda-" + S.id + "-" + zamanSurum() + ".zip" }); document.body.append(a); a.click(); a.remove();
      S.D = yedek;
      kayitBitti("İndirildi", "Zip dosyası indi. Taslak bu bilgisayarda kaldı; GitHub'a yükledikten sonra sayfayı yenileyip taslağı silebilirsiniz.");
    } catch (e) { S.D = yedek; kayitBitti("Hazırlanamadı", e.message); }
  }

  /* ---------------- ayarlar ---------------- */
  function ayarlarAc() {
    var a = GH.ayar();
    $("#ayAnahtar").value = a.anahtar || ""; $("#ayDepo").value = a.depo || "olgunak/lam-basinda"; $("#ayDal").value = a.dal || "main";
    $("#ayarlar").showModal();
  }
  $("#ayarlar").addEventListener("close", function () {
    if ($("#ayarlar").returnValue !== "kaydet") return;
    GH.ayarYaz({ anahtar: $("#ayAnahtar").value.trim(), depo: $("#ayDepo").value.trim() || "olgunak/lam-basinda", dal: $("#ayDal").value.trim() || "main" });
    durumYaz(); if (S.sekme === "ders") formCiz();
  });

  /* ---------------- olaylar ---------------- */
  $("#ders").addEventListener("change", function (e) { if (e.target.value === "__yeni") yeniDers(); else dersAc(e.target.value).catch(hataGoster); });
  $("#slaytEkle").addEventListener("click", ekle);
  $("#oncekiAdim").addEventListener("click", function () { if (S.adim > 0) { S.adim--; onizle(); } });
  $("#sonrakiAdim").addEventListener("click", function () { S.adim++; onizle(); });
  ["slayt", "soru", "ders"].forEach(function (t) { $("#sk-" + t).addEventListener("click", function () { S.sekme = t; formCiz(); }); });
  $("#kaydet").addEventListener("click", kaydet);
  $("#zipIndir").addEventListener("click", zipIndir);
  $("#ayarlarAc").addEventListener("click", ayarlarAc);
  $("#geriAl").addEventListener("click", geriAl);
  $("#galeriKapat").addEventListener("click", function () { $("#galeri").close(); });
  $("#galeriDosya").addEventListener("change", galeriYukle);
  $("#kayitKapat").addEventListener("click", function () { $("#kayit").close(); });
  $("#kayit").addEventListener("cancel", function (e) { if ($("#kayitKapat").hidden) e.preventDefault(); });
  window.addEventListener("resize", olcekle);
  window.addEventListener("hashchange", function () { var id = location.hash.slice(1); if (id && id !== S.id && S.index.some(function (x) { return x.id === id; })) dersAc(id).catch(hataGoster); });
  document.addEventListener("keydown", function (e) {
    var yaziyor = /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName);
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z" && !yaziyor) { e.preventDefault(); geriAl(); return; }
    if (yaziyor || document.querySelector("dialog[open]")) return;
    if (e.key === "ArrowRight") { var kar = S.mod === "kaynak" ? Slayt.kareler(S.D).filter(function (f) { return f.si === S.secili; }) : [];
      if (S.adim < kar.length - 1) S.adim++; else if (S.secili < slaytlar().length - 1) { S.secili++; S.adim = 0; listeCiz(); formCiz(); } onizle(); e.preventDefault(); }
    if (e.key === "ArrowLeft") { if (S.adim > 0) S.adim--; else if (S.secili > 0) { S.secili--; S.adim = 99; listeCiz(); formCiz(); } onizle(); e.preventDefault(); }
  });
  window.addEventListener("beforeunload", function (e) { if (S.D && degisiklikVar()) { e.preventDefault(); e.returnValue = ""; } });
  function hataGoster(e) { console.error(e); $("#durum").innerHTML = "<b>Hata:</b> " + Slayt.esc(e.message || e); }

  (function () {
    var st = h("style"); st.textContent = Slayt.css("../ortak/fontlar/"); document.head.append(st);
  })();
  new ResizeObserver(olcekle).observe($("#cerceve"));
  basla().catch(hataGoster);
})();
