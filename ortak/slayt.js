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

  /* ---------------- görünüm ----------------
     Token'lar üç katman (DESIGN.md):
       ilkel (--p-*: boyanın kendisi) → anlamsal (--bg, --yazi, --vurgu, --simdi…; tema değiştirir) → bileşen (--madde-*, --not-*, --kapak-*…).
     Kurallar yalnız anlamsal ve bileşen token'larını kullanır; ham renk yalnız ilkel katmanda yazılır. */
  var ILKEL = {
    "hema-900": "#22163A", "hema-700": "#4A2C82", "hema-300": "#BBA3F0", "hema-100": "#EEE7F8",
    "eosin-700": "#B0275B", "eosin-300": "#F283AA", "eosin-100": "#FBE8EF", "amber-400": "#F2B705",
    "glass-50": "#FAF7FB", "glass-100": "#F1ECF6", "glass-200": "#E4DAEC", "glass-600": "#5E5070", "beyaz": "#FFFFFF",
    "night-950": "#160F21", "night-900": "#211830", "night-800": "#2D2243", "night-600": "#4A3D60", "night-300": "#AFA1C2", "night-50": "#F3EDF8",
    "deri": "#F3D2C1", "skar": "#C9879A", "kenar-koyu": "rgb(0 0 0 / .1)", "kenar-acik": "rgb(255 255 255 / .1)"
  };
  var ANLAM = {
    acik: { bg: "glass-50", yuzey: "beyaz", yuzey2: "glass-100", yazi: "hema-900", yazi2: "glass-600", cizgi: "glass-200",
      vurgu: "hema-700", "vurgu-acik": "hema-100", "vurgu-ust": "beyaz", simdi: "eosin-700", "simdi-acik": "eosin-100", "simdi-ust": "beyaz",
      dikkat: "amber-400", "dikkat-ust": "hema-900", kenar: "kenar-koyu" },
    koyu: { bg: "night-950", yuzey: "night-900", yuzey2: "night-800", yazi: "night-50", yazi2: "night-300", cizgi: "night-600",
      vurgu: "hema-300", "vurgu-acik": "night-800", "vurgu-ust": "night-950", simdi: "eosin-300", "simdi-acik": "night-800", "simdi-ust": "night-950",
      dikkat: "amber-400", "dikkat-ust": "hema-900", kenar: "kenar-acik" }
  };
  var BILESEN = [
    "--kose:16px", "--kenar-bosluk:96px",
    "--baslik-boy:60px", "--madde-boy:36px", "--altyazi-boy:24px", "--kucuk-boy:19px",
    "--madde-isaret:var(--cizgi)", "--madde-su-zemin:var(--simdi-acik)", "--madde-su-isaret:var(--simdi)", "--madde-once-yazi:var(--yazi2)",
    "--ust-yazi:var(--vurgu)",
    "--secenek-zemin:var(--vurgu)", "--secenek-yazi:var(--vurgu-ust)",
    "--not-zemin:var(--p-hema-900)", "--not-yazi:var(--p-night-50)", "--not-baslik:var(--p-eosin-300)",
    "--kapak-zemin:var(--p-hema-900)", "--kapak-yazi:var(--p-beyaz)", "--kapak-yazi2:var(--p-night-300)", "--kapak-vaka:var(--p-eosin-700)",
    "--alan-zemin:var(--vurgu-acik)", "--cizim-deri:var(--p-deri)", "--cizim-skar:var(--p-skar)", "--karekod-zemin:var(--p-beyaz)"
  ].join(";");

  function css(fontKok) {
    var f = fontKok || "fontlar/";
    var ff = function (fam, st, sub, w) {
      return "@font-face{font-family:'" + fam + "';font-style:" + st + ";font-weight:" + w + ";src:url('" + f + fam.toLowerCase() + "-" + st + "-" + sub + ".woff2') format('woff2')}";
    };
    var fonts = ["latin", "latin-ext"].map(function (sub) {
      return ff("Literata", "normal", sub, "400 700") + ff("Literata", "italic", sub, "400 700") + ff("Figtree", "normal", sub, "400 800") + ff("Figtree", "italic", sub, "400 800");
    }).join("");
    var ilkel = ".sl{" + Object.keys(ILKEL).map(function (k) { return "--p-" + k + ":" + ILKEL[k]; }).join(";") + "}";
    var tema = function (ad) {
      var t = ANLAM[ad];
      return ".sl." + ad + "{" + Object.keys(t).map(function (k) { return "--" + k + ":var(--p-" + t[k] + ")"; }).join(";") + "}";
    };
    return fonts + ilkel + tema("acik") + tema("koyu") + ".sl{" + BILESEN + "}" + [
      "*{box-sizing:border-box}",
      ".sl{width:1920px;height:1080px;position:relative;overflow:hidden;background:var(--bg);color:var(--yazi);font-family:Figtree,system-ui,sans-serif;font-size:var(--madde-boy);line-height:1.3;-webkit-font-smoothing:antialiased;font-variant-numeric:lining-nums}",
      ".sl.alan{background:var(--alan-zemin)}",
      ".sl b{font-weight:700}",
      ".sl .ok-isareti{color:var(--simdi);font-weight:700}",
      ".sl h1{position:absolute;left:var(--kenar-bosluk);right:280px;top:64px;margin:0;font:600 var(--baslik-boy)/1.12 Literata,Georgia,serif;letter-spacing:-.015em;text-wrap:balance}",
      ".sl .dus{position:absolute;right:var(--kenar-bosluk);top:76px;border-radius:999px;padding:9px 20px 10px;font:800 24px/1 Figtree;background:var(--dikkat);color:var(--dikkat-ust)}",
      ".sl .govde{position:absolute;left:var(--kenar-bosluk);right:var(--kenar-bosluk);top:206px;bottom:104px;display:flex;gap:48px}",
      /* alt şerit */
      ".sl .alt{position:absolute;left:var(--kenar-bosluk);right:var(--kenar-bosluk);bottom:34px;height:40px;display:flex;align-items:center;gap:18px;font-size:var(--kucuk-boy);color:var(--yazi2);white-space:nowrap}",
      ".sl .alt .ders{font-weight:600}",
      ".sl .alt .ops{font-weight:700;color:var(--yazi)}",
      ".sl .serit{display:flex;gap:6px}",
      ".sl .serit span{border-radius:999px;padding:5px 13px 6px;font:600 18px/1 Figtree;background:var(--yuzey2);color:var(--yazi2)}",
      ".sl .serit span.on{background:var(--vurgu);color:var(--vurgu-ust)}",
      ".sl .ilerleme{display:flex;align-items:center;gap:10px;font-weight:600;color:var(--yazi)}",
      ".sl .ilerleme i{width:14px;height:14px;border-radius:50%;background:var(--cizgi)}",
      ".sl .ilerleme i.on{background:var(--simdi)}",
      ".sl .ilerleme i.su{background:var(--simdi);width:34px;border-radius:7px}",
      ".sl .alt .bosluk{flex:1}",
      ".sl .alt .kay{font-style:italic;font-size:17px;max-width:900px;overflow:hidden;text-overflow:ellipsis}",
      ".sl .alt .no{font-variant-numeric:tabular-nums;min-width:32px;text-align:right}",
      /* adım listesi */
      ".sl .liste{flex:1;min-width:0;display:flex;flex-direction:column;gap:12px}",
      ".sl .md{border-radius:var(--kose);padding:14px 22px 15px 50px;position:relative;color:var(--madde-once-yazi);font-weight:450}",
      ".sl .md::before{content:'';position:absolute;left:22px;top:calc(.65em + 4px);width:12px;height:12px;border-radius:50%;background:var(--madde-isaret)}",
      ".sl .md.su{background:var(--madde-su-zemin);color:var(--yazi);font-weight:600}",
      ".sl .md.su::before{background:var(--madde-su-isaret)}",
      ".sl .md.sonra{visibility:hidden}",
      ".sl .md .ust{font-weight:750;color:var(--yazi)}",
      ".sl .md.su .ust{color:var(--ust-yazi)}",
      /* görsel sütunu */
      ".sl .gs{flex:0 0 1000px;display:flex;flex-direction:column;gap:20px;min-height:0}",
      ".sl .gs.dar{flex-basis:880px}",
      ".sl .medya{flex:1;display:flex;gap:20px;min-height:0}",
      ".sl figure{margin:0;flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:10px}",
      ".sl figure .cer{flex:1;position:relative;border-radius:var(--kose);overflow:hidden;background:var(--yuzey2);min-height:0}",
      ".sl figure img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;outline:1px solid var(--kenar);outline-offset:-1px;border-radius:var(--kose)}",
      ".sl figure.sig img{object-fit:contain}",
      ".sl figure .lab{position:absolute;left:14px;top:14px;min-width:56px;height:56px;border-radius:12px;background:var(--vurgu);color:var(--vurgu-ust);display:grid;place-items:center;font:800 32px/1 Figtree;padding:0 12px}",
      ".sl figcaption{font-size:var(--altyazi-boy);line-height:1.25;font-weight:650;color:var(--yazi)}",
      ".sl figcaption small{display:block;font-size:var(--kucuk-boy);font-weight:450;color:var(--yazi2);margin-top:2px}",
      ".sl .soru-isareti{flex:1 1 0;border-radius:var(--kose);background:var(--yuzey2);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;padding:24px;text-align:center}",
      ".sl .soru-isareti div{font:600 170px/1 Literata,serif;color:var(--simdi)}",
      ".sl .soru-isareti span{font-size:var(--altyazi-boy);font-weight:600;color:var(--yazi2)}",
      ".sl .rakam{flex:1 1 0;border-radius:var(--kose);background:var(--yuzey2);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;text-align:center}",
      ".sl .rakam div{font:600 160px/1 Literata,serif;color:var(--simdi)}",
      ".sl .rakam span{font-size:36px;font-weight:650;margin-top:32px;text-wrap:balance}",
      ".sl .kutu{border-radius:var(--kose);padding:24px 30px;font-size:30px;font-weight:600;line-height:1.3;background:var(--vurgu-acik)}",
      ".sl .kutu.pembe{background:var(--simdi-acik)}",
      ".sl .kutu.vurgu{background:var(--simdi);color:var(--simdi-ust);font-family:Literata,serif;font-size:32px}",
      ".sl .kutu.koyu{background:var(--vurgu);color:var(--vurgu-ust)}",
      ".sl .pnot{border-radius:var(--kose);padding:22px 28px;background:var(--not-zemin);color:var(--not-yazi)}",
      ".sl .pnot h3{margin:0 0 8px;font:600 30px/1.2 Literata,serif;color:var(--not-baslik)}",
      ".sl .pnot p{margin:0;font-size:var(--altyazi-boy);line-height:1.35}",
      ".sl .cubuk{flex:1;border-radius:var(--kose);background:var(--yuzey2);padding:36px 40px;display:flex;flex-direction:column;justify-content:center;gap:34px}",
      ".sl .cubuk h3{margin:0;font:600 32px/1.2 Literata,serif}",
      ".sl .cubuk .sat{display:flex;flex-direction:column;gap:10px}",
      ".sl .cubuk .sat.gizli{visibility:hidden}",
      ".sl .cubuk .ad{font-size:30px;font-weight:700}",
      ".sl .cubuk .ad small{font-weight:450;font-size:var(--altyazi-boy);color:var(--yazi2)}",
      ".sl .cubuk .iz{height:56px;border-radius:12px;background:var(--yuzey);position:relative}",
      ".sl .cubuk .dol{position:absolute;top:0;bottom:0;border-radius:12px;background:var(--vurgu)}",
      ".sl .cubuk .sat.sic .dol{background:var(--simdi)}",
      ".sl .cubuk .deg{position:absolute;top:50%;transform:translateY(-50%);font:800 28px/1 Figtree;white-space:nowrap;font-variant-numeric:tabular-nums;color:var(--yazi)}",
      ".sl .cubuk .deg.ic{color:var(--vurgu-ust)}",
      ".sl .cubuk .sat.sic .deg.ic{color:var(--simdi-ust)}",
      ".sl .cizim{flex:1;border-radius:var(--kose);overflow:hidden;background:var(--yuzey2)}",
      ".sl .cizim svg{width:100%;height:100%;display:block}",
      /* soru */
      ".sl .soru{flex:1;min-width:0;display:flex;flex-direction:column}",
      ".sl .qq{font:600 66px/1.2 Literata,serif;margin:0;text-wrap:balance;letter-spacing:-.012em}",
      ".sl .sec{margin-top:44px;display:flex;flex-direction:column;gap:20px}",
      ".sl .secenek{display:flex;align-items:center;gap:26px;font-size:44px;line-height:1.22}",
      ".sl .secenek b{flex:0 0 66px;height:66px;border-radius:50%;background:var(--secenek-zemin);color:var(--secenek-yazi);display:grid;place-items:center;font:800 .7em/1 Figtree}",
      ".sl .aciklama{margin-top:40px;font-size:32px;color:var(--yazi2);max-width:1400px}",
      ".sl .telefon{margin-top:auto;padding-top:28px;display:flex;align-items:center;gap:14px;font-size:26px;font-weight:600;color:var(--yazi2)}",
      ".sl .telefon i{width:16px;height:16px;border-radius:50%;background:var(--simdi)}",
      ".sl .esle{margin-top:40px;display:flex;gap:56px}",
      ".sl .esle div{flex:1;display:flex;flex-direction:column;gap:14px}",
      ".sl .esle span{border-radius:14px;background:var(--yuzey2);padding:20px 26px;font-size:30px;font-weight:600}",
      /* kutular (plan) */
      ".sl .kutular{flex:1;display:flex;flex-direction:column;gap:20px;min-width:0}",
      ".sl .kutular .ust3{flex:1;display:flex;gap:20px;min-height:0}",
      ".sl .kt{flex:1 1 0;border-radius:var(--kose);padding:26px 30px;background:var(--vurgu-acik);display:flex;flex-direction:column;gap:14px;min-width:0}",
      ".sl .kt.gizli{visibility:hidden}",
      ".sl .kt.koyu{background:var(--vurgu);color:var(--vurgu-ust)}",
      ".sl .kt.pembe{background:var(--simdi-acik)}",
      ".sl .kt.vurgu{background:var(--simdi-acik);flex:none}",
      ".sl .kt h3{margin:0;font:600 1.2em/1.2 Literata,serif}",
      ".sl .kt ul,.sl .kt ol{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:.36em;font-size:1em;line-height:1.25}",
      ".sl .kt ol{gap:.6em;flex:1;justify-content:space-evenly}",
      ".sl .kt li{padding-left:24px;position:relative}",
      ".sl .kt li::before{content:'';position:absolute;left:2px;top:.5em;width:9px;height:9px;border-radius:50%;background:currentColor;opacity:.55}",
      ".sl .kt ol li{padding-left:1.6em}",
      ".sl .kt ol li::before{content:attr(data-n);left:0;top:0;width:auto;height:auto;border-radius:0;background:none;opacity:1;font:600 1em/1.25 Literata,serif;color:var(--simdi)}",
      ".sl .kt.koyu ol li::before{color:var(--p-eosin-300)}",
      ".sl .kt p{margin:0;font-size:1em;line-height:1.3}",
      ".sl .kt table{border-collapse:collapse;font-size:.86em;line-height:1.25}",
      ".sl .kt td{padding:9px 0;border-top:1px solid color-mix(in oklab,currentColor 18%,transparent);vertical-align:top}",
      ".sl .kt tr:first-child td{border-top:0}",
      ".sl .kt td:first-child{font-weight:700;width:180px;padding-right:18px}",
      /* özet (sentez) */
      ".sl .ozet{flex:1;margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;grid-auto-flow:column;grid-template-rows:repeat(var(--satir,4),1fr);column-gap:72px;row-gap:12px}",
      ".sl .ozet li{display:grid;grid-template-columns:1.3em 1fr;column-gap:.5em;align-content:center;font-size:.8em;line-height:1.28}",
      ".sl .ozet li::before{content:attr(data-n);grid-row:span 2;font:600 1.5em/1 Literata,serif;color:var(--simdi)}",
      ".sl .ozet li b{font:600 1.08em/1.2 Literata,serif}",
      ".sl .ozet li span{color:var(--yazi2)}",
      /* tablo */
      ".sl .tablo{border-collapse:collapse;width:100%;max-width:1500px;font-size:30px;line-height:1.3}",
      ".sl .tablo th{text-align:left;font:600 var(--altyazi-boy)/1.2 Figtree;color:var(--yazi2);padding:0 24px 14px 0}",
      ".sl .tablo td{padding:18px 24px 18px 0;border-top:1px solid var(--cizgi);vertical-align:top}",
      ".sl .tablo td:first-child{font-weight:650;width:44%}",
      /* kaynaklar */
      ".sl .kayn{flex:1;display:flex;flex-direction:column;gap:22px}",
      ".sl .kayn ol{margin:0;padding:0 0 0 1.4em;font-size:26px;line-height:1.35;display:flex;flex-direction:column;gap:10px}",
      ".sl .kayn ol li::marker{color:var(--yazi2);font-variant-numeric:tabular-nums}",
      ".sl .quizk{display:flex;gap:34px;align-items:center;border-radius:var(--kose);background:var(--vurgu-acik);padding:24px 30px}",
      ".sl .quizk img{width:180px;height:180px;border-radius:8px;background:var(--karekod-zemin);padding:8px}",
      ".sl .quizk div{font-size:28px;line-height:1.4}",
      ".sl .quizk b{font-size:30px}",
      ".sl .quizk span{display:block;font-weight:700;color:var(--simdi);font-size:32px}",
      ".sl .cagri{border-radius:var(--kose);background:var(--simdi);color:var(--simdi-ust);padding:22px 30px;font:600 32px/1.3 Literata,serif}",
      /* kapak */
      ".sl.kapak{background:var(--kapak-zemin);color:var(--kapak-yazi)}",
      ".sl .kp-sol{position:absolute;left:0;top:0;bottom:0;width:1240px;padding:96px 110px 64px 112px;display:flex;flex-direction:column}",
      ".sl .kp-sag{position:absolute;left:1240px;right:0;top:0;bottom:0}",
      ".sl .kp-sag img{width:100%;height:100%;object-fit:cover;display:block}",
      ".sl .kp-isaret{display:flex;align-items:center;gap:18px;font:600 26px/1.2 Figtree;color:var(--kapak-yazi2)}",
      ".sl .kp-isaret svg{width:64px;height:64px}",
      ".sl .kp-bas{margin-top:auto;font:600 92px/1.06 Literata,serif;letter-spacing:-.02em;text-wrap:balance}",
      ".sl .kp-alt{margin-top:28px;font-size:36px;line-height:1.3;color:var(--kapak-yazi2);text-wrap:balance}",
      ".sl .kp-tarih{margin-top:36px;font-size:28px;font-variant-numeric:tabular-nums}",
      ".sl .kp-vaka{margin-top:48px;border-radius:18px;background:var(--kapak-vaka);padding:24px 30px;font:600 36px/1.25 Literata,serif;text-wrap:balance}",
      ".sl .kp-kay{margin-top:26px;font-size:16px;font-style:italic;color:var(--kapak-yazi2)}"
    ].join("\n");
  }

  /* Logo (marka varlığı; renkleri sabittir) */
  var ISARET = "<svg viewBox='0 0 40 40' aria-hidden='true'><rect x='2' y='9' width='36' height='22' rx='4' fill='#EEE7F8' stroke='#BBA3F0' stroke-width='1.5'/>" +
    "<rect x='4.5' y='11.5' width='8' height='17' rx='2' fill='#4A2C82' opacity='.16'/><path d='M16 21.5c0-5 4-8 9-7.6 5 .4 9 3 8.6 7-.4 4.4-4.6 6.3-9 6.1-5-.2-8.6-1.5-8.6-5.5z' fill='#F283AA'/>" +
    "<circle cx='21' cy='19' r='1.7' fill='#4A2C82'/><circle cx='26.5' cy='17.4' r='1.5' fill='#4A2C82'/><circle cx='29.5' cy='22.2' r='1.7' fill='#4A2C82'/><circle cx='23.4' cy='24' r='1.4' fill='#4A2C82'/></svg>";

  function keloid(asama) {
    var st = function (v) { return " style='fill:var(" + v + ")'"; };
    var p = ["<svg viewBox='0 0 1000 780' preserveAspectRatio='xMidYMid meet'>"];
    p.push("<text x='500' y='110' text-anchor='middle' font-family='Figtree' font-size='30'" + st("--yazi2") + ">Kesikli çizgi: yaranın sınırı</text>");
    [[250, "Hipertrofik skar"], [750, "Keloid"]].forEach(function (a) {
      var x = a[0];
      p.push("<rect x='" + (x - 210) + "' y='320' width='420' height='300' rx='16'" + st("--cizim-deri") + "/>");
      p.push("<line x1='" + (x - 90) + "' y1='320' x2='" + (x + 90) + "' y2='320' style='stroke:var(--yazi)' stroke-width='4' stroke-dasharray='10 8'/>");
      p.push("<text x='" + x + "' y='690' text-anchor='middle' font-family='Literata' font-weight='600' font-size='38'" + st("--yazi") + ">" + a[1] + "</text>");
    });
    if (asama >= 1) p.push("<path d='M160 320 Q250 220 340 320 Z'" + st("--cizim-skar") + "/>");
    if (asama >= 2) {
      p.push("<path d='M540 320 Q600 140 750 160 Q900 140 960 320 Z'" + st("--cizim-skar") + "/>");
      p.push("<text x='750' y='255' text-anchor='middle' font-family='Figtree' font-weight='700' font-size='30'" + st("--p-beyaz") + ">sınırı aşar</text>");
    }
    p.push("</svg>");
    return p.join("");
  }

  function yol(o, src) { return o.coz ? o.coz(src) : (o.kok || "") + src; }
  function foto(p, o) {
    var src = yol(o, p.foto);
    var pos = p.konum ? "object-position:" + esc(p.konum) : "";
    var cap = p.yazi ? "<figcaption>" + md(p.yazi) + (p.alt ? "<small>" + md(p.alt) + "</small>" : "") + "</figcaption>" : "";
    return "<figure class='" + (p.sigdir ? "sig" : "") + "'><div class='cer'><img src='" + esc(src) + "' alt='' style='" + pos + "'>" +
      (p.etiket ? "<div class='lab'>" + esc(p.etiket) + "</div>" : "") + "</div>" + cap + "</figure>";
  }

  function panelHTML(ps, o) {
    var medya = [], yazi = [];
    (ps || []).forEach(function (p) {
      if (p.foto) medya.push(foto(p, o));
      else if (p.soruIsareti != null) medya.push("<div class='soru-isareti'><div>?</div><span>" + md(p.soruIsareti) + "</span></div>");
      else if (p.rakam != null) medya.push("<div class='rakam'><div>" + esc(p.rakam) + "</div><span>" + md(p.aciklama || "") + "</span></div>");
      else if (p.cubuklar) {
        var kadar = p.kadar == null ? 99 : p.kadar;
        medya.push("<div class='cubuk'>" + (p.baslik ? "<h3>" + md(p.baslik) + "</h3>" : "") + p.cubuklar.map(function (c, i) {
          var dis = c.ust < 70;
          return "<div class='sat" + (c.vurgu ? " sic" : "") + (i > kadar ? " gizli" : "") + "'><div class='ad'>" + esc(c.ad) + (c.not ? " <small>· " + md(c.not) + "</small>" : "") + "</div>" +
            "<div class='iz'><div class='dol' style='left:" + c.alt + "%;width:" + (c.ust - c.alt) + "%'></div>" +
            "<div class='deg" + (dis ? "" : " ic") + "' style='left:calc(" + (dis ? c.ust : c.alt) + "% + 16px)'>%" + c.alt + "–" + c.ust + "</div></div></div>";
        }).join("") + "</div>");
      }
      else if (p.cizim === "keloid") medya.push("<div class='cizim'>" + keloid(p.asama || 0) + "</div>");
      else if (p.kutu != null) yazi.push("<div class='kutu " + esc(p.ton || "mor") + "'>" + md(p.kutu) + "</div>");
      else if (p.not) yazi.push("<div class='pnot'><h3>Patoloğun notu: " + md(p.not.baslik) + "</h3><p>" + md(p.not.metin) + "</p></div>");
    });
    return (medya.length ? "<div class='medya'>" + medya.join("") + "</div>" : "") + yazi.join("");
  }

  function altSerit(ders, s, no) {
    var orta = "";
    if (s.ilerleme) {
      var k = s.ilerleme[0], n = s.ilerleme[1], d = "";
      for (var i = 1; i <= n; i++) d += "<i class='" + (i < k ? "on" : i === k ? "su" : "") + "'></i>";
      orta = "<div class='ilerleme'>Ana maddeler " + d + "</div>";
    } else if (s.serit && ders.serit && ders.serit.gruplar) {
      orta = "<div class='serit'>" + ders.serit.gruplar.map(function (g, i) {
        return "<span class='" + (s.serit.indexOf(i + 1) >= 0 ? "on" : "") + "'>" + esc(g) + "</span>";
      }).join("") + "</div>";
    }
    return "<div class='alt'><span class='ders'>" + esc(ders.kisa || ders.baslik) + "</span><span>4. Sınıf Patoloji</span>" +
      (s.opsiyonel ? "<span class='ops'>Zaman kalırsa</span>" : "") + orta +
      "<span class='bosluk'></span>" + (s.kaynak ? "<span class='kay'>Görseller: " + md(s.kaynak) + "</span>" : "") +
      (s.numarasiz ? "" : "<span class='no'>" + no + "</span>") + "</div>";
  }

  function telefon(yazi) { return "<p class='telefon'><i></i>" + yazi + "</p>"; }

  function soruGovde(ders, s, o) {
    var q = (ders.sorular || []).filter(function (x) { return x.id === s.soru; })[0];
    if (!q) return "<div class='soru'><div class='qq'>Soru bulunamadı: " + esc(s.soru) + "</div></div>";
    var h = "<div class='qq'>" + md(q.q) + "</div>";
    if (q.type === "MATCH" && q.left) {
      h += "<div class='esle'><div>" + q.left.map(function (x) { return "<span>" + md(x) + "</span>"; }).join("") + "</div><div>" +
        (q.right || []).map(function (x) { return "<span>" + md(x) + "</span>"; }).join("") + "</div></div>";
    } else if (q.opts && q.opts.length && !(q.type === "IMGMCQ" && s.gorsel && q.opts.join("") === "ABCD".slice(0, q.opts.length))) {
      h += "<div class='sec'>" + q.opts.map(function (x, i) { return "<div class='secenek'><b>" + "ABCDE"[i] + "</b><span>" + md(x) + "</span></div>"; }).join("") + "</div>";
    }
    if (s.aciklama) h += "<div class='aciklama'>" + md(s.aciklama) + "</div>";
    h += telefon(s.devam ? "Oylama açık; telefondan cevabını değiştirebilirsin" : "Telefondan cevapla · " + esc(TUR_KISA[q.type] || q.type));
    var sol = "<div class='soru' data-kutu data-sigdir='" + (s.yazi || (s.gorsel && s.gorsel.length ? 58 : 68)) + "'>" + h + "</div>";
    if (s.gorsel && s.gorsel.length) {
      var cok = s.gorsel.length > 2 && s.gorsel.every(function (p) { return p.foto; });
      var g = cok ? "<div class='gs dar' style='gap:16px'><div class='medya'>" + s.gorsel.slice(0, 2).map(function (p) { return foto(p, o); }).join("") +
        "</div><div class='medya'>" + s.gorsel.slice(2).map(function (p) { return foto(p, o); }).join("") + "</div></div>"
        : "<div class='gs dar'>" + panelHTML(s.gorsel, o) + "</div>";
      return sol + g;
    }
    return sol;
  }

  /* Bir karenin bütün HTML'i (yalnız .sl öğesi; CSS ayrı). o: {kok | coz: görsel yolu} */
  function kareHTML(ders, f, o) {
    o = o || {};
    var s = f.s, tema = s.tema === "koyu" ? "koyu" : "acik";
    if (s.tip === "kapak") {
      return "<div class='sl kapak koyu'><div class='kp-sol'><div class='kp-isaret'>" + ISARET + "<span>Lam Başında · " + esc(s.ust || "4. Sınıf Patoloji") + "</span></div>" +
        "<div class='kp-bas' data-sigdir='92'>" + md(s.baslik) + "</div>" + (s.alt ? "<div class='kp-alt'>" + md(s.alt) + "</div>" : "") +
        (s.tarih ? "<div class='kp-tarih'>" + esc(s.tarih) + "</div>" : "") + (s.vaka ? "<div class='kp-vaka'>" + md(s.vaka) + "</div>" : "") +
        (s.kaynak ? "<div class='kp-kay'>Görsel: " + md(s.kaynak) + "</div>" : "") + "</div>" +
        "<div class='kp-sag'>" + (s.gorsel && s.gorsel.foto ? "<img src='" + esc(yol(o, s.gorsel.foto)) + "' alt=''" +
          (s.gorsel.konum ? " style='object-position:" + esc(s.gorsel.konum) + "'" : "") + ">" : "") + "</div></div>";
    }
    if (s.tip === "resim") {
      return "<div class='sl acik'><img src='" + esc(yol(o, s.src)) + "' style='width:100%;height:100%;object-fit:contain' alt=''></div>";
    }
    var govde = "";
    if (s.tip === "adim") {
      var ms = s.maddeler || [], gor = null, hepsi = ms.some(function (m) { return m.gorsel && m.gorsel.length; });
      for (var i = 0; i <= f.k && i < ms.length; i++) if (ms[i].gorsel && ms[i].gorsel.length) gor = ms[i].gorsel;
      govde = (hepsi ? "<div class='gs" + (s.soruAc ? " dar" : "") + "'>" + (gor ? panelHTML(gor, o) : "") + "</div>" : "") +
        "<div class='liste' data-kutu data-sigdir='" + (s.yazi || 36) + "'>" + ms.map(function (m, i) {
          return "<div class='md " + (i < f.k ? "once" : i === f.k ? "su" : "sonra") + "'>" + (m.ust ? "<span class='ust'>" + md(m.ust) + ":</span> " : "") + md(m.metin) + "</div>";
        }).join("") + "</div>";
    } else if (s.tip === "soru") {
      govde = soruGovde(ders, s, o);
    } else if (s.tip === "kutular") {
      var ks = s.kutular || [], ust = ks.filter(function (k) { return k.ton !== "vurgu"; }), alt = ks.filter(function (k) { return k.ton === "vurgu"; });
      var kt = function (k) {
        var idx = ks.indexOf(k);
        var ic = k.tablo ? "<table>" + k.tablo.map(function (rw) { return "<tr>" + rw.map(function (c) { return "<td>" + md(c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</table>"
          : k.numara ? "<ol>" + (k.maddeler || []).map(function (m, mi) { return "<li data-n='" + (k.numara + mi) + "'>" + md(m) + "</li>"; }).join("") + "</ol>"
          : (k.maddeler || []).length > 1 || k.baslik ? "<ul>" + (k.maddeler || []).map(function (m) { return "<li>" + md(m) + "</li>"; }).join("") + "</ul>"
            : "<p>" + md((k.maddeler || [])[0] || "") + "</p>";
        return "<div class='kt " + esc(k.ton || "mor") + (idx > f.k ? " gizli" : "") + "'" + (k.genislik ? " style='flex:0 0 " + (+k.genislik) + "px'" : "") + ">" +
          (k.baslik ? "<h3>" + md(k.baslik) + "</h3>" : "") + ic + "</div>";
      };
      govde = "<div class='kutular' data-kutu data-sigdir='" + (s.yazi || 28) + "'><div class='ust3'>" + ust.map(kt).join("") + "</div>" + alt.map(kt).join("") + "</div>";
    } else if (s.tip === "ozet") {
      var oz = s.maddeler || [];
      govde = "<ol class='ozet' data-kutu data-sigdir='" + (s.yazi || 40) + "' style='--satir:" + Math.ceil(oz.length / 2) + "'>" + oz.map(function (m, i) {
        return "<li data-n='" + (i + 1) + "'><b>" + md(m.ust || "") + "</b><span>" + md(m.metin || "") + "</span></li>";
      }).join("") + "</ol>";
    } else if (s.tip === "tablo") {
      var th = (s.tabloBaslik || "").split("→").map(function (x) { return x.trim(); });
      govde = "<div style='flex:1' data-kutu data-sigdir='30'><table class='tablo'>" + (th.length === 2 ? "<tr><th>" + esc(th[0][0].toUpperCase() + th[0].slice(1)) + "</th><th>" + esc(th[1][0].toUpperCase() + th[1].slice(1)) + "</th></tr>" : "") +
        (s.satirlar || []).map(function (rw) { return "<tr>" + rw.map(function (c) { return "<td>" + md(c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</table></div>";
    } else if (s.tip === "kaynaklar") {
      govde = "<div class='kayn' data-kutu data-sigdir='26'><ol>" + (s.maddeler || []).map(function (m) { return "<li>" + md(m) + "</li>"; }).join("") + "</ol>" +
        (s.quizAdres ? "<div class='quizk'><img src='" + esc(yol(o, s.karekod || "img/quiz_qr.png")) + "' alt=''><div><b>Evde tekrar: slaytlar ve quiz (isteyen çözsün)</b><br>" + md(s.quizMetni || "") +
          "<span>" + esc(s.quizAdres) + "</span></div></div>" : "") + (s.cagri ? "<div class='cagri'>" + md(s.cagri) + "</div>" : "") + "</div>";
    } else if (s.tip === "liderlik" || s.tip === "bulut") {
      govde = "<div class='soru'><div class='qq'>" + (s.tip === "liderlik" ? "Liderlik tablosu" : "Kelime bulutu") + "</div>" +
        "<div class='aciklama'>Bu slaytın görüntüsü yok; perde bu sırada canlı veriyi gösterir.</div></div>";
    }
    return "<div class='sl " + tema + (s.alan ? " alan" : "") + "'><h1 data-sigdir='60'>" + md(s.baslik) + "</h1>" + (s.dus ? "<div class='dus'>DUS</div>" : "") +
      "<div class='govde'>" + govde + "</div>" + altSerit(ders, s, f.no) + "</div>";
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
          el.querySelectorAll(".secenek,.esle span").forEach(function (x) { x.style.fontSize = Math.round(fs * 0.73) + "px"; });
          el.querySelectorAll(".secenek b").forEach(function (x) { var d = Math.round(fs * 1.1); x.style.flexBasis = d + "px"; x.style.height = d + "px"; });
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
    ozet: function () { return { tip: "ozet", baslik: "Özet", maddeler: [{ ust: "Konu", metin: "Akılda kalacak cümle" }], sure: 40, not: "" }; },
    liderlik: function () { return { tip: "liderlik", baslik: "Liderlik tablosu", sure: 20, not: "" }; },
    bulut: function () { return { tip: "bulut", baslik: "Geçen dersin çıkış bileti", bulut: { q: "", from: "prev" }, sure: 20, not: "" }; }
  };

  var Slayt = { md: md, esc: esc, ts: ts, kareler: kareler, kareSure: kareSure, kareNot: kareNot, dosyaAdi: dosyaAdi, gorselVar: gorselVar,
    canli: canli, css: css, html: kareHTML, sigdir: sigdir, SABLON: SABLON, TUR_TR: TUR_TR, T_TUR: T_TUR, adimSayisi: adimSayisi };
  if (typeof module !== "undefined" && module.exports) module.exports = Slayt;
  else root.Slayt = Slayt;
})(typeof window !== "undefined" ? window : globalThis);
