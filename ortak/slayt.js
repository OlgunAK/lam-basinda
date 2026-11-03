/* Lam Başında slayt motoru.
   Bir dersin kaynak dosyasından (canli/dersler/kaynak/<ID>.json):
     - 1920×1080 slayt karelerini HTML olarak çizer (Slayt.html),
     - canlı oturumun okuduğu ders dosyasını üretir (Slayt.canli).
   Hem düzenleyici (duzenle/) hem toplu çizim (tools/slaytlar/ciz.mjs) bunu kullanır.
   Görsel kurallar: DESIGN.md. */
(function (root) {
  "use strict";

  var HARF = "abcdefghijklmnopqrstuvwxyz";
  var T_TUR = { WORDCLOUD: 45, POLL: 45, MCQ: 30, IMGMCQ: 30, FINDIMG: 30, SCT: 45, OPEN: 75, SORTGROUP: 60, SORTORDER: 60, MATCH: 60 };
  var TUR_TR = { WORDCLOUD: "Kelime bulutu", POLL: "Anket", MCQ: "Çoktan seçmeli", IMGMCQ: "Görselli çoktan seçmeli",
    FINDIMG: "Görüntüde bul", SCT: "Senaryo uyum testi (SCT)", OPEN: "Açık uçlu", SORTGROUP: "Sıralama (gruplama)",
    SORTORDER: "Sıralama", MATCH: "Eşleştirme" };
  var TUR_KISA = { MCQ: "Çoktan seçmeli", POLL: "Anket", IMGMCQ: "Görselli çoktan seçmeli", SCT: "Senaryo uyum testi",
    MATCH: "Eşleştirme", SORTGROUP: "Gruplama", SORTORDER: "Sıralama", OPEN: "Açık uçlu", WORDCLOUD: "Kelime bulutu", FINDIMG: "Görüntüde bul" };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  /* Küçük biçim dili: **kalın**, *italik*, -> ok. Gerisi düz yazı. */
  function md(s) {
    s = esc(s);
    s = s.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    s = s.replace(/(^|[^\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])/g, "$1<i>$2</i>");
    s = s.replace(/-&gt;/g, "<span class='ok-isareti'>→</span>");
    return s;
  }
  function ts(sn) { return Math.floor(sn / 60) + ":" + String(sn % 60).padStart(2, "0"); }
  function iki(n) { return String(n).padStart(2, "0"); }

  /* ---------------- kareler ---------------- */
  function adimSayisi(s) {
    if (s.tip === "adim") return (s.maddeler || []).length || 1;
    if (s.tip === "kutular") return (s.adimlar || []).length || 1;
    return 0;
  }
  function kareler(ders) {
    var out = [], no = 0;
    (ders.slaytlar || []).forEach(function (s, si) {
      no++;
      var N = adimSayisi(s);
      if (!N) { out.push({ s: s, si: si, k: 0, N: 0, no: no, ek: "" }); return; }
      for (var k = 0; k < N; k++) out.push({ s: s, si: si, k: k, N: N, no: no, ek: HARF[k] });
    });
    return out;
  }
  function kareSure(f) {
    var s = f.s;
    if (s.tip === "adim") return +(((s.maddeler || [])[f.k] || {}).sure || 0);
    if (s.tip === "kutular") return +(((s.adimlar || [])[f.k] || {}).sure || 0);
    return +(s.sure || 0);
  }
  function kareNot(f) {
    var s = f.s;
    if (s.tip === "adim") return ((s.maddeler || [])[f.k] || {}).not || "";
    if (s.tip === "kutular") return ((s.adimlar || [])[f.k] || {}).not || "";
    return s.not || "";
  }
  function gorselVar(f) { return f.s.tip !== "liderlik" && f.s.tip !== "bulut"; }
  function dosyaAdi(f) { return iki(f.no) + f.ek + ".jpg"; }

  /* ---------------- canlı ders dosyası ---------------- */
  function canliBlok(q, lobby) {
    var t = q.t || T_TUR[q.type], typ = q.type, s = "CANLI (" + q.id + ", " + TUR_TR[typ] + "): ";
    if (lobby) s += "Katılım ekranı açıkken soru telefonlarda açık; girenler hemen yazabilir. L ile katılım ekranını kapatınca bulut perdeye düşer. → kapatır, → sonraki slayt.";
    else if (typ === "WORDCLOUD") s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. Bulut canlı akar. → kapatır, → sonraki slayt.";
    else if (typ === "POLL" && q.hide) s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. → oylamayı kapatıp dağılımı gösterir, → sonraki slayt (tahmin anketi; cevap açılmaz).";
    else if (typ === "OPEN") s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. Cevaplar gizli gelir; H ile göster. → kapatır, → beklenen cevabı açar, → sonraki slayt.";
    else s += "Bu slayta gelince soru telefonlarda kendiliğinden açılır. → oylamayı kapatıp sonuçları gösterir, → doğru cevabı ve açıklamayı açar, → sonraki slayt.";
    if (q.a != null && (typ === "MCQ" || typ === "IMGMCQ" || typ === "POLL")) s += " Doğru: " + "ABCDE"[q.a] + ".";
    if (typ === "FINDIMG") s += " Doğru alan: " + q.answer + ".";
    s += " T: " + t + " sn (perdede T düğmesi bu soruda " + t + " sn sayar).";
    return s;
  }

  function canli(ders) {
    var qmap = {};
    (ders.sorular || []).forEach(function (q) { if (q.t == null) q.t = T_TUR[q.type]; qmap[q.id] = q; });
    var t = 0, slides = [];
    kareler(ders).forEach(function (f) {
      var s = f.s, dur = kareSure(f), son = !f.N || f.k === f.N - 1;
      var notes = "[" + ts(t) + "–" + ts(t + dur) + "]" + (s.opsiyonel ? " ZAMAN KALIRSA; yoksa → ile atla." : "") + "\n" + String(kareNot(f)).trim();
      if (s.tip === "liderlik") {
        var b = { board: true, title: s.baslik, notes: notes };
        if (s.ilk) b.top = s.ilk;
        slides.push(b); t += dur; return;
      }
      if (s.tip === "bulut") { slides.push({ cloud: s.bulut, title: s.baslik, notes: notes }); t += dur; return; }
      var title = (s.opsiyonel ? "(Zaman kalırsa) " : "") + s.baslik + (f.N ? " · " + (f.k + 1) + "/" + f.N : "");
      var j = { img: "slaytlar/" + ders.id + "/" + dosyaAdi(f) + "?v=" + ders.surum, title: title };
      if (f.N) j.step = [f.k + 1, f.N];
      if (s.katilim) j.lobby = true;
      if (s.soruAc && son && qmap[s.soruAc]) {
        var qq = qmap[s.soruAc];
        j.qopen = s.soruAc;
        notes += "\n\nCANLI (" + qq.id + ", " + TUR_TR[qq.type] + "): Soru bu slayta gelince telefonlarda açılır; perde slaytı göstermeye devam eder. " +
          "Oylama bir sonraki slayta (dağılım) kadar açık kalır, geri gelsen de kapanmaz. → sonraki slayt. T: " + qq.t + " sn.";
      }
      if (s.tip === "soru" && s.soru && qmap[s.soru]) {
        var q = qmap[s.soru];
        j.q = s.soru;
        if (s.devam) {
          notes += "\n\nCANLI (" + q.id + ", " + TUR_TR[q.type] + "): Soru önceki slaytta açıldı, oylama hâlâ açık. → oylamayı kapatıp dağılımı gösterir, → sonraki slayt" +
            (q.a != null && q.hide ? " (tahmin anketi; cevap açılmaz). Doğru: " + "ABCDE"[q.a] : "") + ".";
        } else notes += "\n\n" + canliBlok(q, !!s.katilim);
      }
      j.notes = notes;
      slides.push(j);
      t += dur;
    });
    var L = { id: ders.id, title: ders.baslik, date: ders.tarih, questions: ders.sorular || [], slides: slides, duration: ts(t) };
    if (ders.cta) L.cta = ders.cta;
    if (ders.cerceve) L.frame = ders.cerceve;
    if (ders.quiz) L.quiz = ders.quiz;
    return L;
  }

  /* ---------------- görünüm ---------------- */
  var RENK = {
    acik: { bg: "#FAF7FB", yuzey: "#FFFFFF", yuzey2: "#F1ECF6", yazi: "#22163A", yazi2: "#5E5070", cizgi: "#E4DAEC",
      vurgu: "#4A2C82", vurguAcik: "#EEE7F8", vurguUst: "#FFFFFF", simdi: "#B0275B", simdiAcik: "#FBE8EF", simdiUst: "#FFFFFF", kenar: "rgb(0 0 0 / .1)" },
    koyu: { bg: "#160F21", yuzey: "#211830", yuzey2: "#2D2243", yazi: "#F3EDF8", yazi2: "#AFA1C2", cizgi: "#4A3D60",
      vurgu: "#BBA3F0", vurguAcik: "#2D2243", vurguUst: "#160F21", simdi: "#F283AA", simdiAcik: "#3A1E2C", simdiUst: "#160F21", kenar: "rgb(255 255 255 / .1)" }
  };

  function css(fontKok) {
    var f = fontKok || "fontlar/";
    var ff = function (fam, st, sub, w) {
      return "@font-face{font-family:'" + fam + "';font-style:" + st + ";font-weight:" + w + ";src:url('" + f + fam.toLowerCase() + "-" + st + "-" + sub + ".woff2') format('woff2')}";
    };
    var fonts = ["latin", "latin-ext"].map(function (sub) {
      return ff("Literata", "normal", sub, "400 700") + ff("Literata", "italic", sub, "400 700") + ff("Figtree", "normal", sub, "400 800") + ff("Figtree", "italic", sub, "400 800");
    }).join("");
    var tema = function (ad, r) {
      return ".sl." + ad + "{--bg:" + r.bg + ";--yuzey:" + r.yuzey + ";--yuzey2:" + r.yuzey2 + ";--yazi:" + r.yazi + ";--yazi2:" + r.yazi2 +
        ";--cizgi:" + r.cizgi + ";--vurgu:" + r.vurgu + ";--vurgu-acik:" + r.vurguAcik + ";--vurgu-ust:" + r.vurguUst + ";--simdi:" + r.simdi +
        ";--simdi-acik:" + r.simdiAcik + ";--simdi-ust:" + r.simdiUst + ";--kenar:" + r.kenar + "}";
    };
    return fonts + tema("acik", RENK.acik) + tema("koyu", RENK.koyu) + [
      "*{box-sizing:border-box}",
      ".sl{--dikkat:#F2B705;--koyu-zemin:#22163A;width:1920px;height:1080px;position:relative;overflow:hidden;background:var(--bg);color:var(--yazi);font-family:Figtree,system-ui,sans-serif;font-size:34px;line-height:1.3;-webkit-font-smoothing:antialiased;font-variant-numeric:lining-nums}",
      ".sl b{font-weight:700}",
      ".sl .ok-isareti{color:var(--simdi);font-weight:700}",
      ".sl h1{position:absolute;left:96px;right:420px;top:64px;margin:0;font:600 60px/1.12 Literata,Georgia,serif;letter-spacing:-.015em;text-wrap:balance}",
      ".sl .etiketler{position:absolute;right:96px;top:72px;display:flex;gap:12px}",
      ".sl .et{border-radius:999px;padding:8px 18px 9px;font:700 22px/1 Figtree;white-space:nowrap}",
      ".sl .et.dus{background:var(--dikkat);color:#22163A}",
      ".sl .et.ops{border:2px solid var(--cizgi);color:var(--yazi2)}",
      ".sl .et.vaka{background:var(--simdi);color:var(--simdi-ust)}",
      ".sl .govde{position:absolute;left:96px;right:96px;top:206px;bottom:104px;display:flex;gap:48px}",
      /* alt şerit */
      ".sl .alt{position:absolute;left:96px;right:96px;bottom:34px;height:40px;display:flex;align-items:center;gap:18px;font-size:19px;color:var(--yazi2);white-space:nowrap}",
      ".sl .alt .ders{font-weight:600}",
      ".sl .serit{display:flex;gap:6px}",
      ".sl .serit span{border-radius:999px;padding:5px 13px 6px;font:600 18px/1 Figtree;background:var(--yuzey2);color:var(--yazi2)}",
      ".sl .serit span.on{background:var(--vurgu);color:var(--vurgu-ust)}",
      ".sl .alt .bosluk{flex:1}",
      ".sl .alt .kay{font-style:italic;font-size:17px;max-width:900px;overflow:hidden;text-overflow:ellipsis}",
      ".sl .alt .no{font-variant-numeric:tabular-nums;min-width:32px;text-align:right}",
      /* adım listesi */
      ".sl .liste{flex:1;min-width:0;display:flex;flex-direction:column;gap:12px}",
      ".sl .md{border-radius:16px;padding:14px 22px 15px 50px;position:relative;color:var(--yazi2);font-weight:450}",
      ".sl .md::before{content:'';position:absolute;left:22px;top:calc(.65em + 4px);width:12px;height:12px;border-radius:50%;background:var(--cizgi)}",
      ".sl .md.su{background:var(--simdi-acik);color:var(--yazi);font-weight:650}",
      ".sl .md.su::before{background:var(--simdi)}",
      ".sl .md.sonra{visibility:hidden}",
      ".sl .md .ust{display:block;font:650 .82em/1.25 Literata,serif;color:var(--vurgu);margin-bottom:2px}",
      ".sl .md:not(.su) .ust{color:var(--yazi2)}",
      /* görsel sütunu */
      ".sl .gs{flex:0 0 1000px;display:flex;flex-direction:column;gap:20px;min-height:0}",
      ".sl .gs.dar{flex-basis:880px}",
      ".sl .medya{flex:1;display:flex;gap:20px;min-height:0}",
      ".sl figure{margin:0;flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:10px}",
      ".sl figure .cer{flex:1;position:relative;border-radius:16px;overflow:hidden;background:var(--yuzey2);min-height:0}",
      ".sl figure img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;outline:1px solid var(--kenar);outline-offset:-1px;border-radius:16px}",
      ".sl figure.sig img{object-fit:contain}",
      ".sl figure .lab{position:absolute;left:14px;top:14px;min-width:56px;height:56px;border-radius:12px;background:var(--vurgu);color:var(--vurgu-ust);display:grid;place-items:center;font:800 32px/1 Figtree;padding:0 12px}",
      ".sl figcaption{font-size:24px;line-height:1.25;font-weight:650;color:var(--yazi)}",
      ".sl figcaption small{display:block;font-size:19px;font-weight:450;color:var(--yazi2);margin-top:2px}",
      ".sl .soru-isareti{flex:1 1 0;border-radius:16px;background:var(--yuzey2);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;padding:24px;text-align:center}",
      ".sl .soru-isareti div{font:600 170px/1 Literata,serif;color:var(--simdi)}",
      ".sl .soru-isareti span{font-size:24px;font-weight:600;color:var(--yazi2)}",
      ".sl .rakam{flex:1 1 0;border-radius:16px;background:var(--yuzey2);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;text-align:center}",
      ".sl .rakam div{font:600 160px/1 Literata,serif;color:var(--simdi);font-variant-numeric:lining-nums}",
      ".sl .rakam span{font-size:36px;font-weight:650;margin-top:32px;text-wrap:balance}",
      ".sl .kutu{border-radius:16px;padding:24px 30px;font-size:30px;font-weight:600;line-height:1.3;background:var(--vurgu-acik)}",
      ".sl .kutu.pembe{background:var(--simdi-acik)}",
      ".sl .kutu.vurgu{background:var(--simdi);color:var(--simdi-ust);font-family:Literata,serif;font-size:32px}",
      ".sl .kutu.koyu{background:var(--vurgu);color:var(--vurgu-ust)}",
      ".sl .pnot{border-radius:16px;padding:22px 28px;background:var(--koyu-zemin);color:#F3EDF8}",
      ".sl.koyu .pnot{background:var(--yuzey2)}",
      ".sl .pnot h3{margin:0 0 8px;font:600 30px/1.2 Literata,serif;color:#F283AA}",
      ".sl .pnot p{margin:0;font-size:24px;line-height:1.35}",
      ".sl .cubuk{flex:1;border-radius:16px;background:var(--yuzey2);padding:36px 40px;display:flex;flex-direction:column;justify-content:center;gap:34px}",
      ".sl .cubuk h3{margin:0;font:600 32px/1.2 Literata,serif}",
      ".sl .cubuk .sat{display:flex;flex-direction:column;gap:10px}",
      ".sl .cubuk .sat.gizli{visibility:hidden}",
      ".sl .cubuk .ad{font-size:30px;font-weight:700}",
      ".sl .cubuk .ad small{font-weight:450;font-size:24px;color:var(--yazi2)}",
      ".sl .cubuk .iz{height:56px;border-radius:12px;background:var(--yuzey);position:relative}",
      ".sl .cubuk .dol{position:absolute;top:0;bottom:0;border-radius:12px;background:var(--vurgu)}",
      ".sl .cubuk .sat.sic .dol{background:var(--simdi)}",
      ".sl .cubuk .deg{position:absolute;top:50%;transform:translateY(-50%);font:800 28px/1 Figtree;white-space:nowrap;font-variant-numeric:tabular-nums}",
      ".sl .cizim{flex:1;border-radius:16px;overflow:hidden;background:var(--yuzey2)}",
      ".sl .cizim svg{width:100%;height:100%;display:block}",
      /* soru */
      ".sl .soru{flex:1;min-width:0;display:flex;flex-direction:column}",
      ".sl .canli{align-self:flex-start;display:inline-flex;align-items:center;gap:14px;border-radius:999px;padding:12px 24px 12px 20px;background:var(--simdi-acik);color:var(--yazi);font:650 26px/1 Figtree}",
      ".sl .canli i{width:16px;height:16px;border-radius:50%;background:var(--simdi);box-shadow:0 0 0 6px color-mix(in oklab,var(--simdi) 25%,transparent)}",
      ".sl .canli small{font-size:22px;font-weight:500;color:var(--yazi2)}",
      ".sl .qq{font:600 44px/1.25 Literata,serif;margin:36px 0 0;text-wrap:balance;letter-spacing:-.01em}",
      ".sl .sec{margin-top:40px;display:flex;flex-direction:column;gap:18px}",
      ".sl .secenek{display:flex;align-items:center;gap:24px;font-size:31px;line-height:1.25}",
      ".sl .secenek b{flex:0 0 60px;height:60px;border-radius:50%;background:var(--vurgu);color:var(--vurgu-ust);display:grid;place-items:center;font:800 28px/1 Figtree}",
      ".sl .aciklama{margin-top:48px;font-size:32px;color:var(--yazi2);max-width:1400px}",
      ".sl .esle{margin-top:40px;display:flex;gap:56px}",
      ".sl .esle div{flex:1;display:flex;flex-direction:column;gap:14px}",
      ".sl .esle span{border-radius:14px;background:var(--yuzey2);padding:20px 26px;font-size:30px;font-weight:600}",
      /* kutular (plan) */
      ".sl .kutular{flex:1;display:flex;flex-direction:column;gap:20px;min-width:0}",
      ".sl .kutular .ust3{flex:1;display:flex;gap:20px;min-height:0}",
      ".sl .kt{flex:1 1 0;border-radius:16px;padding:26px 30px;background:var(--vurgu-acik);display:flex;flex-direction:column;gap:14px;min-width:0}",
      ".sl .kt.gizli{visibility:hidden}",
      ".sl .kt.koyu{background:var(--vurgu);color:var(--vurgu-ust)}",
      ".sl .kt.pembe{background:var(--simdi-acik)}",
      ".sl .kt.vurgu{background:var(--simdi-acik);flex:none}",
      ".sl .kt h3{margin:0;font:600 34px/1.2 Literata,serif}",
      ".sl .kt ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:10px;font-size:28px;line-height:1.25}",
      ".sl .kt li{padding-left:24px;position:relative}",
      ".sl .kt li::before{content:'';position:absolute;left:2px;top:.5em;width:9px;height:9px;border-radius:50%;background:currentColor;opacity:.55}",
      ".sl .kt p{margin:0;font-size:28px;line-height:1.3}",
      ".sl .kt table{border-collapse:collapse;font-size:24px;line-height:1.25}",
      ".sl .kt td{padding:9px 0;border-top:1px solid color-mix(in oklab,currentColor 18%,transparent);vertical-align:top}",
      ".sl .kt tr:first-child td{border-top:0}",
      ".sl .kt td:first-child{font-weight:700;width:180px;padding-right:18px}",
      /* tablo */
      ".sl .tablo{border-collapse:collapse;width:100%;max-width:1500px;font-size:30px;line-height:1.3}",
      ".sl .tablo th{text-align:left;font:600 24px/1.2 Figtree;color:var(--yazi2);padding:0 24px 14px 0}",
      ".sl .tablo td{padding:18px 24px 18px 0;border-top:1px solid var(--cizgi);vertical-align:top}",
      ".sl .tablo td:first-child{font-weight:650;width:44%}",
      /* kaynaklar */
      ".sl .kayn{flex:1;display:flex;flex-direction:column;gap:22px}",
      ".sl .kayn ol{margin:0;padding:0 0 0 1.4em;font-size:26px;line-height:1.35;display:flex;flex-direction:column;gap:10px}",
      ".sl .kayn ol li::marker{color:var(--yazi2);font-variant-numeric:tabular-nums}",
      ".sl .quizk{display:flex;gap:34px;align-items:center;border-radius:16px;background:var(--vurgu-acik);padding:24px 30px}",
      ".sl .quizk img{width:180px;height:180px;border-radius:8px;background:#fff;padding:8px}",
      ".sl .quizk div{font-size:28px;line-height:1.4}",
      ".sl .quizk b{font-size:30px}",
      ".sl .quizk span{display:block;font-weight:700;color:var(--simdi);font-size:32px;letter-spacing:.01em}",
      ".sl .cagri{border-radius:16px;background:var(--simdi);color:var(--simdi-ust);padding:22px 30px;font:600 32px/1.3 Literata,serif}",
      /* kapak */
      ".sl.kapak{background:#22163A;color:#fff}",
      ".sl .kp-sol{position:absolute;left:0;top:0;bottom:0;width:1240px;padding:96px 110px 64px 112px;display:flex;flex-direction:column}",
      ".sl .kp-sag{position:absolute;left:1240px;right:0;top:0;bottom:0}",
      ".sl .kp-sag img{width:100%;height:100%;object-fit:cover;display:block}",
      ".sl .kp-isaret{display:flex;align-items:center;gap:18px;font:600 26px/1.2 Figtree;color:#D9CDEB}",
      ".sl .kp-isaret svg{width:64px;height:64px}",
      ".sl .kp-bas{margin-top:auto;font:600 92px/1.06 Literata,serif;letter-spacing:-.02em;text-wrap:balance}",
      ".sl .kp-alt{margin-top:28px;font-size:36px;line-height:1.3;color:#E4DAF0;text-wrap:balance}",
      ".sl .kp-tarih{margin-top:36px;font-size:28px;color:#fff;font-variant-numeric:tabular-nums}",
      ".sl .kp-vaka{margin-top:48px;border-radius:18px;background:#B0275B;padding:24px 30px;font:600 36px/1.25 Literata,serif;color:#fff;text-wrap:balance}",
      ".sl .kp-kay{margin-top:26px;font-size:16px;font-style:italic;color:#B9ABCD}"
    ].join("\n");
  }

  var ISARET = "<svg viewBox='0 0 40 40' aria-hidden='true'><rect x='2' y='9' width='36' height='22' rx='4' fill='#EEE7F8' stroke='#BBA3F0' stroke-width='1.5'/>" +
    "<rect x='4.5' y='11.5' width='8' height='17' rx='2' fill='#4A2C82' opacity='.16'/><path d='M16 21.5c0-5 4-8 9-7.6 5 .4 9 3 8.6 7-.4 4.4-4.6 6.3-9 6.1-5-.2-8.6-1.5-8.6-5.5z' fill='#F283AA'/>" +
    "<circle cx='21' cy='19' r='1.7' fill='#4A2C82'/><circle cx='26.5' cy='17.4' r='1.5' fill='#4A2C82'/><circle cx='29.5' cy='22.2' r='1.7' fill='#4A2C82'/><circle cx='23.4' cy='24' r='1.4' fill='#4A2C82'/></svg>";

  function keloid(asama, r) {
    var deri = "#F3D2C1", skar = "#C9879A";
    var p = ["<svg viewBox='0 0 1000 780' preserveAspectRatio='xMidYMid meet'>"];
    p.push("<text x='500' y='110' text-anchor='middle' font-family='Figtree' font-size='30' fill='" + r.yazi2 + "'>Kesikli çizgi: yaranın sınırı</text>");
    [[250, "Hipertrofik skar"], [750, "Keloid"]].forEach(function (a) {
      var x = a[0];
      p.push("<rect x='" + (x - 210) + "' y='320' width='420' height='300' rx='16' fill='" + deri + "'/>");
      p.push("<line x1='" + (x - 90) + "' y1='320' x2='" + (x + 90) + "' y2='320' stroke='" + r.yazi + "' stroke-width='4' stroke-dasharray='10 8'/>");
      p.push("<text x='" + x + "' y='690' text-anchor='middle' font-family='Literata' font-weight='600' font-size='38' fill='" + r.yazi + "'>" + a[1] + "</text>");
    });
    if (asama >= 1) p.push("<path d='M160 320 Q250 220 340 320 Z' fill='" + skar + "'/>");
    if (asama >= 2) {
      p.push("<path d='M540 320 Q600 140 750 160 Q900 140 960 320 Z' fill='" + skar + "'/>");
      p.push("<text x='750' y='255' text-anchor='middle' font-family='Figtree' font-weight='700' font-size='30' fill='#fff'>sınırı aşar</text>");
    }
    p.push("</svg>");
    return p.join("");
  }

  function yol(o, src) { return o.coz ? o.coz(src) : (o.kok || "") + src; }
  function foto(p, o) {
    var src = yol(o, p.foto);
    var pos = p.konum ? ";object-position:" + esc(p.konum) : "";
    var cap = p.yazi ? "<figcaption>" + md(p.yazi) + (p.alt ? "<small>" + md(p.alt) + "</small>" : "") + "</figcaption>" : "";
    return "<figure class='" + (p.sigdir ? "sig" : "") + "'><div class='cer'><img src='" + esc(src) + "' alt='' style='" + pos.slice(1) + "'>" +
      (p.etiket ? "<div class='lab'>" + esc(p.etiket) + "</div>" : "") + "</div>" + cap + "</figure>";
  }

  function panelHTML(ps, o, r) {
    var medya = [], yazi = [];
    (ps || []).forEach(function (p) {
      if (p.foto) medya.push(foto(p, o));
      else if (p.soruIsareti != null) medya.push("<div class='soru-isareti'><div>?</div><span>" + md(p.soruIsareti) + "</span></div>");
      else if (p.rakam != null) medya.push("<div class='rakam'><div>" + esc(p.rakam) + "</div><span>" + md(p.aciklama || "") + "</span></div>");
      else if (p.cubuklar) {
        var kadar = p.kadar == null ? 99 : p.kadar;
        medya.push("<div class='cubuk'>" + (p.baslik ? "<h3>" + md(p.baslik) + "</h3>" : "") + p.cubuklar.map(function (c, i) {
          var ic = c.ust < 70;
          return "<div class='sat" + (c.vurgu ? " sic" : "") + (i > kadar ? " gizli" : "") + "'><div class='ad'>" + esc(c.ad) + (c.not ? " <small>· " + md(c.not) + "</small>" : "") + "</div>" +
            "<div class='iz'><div class='dol' style='left:" + c.alt + "%;width:" + (c.ust - c.alt) + "%'></div>" +
            "<div class='deg' style='left:calc(" + (ic ? c.ust : c.alt) + "% + 16px);color:" + (ic ? "var(--yazi)" : (c.vurgu ? "var(--simdi-ust)" : "var(--vurgu-ust)")) + "'>%" + c.alt + "–" + c.ust + "</div></div></div>";
        }).join("") + "</div>");
      }
      else if (p.cizim === "keloid") medya.push("<div class='cizim'>" + keloid(p.asama || 0, r) + "</div>");
      else if (p.kutu != null) yazi.push("<div class='kutu " + esc(p.ton || "mor") + "'>" + md(p.kutu) + "</div>");
      else if (p.not) yazi.push("<div class='pnot'><h3>Patoloğun notu: " + md(p.not.baslik) + "</h3><p>" + md(p.not.metin) + "</p></div>");
    });
    return (medya.length ? "<div class='medya'>" + medya.join("") + "</div>" : "") + yazi.join("");
  }

  function etiketler(s) {
    var e = [];
    if (s.opsiyonel) e.push("<span class='et ops'>Zaman kalırsa</span>");
    if (s.etiket) e.push("<span class='et vaka'>" + esc(s.etiket) + "</span>");
    if (s.dus) e.push("<span class='et dus'>DUS</span>");
    return e.length ? "<div class='etiketler'>" + e.join("") + "</div>" : "";
  }

  function altSerit(ders, s, no) {
    var serit = "";
    if (s.serit && ders.serit && ders.serit.gruplar) {
      serit = "<div class='serit'>" + ders.serit.gruplar.map(function (g, i) {
        return "<span class='" + (s.serit.indexOf(i + 1) >= 0 ? "on" : "") + "'>" + esc(g) + "</span>";
      }).join("") + "</div>";
    }
    return "<div class='alt'><span class='ders'>" + esc(ders.kisa || ders.baslik) + "</span><span>4. Sınıf Patoloji</span>" + serit +
      "<span class='bosluk'></span>" + (s.kaynak ? "<span class='kay'>Görseller: " + md(s.kaynak) + "</span>" : "") +
      (s.numarasiz ? "" : "<span class='no'>" + no + "</span>") + "</div>";
  }

  function soruGovde(ders, s, o, r) {
    var q = (ders.sorular || []).filter(function (x) { return x.id === s.soru; })[0];
    if (!q) return "<div class='soru'><div class='qq'>Soru bulunamadı: " + esc(s.soru) + "</div></div>";
    var h = "<div class='canli'><i></i>Telefonda açık <small>" + esc(TUR_KISA[q.type] || q.type) + "</small></div>";
    h += "<div class='qq'>" + md(q.q) + "</div>";
    if (q.type === "MATCH" && q.left) {
      h += "<div class='esle'><div>" + q.left.map(function (x) { return "<span>" + md(x) + "</span>"; }).join("") + "</div><div>" +
        (q.right || []).map(function (x) { return "<span>" + md(x) + "</span>"; }).join("") + "</div></div>";
    } else if (q.opts && q.opts.length && !(q.type === "IMGMCQ" && s.gorsel && q.opts.join("") === "ABCD".slice(0, q.opts.length))) {
      h += "<div class='sec'>" + q.opts.map(function (x, i) { return "<div class='secenek'><b>" + "ABCDE"[i] + "</b><span>" + md(x) + "</span></div>"; }).join("") + "</div>";
    }
    if (s.aciklama) h += "<div class='aciklama'>" + md(s.aciklama) + "</div>";
    var sol = "<div class='soru' data-kutu data-sigdir='" + (s.yazi || 54) + "'>" + h + "</div>";
    if (s.gorsel && s.gorsel.length) {
      var cok = s.gorsel.length > 2 && s.gorsel.every(function (p) { return p.foto; });
      var g = cok ? "<div class='gs dar' style='gap:16px'><div class='medya'>" + s.gorsel.slice(0, 2).map(function (p) { return foto(p, o); }).join("") +
        "</div><div class='medya'>" + s.gorsel.slice(2).map(function (p) { return foto(p, o); }).join("") + "</div></div>"
        : "<div class='gs dar'>" + panelHTML(s.gorsel, o, r) + "</div>";
      return sol + g;
    }
    return sol;
  }

  /* Bir karenin bütün HTML'i (yalnız .sl öğesi; CSS ayrı). o: {kok: görsel yolu öneki} */
  function kareHTML(ders, f, o) {
    o = o || {};
    var s = f.s, tema = s.tema === "koyu" ? "koyu" : "acik", r = RENK[tema];
    if (s.tip === "kapak") {
      return "<div class='sl kapak koyu'><div class='kp-sol'><div class='kp-isaret'>" + ISARET + "<span>Lam Başında · " + esc(s.ust || "4. Sınıf Patoloji") + "</span></div>" +
        "<div class='kp-bas' data-sigdir='92'>" + md(s.baslik) + "</div>" + (s.alt ? "<div class='kp-alt'>" + md(s.alt) + "</div>" : "") +
        (s.tarih ? "<div class='kp-tarih'>" + esc(s.tarih) + "</div>" : "") + (s.vaka ? "<div class='kp-vaka'>" + md(s.vaka) + "</div>" : "") +
        (s.kaynak ? "<div class='kp-kay'>Görsel: " + md(s.kaynak) + "</div>" : "") + "</div>" +
        "<div class='kp-sag'>" + (s.gorsel && s.gorsel.foto ? "<img src='" + esc(yol(o, s.gorsel.foto)) + "' alt=''" +
          (s.gorsel.konum ? " style='object-position:" + esc(s.gorsel.konum) + "'" : "") + ">" : "") + "</div></div>";
    }
    var govde = "";
    if (s.tip === "adim") {
      var ms = s.maddeler || [], gor = null, hepsi = ms.some(function (m) { return m.gorsel && m.gorsel.length; });
      for (var i = 0; i <= f.k && i < ms.length; i++) if (ms[i].gorsel && ms[i].gorsel.length) gor = ms[i].gorsel;
      var dar = tema === "koyu" && s.soruAc;
      govde = (hepsi ? "<div class='gs" + (dar ? " dar" : "") + "'>" + (gor ? panelHTML(gor, o, r) : "") + "</div>" : "") +
        "<div class='liste' data-kutu data-sigdir='" + (s.yazi || 36) + "'>" + ms.map(function (m, i) {
          return "<div class='md " + (i < f.k ? "once" : i === f.k ? "su" : "sonra") + "'>" + (m.ust ? "<span class='ust'>" + md(m.ust) + "</span>" : "") + md(m.metin) + "</div>";
        }).join("") + "</div>";
    } else if (s.tip === "soru") {
      govde = soruGovde(ders, s, o, r);
    } else if (s.tip === "kutular") {
      var ks = s.kutular || [], ust = ks.filter(function (k) { return k.ton !== "vurgu"; }), alt = ks.filter(function (k) { return k.ton === "vurgu"; });
      var kt = function (k) {
        var idx = ks.indexOf(k);
        var ic = k.tablo ? "<table>" + k.tablo.map(function (rw) { return "<tr>" + rw.map(function (c) { return "<td>" + md(c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</table>"
          : (k.maddeler || []).length > 1 || k.baslik ? "<ul>" + (k.maddeler || []).map(function (m) { return "<li>" + md(m) + "</li>"; }).join("") + "</ul>"
            : "<p>" + md((k.maddeler || [])[0] || "") + "</p>";
        return "<div class='kt " + esc(k.ton || "mor") + (idx > f.k ? " gizli" : "") + "'" + (k.genislik ? " style='flex:0 0 " + (+k.genislik) + "px'" : "") + ">" +
          (k.baslik ? "<h3>" + md(k.baslik) + "</h3>" : "") + ic + "</div>";
      };
      govde = "<div class='kutular' data-kutu data-sigdir='28'><div class='ust3'>" + ust.map(kt).join("") + "</div>" + alt.map(kt).join("") + "</div>";
    } else if (s.tip === "tablo") {
      var th = (s.tabloBaslik || "").split("→").map(function (x) { return x.trim(); });
      govde = "<div style='flex:1' data-kutu data-sigdir='30'><table class='tablo'>" + (th.length === 2 ? "<tr><th>" + esc(th[0][0].toUpperCase() + th[0].slice(1)) + "</th><th>" + esc(th[1][0].toUpperCase() + th[1].slice(1)) + "</th></tr>" : "") +
        (s.satirlar || []).map(function (rw) { return "<tr>" + rw.map(function (c) { return "<td>" + md(c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</table></div>";
    } else if (s.tip === "kaynaklar") {
      govde = "<div class='kayn' data-kutu data-sigdir='26'><ol>" + (s.maddeler || []).map(function (m) { return "<li>" + md(m) + "</li>"; }).join("") + "</ol>" +
        (s.quizAdres ? "<div class='quizk'><img src='" + esc(yol(o, s.karekod || "img/quiz_qr.png")) + "' alt=''><div><b>Evde tekrar: slaytlar ve quiz (isteyen çözsün)</b><br>" + md(s.quizMetni || "") +
          "<span>" + esc(s.quizAdres) + "</span></div></div>" : "") + (s.cagri ? "<div class='cagri'>" + md(s.cagri) + "</div>" : "") + "</div>";
    } else if (s.tip === "liderlik" || s.tip === "bulut") {
      govde = "<div class='soru'><div class='canli'><i></i>" + (s.tip === "liderlik" ? "Liderlik tablosu canlı çizilir" : "Kelime bulutu canlı çizilir") + "</div>" +
        "<div class='aciklama'>Bu slaytın görüntüsü yok; perde bu sırada canlı veriyi gösterir.</div></div>";
    } else if (s.tip === "resim") {
      return "<div class='sl acik'><img src='" + esc(yol(o, s.src)) + "' style='width:100%;height:100%;object-fit:contain' alt=''></div>";
    }
    return "<div class='sl " + tema + "'><h1 data-sigdir='60'>" + md(s.baslik) + "</h1>" + etiketler(s) + "<div class='govde'>" + govde + "</div>" + altSerit(ders, s, f.no) + "</div>";
  }

  /* Taşan yazıyı küçültür: data-sigdir taşıyan öğelerde yazı boyunu, kutusuna sığana kadar indirir. */
  function sigdir(kok) {
    var h1 = kok.querySelector("h1");
    if (h1) {
      var fs = 60;
      while (fs > 40 && h1.offsetHeight > 2 * fs * 1.12 + 4) { fs -= 2; h1.style.fontSize = fs + "px"; }
    }
    var kp = kok.querySelector(".kp-bas");
    if (kp) {
      var k2 = 92;
      while (k2 > 56 && kp.offsetHeight > 3 * k2 * 1.06 + 4) { k2 -= 4; kp.style.fontSize = k2 + "px"; }
    }
    var govde = kok.querySelector(".govde");
    kok.querySelectorAll("[data-kutu]").forEach(function (el) {
      var bas = +el.getAttribute("data-sigdir") || 34, fs = bas, en = Math.max(18, Math.round(bas * 0.6));
      var tasar = function () {
        if (el.scrollHeight > el.clientHeight + 1) return true;
        if (govde) { var g = govde.getBoundingClientRect(), b = el.getBoundingClientRect(), olc = g.height / (govde.clientHeight || 1); return b.bottom > g.bottom + olc || el.scrollHeight > govde.clientHeight + 1; }
        return false;
      };
      var qq = el.querySelector(".qq");
      var uygula = function () {
        if (qq) {
          qq.style.fontSize = fs + "px";
          el.querySelectorAll(".secenek,.esle span").forEach(function (x) { x.style.fontSize = Math.round(fs * 0.74) + "px"; });
          el.querySelectorAll(".secenek b").forEach(function (x) { var d = Math.round(fs * 1.12); x.style.flexBasis = d + "px"; x.style.height = d + "px"; });
        } else el.style.fontSize = fs + "px";
      };
      uygula();
      while (tasar() && fs > en) { fs -= 1; uygula(); }
    });
    var liste = kok.querySelector(".liste");
    if (liste) liste.style.overflow = "hidden";
  }

  /* Yeni boş ders ve slaytlar (düzenleyici için) */
  var SABLON = {
    adim: function () { return { tip: "adim", baslik: "Yeni slayt", maddeler: [{ metin: "Birinci madde", sure: 8, not: "" }] }; },
    soru: function () { return { tip: "soru", baslik: "Soru", soru: "", tema: "koyu", sure: 40, not: "" }; },
    kutular: function () { return { tip: "kutular", baslik: "Dersin planı", kutular: [{ baslik: "Birinci grup", ton: "koyu", maddeler: ["Konu"] }], adimlar: [{ sure: 10, not: "" }] }; },
    tablo: function () { return { tip: "tablo", baslik: "Tablo", tabloBaslik: "Sol → Sağ", satirlar: [["", ""]], sure: 30, not: "" }; },
    kaynaklar: function () { return { tip: "kaynaklar", baslik: "Kaynaklar ve evde tekrar", maddeler: [""], quizMetni: "", quizAdres: "olgunak.github.io/lam-basinda/quiz", cagri: "", sure: 10, not: "" }; },
    kapak: function () { return { tip: "kapak", baslik: "Ders adı", alt: "", tarih: "", ust: "4. Sınıf Patoloji · Diş Hekimliği", vaka: "", katilim: true, numarasiz: true, sure: 60, not: "" }; },
    liderlik: function () { return { tip: "liderlik", baslik: "Liderlik tablosu", sure: 20, not: "" }; },
    bulut: function () { return { tip: "bulut", baslik: "Geçen dersin çıkış bileti", bulut: { q: "", from: "prev" }, sure: 20, not: "" }; }
  };

  var Slayt = { md: md, esc: esc, ts: ts, kareler: kareler, kareSure: kareSure, kareNot: kareNot, dosyaAdi: dosyaAdi, gorselVar: gorselVar,
    canli: canli, css: css, html: kareHTML, sigdir: sigdir, SABLON: SABLON, TUR_TR: TUR_TR, T_TUR: T_TUR, adimSayisi: adimSayisi };
  if (typeof module !== "undefined" && module.exports) module.exports = Slayt;
  else root.Slayt = Slayt;
})(typeof window !== "undefined" ? window : globalThis);
