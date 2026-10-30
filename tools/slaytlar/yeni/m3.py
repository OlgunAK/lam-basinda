# -*- coding: utf-8 -*-
"""M3 · Yumuşak Doku Hastalıkları (17 Kasım 2026, blok dersin birincisi, 25 dk).

Sıra fakültenin resmi ders slaytını izler (10. hafta, Yumuşak Doku Hastalıkları
Patolojisi): neoplastik olmayan kitleler, iyi huylu tümörler, sarkomlar.
Rakamlar Neville 5'ten; Neville'de olmayan konular (juvenil hiyalen
fibromatozis, fibromatozis colli, keloid, tendon kılıfı dev hücreli tümörü)
resmi slayttan, nodüler fasiitis WHO 2022'den.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import *
from foto import F

NEV = "Neville ve ark., *Oral and Maxillofacial Pathology*, 5. baskı (Elsevier, 2024)"
LAS = "Laskaris, *Color Atlas of Oral Diseases*, 4. baskı (Thieme, 2017)"
BOTH = NEV + " · " + LAS
n = lambda k, **kw: F("n", k, **kw)
l = lambda k, **kw: F("l", k, **kw)
GREY = "font-size:21px;color:%s" % C["grey"]

L = Lesson("M3", "Yumuşak Doku Hastalıkları", "Yumuşak Doku Hastalıkları", "17 Kasım 2026", ver="4",
           frame="Üç grup: neoplastik olmayan kitleler, iyi huylu tümörler, sarkomlar",
           quiz="../quiz/#yd",
           strip=("Üç grup", ["1 Neoplastik olmayan", "2 İyi huylu", "3 Sarkom"]),
           cta="24 Kasım'a kadar isteyen Neville'in örnek sorularını Türkçe quiz olarak çözsün: olgunak.github.io/lam-basinda/quiz. İlk üçü gelecek derste burada anarım.")

IMG = os.path.join(CANLI, "img")


def save(src, name):
    from PIL import Image
    Image.open(src).convert("RGB").save(os.path.join(IMG, name), quality=88)
    return "img/" + name


def table(rows, size=24, head=None, w1=330):
    h = "<tr>%s</tr>" % "".join("<th>%s</th>" % md(x) for x in head) if head else ""
    b = "".join("<tr><td style='width:%dpx'>%s</td>%s</tr>" % (w1, md(r[0]), "".join("<td>%s</td>" % md(x) for x in r[1:])) for r in rows)
    return "<table class='t2' style='font-size:%dpx'>%s%s</table>" % (size, h, b)


# ---------------- questions ----------------
VAKA_OPTS = ["Granüler hücreli tümör", "Skuamöz hücreli karsinom", "Schwannom", "Lipom", "Travmatik nöroma"]
W1 = L.q(id="W1", type="POLL", label="Açılış vakası: tahminin ne?", q="Bu hastada ön tanın ne?", scored=False,
         img=save(n("12.84"), "m3_vaka.jpg"), opts=VAKA_OPTS, hide=True)
grid_img([n("12.65"), n("12.61"), n("12.118"), n("12.33")], os.path.join(IMG, "m3_mikroskop.jpg"))
W2 = L.q(id="W2", type="IMGMCQ", label="Dört mikroskop görüntüsü", q="Dört mikroskop görüntüsü. Hangisi schwannom?",
         scored=True, img="img/m3_mikroskop.jpg", opts=["A", "B", "C", "D"], a=1,
         exp="B: Antoni A alanı; iğsi hücrelerin çekirdekleri sıra sıra dizilir (palizat), aralarındaki pembe alanlar Verocay cisimcikleri. "
             "A nörofibrom (dalgalı çekirdekli, düzensiz iğsi hücreler), C leiomiyom (küt uçlu çekirdekli düz kas demetleri), D oral fokal müsinozis (gevşek, miksoid bağ dokusu).")
W3 = L.q(id="W3", type="MCQ", label="DUS Molası 1/2", scored=True,
         q="Aşağıdaki tümörlerden hangisi belirgin bir kadın baskınlığı gösterir?",
         opts=["Konjenital epulis", "Granüler hücreli tümör", "İnverted papillom", "Lenfatik malformasyon", "Schwannom"], a=0,
         exp="Konjenital epulisin yaklaşık %90'ı kız bebeklerde görülür (WHO: K:E 7,7:1). Granüler hücreli tümör de kadında sıktır (3:1), ama bu kadar belirgin değil.")
W4 = L.q(id="W4", type="MCQ", label="DUS Molası 2/2", scored=True,
         q="Lisch nodülleri hangisiyle ilişkilidir?",
         opts=["Embriyonal rabdomiyosarkom", "Granüler hücreli tümör", "Kaposi sarkomu", "Nörofibromatozis tip 1", "Sturge-Weber sendromu"], a=3,
         exp="Lisch nodülleri irisin pigmentli hamartomlarıdır; NF1 hastalarının neredeyse hepsinde bulunur.")
W5 = L.q(id="W5", type="MCQ", label="Patolog gibi düşün", scored=True,
         q="29 yaşında erkek. Yanakta üç haftada 2 cm'ye ulaşan, ağrılı kitle. Biyopsi raporu: atipisi olmayan iğsi hücreler, mitoz bol ama atipik mitoz yok, gevşek miksoid zemin, ekstravaze eritrositler. En olası tanı ve yaklaşım?",
         opts=["Fibrosarkom; geniş sınırla rezeksiyon", "Nodüler fasiitis; yerel eksizyon yeterli", "Embriyonal rabdomiyosarkom; kemoterapi",
               "Kaposi sarkomu; HIV testi", "Leiomiyosarkom; radyoterapi"], a=1,
         exp="Hızlı büyüme ve bol mitoz sarkomu düşündürür, ama atipik mitoz ve pleomorfizm yok; gevşek zemin ve ekstravaze eritrositler nodüler fasiitisin tipik bulguları. "
             "Yerel eksizyon yeterli, nüks nadir. Bu tabloyu sarkom sanıp hastaya geniş rezeksiyon yapmak en büyük hata olur.")
W6 = L.q(id="W6", type="POLL", label="Vakaya dönüş: şimdi ne diyorsun?", q="Dersin başındaki hasta: şimdi ön tanın ne?", scored=False,
         img=save(n("12.87"), "m3_vaka_donus.jpg"), opts=VAKA_OPTS, a=0, compare="W1")
W7 = L.q(id="W7", type="WORDCLOUD", label="Çıkış bileti", q="Bugün en çok kafanı karıştıran konu hangisiydi? (Tek kelime ya da kısa ifade)", scored=False)
Q = L.qmap

R = os.path.join(HERE, "resmi")
r = lambda f: os.path.join(R, f)
RESMI = "Fakültenin resmi ders slaytı (Z. Kahyaoğlu Akkaya)"


def seq_list(items, k, size=34, dark=False):
    out = []
    for i, it in enumerate(items):
        if i > k:
            vis = "visibility:hidden;"
        else:
            vis = ""
        now = i == k
        bg = (C["navy2"] if dark else C["lilac"]) if now else "transparent"
        bar = C["pink"] if now else ("#4a3d63" if dark else C["line"] if "line" in C else "#e3dbee")
        col_ = ("#fff" if dark else C["navy"]) if now else ("#bdb3cc" if dark else "#6e6282")
        h = ("<div style='font:700 %dpx Lora;color:%s;margin:0 0 4px'>%s</div>" % (size - 4, C["pink"], md(it["h"]))) if it.get("h") else ""
        out.append("<div style='%sbackground:%s;border-left:7px solid %s;border-radius:10px;padding:12px 20px;color:%s;"
                   "font-size:%dpx;line-height:1.28;font-weight:%s'>%s%s</div>" % (vis, bg, bar, col_, size, 700 if now else 400, h, md(it["t"])))
    return "".join(out)


def seq_add(title, items, size=34, vis_w=1040, theme="light", gap=14, **kw):
    """Maddeler sırayla açılır; soldaki görsel o maddenin görseli (yoksa bir öncekinin)."""
    def body(k):
        v = None
        for it in items[:k + 1]:
            if it.get("v"):
                v = it["v"]
        lst = div(seq_list(items, k, size, theme == "dark"), "flex:1;display:flex;flex-direction:column;gap:%dpx;justify-content:flex-start" % gap)
        return row(div(v or "", "flex:0 0 %dpx;display:flex" % vis_w), lst, gap=40, style="flex:1")
    L.add(title=title, seq=[{"note": it["note"], "dur": it["dur"]} for it in items], body_fn=body, theme=theme, **kw)


def P(src, cap=None, sub=None, **kw):
    return ph(src, cap, sub, style="flex:1", **kw)


def P2(a, b):
    return row(a, b, gap=16, style="flex:1")


def keloid_svg(k):
    """Basit çizim: yara çizgisi, hipertrofik skar sınır içinde, keloid sınırı aşar."""
    skin = "#f3d2c1"; scar = "#c9879a"; line = C["navy"]
    parts = ["<svg viewBox='0 0 1000 820' style='width:100%;height:100%' xmlns='http://www.w3.org/2000/svg'>",
             "<rect width='1000' height='820' rx='16' fill='#fbf3ee'/>"]
    for i, (x, lab) in enumerate([(250, "Hipertrofik skar"), (750, "Keloid")]):
        parts.append("<rect x='%d' y='330' width='420' height='300' rx='14' fill='%s'/>" % (x - 210, skin))
        parts.append("<line x1='%d' y1='330' x2='%d' y2='330' stroke='%s' stroke-width='4' stroke-dasharray='10 8'/>" % (x - 90, x + 90, line))
        parts.append("<text x='%d' y='700' text-anchor='middle' font-family='Lora' font-weight='700' font-size='40' fill='%s'>%s</text>" % (x, line, lab))
    parts.append("<text x='500' y='120' text-anchor='middle' font-family='Lato' font-size='32' fill='%s'>Kesikli çizgi: yaranın sınırı</text>" % C["grey"])
    if k >= 1:
        parts.append("<path d='M160 330 Q250 230 340 330 Z' fill='%s'/>" % scar)
    if k >= 2:
        parts.append("<path d='M540 330 Q600 150 750 170 Q900 150 960 330 Z' fill='%s'/>" % scar)
        parts.append("<text x='750' y='265' text-anchor='middle' font-family='Lato' font-weight='700' font-size='30' fill='#fff'>sınırı aşar</text>")
    parts.append("</svg>")
    return "".join(parts)


# ---------------- slides ----------------
L.add(title="Yumuşak Doku Hastalıkları", dur=60, lobby=True, nonum=True, raw=title_page(
    "4. Sınıf Patoloji  ·  Diş Hekimliği", "Yumuşak Doku Hastalıkları",
    "Neoplastik olmayan kitleler, iyi huylu tümörler ve sarkomlar",
    "17 Kasım 2026  ·  Uzm. Dr. M. Olgun Ak", "42 yaşında kadın, dil sırtında bir yıldır büyüyen ağrısız nodül.",
    n("12.61"), NEV),
    notes="Günaydın. Bugün iki ders arka arkaya: önce ağzın yumuşak doku hastalıkları, sonra tükürük bezleri. Sağdaki görüntü bir schwannom; dersin ortasında mikroskopta tanıyacaksınız. Karekod perdede: okutun; hesap yok, uygulama yok. Takma ad isterseniz yazın; dersin sonunda liderlik tablosu var. Herkes girince → ile vakaya geçiyoruz. (L: katılım ekranını gizle/göster.)")

VAKA_V = col(row(ph(n("12.84"), "Dil sırtı", style="flex:1"), qmark(), style="flex:1"),
             box("yellow", None, html_="<div class='big' style='font-size:38px'>Tahminini telefondan gir. Cevap dersin sonunda.</div>", style="padding:36px 32px"),
             style="flex:1")
seq_add("Açılış vakası: dil sırtında nodül", [
    dict(t="42 yaşında kadın", v=VAKA_V, dur=10, note="Hastamız 42 yaşında bir kadın."),
    dict(t="Dil sırtında 1 cm, sert, sarımsı nodül", dur=12, note="Dil sırtında bir santimetrelik, sert, sarımsı bir nodül var."),
    dict(t="Bir yıldır yavaş büyüyor; ağrısız", dur=12, note="Bir yıldır yavaş yavaş büyüyor ve ağrımıyor."),
    dict(t="Üstündeki mukoza sağlam; travma öyküsü yok", dur=12, note="Üstündeki mukoza sağlam; ısırma ya da travma öyküsü yok."),
    dict(t="Sigara ve alkol kullanmıyor", dur=11, note="Sigara ve alkol kullanmıyor. Fotoğrafa bakın ve tahmininizi telefondan girin; şıklar açık. Cevabı dersin sonunda açacağım."),
], size=38, vis_w=900, theme="dark", qopen=W1, cred=NEV)

L.add(title="Açılış vakası: tahminin ne?", dur=35, theme="dark", q=W1, cont=True, cred=NEV,
      body=qbody(Q[W1], photo=ph(n("12.84"))),
      notes="Sonuçları gösteriyorum ama yorum yapmıyorum. Şıklardan biri kötü huylu, dördü iyi huylu ya da reaktif. Dersin sonunda biyopsi sonucuyla birlikte aynı soruyu yeniden soracağım.")

PLAN = [
    box("navy", "1 · Neoplastik olmayan kitleler", ["Hamartom ve koristom", "Juvenil hiyalen fibromatozis", "Fibromatozis colli (tortikollis)",
                                                    "Keloid ve hipertrofik skar", "Nodüler fasiitis", "Oral fokal müsinozis", "Travmatik nöroma"], size=30, gap=12, style="flex:1"),
    box("lilac", "2 · İyi huylu tümörler", None, html_=table([
        ["Lif, histiyosit", "fibröz histiyositom, fibromatozis, miyofibrom, soliter fibröz tümör"],
        ["Yağ", "lipom"],
        ["Sinir", "palizatlı kapsüllü nöroma, schwannom, nörofibrom, paragangliom, granüler hücreli tümör, konjenital epulis"],
        ["Damar", "hemanjiyom, lenfanjiyom, nazofarengeal anjiyofibrom"],
        ["Kas", "leiomiyom, rabdomiyom"]], size=26, w1=170), style="flex:1;padding:22px 24px"),
    box("rose", "3 · Sarkomlar", ["Pleomorfik sarkom, fibrosarkom, liposarkom", "Malign periferik sinir kılıfı tümörü, olfaktör nöroblastom",
                                  "Anjiyosarkom, Kaposi sarkomu", "Leiomiyosarkom, rabdomiyosarkom", "Sinovyal sarkom, alveoler yumuşak doku sarkomu"],
        size=29, gap=16, style="flex:1"),
    box("yellow", None, ["Her hastalıkta aynı dört soru: **hangi dokudan** köken alıyor, **kaç yaşında**, **ağızda nerede**, **mikroskopta ne görülür**."],
        size=28, style="padding:20px 30px")]


def plan_body(k):
    fx = ["flex:1", "flex:0 0 760px", "flex:1", ""]
    hid = lambda i: div(PLAN[i], "display:flex;flex-direction:column;%s;%s" % (fx[i], "" if i <= k else "visibility:hidden"))
    return col(row(*[hid(i) for i in range(3)], style="flex:1"), hid(3))


L.add(title="Dersin planı: üç grup", body_fn=plan_body, seq=[
    dict(dur=12, note="Ders fakültemizin resmi slaytıyla aynı sırada: üç grup. Birincisi neoplastik olmayan kitleler; tümör gibi görünürler ama gerçek tümör değildirler."),
    dict(dur=12, note="İkincisi iyi huylu tümörler; köken aldıkları dokuya göre sıraladım: lif, yağ, sinir, damar, kas."),
    dict(dur=10, note="Üçüncüsü sarkomlar, yani yumuşak dokunun kötü huylu tümörleri."),
    dict(dur=11, note="Her hastalıkta aynı dört soruyu soracağız: hangi doku, kaç yaş, ağızda nerede, mikroskopta ne var. Rakamlar Neville 5. baskıdan; resmi slaytla ayrıldığı yerleri ayrıca söyleyeceğim.")])

# ---- 1. Neoplastik olmayan kitleler ----
seq_add("Hamartom ve koristom", [
    dict(h="Hamartom", t="O bölgede normalde bulunan dokunun düzensiz büyümesi", v=P(n("12.116"), "Leiomiyomatöz hamartom", "7 yaşında çocuk, üst alveol kreti"), dur=8,
         note="Hamartom: o bölgede normalde bulunan dokunun düzensiz büyümesi."),
    dict(t="Sürekli büyümez; gerçek tümör değildir", dur=5, note="Tümör gibi sürekli büyümez."),
    dict(t="Ağızda örnek: leiomiyomatöz hamartom; üst ön diş eti ya da dil sırtı", dur=7,
         note="Ağızdaki örneği leiomiyomatöz hamartom: üst ön diş etinde ya da dil sırtının orta hattında; doğumda varsa konjenital epulis sanılabilir."),
    dict(h="Koristom", t="Normal doku, olmaması gereken bir yerde", v=P(n("12.127"), "Kemik koristomu", "Dil kökünde sert nodül"), dur=7,
         note="Koristom: normal doku ama olmaması gereken bir yerde."),
    dict(t="Ağızda en sık kemik ve kıkırdak; %85'i dilde, foramen çekum çevresinde", v=P(n("12.128"), "Epitel altında olgun lameller kemik"), dur=8,
         note="Ağızda en sık kemik ve kıkırdak koristomu görülür; Neville'e göre yüzde 85'i dilde, çoğu foramen çekum çevresinde. Hasta öğürmeden yakınabilir."),
    dict(t="Tedavi eksizyon; nüks bildirilmemiş", dur=5, note="Eksizyon yeterli; nüks bildirilmemiş."),
], strip={1}, dus=True, cred=NEV)

seq_add("Juvenil hiyalen fibromatozis", [
    dict(t="Otozomal resesif; akraba evliliğinde sık", v=P(r("jhf_yuz.jpg"), "Yüzde ve kulakta nodüller"), dur=6,
         note="Juvenil hiyalen fibromatozis otozomal resesif bir hastalık; akraba evliliğinde daha sık."),
    dict(t="2–5 yaşta başlar; baş-boyunda papül ve nodüller", dur=6, note="İki ile beş yaş arasında başlar; baş-boyunda milimetreden beş santimetreye kadar nodüller yapar."),
    dict(t="Ağızda en sık bulgu: diş eti büyümesi", v=P(r("jhf_dis_eti.jpg"), "Diş eti büyümesi"), dur=6, note="Ağızda en sık bulgu diş eti büyümesi."),
    dict(t="Eklem kontraktürleri eşlik edebilir", dur=4, note="Eklemlerde kontraktür eşlik edebilir."),
    dict(t="Mikroskop: hücreden fakir, camsı (hiyalin) matriks; PAS ve Alcian mavisi pozitif", v=P(r("jhf_mikroskop.jpg"), "Hiyalinize matriks"), dur=8,
         note="Mikroskopta hücreden fakir, camsı bir matriks görürüz; PAS ve Alcian mavisi ile boyanır."),
], strip={1}, dus=True, cred=RESMI)

seq_add("Fibromatozis colli (tortikollis)", [
    dict(t="Sternokleidomastoid kasın alt bölümünde fibröz kitle", v=P(r("colli_bebek.jpg"), "Yenidoğanda boyunda şişlik"), dur=6,
         note="Fibromatozis colli sternokleidomastoid kasın alt bölümünde bir fibröz kitle."),
    dict(t="Doğumdan 2–4 hafta sonra boyunda şişlik", dur=5, note="Doğumdan iki ile dört hafta sonra boyunda şişlik olarak fark edilir."),
    dict(t="Zor doğumda travma ve kanamayla ilişkili; tümör değil, onarım süreci", dur=7, note="Zor doğumdaki travma ve kanamayla ilişkili; gerçek tümör değil, bir onarım süreci."),
    dict(t="Kas kısalır, baş lezyon tarafına eğilir", dur=5, note="Fibröz doku çekince kas kısalır ve baş lezyon tarafına eğilir."),
    dict(t="Mikroskop: kası infiltre eden fibroblastlar; atipi yok", v=P(r("colli_mikroskop.jpg"), "Kas lifleri arasında fibroblastlar"), dur=6,
         note="Mikroskopta kas lifleri arasına giren fibroblastlar; atipi yok, zamanla kollajen artar."),
    dict(t="Fizik tedavi; kendiliğinden gerileyebilir", dur=6, note="Tedavi fizik tedavi; kendiliğinden gerileyebilir. Tedavi edilmezse ileride yüzde asimetri kalabilir."),
], strip={1}, dus=True, cred=RESMI)

seq_add("Keloid ve hipertrofik skar", [
    dict(t="İkisi de yara iyileşmesinde aşırı kollajen birikimi", dur=6, note="Keloid ve hipertrofik skar: ikisi de yara iyileşirken aşırı kollajen birikmesi."),
    dict(t="Hipertrofik skar yaranın sınırları içinde kalır, zamanla yumuşar", dur=6, note="Hipertrofik skar yaranın sınırları içinde kalır ve zamanla yumuşar."),
    dict(t="Keloid yaranın sınırını aşar; çıkarılınca sık nükseder", dur=6, note="Keloid yaranın sınırını aşar; çıkarılınca sık nükseder."),
    dict(t="Mikroskop: keloidde kalın, camsı kollajen demetleri", dur=5, note="Mikroskopta keloidde kalın, camsı kollajen demetleri görürüz."),
], strip={1})
# keloid: görsel adım adım değişen çizim
L.slides[-1]["body_fn"] = (lambda items: (lambda k: row(div(keloid_svg(min(k, 2)), "flex:0 0 1000px;display:flex"),
                                                        div(seq_list(items, k, 34), "flex:1;display:flex;flex-direction:column;gap:14px"), gap=40, style="flex:1")))(
    [dict(t="İkisi de yara iyileşmesinde aşırı kollajen birikimi"), dict(t="Hipertrofik skar yaranın sınırları içinde kalır, zamanla yumuşar"),
     dict(t="Keloid yaranın sınırını aşar; çıkarılınca sık nükseder"), dict(t="Mikroskop: keloidde kalın, camsı kollajen demetleri")])

seq_add("Nodüler fasiitis: hızlı büyür ama iyi huyludur", [
    dict(t="Genç erişkin; birkaç haftada hızla büyüyen, sıklıkla ağrılı kitle", v=P(r("nf_yanak.jpg"), "Yanakta kitle"), dur=8,
         note="Nodüler fasiitis genç erişkinde birkaç haftada hızla büyüyen, sıklıkla ağrılı bir kitle."),
    dict(t="Çoğu 3 cm'den küçük; ağızda herhangi bir yerde", v=P(r("nf_retromolar.jpg"), "Retromolar bölgede kitle"), dur=6,
         note="Çoğu üç santimetreden küçük; ağızda herhangi bir yerde olabilir."),
    dict(t="Hızlı büyüdüğü için klinikte sarkom sanılır", dur=5, note="Hızlı büyüdüğü için klinikte sarkom sanılır; bu lezyonu bilmenin nedeni bu."),
    dict(t="Mikroskop: düzensiz demetler yapan iğsi-yıldızsı miyofibroblastlar", v=P(r("nf_mikroskop.jpg"), "Miksoid zeminde iğsi hücreler"), dur=7,
         note="Mikroskopta gevşek, miksoid bir zeminde düzensiz demetler yapan iğsi ve yıldızsı miyofibroblastlar."),
    dict(t="Mitoz bol olabilir ama atipik mitoz ve pleomorfizm yok", dur=7, note="Mitoz bol olabilir; ama atipik mitoz yok, hücrelerde pleomorfizm yok. Sarkomdan ayıran bu."),
    dict(t="Ekstravaze eritrositler, lenfosit ve makrofajlar", dur=5, note="Zeminde ekstravaze eritrositler, lenfosit ve makrofajlar var."),
    dict(t="WHO 2022: USP6 nedeniyle kendiliğinden geçen bir neoplazi; nüks nadir", dur=8,
         note="Resmi slaytımız bunu neoplastik olmayan grupta sayıyor; WHO 2022 ise USP6 gen değişikliği nedeniyle kendiliğinden geçen bir neoplazi diyor. Tedavi değişmiyor: yerel eksizyon yeterli, nüks nadir. Şimdi telefon."),
], size=31, gap=10, strip={1}, dus=True, cred=RESMI)

L.add(title="Patolog gibi düşün", dur=60, theme="dark", q=W5, strip={1}, body=qbody(Q[W5], qsize=32, osize=29),
      notes="Rapor geldi. Ne dersiniz, ne yaparsınız? (Sonuç.) Doğru B: nodüler fasiitis, yerel eksizyon yeterli. Hızlı büyüme ve bol mitoz sizi sarkoma götürebilir; ama atipik mitoz yok, pleomorfizm yok ve ekstravaze eritrositler var. Bu hastaya geniş rezeksiyon yapmak en büyük hata olur.")

seq_add("Oral fokal müsinozis", [
    dict(t="Derinin fokal müsinozisinin ağızdaki karşılığı", v=P(n("12.31"), "Diş etinde nodül", "Alt azı dişleri arası"), dur=5,
         note="Oral fokal müsinozis derinin fokal müsinozisinin ağızdaki karşılığı."),
    dict(t="Genç erişkin; kadında 2 kat sık", dur=4, note="Genç erişkinde, kadında iki kat sık."),
    dict(t="Yarıdan fazlası diş etinde; sonra sert damak", dur=5, note="Yarıdan fazlası diş etinde, sonra sert damakta."),
    dict(t="Mikroskop: iyi sınırlı miksoid alan; Alcian mavisi pozitif", v=P(n("12.33"), "Gevşek, miksoid bağ dokusu"), dur=7,
         note="Mikroskopta iyi sınırlı, gevşek, miksoid bir alan; içindeki hiyalüronik asit Alcian mavisiyle boyanır."),
    dict(t="Eksizyon; nüks yok", dur=4, note="Eksizyon yeterli, nüks etmez."),
], strip={1}, dus=True, cred=NEV)

seq_add("Travmatik nöroma", [
    dict(t="Kesilen sinirin düzensiz iyileşmesi: akson, Schwann hücresi ve skar", v=P(n("12.54"), "Mental sinir boyunca nodül", "Ameliyat sırasında"), dur=7,
         note="Travmatik nöroma kesilen bir sinirin düzensiz iyileşmesi: akson, Schwann hücresi ve fibroblastlardan oluşan bir skar."),
    dict(t="En sık mental foramen bölgesi, dil, alt dudak", dur=5, note="En sık mental foramen bölgesinde, dilde ve alt dudakta."),
    dict(t="Diş çekimi ya da cerrahi öyküsü var", dur=4, note="Hastada diş çekimi ya da cerrahi öyküsü vardır."),
    dict(t="Yalnız ¼–⅓'i ağrılı; mental sinirdeki protez bastırınca ağrır", dur=7,
         note="Resmi slayt ağrılı der; Neville'e göre yalnız dörtte biri ile üçte biri ağrılı. Mental sinirdekiler protez bastırınca ağrır."),
    dict(t="Mikroskop: skar içinde düzensiz sinir demetleri", v=P(n("12.55"), "Fibröz doku içinde sinir demetleri"), dur=5, note="Mikroskopta fibröz doku içinde gelişigüzel sinir demetleri."),
    dict(t="Tedavi: sinirin proksimal ucuyla birlikte eksizyon", dur=5, note="Tedavi sinirin proksimal ucuyla birlikte eksizyon. Sırada iyi huylu tümörler."),
], strip={1}, dus=True, cred=NEV)

seq_add("Diş eti ve protezle ilişkili reaktif kitleler", [
    dict(h="Diş eti", t="Piyojenik granülom: kırmızı, kolay kanayan, hızla büyüyen kitle; gebelikte sık", v=P(n("12.34"), "Piyojenik granülom", "Üst ön diş eti"), dur=8,
         note="Neville'in bu bölümünde olup resmi slaytımızda olmayan reaktif kitleler; her birine bir cümle. Piyojenik granülom: kırmızı, kolay kanayan, hızla büyüyen bir diş eti kitlesi; gebelikte sık, doğumdan sonra küçülebilir."),
    dict(t="Periferik dev hücreli granülom: mor-mavi; yalnız diş eti ve alveol kretinde", v=P(n("12.41"), "Periferik dev hücreli granülom"), dur=7,
         note="Periferik dev hücreli granülom mor-mavi renktedir ve yalnız diş etinde ya da dişsiz alveol kretinde görülür; mikroskopta çok çekirdekli dev hücreler."),
    dict(t="Periferik ossifiye fibrom: yalnız diş etinde; içinde kemik; genç kadında", v=P(n("12.46"), "Periferik ossifiye fibrom"), dur=7,
         note="Periferik ossifiye fibrom da yalnız diş etinde, diş arası papilladan çıkar; içinde kemik ya da kalsifikasyon vardır, çoğu genç kadında."),
    dict(t="Fibrom: ağzın en sık 'tümörü'; aslında reaktif, en sık yanakta ısırma hattında", v=P(n("12.1"), "Fibrom", "Yanakta ısırma hattı"), dur=7,
         note="Fibrom ağzın en sık tümörü sayılır ama aslında reaktif bir hiperplazi; en sık yanakta, ısırma hattında. Diş eti lezyonlarında kural: periosta kadar çıkar, komşu dişleri temizle."),
    dict(h="Protez", t="Epulis fissuratum: uyumsuz protez kenarının açtığı kıvrımlar", v=P(n("12.13"), "Epulis fissuratum", "Ön vestibül"), dur=7,
         note="Epulis fissuratum uyumsuz bir protez kenarının açtığı kıvrımlar; protez kenarı iki kıvrım arasındaki yarığa oturur."),
    dict(t="İnflamatuvar papiller hiperplazi: protez altında, sert damakta çakıl taşı görünümü", v=P(n("12.18"), "İnflamatuvar papiller hiperplazi", "Sert damak"), dur=8,
         note="İnflamatuvar papiller hiperplazi protezin altında, sert damakta çakıl taşı gibi papiller. İkisinde de protez düzeltilmezse lezyon geri gelir."),
], size=31, gap=10, strip={1}, dus=True, cred=NEV)

# ---- 2. İyi huylu tümörler ----
seq_add("Lif ve histiyosit kökenli iyi huylu tümörler", [
    dict(t="**Fibröz histiyositom:** deride sık, ağızda nadir", v=P(n("12.21"), "Fibröz histiyositom", "Dil sırtı"), dur=6,
         note="İyi huylu tümörlere lif ve histiyosit kökenlilerle başlıyoruz. Fibröz histiyositom deride dermatofibrom adıyla sık, ağızda nadir."),
    dict(t="İğsi hücreler girdap gibi (storiform) dizilir", v=P(n("12.22"), "Storiform desen"), dur=5, note="Mikroskopta iğsi hücreler girdap gibi dizilir; buna storiform desen diyoruz."),
    dict(t="**Fibromatozis (desmoid):** iyi huylu ama lokal agresif; metastaz yapmaz", v=P(n("12.26"), "Fibromatozis", "Alt çene lingual diş eti"), dur=8,
         note="Fibromatozis, desmoid tip: iyi huylu ama lokal agresif; metastaz yapmaz. Resmi slayttaki 'gingival fibromatozis' kalıtsal diş eti büyümesiyle karışmasın; burada diş etindeki desmoid tip kastediliyor."),
    dict(t="Nükleer β-katenin; nüks ~%30", v=P(n("12.27"), "Uzun demetler yapan fibroblastlar"), dur=5, note="Nükleer beta-katenin pozitif; yaklaşık üçte biri nükseder."),
    dict(t="**Miyofibrom:** genç hasta; ağızda en sık alt çene", v=P(n("12.28"), "Miyofibrom", "Üst çene diş eti"), dur=5, note="Miyofibrom genç hastada; ağızda en sık alt çenede."),
    dict(t="SMA pozitif; bebekte çok odaklı form (miyofibromatozis)", v=P(n("12.30"), "İğsi hücreler; SMA"), dur=5, note="SMA pozitif; bebeklerde çok odaklı formu var, miyofibromatozis."),
    dict(t="**Soliter fibröz tümör:** ağızda en sık yanak; eski 'hemanjiyoperisitomların' çoğu", v=P(n("12.24"), "Soliter fibröz tümör", "Retromolar bölge"), dur=7,
         note="Soliter fibröz tümör ağızda en sık yanakta; eskiden hemanjiyoperisitom denen tümörlerin çoğu bu."),
    dict(t="Geyik boynuzu damarlar; CD34 ve STAT6 pozitif", v=P(n("12.25"), "Geyik boynuzu damarlar", pos="50% 100%"), dur=5, note="Geyik boynuzu gibi dallanan damarlar; CD34 ve STAT6 pozitif."),
], size=30, gap=10, strip={2}, dus=True, cred=NEV)

seq_add("Lipom", [
    dict(t="Yağ dokusunun iyi huylu tümörü; ağız-çene tümörlerinin yalnız %1–4'ü", v=P(n("12.50"), "Yanak mukozasında nodül"), dur=7,
         note="Lipom yağ dokusunun iyi huylu tümörü; ağızda beklenenden az, ağız-çene tümörlerinin yüzde 1 ila 4'ü."),
    dict(t="Yumuşak, sarımsı, ağrısız; çoğu 40 yaş üstü", dur=5, note="Yumuşak, sarımsı, ağrısız bir nodül; çoğu 40 yaşın üstünde."),
    dict(t="Ağızda en sık yanak ve vestibül (~yarısı)", dur=6, note="Resmi slayt en sık yeri dil olarak sıralıyor; Neville'e göre yanak ve vestibül olguların yaklaşık yarısı."),
    dict(t="Mikroskop: ince kapsüllü olgun yağ dokusu", v=P(n("12.52"), "Olgun yağ hücreleri"), dur=5, note="Mikroskopta ince bir kapsülle çevrili olgun yağ dokusu."),
    dict(t="Tipler: fibrolipom (en sık), iğsi hücreli, anjiyolipom, miksoid, pleomorfik", dur=6, note="Tiplerinden en sık fibrolipom; iğsi hücreli lipom CD34 pozitif."),
    dict(t="Atipi varsa MDM2/CDK4 ile liposarkom dışlanır", dur=6, note="Hücrelerde atipi görürsek MDM2 ve CDK4 boyalarıyla iyi diferansiye liposarkomu dışlarız. Tedavi eksizyon; nüks nadir."),
], strip={2}, dus=True, cred=NEV)

seq_add("Palizatlı kapsüllü nöroma ve schwannom", [
    dict(h="Palizatlı kapsüllü nöroma", t="Küçük, ağrısız, kapsüllü nodül; %90'ı yüzde", v=P(n("12.57"), "Sert damakta nodül"), dur=7,
         note="Sinir kökenli tümörler. Palizatlı kapsüllü nöroma küçük, ağrısız, kapsüllü bir nodül; yüzde 90'ı yüzde."),
    dict(t="Ağızda sert damak, diş eti, dudak; travma öyküsü yok", dur=6, note="Ağızda sert damakta, diş etinde, dudakta. Travmatik nöromadan farkı: travma öyküsü yok."),
    dict(t="NF ve MEN 2B ile ilişkisi yok", v=P(n("12.58"), "İyi sınırlı nöral proliferasyon"), dur=5, note="Nörofibromatozis ve MEN 2B ile ilişkisi yok."),
    dict(h="Schwannom", t="Schwann hücresinden; kapsüllü, yavaş büyür", v=P(n("12.60"), "Ağız tabanında kitle"), dur=6, note="Schwannom Schwann hücresinden köken alan, kapsüllü, yavaş büyüyen bir tümör."),
    dict(t="Ağızda en sık dil; kemik içinde alt çene arka bölge", dur=6, note="Ağızda en sık dilde; kemik içindekiler alt çenenin arka bölgesinde, mandibular kanal boyunca."),
    dict(t="Antoni A: palizat çekirdekler, Verocay cisimcikleri", v=P(n("12.61"), "Antoni A ve B"), dur=8,
         note="Mikroskopta iki alan var. Antoni A'da çekirdekler sıra sıra dizilir; iki sıra arasındaki pembe alana Verocay cisimciği denir."),
    dict(t="Antoni B: gevşek, miksoid; S100 yaygın pozitif", dur=7, note="Antoni B gevşek ve miksoiddir. S100 yaygın pozitif; kötü huylu dönüşüm neredeyse hiç olmaz."),
], size=29, gap=8, strip={2}, dus=True, cred=NEV)

seq_add("Nörofibrom ve nörofibromatozis tip 1", [
    dict(h="Nörofibrom", t="Periferik sinir kılıfının en sık tümörü", v=P(n("12.62"), "Üst çene diş etinde nodül"), dur=6, note="Nörofibrom periferik sinir kılıfının en sık tümörü."),
    dict(t="Kapsülsüz; sinirle iç içe büyür", dur=5, note="Schwannomdan farkı: kapsülü yok, sinirle iç içe büyür."),
    dict(t="Mikroskop: dalgalı çekirdekli iğsi hücreler, mast hücreleri", v=P(n("12.65"), "Dalgalı çekirdekler"), dur=6, note="Mikroskopta dalgalı çekirdekli iğsi hücreler ve aralarda mast hücreleri."),
    dict(h="NF1", t="Nörofibrom görürsen hastayı NF1 için muayene et", v=P(n("12.68"), "Café-au-lait lekeleri"), dur=6,
         note="Bir nörofibrom gördüğünüzde hastayı nörofibromatozis tip 1 için muayene edin."),
    dict(t="Otozomal dominant; café-au-lait, aksiller çillenme, Lisch nodülleri", dur=8, note="NF1 otozomal dominant; deride café-au-lait lekeleri, koltuk altında çillenme, gözde Lisch nodülleri."),
    dict(t="Malign periferik sinir kılıfı tümörü riski %8–13", v=P(n("12.69"), "Dilin tek taraflı büyümesi"), dur=7,
         note="Hastaların yüzde 8 ila 13'ünde malign periferik sinir kılıfı tümörü gelişir; büyüyen ya da ağrıyan bir nörofibrom beklemez."),
    dict(h="Ayrıca: MEN 2B", t="Dil ucunda çok sayıda nöroma → medüller tiroid karsinomu", v=P(n("12.74"), "MEN 2B: dil ucunda nöromalar"), dur=8,
         note="Bir not: dil ucunda ve dudaklarda çok sayıda küçük nöroma MEN 2B'yi düşündürür; bu hastaların hepsinde medüller tiroid karsinomu gelişir. Endokrinolojiye yönlendirin."),
], size=29, gap=8, strip={2}, dus=True, cred=NEV)

L.add(title="Dört mikroskop görüntüsü: hangisi schwannom?", dur=40, theme="dark", q=W2, strip={2}, cred=NEV,
      body=qbody(Q[W2], qsize=40, photo=col(row(ph(n("12.65"), label="A"), ph(n("12.61"), label="B"), style="flex:1"),
                                            row(ph(n("12.118"), label="C"), ph(n("12.33"), label="D"), style="flex:1"), gap=16, style="flex:1")),
      notes="Dört mikroskop görüntüsü. Hangisi schwannom? (Sonuç.) Doğru B: çekirdeklerin sıra sıra dizildiği Antoni A alanı. A nörofibrom: dalgalı çekirdekli, düzensiz iğsi hücreler. C leiomiyom: küt uçlu çekirdekli düz kas demetleri. D oral fokal müsinozis: gevşek, miksoid bağ dokusu.")

seq_add("Granüler hücreli tümör ve konjenital epulis", [
    dict(h="Granüler hücreli tümör", t="En sık ağızda (ve deride); ağızda ⅓–½'i dil sırtında", v=P(n("12.85"), "Yanakta nodül"), dur=8,
         note="Granüler hücreli tümör vücutta en sık ağızda ve deride görülür; ağızda üçte biri ile yarısı dil sırtında."),
    dict(t="4.–6. dekat; kadında 3 kat sık; çoğu <2 cm", dur=6, note="Kırk ile altmış yaş arasında, kadında üç kat sık; çoğu iki santimetreden küçük."),
    dict(t="İri, poligonal, granüler sitoplazmalı hücreler; PAS ve S100 pozitif", v=P(n("12.86"), "Granüler hücreler"), dur=8,
         note="Hücreler iri, poligonal ve sitoplazmaları ince pembe granüllerle dolu; PAS ve S100 pozitif, yani Schwann hücresi özellikleri taşıyor."),
    dict(t="Yarısına kadarında yüzeyde psödoepitelyomatöz hiperplazi", v=P(n("12.87"), "Epitelde aşağı uzanan dallar"), dur=8,
         note="Olguların yarısına kadarında üstteki epitel aşağı doğru dallar yapar; buna psödoepitelyomatöz hiperplazi diyoruz. Bunu dersin sonunda tekrar göreceğiz."),
    dict(h="Konjenital epulis", t="Yenidoğanın alveol kretinde; ~%90'ı kız", v=P(n("12.88"), "Yenidoğan, üst alveol kreti"), dur=7,
         note="Yenidoğandaki benzeri konjenital epulis: doğumda alveol kretinde polipoid kitle; yaklaşık yüzde 90'ı kız bebek."),
    dict(t="Benzer hücreler ama S100 negatif; reteler atrofik", v=P(n("12.89"), "İnce yüzey epiteli"), dur=7,
         note="Hücreleri benzer ama S100 negatif; yüzeyde hiperplazi yok, reteler incelmiş."),
    dict(t="Nüksetmez; kendiliğinden gerileyebilir", dur=5, note="Nüksetmez; hatta kendiliğinden küçülebilir."),
], size=32, gap=10, strip={2}, dus=True, cred=NEV)

L.add(title="DUS Molası 1/2", dur=45, theme="dark", q=W3, body=qbody(Q[W3]),
      notes="İlk DUS sorusu, Neville'in kitap sonundaki örnek sınav sorularından. 30 saniye. (Sonuç.) Konjenital epulis: yaklaşık yüzde 90'ı kız bebek. Granüler hücreli tümör de kadında sık, ama oran üçe bir.")

L.add(title="DUS Molası 2/2", dur=40, theme="dark", q=W4, body=qbody(Q[W4]),
      notes="İkinci soru. (Sonuç.) Nörofibromatozis tip 1. Lisch nodülleri irisin pigmentli hamartomları; NF1 hastalarının neredeyse hepsinde var. Sırada damar kökenli tümörler.")

L.add(title="Ara liderlik: ilk 5", dur=15, board=True, top=5,
      notes="On saniye: ilk beş. (→ ile devam.)")

seq_add("Hemanjiyom mu, vasküler malformasyon mu?", [
    dict(h="Hemanjiyom (tümör)", t="Çoğu doğumda yok; ilk haftalarda çıkar, hızla büyür", v=P(n("12.93"), "İnfantil hemanjiyom", "4 yaşında çocuk, üst dudak"), dur=8,
         note="Damar lezyonlarında iki ayrı grup var. Hemanjiyom bir tümör: çoğu doğumda yoktur, ilk haftalarda çıkar ve hızla büyür."),
    dict(t="Sonra geriler: 5 yaşta %50, 9 yaşta %90", dur=7, note="Sonra geriler: yarısı beş yaşında, yüzde 90'ı dokuz yaşında kaybolur."),
    dict(t="GLUT1 pozitif; çoğu beklenir, gerekirse propranolol", v=P(n("12.99"), "Hücreden zengin endotel proliferasyonu"), dur=8,
         note="GLUT1 pozitiftir. Çoğunu bekleriz; gerekirse propranolol veririz."),
    dict(h="Vasküler malformasyon", t="Doğumda var; çocukla büyür, gerilemez; GLUT1 negatif", v=P(n("12.94"), "Venöz malformasyon", "Dil"), dur=9,
         note="Malformasyon damar yapısının gelişim bozukluğu: doğumda vardır, çocukla birlikte büyür ve gerilemez; GLUT1 negatif."),
    dict(t="Venöz malformasyon mor-mavi; bastırınca söner", v=P(n("12.101"), "Genişlemiş büyük damarlar"), dur=7, note="Venöz malformasyon mor-mavidir ve bastırınca kolayca söner."),
    dict(t="ISSVA sınıflaması tümörü malformasyondan ayırır", dur=6, note="ISSVA sınıflaması bu iki grubu ayırır: vasküler tümörler ve vasküler malformasyonlar."),
    dict(t="Kemik içi lezyonda biyopsiden önce iğne aspirasyonu: ölümcül kanama riski", v=P(n("12.95"), "Kemik içi venöz malformasyon"), dur=15,
         note="Neville'den pratik uyarı: tanısı konmamış kemik içi bir lezyonda biyopsiden önce iğneyle aspirasyon yapın. Malformasyonun yanında diş çekiminden sonra ölümcül kanamalar bildirildi."),
], size=28, gap=8, strip={2}, dus=True, cred=NEV)

seq_add("Sturge-Weber ve melanotik nöroektodermal tümör", [
    dict(h="Sturge-Weber sendromu", t="Yüzde trigeminal dağılımda porto şarabı lekesi", v=P(n("12.103"), "Porto şarabı lekesi", "Trigeminal birinci dal"), dur=6,
         note="Sturge-Weber sendromu: yüzde trigeminal sinir dağılımında porto şarabı lekesi; leke birinci dalı tutuyorsa risk yüzde 15 ila 20."),
    dict(t="Aynı tarafta beyin zarında damar anomalisi: nöbet, zihinsel yetersizlik", v=P(n("12.104"), "Kafa grafisinde 'tramvay rayı' kalsifikasyonları"), dur=7,
         note="Aynı tarafta beyin zarında damar anomalisi olur: nöbet ve zihinsel yetersizlik. Ağızda o bölgede cerrahi ciddi kanayabilir."),
    dict(h="Bebeğin melanotik nöroektodermal tümörü", t="1 yaşın altında, üst çene ön bölgede hızla büyüyen kitle", v=P(n("12.77"), "Üst çene ön bölgede kitle", "Bebek"), dur=7,
         note="Bebeğin melanotik nöroektodermal tümörü: bir yaşın altında, üst çene ön bölgede hızla büyüyen, mavi-siyah bir kitle; idrarda vanilmandelik asit yüksek olabilir."),
], size=32, strip={2}, dus=True, cred=NEV)

seq_add("Lenfanjiyom ve nazofarengeal anjiyofibrom", [
    dict(h="Lenfanjiyom", t="Neville 5: lenfatik malformasyon; WHO 2022: lenfanjiyom", v=P(n("12.110"), "Dilde lenfatik malformasyon", "Kabarcıklı yüzey"), dur=7,
         note="Lenfanjiyom Neville'in yeni baskısında lenfatik malformasyon adıyla geçiyor; WHO hâlâ lenfanjiyom diyor. İkisini de bilin."),
    dict(t="Yarısı doğumda, %90'ı 2 yaşa kadar ortaya çıkar", dur=6, note="Yarısı doğumda vardır, yüzde 90'ı iki yaşına kadar ortaya çıkar."),
    dict(t="Ağızda en sık dilin ön ⅔'ü: dil büyür, yüzey kabarcıklı", v=P(n("12.112"), "Epitel altında genişlemiş lenf damarları"), dur=8,
         note="Ağızda en sık dilin ön üçte ikisinde; damarlar epitelin hemen altında olduğu için yüzey küçük, saydam kabarcıklarla kaplıdır ve dil büyür."),
    dict(t="Boyunda kistik higroma: havayolunu tıkayabilir", v=P(n("12.109"), "Kistik higroma", pos="50% 30%"), dur=7,
         note="Boyundaki büyük kistli formuna kistik higroma deniyor; yenidoğanda havayolunu tıkayabilir."),
    dict(h="Nazofarengeal anjiyofibrom", t="Neredeyse yalnız ergen erkek; burun tıkanıklığı ve kanama", v=P(n("12.106"), "BT: nazofarenkste kitle"), dur=8,
         note="Nazofarengeal anjiyofibrom neredeyse yalnız ergen erkeklerde görülür: burun tıkanıklığı ve tekrarlayan burun kanaması. Hücreleri androjen reseptörü taşır."),
    dict(t="Damar duvarında kas eksik, elastik lif yok: çok kanar", v=P(n("12.108"), "Fibröz doku içinde ince duvarlı damarlar"), dur=7,
         note="Damar duvarlarında kas tabakası eksik ve elastik lif yok; bu yüzden çok kanar."),
    dict(t="Ameliyattan önce embolizasyon; nüks %20–40", v=P(n("12.107"), "Anjiyografi: yoğun damarlanma"), dur=7,
         note="Ameliyattan önce embolizasyon yapılır; yüzde 20 ila 40 nükseder. WHO 2022'deki adı sinonazal anjiyofibrom."),
], size=28, gap=8, strip={2}, dus=True, cred=NEV)

seq_add("Kas kökenli iyi huylu tümörler ve diğerleri", [
    dict(h="Leiomiyom", t="Düz kas tümörü; ağızda nadir, ~%75'i anjiyomiyom", v=P(n("12.115"), "Sert damakta pembe-kırmızı nodül"), dur=7,
         note="İyi huylu tümörlerin sonuncusu kas. Leiomiyom düz kas tümörü; ağızda nadir ve dörtte üçü damar duvarındaki kastan, yani anjiyomiyom."),
    dict(t="Dudak, dil, damak, yanak; anjiyomiyom ağrılı olabilir", dur=5, note="Dudak, dil, damak ve yanakta görülür; anjiyomiyom ağrılı olabilir."),
    dict(t="Küt uçlu çekirdekler; SMA pozitif", v=P(n("12.118"), "Düz kas demetleri"), dur=5, note="Mikroskopta küt uçlu, puro biçimli çekirdekler; SMA pozitif."),
    dict(h="Rabdomiyom", t="Erişkin tip: orta-ileri yaş, %80 erkek; ağız tabanı, yumuşak damak", v=P(n("12.121"), "Yanakta kitle (ok)"), dur=7,
         note="Rabdomiyom çizgili kas tümörü: erişkin tip orta ve ileri yaşta, yüzde 80'i erkekte; ağız tabanında, yumuşak damakta, dil kökünde."),
    dict(t="Vakuollü sitoplazma: örümcek ağı görünümü", v=P(n("12.123"), "Geniş eozinofilik sitoplazmalı hücreler"), dur=6,
         note="Hücrelerin sitoplazması vakuollüdür, örümcek ağı gibi görünür. Çocuktaki fetal tipi rabdomiyosarkomla karışabilir."),
    dict(h="Tek satır", t="Paragangliom: en sık karotis cisimciği; hücre yuvaları (zellballen)", v=P(n("12.83"), "Paragangliom: hücre yuvaları"), dur=7,
         note="Paragangliom en sık karotis cisimciğinde; hücreler yuvalar yapar, buna zellballen denir. Üçte biri kadarı kalıtsal."),
    dict(t="Tendon kılıfının dev hücreli tümörü: ağızda çok nadir", dur=5, note="Tendon kılıfının dev hücreli tümörü resmi slaytta var ama ağızda çok nadir."),
], size=28, gap=8, strip={2}, dus=True, cred=NEV)

# ---- 3. Sarkomlar ----
seq_add("Sarkomlar: ortak özellikler", [
    dict(t="Ağız-çene bölgesi kanserlerinin %1'inden azı", v=P(n("12.129"), "Fibrosarkom", "Çocukta damak ve alveol kretinde kitle"), dur=6,
         note="Üçüncü grup: sarkomlar, yumuşak dokunun kötü huylu tümörleri. Ağız ve çene bölgesinde nadir: Neville'e göre bu bölgedeki kanserlerin yüzde birinden azı."),
    dict(t="Lokal agresif büyür; önce çevre dokuyu yıkar", dur=5, note="Lokal agresif büyür; önce çevre dokuyu yıkar."),
    dict(t="Lenf noduna az gider; uzak metastaz en sık akciğere", dur=6, note="Karsinomların aksine lenf noduna az gider; uzak metastaz en sık akciğere."),
    dict(t="Risk: eski radyoterapi, kronik travma, yanık skarı, metal implant", dur=7, note="Risk etkenleri: yıllar önce alınmış radyoterapi, kronik travma, yanık skarı, metal implant."),
    dict(t="Kalıtsal zemin: nörofibromatozis, retinoblastom", v=P(n("12.70"), "NF1'li hastada yanakta MPNST"), dur=6, note="Kalıtsal zemin: nörofibromatozis ve retinoblastom."),
    dict(t="Davranışı tip, derece, boyut ve cerrahi sınır belirler; baş-boyunda nüks sık", dur=10,
         note="Davranışını tipi, derecesi, boyutu, evresi ve cerrahi sınır belirler. Baş-boyunda geniş sınır bırakmak zor; yerel nüks sık."),
], size=34, strip={3}, dus=True, cred=NEV)

seq_add("Pleomorfik sarkom, fibrosarkom, liposarkom", [
    dict(h="İndiferansiye pleomorfik sarkom", t="Eski adı malign fibröz histiyositom; yaşlıda", v=P(n("12.131"), "Belirgin pleomorfizm, mitozlar"), dur=7,
         note="İndiferansiye pleomorfik sarkom, eski adıyla malign fibröz histiyositom: yaşlı hastada, daha çok bacakta ve gövdede."),
    dict(t="Storiform demetler ve tuhaf, çok çekirdekli dev hücreler", dur=6, note="Mikroskopta girdap gibi demetler ve tuhaf, çok çekirdekli dev hücreler."),
    dict(t="Baş-boyunda sinonazal; bir kısmı radyoterapiden sonra; nüks %40", dur=7, note="Baş-boyunda burun ve sinüslerde; bir kısmı radyoterapiden yıllar sonra gelişir. Yüzde 40'ı nükseder."),
    dict(h="Fibrosarkom", t="Bugün bir dışlama tanısı; baş-boyunda %10–19", v=P(n("12.129"), "Çocukta damakta kitle"), dur=6,
         note="Fibrosarkom bugün bir dışlama tanısı; olguların yüzde 10 ila 19'u baş-boyunda."),
    dict(t="İğsi hücreler balık kılçığı (herringbone) deseninde", v=P(n("12.130"), "İğsi hücre demetleri"), dur=6, note="İğsi hücreler balık kılçığı deseninde dizilir."),
    dict(h="Liposarkom", t="Ağızda dil ve yanak; ağızdakilerin %67'si iyi diferansiye", v=P(n("12.132"), "Vakuollü lipoblastlar"), dur=7,
         note="Liposarkom ağızda en sık dilde ve yanakta; ağızdakilerin üçte ikisi iyi diferansiye tip."),
    dict(t="Lipoblastlar; MDM2/CDK4 pozitif; ağızdakiler iyi seyirli", dur=6, note="Lipoma benzer ama lipoblast ve atipik hücreler içerir; MDM2 ve CDK4 pozitif. Ağızdakiler iyi seyirli."),
    dict(t="En sık sarkom: resmi slayt pleomorfik sarkom der; Neville 5'e göre bugün liposarkom", dur=15,
         note="Bir uyuşmazlık: resmi slayt en sık sarkom olarak pleomorfik sarkomu sayıyor. Neville 5'e göre bu eski bilgi; malign fibröz histiyositom denen tümörlerin çoğu başka sarkomlara ayrıldı ve bugün en sık sarkom liposarkom."),
], size=27, gap=7, vis_w=960, strip={3}, dus=True, cred=NEV)

seq_add("Sinir ve damar kökenli sarkomlar", [
    dict(h="Malign periferik sinir kılıfı tümörü", t="Dörtte biri ile yarısı NF1'li hastada", v=P(n("12.71"), "NF1'li hastada yanak"), dur=7,
         note="Malign periferik sinir kılıfı tümörü, eski adıyla malign schwannom: dörtte biri ile yarısı NF1'li hastalarda gelişir; NF1'de büyüyen kitle hemen biyopsi ister."),
    dict(t="Dalgalı çekirdekli atipik iğsi hücreler; prognoz kötü", v=P(n("12.72"), "Atipik iğsi hücreler"), dur=6, note="Mikroskopta dalgalı çekirdekli atipik iğsi hücreler; prognozu kötü."),
    dict(h="Olfaktör nöroblastom", t="Burun tavanında; çocukta değil erişkinde (ort. 45–56 yaş)", v=P(n("12.133"), "MR: burun tavanında kitle"), dur=7,
         note="Olfaktör nöroblastom burun tavanında koku epitelinden köken alır; adına rağmen çocukta değil erişkinde görülür."),
    dict(t="Küçük yuvarlak mavi hücreler, rozetler; kromogranin, sinaptofizin", v=P(n("12.134"), "Küçük, bazofilik hücreler"), dur=6,
         note="Mikroskopta küçük, yuvarlak, mavi hücreler ve rozetler; kromogranin ve sinaptofizin pozitif."),
    dict(h="Anjiyosarkom", t="Yarısı baş-boyunda, en sık saçlı deri; ağızda çok nadir", v=P(n("12.136"), "Atipik endotelle döşeli kanallar"), dur=7,
         note="Anjiyosarkomun yarısı baş-boyunda, en sık saçlı deride ve alında; ağızda çok nadir."),
    dict(t="Erken lezyon morluk gibi; CD31 ve ERG pozitif", dur=5, note="Erken dönemde morluk gibi görünür, bu yüzden tanı gecikir; CD31 ve ERG pozitif."),
    dict(h="Kaposi sarkomu", t="HHV-8; dört form: klasik, endemik, nakil, AIDS", v=P(n("7.42"), "HIV; sert damakta nodüler büyüme"), dur=8,
         note="Kaposi sarkomu HHV-8 ile ilişkili; dört formu var. Resmi slayt endemik formu HIV ve HHV-8 ile ilişkilendiriyor; Neville'e göre dört formun hepsinin etkeni HHV-8, HIV yalnız AIDS formunda."),
    dict(t="AIDS'li hastaların ~%70'inde ağız lezyonu; en sık sert damak", dur=6, note="AIDS'li hastaların yaklaşık yüzde 70'inde ağız lezyonu olur, en sık sert damakta."),
    dict(t="İğsi hücreler, yarık benzeri damarlar, ekstravaze eritrositler", v=P(n("12.139"), "İğsi hücreler ve yarık benzeri damarlar"), dur=8,
         note="Mikroskopta iğsi hücreler, yarık benzeri damarlar ve ekstravaze eritrositler."),
], size=26, gap=6, vis_w=940, strip={3}, dus=True, cred=NEV)

seq_add("Kas kökenli sarkomlar ve diğerleri", [
    dict(h="Leiomiyosarkom", t="Ağızda nadir; üçte biri alt çenede", v=P(n("12.140"), "Üst alveol kretinde ülserli kitle"), dur=6,
         note="Leiomiyosarkom düz kas sarkomu; ağızda nadir, üçte biri alt çenede."),
    dict(t="Puro biçimli çekirdekler; 10 BBA'da ≥5 mitoz malign", v=P(n("12.141"), "Pleomorfik iğsi hücreler"), dur=6,
         note="Çekirdekler puro biçimli; on büyük büyütme alanında beş ya da daha fazla mitoz varsa malign kabul edilir."),
    dict(h="Rabdomiyosarkom", t="Çocuk yumuşak doku sarkomlarının yarısı; en sık baş-boyun", v=P(n("12.142"), "Çocukta maksillada kitle"), dur=7,
         note="Rabdomiyosarkom çocukların sarkomu: çocukluk çağı yumuşak doku sarkomlarının yarısı, en sık baş-boyunda."),
    dict(t="Embriyonal en sık (ilk 10 yıl); alveoler ergen ve gençte", v=P(n("12.144"), "Küçük yuvarlak hücreler"), dur=6,
         note="Embriyonal tip en sık ve ilk on yaşta; alveoler tip ergenlik ve gençlikte; pleomorfik tip erişkinde."),
    dict(t="Ağız içinde en sık damak; desmin ve miyogenin pozitif", v=P(n("12.145"), "Desmin pozitif rabdomiyoblastlar"), dur=6,
         note="Ağız içinde en sık damakta; desmin ve miyogenin pozitif."),
    dict(h="Sinovyal sarkom", t="Eklem çevresinde ama sinovyadan köken almaz; baş-boyunda parafarenks", v=P(n("12.146"), "İğsi hücreler ve bez benzeri yapılar"), dur=8,
         note="Sinovyal sarkom eklem çevresinde görülür ama adına rağmen sinovyadan köken almaz; baş-boyunda en sık parafarenkste."),
    dict(t="SS18::SSX füzyonu; Neville'e göre monofazik tip daha sık", dur=6,
         note="Tanıyı SS18::SSX füzyonu koydurur. Resmi slayt genellikle bifazik der; Neville'e göre monofazik tip daha sık."),
    dict(h="Alveoler yumuşak doku sarkomu", t="Çocukta baş-boyunda: orbita ve dil", v=P(n("12.147"), "Alveol benzeri yuvalar"), dur=6,
         note="Alveoler yumuşak doku sarkomu nadir; çocukta baş-boyunda en sık orbitada ve dilde."),
    dict(t="PAS pozitif, diastaza dirençli kristaller; TFE3 pozitif", dur=5, note="Hücrelerde PAS pozitif, diastaza dirençli kristaller; TFE3 pozitif."),
], size=26, gap=6, vis_w=940, strip={3}, dus=True, cred=NEV)

seq_add("Ağız yumuşak dokusuna metastaz", [
    dict(t="En sık diş eti (%54); piyojenik granülom gibi görünebilir", v=P(n("12.148"), "Melanom metastazı", "Alt çene diş eti"), dur=7,
         note="Son olarak metastaz. Ağız yumuşak dokusuna gelen metastazların yarıdan fazlası diş etinde ve piyojenik granülom gibi görünebilir."),
    dict(t="Erkekte akciğer, kadında meme; %25'inde kanserin ilk bulgusu", v=P(n("12.150"), "Kolon adenokarsinomu metastazı", "Retromolar bölge"), dur=8,
         note="Erkekte en sık akciğerden, kadında memeden gelir; hastaların dörtte birinde ağızdaki lezyon kanserin ilk bulgusu. Bu yüzden çıkardığınız her doku patolojiye gider."),
], size=34, strip={3}, dus=True, cred=NEV)

# ---- Vakaya dönüş ----
BIYOPSI_V = col(ph(n("12.87"), "Biyopsi: epitelde aşağı uzanan dallar", style="flex:1"),
                box("yellow", None, html_="<div class='big' style='font-size:36px'>Karsinom mu? Tahminin değişti mi?</div>", style="padding:30px 32px"),
                style="flex:1")
seq_add("Açılış vakası: biyopsi sonucu", [
    dict(t="42 yaşında kadın; dil sırtında ağrısız, sarımsı nodül", v=BIYOPSI_V, dur=8, note="Dersin başındaki hastamıza dönüyoruz: dil sırtında ağrısız, sarımsı nodül."),
    dict(t="Yüzeysel insizyonel biyopsi yapıldı", dur=7, note="Yüzeysel bir insizyonel biyopsi yapıldı."),
    dict(t="Rapor: yüzeyde psödoepitelyomatöz hiperplazi; invaziv karsinom dışlanamadı", dur=15,
         note="Rapor: yüzeyde psödoepitelyomatöz hiperplazi, invaziv karsinom dışlanamadı. Epitel aşağı doğru dallar yapıyor ve karsinoma benziyor. Tahmininizi yenileyin; sıradaki slaytta ilk tahminle karşılaştıracağız."),
], size=38, vis_w=900, theme="dark", tag=("pink", "VAKAYA DÖNÜŞ"), cred=NEV)

L.add(title="Vakaya dönüş: şimdi ne diyorsun?", dur=40, theme="dark", q=W6, cred=NEV,
      body=qbody(Q[W6], photo=ph(n("12.87"), "Yüzeysel biyopsi")),
      notes="Aynı soru, aynı şıklar. Dersin başındaki dağılımı hatırlayın. (İki sonucu yan yana göster.)")

seq_add("Tanı: granüler hücreli tümör", [
    dict(h="Yer", t="Dil sırtı: granüler hücreli tümörün en sık yeri; ağız kanserinin olağan yeri değil", v=P(n("12.84"), "Dil sırtında nodül"), dur=10,
         note="Kanıtları sırayla koyalım. Yer: dil sırtı; granüler hücreli tümörün en sık yeri, ama ağız kanserinin olağan yeri değil."),
    dict(h="Klinik", t="Ağrısız, sert, sarımsı nodül; kadın, 4.–6. dekat", dur=7, note="Klinik: ağrısız, sert, sarımsı nodül; orta yaşta kadın."),
    dict(h="Yüzeysel biyopsi", t="Psödoepitelyomatöz hiperplazi: karsinoma benzer", v=P(n("12.87"), "Yüzeyde psödoepitelyomatöz hiperplazi"), dur=9,
         note="Yüzeysel biyopsi epitelin aşağı uzanan dallarını gösterdi; psödoepitelyomatöz hiperplazi karsinoma çok benzer."),
    dict(h="Derin biyopsi", t="İri, poligonal, granüler sitoplazmalı hücreler; S100 ve PAS pozitif", v=P(n("12.86"), "Derin biyopsi: granüler hücreler"), dur=9,
         note="Derin biyopsi altındaki asıl tümörü gösterdi: iri, granüler sitoplazmalı hücreler, S100 ve PAS pozitif. Tanı granüler hücreli tümör."),
    dict(h="Yönetim", t="Konservatif eksizyon; nüks nadir", dur=6, note="Tedavi konservatif eksizyon; nüks nadir."),
    dict(h="Patoloğun notu", t="Yüzeysel biyopsi karsinom sanılabilir: dil sırtındaki nodülde biyopsiyi derin al, istek formuna yeri ve kliniği yaz",
         v=col(ph(n("12.86"), "Derin biyopsi: granüler hücreler", style="flex:1"),
               pato("Yüzeysel biyopsi tuzağı", "Neville: psödoepitelyomatöz hiperplazi bazen o kadar belirgindir ki karsinom tanısı konup **gereksiz kanser ameliyatı** yapılabilir.",
                    size=24, style="padding:18px 22px 18px 26px"), style="flex:1;gap:14px"), dur=19,
         note="Patoloğun notu: Neville bu görüntü yüzünden karsinom tanısı konup gereksiz kanser ameliyatı yapılan hastalardan söz ediyor. Dil sırtındaki bir nodülde biyopsiyi derin alın ve istek formuna yeri ve kliniği yazın."),
], size=27, gap=8, cred=NEV)

L.add(title="Eski ad, yeni ad", dur=40, optional=True,
      body=row(col(box("lilac", "Eski ad → güncel ad", None, html_=table([
                       ["Malign fibröz histiyositom", "İndiferansiye pleomorfik sarkom"],
                       ["Hemanjiyoperisitom", "Soliter fibröz tümör"],
                       ["Malign schwannom", "Malign periferik sinir kılıfı tümörü"],
                       ["Estezyonöroblastom", "Olfaktör nöroblastom"],
                       ["Nazofarengeal anjiyofibrom", "Sinonazal anjiyofibrom (WHO 2022)"],
                       ["Lenfanjiyom", "Lenfatik malformasyon (Neville 5; WHO hâlâ lenfanjiyom)"],
                       ["Nodüler fasiitis", "WHO 2022: kendiliğinden geçen neoplazi (USP6)"]], size=30, w1=520), style="padding:26px 30px"), style="flex:0 0 1300px")),
      notes="Zaman kalırsa; yoksa atlayın. Adı değişen tümörler; sınavda iki adı da görebilirsiniz.")

L.add(title="Çıkış bileti", dur=40, theme="dark", q=W7,
      body=div("<div class='live'>CANLI · W7 · Kelime bulutu</div><div class='qq' style='font-size:56px;margin-top:60px;max-width:1500px'>%s</div>"
               "<div style='margin-top:60px;font-size:32px;color:%s'>Tek kelime ya da kısa ifade. En büyük çıkan kelimeyle bir sonraki derse başlıyorum.</div>" % (md(Q[W7]["q"]), C["soft"])),
      notes="Son kelime bulutu. Hangi konu kafanızı karıştırdı? En büyük çıkan kelimeyle hemen sonraki derse, tükürük bezlerine başlayacağım.")

L.add(title="Liderlik tablosu", dur=25, board=True,
      notes="Liderlik tablosu. İlk üçü alkışlayalım. Eşit puanda hızlı olan önde.")

L.add(title="Kaynaklar ve evde tekrar", dur=10,
      body=col(bl(["Neville BW, Damm DD, Allen CM, Chi AC. *Oral and Maxillofacial Pathology.* 5. baskı. Elsevier; 2024. Bölüm 12: Yumuşak doku tümörleri.",
                   "WHO Classification of Tumours Editorial Board. *Head and Neck Tumours.* 5. baskı. IARC; 2022. Bölüm 10 (yumuşak doku).",
                   "Laskaris G. *Color Atlas of Oral Diseases.* 4. baskı. Thieme; 2017. (Klinik fotoğraflar)",
                   "Kahyaoğlu Akkaya Z. Yumuşak doku hastalıkları patolojisi. Fakülte ders slaytı (sıra ve Neville'de olmayan konular)."], size=28, gap=14),
               div("<div style='display:flex;gap:34px;align-items:center;background:%s;border-radius:16px;padding:22px 28px;margin-top:18px'>"
                   "<img src='file://%s' style='width:190px;height:190px;border-radius:8px'>"
                   "<div style='font-size:30px;line-height:1.35'><b>Evde tekrar: slaytlar ve quiz (isteyen çözsün)</b><br>%s<br>"
                   "<span style='font:700 34px monospace;color:%s'>olgunak.github.io/lam-basinda/quiz</span></div></div>" % (C["lilac"], os.path.join(CANLI, "img", "quiz_qr.png"), "24 soru: Neville'in örnek sınav soruları, Türkçe, cevap açıklamalı.", C["pink"])),
               box("pink", None, html_="<div class='big' style='font-size:34px'>İlk üçü 24 Kasım'da burada anarım.</div>", style="padding:24px 34px;margin-top:18px")),
      notes="Kaynaklar burada. Evde tekrar için quiz: Neville'in örnek sınav soruları Türkçe, cevap açıklamalı; isteyen karekodu okutup çözsün. İlk üçü gelecek derste burada anarım. On dakika ara; sonra tükürük bezleri. Telefonlarınızı kapatmayın: aynı adla 'Sıradaki derse geç' düğmesi çıkacak.")

if __name__ == "__main__":
    only = set(int(x) for x in sys.argv[1:]) or None
    L.build(only)
