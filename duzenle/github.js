/* GitHub'a tek commit ile dosya yazar (Git Data API). Anahtar yalnız bu tarayıcıda saklanır. */
(function () {
  "use strict";
  var API = "https://api.github.com";

  function ayar() {
    try { return JSON.parse(localStorage.getItem("lb_github") || "{}"); } catch (e) { return {}; }
  }
  function ayarYaz(a) { try { localStorage.setItem("lb_github", JSON.stringify(a)); } catch (e) {} }

  async function istek(a, yol, secenek) {
    secenek = secenek || {};
    var r = await fetch(API + yol, {
      method: secenek.method || "GET",
      headers: { Authorization: "Bearer " + a.anahtar, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json" },
      body: secenek.body ? JSON.stringify(secenek.body) : undefined
    });
    if (!r.ok) {
      var m = "";
      try { m = (await r.json()).message; } catch (e) {}
      if (r.status === 401) throw new Error("GitHub anahtarı geçersiz ya da süresi dolmuş. Ayarlardan yeni anahtar girin.");
      if (r.status === 403 || r.status === 404) throw new Error("GitHub bu depoya yazma izni vermedi (" + r.status + "). Anahtarın bu depo için 'Contents: Read and write' izni olmalı.");
      throw new Error("GitHub hatası " + r.status + (m ? ": " + m : ""));
    }
    return r.status === 204 ? null : r.json();
  }

  function b64(bytes) {
    var s = "", parca = 0x8000;
    for (var i = 0; i < bytes.length; i += parca) s += String.fromCharCode.apply(null, bytes.subarray(i, i + parca));
    return btoa(s);
  }
  async function baytlar(icerik) {
    if (icerik instanceof Blob) return new Uint8Array(await icerik.arrayBuffer());
    return new TextEncoder().encode(icerik);
  }
  /* git'in blob kimliği: sha1("blob <boy>\0" + içerik). Aynıysa yüklemeye gerek yok. */
  async function blobSha(b) {
    var bas = new TextEncoder().encode("blob " + b.length + "\0");
    var t = new Uint8Array(bas.length + b.length); t.set(bas); t.set(b, bas.length);
    var h = new Uint8Array(await crypto.subtle.digest("SHA-1", t));
    return Array.from(h).map(function (x) { return x.toString(16).padStart(2, "0"); }).join("");
  }

  async function dosyaOku(a, yol) {
    var r = await fetch(API + "/repos/" + a.depo + "/contents/" + yol.split("/").map(encodeURIComponent).join("/") + "?ref=" + encodeURIComponent(a.dal), {
      headers: { Authorization: "Bearer " + a.anahtar, Accept: "application/vnd.github.raw+json" }, cache: "no-store" });
    if (r.status === 404) return null;
    if (!r.ok) throw new Error("GitHub'dan okunamadı: " + yol + " (" + r.status + ")");
    return r.text();
  }

  /* dosyalar: [{yol, icerik (string|Blob)}], sil: [yol], ilerle(metin) */
  async function kaydet(dosyalar, sil, mesaj, ilerle) {
    var a = ayar();
    if (!a.anahtar) throw new Error("Önce Ayarlar'dan GitHub anahtarını girin.");
    ilerle = ilerle || function () {};
    ilerle("Depo okunuyor…");
    var ref = await istek(a, "/repos/" + a.depo + "/git/ref/heads/" + encodeURIComponent(a.dal));
    var basSha = ref.object.sha;
    var commit = await istek(a, "/repos/" + a.depo + "/git/commits/" + basSha);
    var agac = await istek(a, "/repos/" + a.depo + "/git/trees/" + commit.tree.sha + "?recursive=1");
    var mevcut = new Map(agac.tree.filter(function (x) { return x.type === "blob"; }).map(function (x) { return [x.path, x.sha]; }));
    var girdiler = [], yuklenen = 0;
    for (var i = 0; i < dosyalar.length; i++) {
      var d = dosyalar[i], b = await baytlar(d.icerik), sha = await blobSha(b);
      if (mevcut.get(d.yol) === sha) continue;
      ilerle("Yükleniyor " + (i + 1) + "/" + dosyalar.length + ": " + d.yol.split("/").pop());
      var blob = await istek(a, "/repos/" + a.depo + "/git/blobs", { method: "POST", body: { content: b64(b), encoding: "base64" } });
      girdiler.push({ path: d.yol, mode: "100644", type: "blob", sha: blob.sha });
      yuklenen++;
    }
    (sil || []).forEach(function (y) { if (mevcut.has(y)) girdiler.push({ path: y, mode: "100644", type: "blob", sha: null }); });
    if (!girdiler.length) return { degisen: 0 };
    ilerle("Commit yazılıyor…");
    var yeniAgac = await istek(a, "/repos/" + a.depo + "/git/trees", { method: "POST", body: { base_tree: commit.tree.sha, tree: girdiler } });
    var yeni = await istek(a, "/repos/" + a.depo + "/git/commits", { method: "POST", body: { message: mesaj, tree: yeniAgac.sha, parents: [basSha] } });
    await istek(a, "/repos/" + a.depo + "/git/refs/heads/" + encodeURIComponent(a.dal), { method: "PATCH", body: { sha: yeni.sha } });
    return { degisen: girdiler.length, yuklenen: yuklenen, commit: yeni.sha, url: "https://github.com/" + a.depo + "/commit/" + yeni.sha };
  }

  window.GH = { ayar: ayar, ayarYaz: ayarYaz, kaydet: kaydet, dosyaOku: dosyaOku };
})();
