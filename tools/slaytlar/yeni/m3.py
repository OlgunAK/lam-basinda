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
    dict(t="Sigara ve alkol kullanmıyor", dur=14, note="Sigara ve alkol kullanmıyor. Fotoğrafa bakın ve tahmininizi telefondan girin; şıklar açık. Cevabı dersin sonunda açacağım."),
], size=38, vis_w=900, theme="dark", qopen=W1, cred=NEV)

L.add(title="Açılış vakası: tahminin ne?", dur=40, theme="dark", q=W1, cont=True, cred=NEV,
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

L.add(title="Hemanjiyom mu, vasküler malformasyon mu?", dur=65, strip={2}, dus=True, cred=NEV,
      body=row(col(ph(n("12.93"), "İnfantil hemanjiyom", "4 yaşında çocuk, üst dudak"), ph(n("12.94"), "Venöz malformasyon", "Dil, mor-mavi"), style="flex:0 0 520px"),
               col(div(table([["Doğumda", "Çoğu yok; ilk haftalarda çıkar", "Var"],
                              ["Seyir", "Hızlı büyür, sonra geriler: 5 yaşta %50, 9 yaşta %90", "Çocukla birlikte büyür, gerilemez"],
                              ["GLUT1", "Pozitif", "Negatif"],
                              ["Bastırınca", "Kan boşalmaz; sert, lastiksi", "Venöz olan kolayca söner"],
                              ["Tedavi", "Bekle; gerekirse propranolol", "Lazer, skleroterapi, embolizasyon"]],
                             size=25, head=["", "Hemanjiyom (tümör)", "Malformasyon"], w1=200)),
                   box("pink", None, ["**Dikkat:** tanısı konmamış kemik içi lezyonda biyopsiden ya da çekimden önce **iğne aspirasyonu** yap. Malformasyonun yanında diş çekiminden sonra ölümcül kanamalar bildirildi."],
                       size=25, style="padding:18px 26px"),
                   div("Sınıflama: ISSVA · vasküler tümör ile vasküler malformasyonu ayırır", GREY),
                   style="flex:1;gap:14px"), gap=30),
      notes="Damar lezyonlarında iki ayrı grup var; ISSVA sınıflaması bunları ayırır. Hemanjiyom bir tümör: çoğu doğumda yoktur, ilk haftalarda çıkar, hızla büyür, sonra geriler; yarısı beş yaşında, yüzde 90'ı dokuz yaşında kaybolur. GLUT1 pozitiftir; çoğunu bekleriz, gerekirse propranolol veririz. Malformasyon ise damar yapısının gelişim bozukluğu: doğumda vardır, çocukla birlikte büyür ve gerilemez; GLUT1 negatif. Venöz malformasyon mor-mavidir ve bastırınca kolayca söner. Neville'den pratik uyarı: tanısı konmamış kemik içi bir lezyonda biyopsiden önce iğneyle aspirasyon yapın; malformasyonun yanında diş çekiminden sonra ölümcül kanamalar bildirildi.")

L.add(title="Lenfanjiyom ve nazofarengeal anjiyofibrom", dur=60, strip={2}, dus=True, cred=NEV,
      body=col(row(ph(n("12.110"), "Dilde lenfatik malformasyon", "Kabarcıklı yüzey"), ph(n("12.109"), "Kistik higroma", pos="50% 30%"),
                   ph(n("12.106"), "Nazofarengeal anjiyofibrom", "BT: nazofarenkste kitle"), ph(n("12.108"), "Fibröz doku içinde ince duvarlı damarlar"), style="flex:1;min-height:320px"),
               row(box("lilac", "Lenfanjiyom (lenfatik malformasyon)", ["Neville 5 'lenfatik malformasyon' der; WHO 2022 'lenfanjiyom' adını korur",
                                                                        "Yarısı doğumda, %90'ı 2 yaşa kadar ortaya çıkar; %50–75'i baş-boyunda",
                                                                        "Ağızda en sık dilin ön ⅔'ü: dil büyür (makroglossi), yüzey kabarcıklı",
                                                                        "Boyunda büyük kistli formu kistik higroma: havayolunu tıkayabilir"],
                       size=24, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "Nazofarengeal anjiyofibrom", ["Neredeyse yalnız **ergen erkek** (10–17 yaş)", "Burun tıkanıklığı ve tekrarlayan burun kanaması",
                                                               "Androjen reseptörü pozitif fibroblastlar; damar duvarında kas eksik, elastik lif yok: **kolay kanar**",
                                                               "Ameliyattan önce embolizasyon; nüks %20–40; WHO 2022: sinonazal anjiyofibrom"],
                       size=24, gap=6, style="flex:1;padding:20px 24px"))),
      notes="İki damar lezyonu daha. Lenfanjiyom, Neville'in yeni baskısında lenfatik malformasyon adıyla geçiyor; WHO hâlâ lenfanjiyom diyor, ikisini de bilin. Yarısı doğumda vardır, yüzde 90'ı iki yaşına kadar ortaya çıkar. Ağızda en sık dilin ön üçte ikisinde; yüzey küçük, saydam kabarcıklarla kaplıdır ve dil büyür. Boyundaki büyük kistli formuna kistik higroma deniyor; yenidoğanda havayolunu tıkayabilir. Nazofarengeal anjiyofibrom neredeyse yalnız ergen erkeklerde görülür: burun tıkanıklığı ve tekrarlayan burun kanaması. Hücreleri androjen reseptörü taşır. Damar duvarlarında kas tabakası eksik ve elastik lif yok; bu yüzden ameliyatta çok kanar ve önce embolizasyon yapılır. WHO 2022'deki adı sinonazal anjiyofibrom.")

L.add(title="Kas kökenli iyi huylu tümörler ve diğerleri", dur=50, strip={2}, dus=True, cred=NEV,
      body=col(row(ph(n("12.115"), "Leiomiyom", "Sert damakta pembe-kırmızı nodül"), ph(n("12.118"), "Küt uçlu çekirdekli düz kas demetleri"),
                   ph(n("12.121"), "Erişkin rabdomiyom", "Yanakta kitle (ok)"), ph(n("12.123"), "Geniş eozinofilik sitoplazmalı poligonal hücreler"), style="flex:1;min-height:300px"),
               row(box("lilac", "Leiomiyom", ["Ağızda nadir; çoğu damar düz kasından", "Olguların ~%75'i **anjiyomiyom** (vasküler leiomiyom); bazen ağrılı",
                                              "%80'i dudak, dil, damak ve yanakta", "SMA+; Masson trikromda kırmızı; nüks etmez"],
                       size=23, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Rabdomiyom", ["Erişkin tip: orta-ileri yaş, **%80 erkek**; ağız tabanı, yumuşak damak, dil kökü",
                                               "Sitoplazmada vakuoller: **örümcek ağı** görünümü; çapraz çizgilenme",
                                               "Fetal tip: çocukta, yüz ve kulak çevresi; rabdomiyosarkom sanılabilir"],
                       size=23, gap=6, style="flex:1;padding:18px 22px"),
                   box("rose", "Tek satır", ["**Paragangliom:** en sık karotis cisimciği; hücre yuvaları (zellballen); %30–40 kalıtsal",
                                             "**Tendon kılıfının dev hücreli tümörü:** resmi slaytta var, ağızda çok nadir; Neville'de yok"],
                       size=23, gap=8, style="flex:1;padding:18px 22px"))),
      notes="İyi huylu tümörlerin sonuncusu kas. Leiomiyom düz kas tümörü; ağızda nadir ve çoğu damar duvarındaki düz kastan köken alır: dörtte üçü anjiyomiyom. Dudak, dil, damak ve yanakta görülür; anjiyomiyom ağrılı olabilir. Mikroskopta küt uçlu, puro biçimli çekirdekler ve SMA pozitifliği. Rabdomiyom çizgili kas tümörü: erişkin tip orta ve ileri yaşta, büyük çoğunluğu erkekte; ağız tabanında, yumuşak damakta, dil kökünde. Hücrelerin sitoplazması vakuollüdür, örümcek ağı gibi görünür. Çocuktaki fetal tipi rabdomiyosarkomla karışabilir. Sağda iki tek satır: paragangliom en sık karotis cisimciğinde, hücreler yuvalar yapar; tendon kılıfının dev hücreli tümörü resmi slaytta var ama ağızda çok nadir.")

# ---- 3. Sarkomlar ----
L.add(title="Sarkomlar: ortak özellikler", dur=40, strip={3}, dus=True,
      body=row(col(box("navy", "Genel", ["Ağız-çene bölgesi kanserlerinin **%1'inden azı** (Neville)", "Lokal agresif büyür; önce çevre dokuyu yıkar",
                                         "Lenf nodu metastazı az; uzak metastaz en sık **akciğere**",
                                         "Baş-boyunda geniş cerrahi sınır zor: yerel nüks sık"], size=36, gap=26, style="padding:24px 30px"), style="flex:1"),
               col(box("lilac", "Risk etkenleri", ["Baş-boyuna radyoterapi öyküsü (çoğu >10 yıl önce)", "Kronik travma, yanık skarı, metal implant",
                                                   "Kalıtsal: nörofibromatozis, retinoblastom"], size=33, gap=18, style="padding:22px 28px"),
                   box("lilac", "Davranışı belirleyen", ["Histolojik tip ve derece, boyut, derinlik, evre", "Tümörün tam çıkarılıp çıkarılamadığı ve cerrahi sınır"],
                       size=33, gap=18, style="padding:22px 28px"), style="flex:1;gap:18px"), gap=30),
      notes="Üçüncü grup: sarkomlar, yumuşak dokunun kötü huylu tümörleri. Ağız ve çene bölgesinde nadirdir; Neville'e göre bu bölgedeki kanserlerin yüzde birinden azı. Lokal agresif büyür, önce çevre dokuyu yıkar. Karsinomların aksine lenf noduna az gider; uzak metastaz en sık akciğere. Risk etkenleri: yıllar önce alınmış radyoterapi, kronik travma, yanık skarı, metal implant ve kalıtsal hastalıklar, özellikle nörofibromatozis. Davranışını tipi, derecesi, boyutu, evresi ve cerrahi sınır belirler. Baş-boyunda geniş sınır bırakmak zor olduğu için yerel nüks sık.")

L.add(title="Pleomorfik sarkom, fibrosarkom, liposarkom", dur=60, strip={3}, dus=True, cred=NEV,
      body=col(row(ph(n("12.131"), "İndiferansiye pleomorfik sarkom", "Belirgin pleomorfizm, mitozlar"), ph(n("12.129"), "Fibrosarkom", "Çocukta damak ve alveol kretinde kitle"),
                   ph(n("12.132"), "Liposarkom", "Vakuollü lipoblastlar"), style="flex:1;min-height:300px"),
               row(box("lilac", "İndiferansiye pleomorfik sarkom", ["Eski adı malign fibröz histiyositom", "Yaşlı; ekstremite ve derin gövde; baş-boyunda sinonazal",
                                                                     "Baş-boyundakilerin bir kısmı radyoterapiden sonra", "Storiform demetler + pleomorfik dev hücreler", "Yerel nüks %40; 5 yıl sağkalım %52–55"],
                       size=23, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Fibrosarkom", ["Baş-boyunda olguların %10–19'u; burun ve sinüslerde", "Yavaş büyür; radyoterapiden sonra gelişebilir",
                                                "**Balık kılçığı** (herringbone) deseninde iğsi hücreler; dışlama tanısı", "Çocukta infantil fibromatozisten ayırmak zor", "Nüks yarısında"],
                       size=23, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Liposarkom", ["Baş-boyunda %3; ort. 57 yaş; en sık boyun, ağızda **dil ve yanak**", "Ağızdakilerin %67'si **iyi diferansiye** (atipik lipomatöz tümör)",
                                               "Lipoblastlar, atipik iğsi hücreler; **MDM2/CDK4**+", "Ağızdakiler iyi seyirli; nüks %15–20"],
                       size=23, gap=6, style="flex:1;padding:18px 22px")),
               box("yellow", None, ["**En sık sarkom hangisi?** Resmi slayt: pleomorfik sarkom, ikinci liposarkom. Neville 5: eskiden malign fibröz histiyositom en sık tanıydı; bu tümörlerin çoğu başka sarkomlara ayrıldı, bugün **liposarkom** en sık kabul ediliyor."],
                   size=23, style="padding:16px 24px")),
      notes="Lif ve yağ kökenli sarkomlar. İndiferansiye pleomorfik sarkom, eski adıyla malign fibröz histiyositom: yaşlı hastada, daha çok bacakta ve gövdede; baş-boyunda burun ve sinüslerde. Bir kısmı radyoterapiden yıllar sonra gelişir. Mikroskopta girdap gibi demetler ve tuhaf, çok çekirdekli dev hücreler. Fibrosarkom bugün bir dışlama tanısı: iğsi hücreler balık kılçığı deseninde dizilir. Liposarkom ağızda en sık dilde ve yanakta; ağızdakilerin üçte ikisi iyi diferansiye tip, lipoma benzer ama lipoblast ve atipik hücreler içerir; MDM2 ve CDK4 pozitif. Bir uyuşmazlık: resmi slayt en sık sarkom olarak pleomorfik sarkomu sayıyor. Neville 5'e göre bu eski bir bilgi; malign fibröz histiyositom denen tümörlerin çoğu başka sarkomlara ayrıldı ve bugün en sık sarkom liposarkom.")

L.add(title="Sinir ve damar kökenli sarkomlar", dur=65, strip={3}, dus=True, cred=NEV,
      body=col(row(ph(n("12.71"), "Malign periferik sinir kılıfı tümörü", "NF1'li hastada yanak"), ph(n("12.134"), "Olfaktör nöroblastom", "Küçük, bazofilik hücreler"),
                   ph(n("12.136"), "Anjiyosarkom", "Atipik endotelle döşeli kanallar"), ph(n("7.42"), "Kaposi sarkomu", "HIV; sert damakta nodüler büyüme"), style="flex:1;min-height:290px"),
               row(box("lilac", "MPNST (malign schwannom)", ["Sarkomların %5–10'u; **¼–½'i NF1'li** hastada", "Genç erişkin; ağızda çene, dudak, yanak",
                                                             "Dalgalı çekirdekli atipik iğsi hücreler; hücreden zengin ve fakir alanlar", "S100/SOX10 yalnız %50–60; prognoz kötü"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"),
                   box("lilac", "Olfaktör nöroblastom", ["Burun tavanı, kribriform plak; **erişkin** (ort. 45–56 yaş)", "Burun tıkanıklığı, kanama, koku kaybı",
                                                         "Küçük yuvarlak mavi hücreler; **rozet**, psödorozet; kromogranin, sinaptofizin+", "5 yıl sağkalım ~%75"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"),
                   box("lilac", "Anjiyosarkom", ["Sarkomların %1'i; yarısı baş-boyunda: en sık **saçlı deri ve alın**", "Ağızda çok nadir: diş eti, dil",
                                                 "Erken lezyon morluk gibi görünür", "Anastomoz yapan atipik damarlar; CD31, ERG+"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"),
                   box("lilac", "Kaposi sarkomu", ["**HHV-8**; dört form: klasik, endemik, iatrojenik (nakil), AIDS", "AIDS'li hastaların ~%70'inde ağız lezyonu; en sık sert damak",
                                                   "İğsi hücreler, yarık benzeri damarlar, ekstravaze eritrositler", "Klasik form: yaşlı erkek, bacak"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"))),
      notes="Sinir ve damar sarkomları. Malign periferik sinir kılıfı tümörü, eski adıyla malign schwannom: dörtte biri ile yarısı NF1'li hastalarda gelişir; bu yüzden NF1'de büyüyen bir kitle hemen biyopsi ister. Prognozu kötü. Olfaktör nöroblastom burun tavanında, koku epitelinden köken alır; adındaki nöroblastoma rağmen çocukta değil erişkinde görülür. Mikroskopta küçük, yuvarlak, mavi hücreler ve rozetler. Anjiyosarkom yaşlıda en sık saçlı deride ve alında; ağızda çok nadir. Erken dönemde morluk gibi görünür, bu yüzden tanı gecikir. Kaposi sarkomu HHV-8 ile ilişkili; dört formu var. Resmi slayt endemik formu HIV ve HHV-8 ile ilişkilendiriyor; Neville'e göre dört formun hepsinin etkeni HHV-8, HIV yalnız AIDS formunda. AIDS'li hastaların yaklaşık yüzde 70'inde ağız lezyonu olur, en sık sert damakta.")

L.add(title="Kas kökenli sarkomlar ve diğerleri", dur=65, strip={3}, dus=True, cred=NEV,
      body=col(row(ph(n("12.140"), "Leiomiyosarkom", "Üst alveol kretinde ülserli kitle"), ph(n("12.142"), "Embriyonal rabdomiyosarkom", "Çocukta maksillada kitle"),
                   ph(n("12.146"), "Sinovyal sarkom", "İğsi hücreler ve bez benzeri yapılar"), ph(n("12.147"), "Alveoler yumuşak doku sarkomu"), style="flex:1;min-height:290px"),
               row(box("lilac", "Leiomiyosarkom", ["Sarkomların %5–10'u; ağızda nadir, **⅓'ü alt çenede**", "Puro biçimli çekirdekli iğsi hücreler", "≥5 mitoz/10 BBA: malign kabul",
                                                   "SMA, desmin, h-kaldesmon+; akciğere metastaz"], size=22, gap=5, style="flex:1;padding:16px 20px"),
                   box("lilac", "Rabdomiyosarkom", ["Çocuk yumuşak doku sarkomlarının **yarısı**; en sık baş-boyun (%26)", "Embriyonal %60 (ilk 10 yıl), alveoler %30, pleomorfik <%5",
                                                    "Ağız içinde en sık **damak**; küçük yuvarlak hücreler; desmin, miyogenin+", "5 yıl: embriyonal %63, alveoler %35"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"),
                   box("lilac", "Sinovyal sarkom", ["Sarkomların %5–10'u; eklem çevresinde ama **sinovyadan köken almaz**", "Baş-boyunda parafarenks; ağızda dil, yanak, yumuşak damak",
                                                    "Bifazik (iğsi + epitelyal) ya da monofazik; **SS18::SSX**", "Ort. 33 yaş; nüks ve metastaz sık"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"),
                   box("lilac", "Alveoler yumuşak doku sarkomu", ["Sarkomların %0,5–1'i; 15–35 yaş", "Çocukta baş-boyun: **orbita ve dil**",
                                                                  "Alveol benzeri yuvalar; PAS+, diastaza dirençli kristaller", "TFE3+; geç metastaz"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"))),
      notes="Son sarkom grubu. Leiomiyosarkom düz kas sarkomu; ağızda nadir, üçte biri alt çenede. Çekirdekler puro biçimli; on büyük büyütme alanında beş ya da daha fazla mitoz varsa malign kabul edilir. Rabdomiyosarkom çocukların sarkomu: çocukluk çağı yumuşak doku sarkomlarının yarısı, en sık baş-boyunda. Üç tipi var: embriyonal en sık ve ilk on yaşta, alveoler ergenlik ve gençlikte, pleomorfik erişkinde. Ağız içinde en sık damakta. Sinovyal sarkom eklem çevresinde görülür ama adına rağmen sinovyadan köken almaz; baş-boyunda en sık parafarenkste. Resmi slayt genellikle bifazik olduğunu söylüyor; Neville'e göre monofazik tip daha sık. Tanıyı SS18::SSX füzyonu koydurur. Alveoler yumuşak doku sarkomu nadir; çocukta en sık orbitada ve dilde; hücrelerde PAS pozitif kristaller görülür.")

# ---- Vakaya dönüş ----
L.add(title="Açılış vakası: biyopsi sonucu", dur=35, theme="dark", tag=("pink", "VAKAYA DÖNÜŞ"), cred=NEV,
      body=row(div(bl(["42 yaşında kadın; dil sırtında 1 cm, ağrısız, sarımsı nodül",
                       "Yüzeysel insizyonel biyopsi yapıldı",
                       "Rapor: **yüzeyde psödoepitelyomatöz hiperplazi; invaziv karsinom dışlanamadı**"], size=36, gap=28), "flex:0 0 860px"),
               col(ph(n("12.87"), "Biyopsi: epitelde aşağı uzanan dallar", style="height:420px"),
                   box("yellow", None, html_="<div class='big' style='font-size:38px'>Karsinom mu? Tahminin değişti mi?</div>", style="padding:44px 36px"),
                   style="flex:1"), gap=40),
      notes="Hastamıza yüzeysel bir biyopsi yapıldı. Rapor: yüzeyde psödoepitelyomatöz hiperplazi, invaziv karsinom dışlanamadı. Epitel aşağı doğru dallar yapıyor ve bu görüntü karsinoma benziyor. Şimdi tahmininizi yenileyin; sıradaki slaytta ilk tahminle karşılaştıracağız.")

L.add(title="Vakaya dönüş: şimdi ne diyorsun?", dur=40, theme="dark", q=W6, cred=NEV,
      body=qbody(Q[W6], photo=ph(n("12.87"), "Yüzeysel biyopsi")),
      notes="Aynı soru, aynı şıklar. Dersin başındaki dağılımı hatırlayın. (İki sonucu yan yana göster.)")

L.add(title="Tanı: granüler hücreli tümör", dur=60, cred=NEV,
      body=row(div(steps([("Yer", "Dil sırtı: granüler hücreli tümörün en sık yeri; ağız kanserinin olağan yeri değil"),
                          ("Klinik", "Ağrısız, sert, sarımsı nodül; kadın, 4.–6. dekat"),
                          ("Yüzeysel biyopsi", "Psödoepitelyomatöz hiperplazi: karsinoma benzer"),
                          ("Derin biyopsi", "İri, poligonal, granüler sitoplazmalı hücreler; S100+, PAS+"),
                          ("Yönetim", "Konservatif eksizyon; nüks nadir")], size=28), "flex:0 0 1060px"),
               col(ph(n("12.86"), "Derin biyopsi: granüler hücreler", style="flex:1"),
                   pato("Yüzeysel biyopsi tuzağı", "Neville: psödoepitelyomatöz hiperplazi bazen o kadar belirgindir ki karsinom tanısı konup **gereksiz kanser ameliyatı** yapılabilir. Dil sırtındaki nodülde biyopsiyi **derin al**, istek formuna yeri ve kliniği yaz.",
                        size=23, style="padding:18px 22px 18px 26px"), style="flex:1;gap:16px")),
      notes="Kanıtları sırayla koyalım. Yer: dil sırtı; granüler hücreli tümörün en sık yeri, ama ağız kanserinin olağan yeri değil. Klinik: ağrısız, sert, sarımsı nodül, orta yaşta kadın. Yüzeysel biyopsi epitelin aşağı uzanan dallarını gösterdi; buna psödoepitelyomatöz hiperplazi diyoruz ve karsinoma çok benzer. Derin biyopsi altındaki asıl tümörü gösterdi: iri, granüler sitoplazmalı hücreler, S100 ve PAS pozitif. Patoloğun notu: Neville bu görüntü yüzünden karsinom tanısı konup gereksiz kanser ameliyatı yapılan hastalardan söz ediyor. Dil sırtındaki bir nodülde biyopsiyi derin alın ve istek formuna yeri ve kliniği yazın. Tedavi konservatif eksizyon; nüks nadir.")

L.add(title="Eski ad, yeni ad ve resmi slaytta olmayanlar", dur=40, optional=True,
      body=row(col(box("lilac", "Eski ad → güncel ad", None, html_=table([
                       ["Malign fibröz histiyositom", "İndiferansiye pleomorfik sarkom"],
                       ["Hemanjiyoperisitom", "Soliter fibröz tümör"],
                       ["Malign schwannom", "Malign periferik sinir kılıfı tümörü"],
                       ["Estezyonöroblastom", "Olfaktör nöroblastom"],
                       ["Nazofarengeal anjiyofibrom", "Sinonazal anjiyofibrom (WHO 2022)"],
                       ["Lenfanjiyom", "Lenfatik malformasyon (Neville 5; WHO hâlâ lenfanjiyom)"],
                       ["Nodüler fasiitis", "WHO 2022: kendiliğinden geçen neoplazi (USP6)"]], size=26, w1=380), style="padding:22px 26px"), style="flex:1"),
               col(box("rose", "Neville 12. bölümde var, resmi slaytta yok", ["**Diş etinin reaktif lezyonları:** piyojenik granülom, periferik dev hücreli granülom, periferik ossifiye fibrom, fibrom",
                                                                            "**Protez hiperplazileri:** epulis fissuratum, inflamatuvar papiller hiperplazi",
                                                                            "**MEN 2B**, bebeğin melanotik nöroektodermal tümörü, Sturge-Weber",
                                                                            "**Ağız yumuşak dokusuna metastaz:** en sık diş eti"], size=30, gap=22, style="padding:22px 26px"),
                   div("Bunlar quizde var; isteyen oradan çalışsın.", GREY), style="flex:1;gap:10px")),
      notes="Zaman kalırsa; yoksa atlayın. Solda adı değişen tümörler; sınavda iki adı da görebilirsiniz. Sağda Neville'in bu bölümünde olup resmi slaytımızda olmayan konular: diş etinin reaktif lezyonları, protez hiperplazileri, MEN 2B, metastazlar. Bunlar quizde var; isteyen oradan çalışsın.")

L.add(title="Çıkış bileti", dur=40, theme="dark", q=W7,
      body=div("<div class='live'>CANLI · W7 · Kelime bulutu</div><div class='qq' style='font-size:56px;margin-top:60px;max-width:1500px'>%s</div>"
               "<div style='margin-top:60px;font-size:32px;color:%s'>Tek kelime ya da kısa ifade. En büyük çıkan kelimeyle bir sonraki derse başlıyorum.</div>" % (md(Q[W7]["q"]), C["soft"])),
      notes="Son kelime bulutu. Hangi konu kafanızı karıştırdı? En büyük çıkan kelimeyle hemen sonraki derse, tükürük bezlerine başlayacağım.")

L.add(title="Liderlik tablosu", dur=25, board=True,
      notes="Liderlik tablosu. İlk üçü alkışlayalım. Eşit puanda hızlı olan önde.")

L.add(title="Kaynaklar ve evde tekrar", dur=15,
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
