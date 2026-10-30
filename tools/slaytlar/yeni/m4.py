# -*- coding: utf-8 -*-
"""M4 · Tükürük Bezi Hastalıkları ve Tümörleri (17 Kasım 2026, blok dersin ikincisi, 25 dk).

Sıra fakültenin resmi ders slaytını izler (9. hafta, Tükürük Bezi Hastalıkları
Patolojisi): genel bilgi, tümör dışı hastalıklar, iyi huylu tümörler, kötü
huylu tümörler. Rakamlar Neville 5 ve WHO 2022'den; Neville'de ayrıntısı
olmayan konular (ektopi, lenfoepitelyal kist, duktus karsinomu, lenfoepitelyal
karsinom, epitelyal-miyoepitelyal karsinom) resmi slayttan. Neville'de olup
resmi slaytta olmayan mukosel, ranula ve sialadenoz birer cümleyle eklendi.
Bütün içerik slaytları adım adım açılır (seq).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import *
from foto import F

NEV = "Neville ve ark., *Oral and Maxillofacial Pathology*, 5. baskı (Elsevier, 2024)"
LAS = "Laskaris, *Color Atlas of Oral Diseases*, 4. baskı (Thieme, 2017)"
RESMI = "Fakültenin resmi ders slaytı (Z. Kahyaoğlu Akkaya)"
IKI = "Neville 5. baskı (2024) · fakültenin resmi ders slaytı"
n = lambda k, **kw: F("n", k, **kw)
l = lambda k, **kw: F("l", k, **kw)
r = lambda f: os.path.join(HERE, "resmi", f)

L = Lesson("M4", "Tükürük Bezi Hastalıkları ve Tümörleri", "Tükürük Bezi Hastalıkları", "17 Kasım 2026", ver="5",
           frame="Üç grup: tümör dışı hastalıklar, iyi huylu tümörler, kötü huylu tümörler",
           quiz="../quiz/#tb",
           strip=("Üç grup", ["1 Tümör dışı", "2 İyi huylu", "3 Kötü huylu"]),
           cta="24 Kasım'a kadar isteyen Neville'in örnek sorularını Türkçe quiz olarak çözsün: olgunak.github.io/lam-basinda/quiz. İlk üçü gelecek derste burada anarım.")

IMG = os.path.join(CANLI, "img")
def S(title, items, **kw):
    for it in items:                      # adım süreleri dersi 25 dakikaya tamamlar
        it["dur"] = int(round(it["dur"] * 1.18))
    seq_slide(L, title, items, **kw)


def P(src, cap=None, sub=None, **kw):
    return ph(src, cap, sub, style="flex:1", **kw)


def save(src, name):
    from PIL import Image
    Image.open(src).convert("RGB").save(os.path.join(IMG, name), quality=88)
    return "img/" + name


def bars(rows, size=30, upto=99):
    """Malign oranı çubukları (0–100): (etiket, alt, üst, not, vurgu). upto: kaçıncı satıra kadar görünür."""
    out = ["<div style='flex:1;display:flex;flex-direction:column;justify-content:center;gap:%dpx;background:#fbf8fc;border-radius:16px;padding:30px'>" % int(size * 1.3),
           "<div style='font:700 30px Lora;color:%s'>Tümörün kötü huylu olma olasılığı</div>" % C["purple"]]
    for i, (lab, lo, hi, note, hot) in enumerate(rows):
        col_ = C["pink"] if hot else C["purple"]
        vis = "" if i <= upto else "visibility:hidden;"
        out.append(
            "<div style='%sdisplay:flex;flex-direction:column;gap:8px'>"
            "<div style='font:700 %dpx Lato;color:%s'>%s <span style='font-weight:400;color:%s;font-size:%dpx'>· %s</span></div>"
            "<div style='height:%dpx;background:%s;border-radius:12px;position:relative'>"
            "<div style='position:absolute;left:%g%%;width:%g%%;top:0;bottom:0;background:%s;border-radius:10px'></div>"
            "<div style='position:absolute;%s;top:50%%;transform:translateY(-50%%);font:900 %dpx Lato;color:%s;white-space:nowrap'>%%%d–%d</div></div></div>" % (
                vis, size, col_, E(lab), C["grey"], size - 6, md(note), int(size * 1.9), C["lilac"], lo, hi - lo, col_,
                ("left:calc(%g%% + 14px)" % hi) if hi < 70 else ("left:calc(%g%% + 14px)" % lo), size, col_ if hi < 70 else "#fff", lo, hi))
    out.append("</div>")
    return "".join(out)


BARS = [("Parotis", 15, 32, "tümörlerin %61–80'i", False), ("Submandibuler", 26, 45, "tümörlerin ~%10'u", False),
        ("Küçük bezler", 38, 54, "en sık damak", True), ("Sublingual", 70, 97, "nadir", True)]

# ---------------- questions ----------------
VAKA_OPTS = ["Pleomorfik adenom", "Mukoepidermoid karsinom", "Adenoid kistik karsinom", "Polimorf adenokarsinom", "Nekrotizan sialometaplazi"]
W1 = L.q(id="W1", type="POLL", label="Açılış vakası: tahminin ne?", q="Bu hastada en olası tanı ne?", scored=False,
         img=save(n("11.38"), "m4_vaka.jpg"), opts=VAKA_OPTS, hide=True)
W2 = L.q(id="W2", type="MCQ", label="Sjögren: puanla", scored=True,
         q="Ağız ve göz kuruluğu yakınması olan kadın. Dudak biyopsisinde odak skoru 1,5/4 mm²; anti-SSA/Ro negatif; Schirmer 4 mm/5 dk. ACR/EULAR 2016'ya göre?",
         opts=["Toplam 4: primer Sjögren sınıflamasına girer", "Toplam 3: girmez; anti-SSA olmadan olmaz", "Toplam 2: girmez",
               "Toplam 5: girer", "Biyopsi tek başına yeter; puan hesaplanmaz"], a=0,
         exp="Biyopsi (odak skoru ≥1) 3 puan + Schirmer ≤5 mm/5 dk 1 puan = 4. Anti-SSA negatif olsa da eşik aşıldı. Önce dışlama ölçütlerine bak: IgG4 ilişkili hastalık, baş-boyun radyoterapisi, aktif HCV, AIDS, sarkoidoz, amiloidoz, GVHD.")
W3 = L.q(id="W3", type="MCQ", label="DUS Molası 1/2", scored=True,
         q="Mukosel en az hangi bölgede görülür?",
         opts=["Yanak mukozası", "Ağız tabanı", "Alt dudak", "Üst dudak", "Dilin ventral yüzü"], a=3,
         exp="1715 mukoselin %82'si alt dudakta, üst dudakta hiç yok. Tümörlerde tablo ters: üst dudak tümörü sık, alt dudak tümörü nadir. Üst dudakta 'mukosel' gören, tümörü düşünür.")
W4 = L.q(id="W4", type="MCQ", label="DUS Molası 2/2", scored=True,
         q="Sjögren sendromlu hastalarda hangi tümörün gelişme riski artmıştır?",
         opts=["Asinik hücreli karsinom", "Hepatoselüler karsinom", "Kaposi sarkomu", "Lenfoma", "Melanom"], a=3,
         exp="Yaşam boyu lenfoma riski %5–10, genel nüfusun 15–20 katı; çoğu MALT lenfoması. Kalıcı parotis büyümesi, lenfadenopati, düşük C4 ve kriyoglobulinemi uyarı işaretleri.")
W5 = L.q(id="W5", type="MCQ", label="Üst dudakta nodül", scored=True,
         q="Yetmiş yaşında kadın. Üst dudak mukozasında 1 cm, mavimsi, yavaş büyüyen, ağrısız nodül. En olası tanı?",
         opts=["Mukosel", "Kanaliküler adenom", "Mukoepidermoid karsinom", "Fibrom", "Adenoid kistik karsinom"], a=1,
         exp="Üst dudakta mukosel neredeyse hiç olmaz; yaşlı hastada üst dudak nodülü kanaliküler adenomdur (%66–78'i üst dudakta). Üst dudak tümörlerinin yalnız %9–25'i malign; nedeni kanaliküler adenomun sıklığı.")
W6 = L.q(id="W6", type="MATCH", label="Tümör ve gen", scored=True,
         q="Her tümörü kendi gen değişikliğiyle eşleştir.",
         left=["Pleomorfik adenom", "Mukoepidermoid karsinom", "Adenoid kistik karsinom", "Sekretuar karsinom"],
         right=["MYB::NFIB", "ETV6::NTRK3", "PLAG1 / HMGA2", "CRTC1/3::MAML2"],
         key=["PLAG1 / HMGA2", "CRTC1/3::MAML2", "MYB::NFIB", "ETV6::NTRK3"],
         exp="Pleomorfik adenom PLAG1 ya da HMGA2; mukoepidermoid karsinom MAML2 füzyonu; adenoid kistik karsinom MYB::NFIB; sekretuar karsinom ETV6::NTRK3. Patolog küçük biyopside tanıyı bu genlerle doğrular.")
W7 = L.q(id="W7", type="POLL", label="Vakaya dönüş: şimdi ne diyorsun?", q="Dersin başındaki hasta damakta karıncalanma ve uyuşma tarifliyor. Şimdi en olası tanı?",
         scored=False, img="img/m4_vaka.jpg", opts=VAKA_OPTS, a=2, compare="W1")
W8 = L.q(id="W8", type="WORDCLOUD", label="Çıkış bileti", q="Bugün en çok kafanı karıştıran konu hangisiydi? (Tek kelime ya da kısa ifade)", scored=False)
Q = L.qmap

# ---------------- slides ----------------
L.add(title="Tükürük Bezi Hastalıkları ve Tümörleri", dur=60, lobby=True, nonum=True, raw=title_page(
    "4. Sınıf Patoloji  ·  Diş Hekimliği", "Tükürük Bezi Hastalıkları ve Tümörleri", "Tümör dışı hastalıklar, iyi huylu ve kötü huylu tümörler",
    "17 Kasım 2026  ·  Uzm. Dr. M. Olgun Ak", "45 yaşında kadın, sert damakta iki yıldır büyüyen ağrısız kitle.", n("11.77"), NEV),
    notes="Sağdaki görüntü bugünün tümörlerinden birinin mikroskobu; dersin ortasında adını söyleyeceğim. Katılım ekranı bu slaytta açık. İlk dersten gelenler telefondaki 'Sıradaki derse geç' düğmesine dokunur; tekrar kod okutmak gerekmez. Yeni gelenler için kod perdede. Herkes girince L ile kapatıp başlıyoruz.")

L.add(title="Geçen dersin çıkış bileti", dur=20, cloud={"q": "W7", "from": "prev"},
      notes="Az önceki dersin sonunda en çok kafa karıştıran konuyu sormuştum; en büyük kelime bu. (Bir cümleyle cevapla.) Şimdi tükürük bezleri.")

VAKA_V = col(row(ph(n("11.38"), "Sert damak, lateral", style="flex:1"), qmark(), style="flex:1"),
             box("yellow", None, html_="<div class='big' style='font-size:38px'>Tahminini telefondan gir. Cevap dersin sonunda.</div>", style="padding:36px 32px"),
             style="flex:1")
S("Açılış vakası: damakta kitle", [
    dict(t="45 yaşında kadın", v=VAKA_V, dur=8, note="Hastamız 45 yaşında bir kadın."),
    dict(t="Sert damakta, orta hattın yanında kitle", dur=10, note="Sert damakta, orta hattın yanında bir kitle var."),
    dict(t="İki yıldır yavaş büyüyor; ağrısız", dur=10, note="İki yıldır yavaş büyüyor ve ağrımıyor."),
    dict(t="Üstündeki mukoza sağlam, ülser yok", dur=10, note="Üstündeki mukoza sağlam, ülser yok."),
    dict(t="Sert, lastiksi; kemiğe yapışık değil", dur=12, note="Sert, lastiksi kıvamda; kemiğe yapışık değil. Tahmininizi telefondan girin; cevabı dersin sonunda açacağım."),
], size=38, vis_w=900, theme="dark", qopen=W1, cred=NEV)

L.add(title="Açılış vakası: tahminin ne?", dur=35, theme="dark", q=W1, cont=True, cred=NEV,
      body=qbody(Q[W1], photo=ph(n("11.38"))),
      notes="Dağılımı gösteriyorum, yorum yok. Beş şıktan biri tümör değil, biri iyi huylu, üçü kötü huylu. Dersin sonunda hastanın söylemediği bir şikâyeti öğreneceğiz.")

PLAN = [box("navy", "1 · Tümör dışı hastalıklar", ["Gelişim bozuklukları: aplazi, hipoplazi, ektopi", "Mukosel, ranula, kanal kisti", "Taş ve sialadenitler",
                                                    "Sialore ve kserostomi", "Lenfoepitelyal sialadenit, Sjögren", "Nekrotizan sialometaplazi", "Lenfoepitelyal kistler"], size=29, gap=10, style="flex:1"),
        box("lilac", "2 · İyi huylu tümörler", ["Pleomorfik adenom", "Warthin tümörü", "Onkositom", "Bazal hücreli adenom", "Kanaliküler adenom"], size=30, gap=12, style="flex:1"),
        box("rose", "3 · Kötü huylu tümörler", ["Mukoepidermoid karsinom", "Adenoid kistik karsinom", "Asinik hücreli ve sekretuar karsinom", "Polimorf adenokarsinom",
                                                "Karsinom ex pleomorfik adenom", "Bazal hücreli adenokarsinom, duktus karsinomu, diğerleri"], size=29, gap=10, style="flex:1"),
        box("yellow", None, ["Her hastalıkta aynı dört soru: **hangi bez**, **kaç yaşında**, **ağızda nerede**, **mikroskopta ne görülür**."], size=28, style="padding:20px 30px")]


def plan_body(k):
    hid = lambda i: div(PLAN[i], "display:flex;flex-direction:column;flex:1;%s" % ("" if i <= k else "visibility:hidden"))
    return col(row(*[hid(i) for i in range(3)], style="flex:1"), hid(3))


L.add(title="Dersin planı: üç grup", body_fn=plan_body, seq=[
    dict(dur=10, note="Ders fakültemizin resmi slaytıyla aynı sırada. Birinci grup tümör dışı hastalıklar: gelişim bozuklukları, kistler, taş, iltihap, otoimmün hastalıklar."),
    dict(dur=8, note="İkinci grup iyi huylu tümörler; en sık olanı pleomorfik adenom."),
    dict(dur=8, note="Üçüncü grup kötü huylu tümörler; en sık olanı mukoepidermoid karsinom."),
    dict(dur=9, note="Her hastalıkta aynı dört soruyu soracağız: hangi bez, kaç yaşında, ağızda nerede, mikroskopta ne var. Rakamlar Neville 5 ve WHO 2022'den.")])

# ---- 1. Tümör dışı ----
S("Tükürük bezleri: yapı ve salgı", [
    dict(t="Majör bezler: parotis, submandibuler, sublingual; ayrıca yüzlerce küçük bez", v=P(r("tb_uc_bez.jpg"), "Üç majör bezin mikroskobu"), dur=7,
         note="Önce kısa bir hatırlatma. Üç çift majör bez var: parotis, submandibuler ve sublingual; ayrıca ağız ve orofarenkste yüzlerce küçük bez."),
    dict(t="Günde yaklaşık 1 litre tükürük; sabah az, akşamüstü çok", dur=5, note="Günde yaklaşık bir litre tükürük üretilir; sabah az, akşamüstü çoktur."),
    dict(t="Asinus: seröz, müköz ya da karışık; dışında miyoepitel hücreleri", v=P(r("tb_sema.jpg"), "Asinus, kanallar, miyoepitel"), dur=7,
         note="Salgı birimi asinus: seröz, müköz ya da karışık olabilir. Asinusu ve ara kanalı miyoepitel hücreleri sarar; kasılarak salgıyı iter. Tümörlerin çoğu bu iki hücreden çıkar."),
    dict(t="Parotis: saf seröz; Stensen kanalı üst 2. büyük azı hizasında açılır", dur=6, note="Parotis en büyük bez, saf seröz salgı yapar; Stensen kanalı üst ikinci büyük azı hizasında açılır."),
    dict(t="Submandibuler: karışık; Wharton kanalı dil altında, frenulumun yanında", dur=6, note="Submandibuler bez karışık salgı yapar; Wharton kanalı dil altında, frenulumun yanında açılır."),
    dict(t="Sublingual ve küçük bezler: çoğu müköz", dur=5, note="Sublingual bez ve küçük bezlerin çoğu müköz salgı yapar."),
], size=32, gap=10, cred=RESMI)

S("Gelişim bozuklukları: aplazi, hipoplazi, ektopi", [
    dict(h="Aplazi, hipoplazi", t="Bezin hiç olmaması ya da az gelişmesi; erkekte 2 kat", v=P(n("11.1"), "Aplazi: kuru, deri gibi dil; mine erozyonu"), dur=8,
         note="Aplazide bez hiç yoktur, hipoplazide az gelişmiştir; nadir ve erkekte iki kat sık. Treacher Collins gibi sendromlarla birlikte olabilir."),
    dict(t="Sonuç: ağır kuruluk, çürük ve diş erozyonu", dur=6, note="Sonuç ağır ağız kuruluğu: dil deri gibi olur, çürük ve diş erozyonu artar."),
    dict(h="Ektopi", t="Bez dokusu başka yerde; en sık lenf nodunda", v=P(r("tb_ektopi.jpg"), "Lenf nodunda tükürük bezi dokusu"), dur=8,
         note="Ektopide tükürük bezi dokusu normal yeri dışında bulunur; en sık boyundaki lenf nodlarının içinde. Mandibulada kemik içinde de olabilir."),
    dict(t="Ektopik bezden de kist ve tümör gelişebilir", dur=6, note="Ektopik bezden de normal bezde olduğu gibi kist ve tümör gelişebilir."),
], strip={1}, cred=IKI)

S("Mukosel, ranula ve tükürük kanalı kisti", [
    dict(h="Mukosel", t="Küçük kanal yırtılır, müsin dokuya dökülür", v=P(n("11.2"), "Alt dudakta mavimsi nodül"), dur=7,
         note="Resmi slaytta yok ama ağızda en sık gördüğünüz şişlik: mukosel. Alt dudağı ısırırsınız, küçük bir kanal yırtılır, müsin dokuya dökülür."),
    dict(t="%82'si alt dudakta; üst dudakta neredeyse hiç yok", dur=6, note="Neville'in 1715 olguluk serisinde yüzde 82'si alt dudakta, üst dudakta bir tane bile yok. Bu cümleyi tümörlerde kullanacağız."),
    dict(t="Epitel yok: gerçek kist değil; besleyen bezlerle birlikte çıkar", v=P(n("11.6"), "Dökülmüş müsin; epitel yok"), dur=7,
         note="Mikroskopta epitel yok; müsin ve köpüklü makrofajlar var, bu yüzden gerçek kist değil. Besleyen küçük bezleri de çıkarın, yoksa nükseder."),
    dict(h="Ranula", t="Ağız tabanında mukosel; sublingual bezden", v=P(n("11.8"), "Ağız tabanında mavimsi şişlik"), dur=6,
         note="Ranula ağız tabanındaki mukosel; sublingual bezden gelir."),
    dict(t="Milohyoidi geçerse boyunda şişlik; tedavi sublingual bezi çıkarmak", v=P(n("11.9"), "Dalan ranula: boyunda şişlik"), dur=7,
         note="Milohyoid kası geçerse boyunda şişlik yapar; buna dalan ranula deniyor. Tedavide en önemli adım sublingual bezi çıkarmak."),
    dict(h="Tükürük kanalı kisti", t="Epitelle döşeli gerçek kist; erişkinde", v=P(n("11.10"), "Wharton kanalı üzerinde şişlik"), dur=6,
         note="Tükürük kanalı kisti ise epitelle döşeli gerçek bir kist; erişkinde görülür ve nüks etmez."),
], size=32, gap=10, strip={1}, dus=True, cred=NEV)

S("Tükürük bezi taşı (sialolitiazis)", [
    dict(t="En sık submandibuler bezde; uzun, yukarı kıvrılan Wharton kanalı", v=P(n("11.13"), "Wharton kanalı ağzında taş"), dur=7,
         note="Taşlar en sık submandibuler bezde. Nedeni anatomi: Wharton kanalı uzun ve yukarı doğru kıvrılıyor, salgı da daha koyu."),
    dict(t="Bir çekirdek çevresinde kalsiyum katman katman çöker", v=P(n("11.17"), "Kanal içinde katmanlı taş"), dur=6,
         note="Hücre artığı, bakteri ya da koyu mukustan oluşan bir çekirdeğin çevresinde kalsiyum katman katman çöker."),
    dict(t="Yemek sırasında artan ağrı ve bezde şişlik", dur=5, note="Hasta yemek sırasında ağrıyan ve şişen bir bezle gelir."),
    dict(t="Okluzal film en iyi gösterir; panoramikte kemik içi lezyon sanılabilir", v=P(n("11.14"), "Mandibula açısında radyoopak kitle"), dur=7,
         note="Okluzal film en iyi gösterir. Panoramikte kemiğin üstüne düşen taş kemik içi lezyon sanılabilir; her taş radyoopak da değildir."),
    dict(t="Mikroskop: kanalda genişleme, çevresinde iltihap, skuamöz metaplazi", dur=6, note="Mikroskopta kanal genişler, çevresinde iltihap ve fibrozis olur; kanal epitelinde en sık skuamöz metaplazi görülür."),
], size=33, strip={1}, dus=True, cred=NEV)

S("Sialadenit: akut ve kronik", [
    dict(h="Kabakulak", t="Paramiksovirüs; önce bir parotis, birkaç gün sonra diğeri", v=P(l("15.26"), "Kabakulak: parotis şişliği"), dur=7,
         note="Akut sialadenitin en sık nedeni viral: kabakulak, paramiksovirüs. Şişlik önce bir parotiste başlar, birkaç gün sonra diğerinde de görülür."),
    dict(h="Akut süpüratif sialadenit", t="Akış azalınca: sıvı kaybı, ameliyat sonrası, kanal tıkanması", v=P(n("11.19"), "Stensen kanalından irin"), dur=7,
         note="Akut bakteriyel sialadenit tükürük akışı azalınca olur: sıvı kaybı, ameliyat sonrası, kanal tıkanması. Bezi masaj yapınca Stensen kanalından irin gelir."),
    dict(t="En sık etken *S. aureus*; tedavi antibiyotik ve sıvı", dur=5, note="En sık etken Staphylococcus aureus; tedavi antibiyotik, sıvı ve gerekirse drenaj."),
    dict(h="Kronik sialadenit", t="Yavaş tıkanma ve taş: fibrozis, parankim atrofisi", v=P(n("11.20"), "Sialografi: daralmanın gerisinde genişleme"), dur=7,
         note="Kronik sialadenit yavaş gelişen tıkanma ve taşla olur: bezde fibrozis ve parankim atrofisi gelişir. İleri evrede bez çıkarılır."),
], size=33, strip={1}, cred=NEV)

S("Kronik sklerozan ve granülomatöz sialadenit", [
    dict(h="Kronik sklerozan sialadenit (Küttner tümörü)", t="Submandibuler bezde tek taraflı sert kitle; tümör sanılır", v=P(r("tb_kuttner.jpg"), "Fibrozis ve lenfoplazmositer iltihap"), dur=8,
         note="Kronik sklerozan sialadenit, eski adıyla Küttner tümörü: submandibuler bezde sert bir kitle; klinikte tümör sanılır."),
    dict(t="Bugün çoğu IgG4 ilişkili hastalığın parçası", v=P(n("11.23"), "IgG4: iki taraflı submandibuler büyüme"), dur=7,
         note="Bugün bu olguların çoğu IgG4 ilişkili hastalığın parçası sayılıyor; çoğu iki taraflı."),
    dict(t="IgG4+ plazma hücreleri, storiform fibrozis; steroide hızlı yanıt", v=P(n("11.24"), "Lenfoplazmositer infiltrat"), dur=7,
         note="Mikroskopta IgG4 pozitif plazma hücreleri ve storiform fibrozis; steroide hızlı yanıt verir. Sjögren'in dışlama ölçütlerinden biri."),
    dict(h="Granülomatöz sialadenit", t="Tüberküloz, sarkoidoz, mantar; sarkoidozda parotis + üveit + yüz felci (Heerfordt)", v=P(r("tb_tbc.jpg"), "Parotis tüberkülozu"), dur=9,
         note="Granülomatöz sialadenit: tüberküloz, sarkoidoz ve mantarlar. Sarkoidozda parotis büyümesi, üveit, yüz felci ve ateş birlikte olursa Heerfordt sendromu."),
], size=31, gap=10, strip={1}, dus=True, cred=IKI)

S("Sialore, kserostomi ve sialadenoz", [
    dict(h="Sialore", t="4 yaşından sonra süren aşırı tükürük", v=stat("4 yaş", "Bu yaştan sonra süren salya: sialore"), dur=6,
         note="Sialore aşırı tükürük üretimi; dört yaşından sonra sürüyorsa anormal kabul edilir."),
    dict(t="Neden: aft, yeni protez, kuduz, ağır metal, ilaçlar (klozapin)", dur=6, note="Nedenleri: aft gibi ağız yaraları, yeni protez, kuduz, ağır metal zehirlenmesi, klozapin gibi ilaçlar."),
    dict(t="Nörolojik hastada sorun çoğu zaman salya fazlası değil, yutma kontrolü", dur=6, note="Serebral palsi ya da Parkinson hastasında sorun çoğu zaman salya fazlası değil, yutma kontrolünün bozulması."),
    dict(h="Kserostomi", t="Öznel ağız kuruluğu; yaşlıların %25'inde", v=stat("%25", "Yaşlılarda kserostomi"), dur=6,
         note="Kserostomi öznel bir ağız kuruluğu yakınması; yaşlıların dörtte birinde var."),
    dict(t="En sık neden ilaçlar: 500'den fazla ilaç kuruluk yapar", v=stat("500+", "Kuruluk yapan ilaç"), dur=6,
         note="Yaşlıda nedeni çoğu zaman yaşlanma değil, ilaçlar: 500'den fazla ilaç kuruluk yapar ve ilaç sayısı arttıkça kuruluk artar."),
    dict(t="Sonuç: kandida, kök çürüğü, protez güçlüğü", v=P(n("11.25"), "Kuru, fissürlü dil"), dur=6, note="Sonuçları: kandida, kök çürüğü, çiğneme ve protez güçlüğü."),
    dict(h="Sialadenoz", t="İltihapsız, iki taraflı parotis büyümesi: diyabet, alkol, bulimia", v=P(n("11.30"), "Alkolizmde parotis ve submandibuler büyüme"), dur=8,
         note="Resmi slaytta yok: sialadenoz. İltihapsız, iki taraflı parotis büyümesi; diyabet, alkolizm, bulimia ve kötü beslenmede görülür."),
], size=30, gap=8, strip={1}, cred=NEV)

S("Lenfoepitelyal sialadenit", [
    dict(t="Eski adı benign lenfoepitelyal lezyon (miyoepitelyal sialadenit); otoimmün", v=P(n("11.26"), "Parotiste lenfoepitelyal lezyon"), dur=7,
         note="Lenfoepitelyal sialadenit, eski adıyla benign lenfoepitelyal lezyon: otoimmün bir sialadenit; çoğu Sjögren hastasında."),
    dict(t="Çoğu iki taraflı bez büyümesi; ileri yaş kadın", dur=5, note="Çoğu iki taraflı ve simetrik bez büyümesi; ileri yaşta kadında sık."),
    dict(t="Asinusları silen yoğun lenfosit infiltrasyonu", v=P(n("11.28"), "Lenfosit infiltrasyonu"), dur=6, note="Mikroskopta asinusları silen yoğun lenfosit infiltrasyonu; germinal merkezli foliküller."),
    dict(t="Kanal çevresinde epimiyoepitelyal adalar", v=P(r("tb_blel.jpg"), "Epimiyoepitelyal adalar"), dur=6, note="Kanallar korunur; çevrelerinde epitel ve miyoepitel hücreleri çoğalır: epimiyoepitelyal adalar."),
    dict(t="Lenfoma riski: en sık MALT lenfoması", dur=6, note="Bu zeminde lenfoma riski artar; en sık MALT tipi düşük dereceli lenfoma, sonra diffüz büyük B hücreli lenfoma."),
], strip={1}, cred=NEV)

S("Sjögren sendromu", [
    dict(t="Sistemik otoimmün hastalık: tükürük ve gözyaşı bezleri", v=P(n("11.25"), "Kuru, fissürlü dil"), dur=6,
         note="Sjögren sendromu sistemik bir otoimmün hastalık; öncelikle tükürük ve gözyaşı bezlerini tutar: ağız ve göz kuruluğu."),
    dict(t="Primer: tek başına; sekonder: romatoid artrit (%15), lupus (%30)", dur=7, note="Primer Sjögren tek başınadır; sekonder Sjögren başka bir otoimmün hastalıkla birliktedir: romatoid artritlilerin yüzde 15'i, lupuslu hastaların yüzde 30'u."),
    dict(t="Kadın:erkek 9:1; orta yaş", dur=5, note="Hastaların onda dokuzu kadın; orta yaşta."),
    dict(t="Bulgular: kuruluk, kandida, boyun çürükleri; hastaların ⅓–½'inde bez büyümesi", dur=7,
         note="Ağızda kuruluk, kandida, boyun çürükleri; hastaların üçte biri ile yarısında majör bez büyümesi. Resmi slayt tek taraflı der; Neville'e göre büyüme çoğu zaman iki taraflı."),
    dict(t="Sialografi: 'meyveli dalsız ağaç'", v=P(n("11.27"), "Noktasal sialektazi"), dur=5, note="Sialografide kanal dalları kaybolur, uçlarda noktasal genişlemeler kalır: meyveli dalsız ağaç."),
    dict(t="Dudak biyopsisi: ≥50 lenfositlik odak / 4 mm² = odak skoru ≥1", v=P(n("11.29"), "Dudak bezlerinde lenfosit odakları"), dur=8,
         note="Diş hekiminin tanı aracı: normal görünen alt dudaktan en az beş küçük bez alınır. Dört milimetrekarede en az 50 lenfositlik bir odak, odak skoru 1 demek."),
    dict(t="ACR/EULAR 2016: biyopsi 3, anti-SSA 3, göz ve tükürük testleri 1'er; toplam ≥4", dur=8,
         note="Sınıflama ACR/EULAR 2016'ya göre: biyopsi 3 puan, anti-SSA 3 puan, göz ve tükürük testleri birer puan. Toplam dört ve üstü primer Sjögren."),
    dict(t="Lenfoma riski %5–10 (15–20 kat); kalıcı parotis büyümesi uyarıdır", dur=8,
         note="Yaşam boyu lenfoma riski yüzde 5 ila 10, genel nüfusun 15 ila 20 katı; çoğu MALT. Parotis sürekli büyükse beklemeyin. Sırada telefon: puanı siz hesaplayacaksınız."),
], size=30, gap=8, strip={1}, dus=True, cred=NEV)

L.add(title="Sjögren: puanla", dur=45, theme="dark", q=W2, strip={1}, body=qbody(Q[W2], qsize=34, osize=29),
      notes="Hesaplayın. (Sonuç.) Doğru A: biyopsi 3, Schirmer 1, toplam 4. Anti-SSA negatif olabilir; biyopsi bu yüzden değerli. Ama önce dışlama ölçütlerine bakın: IgG4 ilişkili hastalık, radyoterapi, hepatit C, AIDS, sarkoidoz.")

S("Nekrotizan sialometaplazi", [
    dict(t="Küçük bezlerin enfarktı; klinikte ve mikroskopta kansere benzer", v=P(n("11.31"), "Erken: arka damakta şişlik"), dur=7,
         note="Nekrotizan sialometaplazi küçük tükürük bezlerinin enfarktı: kan akımı kesilir, bez ölür. Klinikte de mikroskopta da kansere benzer."),
    dict(t="%75'ten fazlası arka sert damakta; çoğu tek taraflı", dur=5, note="Yüzde 75'ten fazlası arka sert damakta; çoğu tek taraflı."),
    dict(t="Neden: travma, anestezi iğnesi, protez, yakın cerrahi, sigara", dur=6, note="Neden olanlar: travma, anestezi iğnesi, uyumsuz protez, yakın bir ameliyat, sigara."),
    dict(t="Önce şişlik, 2–3 hafta içinde krater gibi derin ülser", v=P(n("11.32"), "2–3 hafta sonra: krater ülser"), dur=6,
         note="Önce şişlik olur, iki üç hafta içinde krater gibi derin bir ülsere döner. Hasta 'damağımın bir parçası düştü' diye gelir."),
    dict(t="Mikroskop: lobül yapısı korunur; nekroz + kanallarda skuamöz metaplazi", v=P(n("11.33"), "Nekroz ve duktal skuamöz metaplazi"), dur=7,
         note="Mikroskopta lobül yapısı korunur; asinuslarda nekroz, kanallarda skuamöz metaplazi ve üstteki epitelde psödoepitelyomatöz hiperplazi."),
    dict(h="Patoloğun notu", t="Skuamöz ya da mukoepidermoid karsinom sanılabilir: istek formuna enjeksiyonu, protezi, ani başlangıcı yaz",
         v=col(ph(n("11.33"), "Nekroz ve duktal skuamöz metaplazi", style="flex:1"),
               pato("Formu boş gönderme", "'İki hafta önce bu bölgeye anestezi yapıldı', 'yeni protez', 'birden başladı': patoloğun karşısındaki en değerli bilgi.",
                    size=24, style="padding:18px 22px 18px 26px"), style="flex:1;gap:14px"), dur=12,
         note="Patoloğun notu: bu tablo skuamöz hücreli karsinom ya da mukoepidermoid karsinom sanılabilir. İstek formunu boş göndermeyin: enjeksiyon, protez, ani başlangıç. Lezyon birkaç haftada kendiliğinden iyileşir; iyileşmezse yeniden biyopsi."),
], size=30, gap=8, strip={1}, dus=True, cred=NEV)

S("Lenfoepitelyal kistler", [
    dict(h="Benign lenfoepitelyal kist", t="Çoğu parotiste; ağrısız şişlik", v=P(r("tb_le_kist.jpg"), "Yassı epitel, altında lenfoid doku"), dur=6,
         note="Benign lenfoepitelyal kist çoğu parotiste, ağrısız bir şişlik."),
    dict(t="Yassı epitelle döşeli kist; duvarında germinal merkezli lenfoid doku", dur=6, note="Kist yassı, bazen silyalı epitelle döşeli; duvarında germinal merkezli lenfoid doku var."),
    dict(h="HIV'de kistik lenfoepitelyal lezyon", t="Çoğu HIV pozitif hastada; iki taraflı, çok sayıda parotis kisti", v=P(r("tb_hiv_ln.jpg"), "AIDS: lenf nodunda bez inklüzyonları"), dur=7,
         note="Kistik lenfoepitelyal lezyon büyük çoğunlukla HIV pozitif hastada görülür: iki taraflı, çok sayıda parotis kisti."),
    dict(t="Ek olarak epimiyoepitelyal adalar içerir", dur=5, note="Lenfoepitelyal kiste benzer, ek olarak epimiyoepitelyal adalar içerir. İki taraflı parotis kistlerinde HIV testi isteyin."),
], size=33, strip={1}, cred=RESMI)

L.add(title="DUS Molası 1/2", dur=40, theme="dark", q=W3, body=qbody(Q[W3]),
      notes="Neville'in kitap sonundaki örnek sınav sorularından. 30 saniye. (Sonuç.) Üst dudak. Bu cümleyi birazdan tümörlerde kullanacağız.")

L.add(title="DUS Molası 2/2", dur=35, theme="dark", q=W4, body=qbody(Q[W4]),
      notes="(Sonuç.) Lenfoma; çoğu MALT. Bu ara tümör dışı bloğu kapatıyor; sırada tümörler.")

L.add(title="Ara liderlik: ilk 5", dur=15, board=True, top=5, notes="On saniye: ilk beş. (→ ile devam.)")

# ---- 2. İyi huylu tümörler ----
S("Tükürük bezi tümörleri: genel", [
    dict(t="Baş-boyun tümörlerinin %2–6'sı; en bilinen etken radyasyon", v=stat("%2–6", "Baş-boyun tümörleri içinde"), dur=6,
         note="Tükürük bezi tümörleri baş-boyun tümörlerinin yüzde 2 ila 6'sı. Bilinen en önemli etken radyasyon."),
    dict(t="Çoğu parotiste; sonra submandibuler bez", dur=5, note="Çoğu parotiste, sonra submandibuler bezde."),
    dict(t="Çoğu iyi huylu; her bezde en sık tümör pleomorfik adenom", dur=6, note="Çoğu iyi huylu ve her bezde en sık tümör pleomorfik adenom."),
    dict(t="Parotiste malign oranı %15–32", v=bars(BARS, upto=0), dur=6, note="Kötü huylu olma olasılığı beze göre değişir. Parotiste yüzde 15 ila 32."),
    dict(t="Submandibulerde %26–45", v=bars(BARS, upto=1), dur=5, note="Submandibuler bezde yüzde 26 ila 45; en sık malign tümörü adenoid kistik karsinom."),
    dict(t="Küçük bezlerde %38–54; en sık yer damak", v=bars(BARS, upto=2), dur=6, note="Küçük bezlerde yaklaşık yarısı; en sık yer damak."),
    dict(t="Sublingualde %70–97: bez küçüldükçe malign olasılığı artar", v=bars(BARS, upto=3), dur=8,
         note="Sublingual bezde tümör nadir ama gördüğünüzde neredeyse hep malign. Kural: bez küçüldükçe malign olasılığı artar. Rakamlar Neville'in beş büyük serisinden; resmi slayttaki oranlar da aynı yönde."),
], size=33, strip={2}, dus=True)

S("Pleomorfik adenom", [
    dict(t="En sık tükürük bezi tümörü; çoğu parotiste", v=P(n("11.34"), "Kulak altında küçük nodül"), dur=6, note="Pleomorfik adenom, eski adıyla benign miks tümör: en sık tükürük bezi tümörü; çoğu parotiste."),
    dict(t="Ortalama 45 yaş; kadında biraz sık", dur=4, note="Ortalama 45 yaş; kadında biraz daha sık."),
    dict(t="Yavaş büyüyen, ağrısız, sert, hareketli kitle", v=P(n("11.38"), "Damakta, orta hattın yanında"), dur=6,
         note="Yavaş büyüyen, ağrısız, sert, hareketli bir kitle; ağızda en sık damakta, orta hattın yanında."),
    dict(t="Makroskopi: iyi sınırlı, lobüllü, parlak krem-beyaz", v=P(n("11.40"), "Kapsüllü, sınırlı kitle"), dur=5, note="Makroskopide iyi sınırlı, lobüllü, parlak krem-beyaz bir kitle."),
    dict(t="Üç bileşen: epitel (kanal), miyoepitel, miksoid-kondroid stroma", v=P(n("11.43"), "Kondroid madde ve epitel"), dur=7,
         note="Mikroskopta üç bileşen: kanal yapan epitel, dıştaki miyoepitel hücreleri ve miyoepitelin yaptığı miksoid ya da kıkırdak benzeri stroma. Adındaki pleomorfizm hücrelerin değil, yapının."),
    dict(t="Kapsül eksik olabilir: enükleasyon yapma, yüzeyel parotidektomi", dur=7,
         note="Kapsül eksik olabilir; tümör kapsülün dışına uzanır. Bu yüzden enükleasyon yapılmaz, tümör yatağına ekilir ve nükseder. Parotiste yüzeyel parotidektomi."),
    dict(t="Uzun süre kalırsa malign dönüşüm: %3–4'e kadar; PLAG1/HMGA2", dur=6, note="Uzun süre bırakılırsa yüzde 3 ila 4'üne kadar malign dönüşür ve risk süreyle artar. Gen değişikliği PLAG1 ya da HMGA2."),
], size=32, gap=10, strip={2}, dus=True, cred=NEV)

S("Warthin tümörü", [
    dict(t="İkinci en sık iyi huylu tümör; neredeyse yalnız parotis", v=P(n("11.47"), "Parotis kuyruğunda kitle", pos="50% 30%"), dur=6,
         note="Warthin tümörü ikinci en sık iyi huylu tümör; neredeyse yalnız parotiste, kuyruk bölümünde."),
    dict(t="Sigara içende 8 kat risk; 6.–7. dekat", dur=6, note="Sigarayla en güçlü ilişkili tükürük bezi tümörü: risk sekiz kat. Çoğu 60'lı ve 70'li yaşlarda."),
    dict(t="İki taraflı ve çok sayıda olma olasılığı en yüksek tümör (%5–17)", dur=6, note="İki taraflı ve çok odaklı olma olasılığı en yüksek tükürük bezi tümörü; yüzde 5 ila 17'si iki taraflı."),
    dict(t="Resmi slayt erkekte sık der; Neville: kadınlar sigara içtikçe oran eşitlendi", dur=6,
         note="Resmi slayt erkekte sık diyor; Neville'e göre bu eskide kaldı, kadınlar sigara içtikçe oran eşitlendi."),
    dict(t="Mikroskop: iki sıra onkositik epitel + germinal merkezli lenfoid stroma", v=P(n("11.49"), "İki sıra onkositik epitel"), dur=6,
         note="Mikroskopta papiller kistik yapılar: iki sıra pembe onkositik hücre ve altında germinal merkezli lenfoid doku."),
], size=33, strip={2}, dus=True, cred=NEV)

S("Onkositom, bazal hücreli ve kanaliküler adenom", [
    dict(h="Onkositom", t="Nadir (~%1); yaşlıda, %85–90'ı parotiste", v=P(r("tb_onkositom.jpg"), "Geniş granüler sitoplazmalı hücreler"), dur=6,
         note="Onkositom nadir, tümörlerin yaklaşık yüzde biri; yaşlıda, çoğu parotiste."),
    dict(t="Mitokondriyle dolu, iri pembe hücreler (onkosit)", dur=5, note="Hücreleri mitokondriyle dolu, iri ve pembe: onkosit."),
    dict(h="Bazal hücreli adenom", t="Çoğu parotiste; ileri yaş, kadında sık", v=P(n("11.52"), "Bazaloid hücre kordonları"), dur=6, note="Bazal hücreli adenom çoğu parotiste; ileri yaşta, kadında sık."),
    dict(t="Bazaloid hücre adaları; solid, trabeküler, tübüler, membranöz tip", v=P(r("tb_bha.jpg"), "Tübüler tip"), dur=6,
         note="Bazaloid hücre adaları, aralarında bazal membran maddesi; solid, trabeküler, tübüler ve membranöz tipleri var."),
    dict(h="Kanaliküler adenom", t="Küçük bezlerde, özellikle üst dudakta (%66–78)", v=P(n("11.50"), "Üst dudakta kitle"), dur=6,
         note="Kanaliküler adenom neredeyse yalnız küçük bezlerde; yüzde 66 ila 78'i üst dudakta."),
    dict(t="Yaşlı kadında mavimsi nodül; mukosel sanılabilir", v=P(n("11.51"), "Kanal benzeri hücre dizileri"), dur=6,
         note="Yaşlı kadında mavimsi bir nodül olarak gelir ve mukosel sanılabilir. Sırada telefon: üst dudakta bir nodül."),
], size=31, gap=8, strip={2}, cred=IKI)

L.add(title="Üst dudakta nodül", dur=40, theme="dark", q=W5, strip={2}, body=qbody(Q[W5], qsize=40),
      notes="(Sonuç.) Doğru B: kanaliküler adenom. İki ipucu: üst dudak ve yaş. Mukosel üst dudakta neredeyse hiç olmaz; DUS sorusunu hatırlayın.")

# ---- 3. Kötü huylu tümörler ----
S("Mukoepidermoid karsinom", [
    dict(t="En sık kötü huylu tükürük bezi tümörü; çocukta da en sık", v=P(n("11.57"), "Arka sert damakta mavimsi kitle"), dur=6,
         note="Mukoepidermoid karsinom en sık kötü huylu tükürük bezi tümörü; çocukta da en sık malign tümör."),
    dict(t="Çoğu parotiste; ağızda en sık damak", dur=5, note="Çoğu parotiste; ağızda en sık damakta."),
    dict(t="Mavi-kırmızı ve yumuşak olunca mukosel sanılır", dur=5, note="Ağızda mavi-kırmızı ve yumuşak olunca mukosel sanılır."),
    dict(t="Üç hücre: mukus, epidermoid ve ara hücreler", v=P(n("11.60"), "Mukus hücreleri, kistik alan"), dur=6, note="Adı hücrelerinden: mukus hücreleri, epidermoid hücreler ve aradaki ara hücreler."),
    dict(t="Düşük derece kistik, yüksek derece solid; 5 yıl sağkalım %90 / %55", v=P(n("11.63"), "Yüksek derece: pleomorfik skuamöz hücreler"), dur=8,
         note="Düşük dereceli tümör kistik ve mukus hücresi bol; yüksek dereceli olan solid, skuamöz hücreli karsinoma benzer. Beş yıllık sağkalım düşük derecede yüzde 90, yüksek derecede yüzde 55."),
    dict(t="Kemik içinde de olur: arka mandibula, çok gözlü radyolüsensi", v=P(n("11.64"), "Santral MEC: arka mandibula"), dur=6,
         note="Kemik içinde de görülür: santral mukoepidermoid karsinom, arka mandibulada çok gözlü radyolüsensi."),
    dict(t="Gen: CRTC1/3::MAML2", dur=4, note="Gen değişikliği CRTC1 ya da 3 ile MAML2 füzyonu."),
], size=32, gap=10, strip={3}, dus=True, cred=NEV)

S("Adenoid kistik karsinom", [
    dict(t="Küçük bezlerde ve parotiste; submandibuler bezin en sık malign tümörü", v=P(n("11.74"), "Damakta silik bir şişlik"), dur=7,
         note="Adenoid kistik karsinom küçük bezlerde ve parotiste görülür; submandibuler bezin en sık kötü huylu tümörü."),
    dict(t="Yavaş büyür; erişkin ve ileri yaşta", dur=4, note="Yavaş büyür; erişkin ve ileri yaşta."),
    dict(t="Perinöral invazyon: ağrı, uyuşma, yüz felci; ağrı şişlikten önce olabilir", v=P(n("11.79"), "Perinöral invazyon"), dur=8,
         note="En önemli özelliği sinirlere yayılması. Ağrı, uyuşma ve yüz felci en sık bu tümörde; ağrı şişlikten önce bile başlayabilir."),
    dict(t="Desen: kribriform, tübüler, solid; solid en kötü", v=P(n("11.77"), "Kribriform desen"), dur=6,
         note="Mikroskopta üç desen: kribriform, yani delikli adalar; tübüler; ve solid. Solid desen en kötü prognozlu. Başlık slaytındaki görüntü buydu."),
    dict(t="Lenf noduna az, akciğere geç metastaz; 5 yıl %68–89, 20 yıl %25–40", dur=8,
         note="Lenf noduna az gider ama yıllar sonra akciğere gider. Neville'in cümlesi: beş yıllık sağkalım bu tümörde şifa demek değil; yirmi yılda hastaların yarısından fazlası kaybedilir."),
    dict(t="Gen: MYB::NFIB", v=P(n("11.76"), "BT: damaktan yayılan büyük tümör"), dur=5, note="Gen değişikliği MYB::NFIB."),
], size=32, gap=10, strip={3}, dus=True, cred=NEV)

S("Asinik hücreli karsinom ve sekretuar karsinom", [
    dict(h="Asinik hücreli karsinom", t="Seröz asinus hücresine benzeyen hücreler; %80–90 parotiste", v=P(n("11.65"), "Parotiste büyük, sert kitle"), dur=7,
         note="Asinik hücreli karsinomun hücreleri seröz asinus hücresine benzer; yüzde 80 ila 90'ı parotiste."),
    dict(t="Bazofilik, granüllü sitoplazma; PAS+ zimojen granülleri", v=P(n("11.67"), "Bazofilik granüllü seröz hücreler"), dur=6,
         note="Sitoplazma bazofilik ve granüllü; zimojen granülleri PAS pozitif."),
    dict(t="Düşük dereceli; prognoz iyi", dur=4, note="Düşük dereceli bir tümör; prognozu iyi."),
    dict(h="Sekretuar karsinom", t="ETV6::NTRK3; memenin sekretuar karsinomuna benzer", v=P(n("11.68"), "Yanakta mavimsi şişlik", "Mukosel sanılabilir"), dur=8,
         note="Resmi slaytta yok: sekretuar karsinom. Memenin sekretuar karsinomuyla aynı ETV6::NTRK3 füzyonunu taşır; 2010'dan önce çoğu asinik hücreli karsinom sanılıyordu."),
    dict(t="TRK inhibitörleri için olası hedef", dur=5, note="Bu füzyon TRK inhibitörü ilaçlar için bir hedef olabilir."),
], size=32, gap=10, strip={3}, cred=NEV)

S("Polimorf adenokarsinom ve karsinom ex PA", [
    dict(h="Polimorf adenokarsinom", t="Neredeyse yalnız küçük bezler; %60–65'i damakta; ⅔ kadın", v=P(n("11.80"), "Arka-lateral sert damakta kitle"), dur=7,
         note="Polimorf adenokarsinom, eski adıyla polimorf düşük dereceli adenokarsinom: neredeyse yalnız küçük bezlerde, çoğu damakta; üçte ikisi kadın."),
    dict(t="Hücreler tek tip, desen çok çeşitli; tek sıra dizilim, perinöral invazyon", v=P(n("11.82"), "Tek sıra dizilen hücreler"), dur=7,
         note="Hücreler tek tip ama desen çok çeşitli; hücreler tek sıra dizilir ve sinir çevresine yayılır. Yine de prognozu iyi."),
    dict(h="Karsinom ex pleomorfik adenom", t="Pleomorfik adenom zemininde karsinom; yıllardır duran kitle hızla büyür", v=P(n("11.71"), "Damakta ülserli kitle"), dur=8,
         note="Karsinom ex pleomorfik adenom: pleomorfik adenom zemininde gelişen karsinom. Yıllardır duran bir kitle birden hızla büyümeye başlarsa düşünün."),
    dict(t="Hasta pleomorfik adenomdan 10–15 yaş büyük; en sık parotis", v=P(r("tb_expa_makro.jpg"), "Makroskopi: iki farklı bileşen"), dur=6,
         note="Hasta pleomorfik adenomlu hastalardan 10 ila 15 yaş büyük; en sık parotiste."),
    dict(t="Kapsül invazyonu prognozu belirler: kapsül içi iyi, yaygın invaziv kötü", dur=7,
         note="Prognozu kapsül invazyonu belirler: kapsül içinde kalan iyi, çevre dokuya yaygın yayılan kötü seyirli."),
], size=31, gap=10, strip={3}, dus=True, cred=IKI)

S("Diğer kötü huylu tümörler", [
    dict(h="Bazal hücreli adenokarsinom", t="Bazal hücreli adenomun malign karşılığı; nodüller hâlinde infiltrasyon", v=P(r("tb_bhak.jpg"), "İnfiltratif bazaloid adalar"), dur=7,
         note="Bazal hücreli adenokarsinom bazal hücreli adenomun malign karşılığı; adenomdan ayıran nodüler infiltrasyon, atipi ve mitoz."),
    dict(h="Tükürük bezi duktus karsinomu", t="Yüksek dereceli; yaşlı erkek, parotis; memenin duktal karsinomuna benzer", v=P(r("tb_duktus.jpg"), "Pleomorfik hücreler"), dur=8,
         note="Tükürük bezi duktus karsinomu yüksek dereceli bir tümör; yaşlı erkekte, parotiste. Memenin duktal karsinomuna benzer; yüzde 90'ından fazlası androjen reseptörü pozitif; prognozu kötü."),
    dict(h="Lenfoepitelyal karsinom", t="EBV ilişkili; nazofarenks karsinomunun benzeri; önce nazofarenksi dışla", v=P(r("tb_lek.jpg"), "Lenfoid stroma içinde tümör adaları"), dur=8,
         note="Lenfoepitelyal karsinom EBV ile ilişkili; nazofarenks karsinomunun benzeri. Tanıdan önce nazofarenkste bir tümör dışlanmalı."),
    dict(h="Epitelyal-miyoepitelyal karsinom", t="Parotiste (%70); iç sıra kanal hücresi, dış sıra berrak miyoepitel", v=P(r("tb_emk.jpg"), "İki sıralı yapı"), dur=7,
         note="Epitelyal-miyoepitelyal karsinom çoğu parotiste; iç sırada kanal hücreleri, dış sırada glikojenden berrak görünen miyoepitel hücreleri. Düşük derecelidir."),
    dict(h="Adenokarsinom, NOS", t="Başka bir sınıfa girmeyen adenokarsinom; dışlama tanısı", v=P(n("11.85"), "Arka-lateral damakta kitle"), dur=6,
         note="Adenokarsinom NOS başka hiçbir sınıfa girmeyen adenokarsinomlar; dışlama tanısı. Sırada telefon: tümörleri genleriyle eşleştireceksiniz."),
], size=29, gap=8, strip={3}, cred=IKI)

L.add(title="Tümör ve gen", dur=55, theme="dark", q=W6, strip={3},
      body=div("<div class='live'>CANLI · W6 · Eşleştirme</div><div class='qq'>%s</div>" % md(Q[W6]["q"]) +
               row(col(*[box("navy2", None, [x], size=32, style="padding:22px 28px") for x in Q[W6]["left"]], gap=16, style="flex:1"),
                   col(*[box("navy2", None, [x], size=32, style="padding:22px 28px;font-family:monospace") for x in Q[W6]["right"]], gap=16, style="flex:1"),
                   gap=60, style="margin-top:40px")),
      notes="Telefonda dört tümör, dört gen. Eşleştirin. (Sonuç.) Pleomorfik adenom PLAG1 ya da HMGA2; mukoepidermoid karsinom MAML2; adenoid kistik karsinom MYB::NFIB; sekretuar karsinom ETV6::NTRK3. Küçük bir biyopside patolog tanıyı bu genlerle doğruluyor.")

# ---- Vakaya dönüş ----
DONUS_V = col(row(ph(n("11.38"), "Sert damak, lateral", style="flex:1"), qmark("Bu bulgu ne anlatıyor?"), style="flex:1"),
              box("yellow", None, html_="<div class='big' style='font-size:36px'>Yeni bulgu: karıncalanma. Tahminin değişti mi?</div>", style="padding:32px 32px"),
              style="flex:1")
S("Açılış vakası: hastanın söylemediği", [
    dict(t="45 yaşında kadın; sert damakta, orta hattın yanında kitle", v=DONUS_V, dur=7, note="Dersin başındaki hastamıza dönüyoruz: sert damakta, orta hattın yanında kitle."),
    dict(t="İki yıldır yavaş büyüyor; mukoza sağlam", dur=6, note="İki yıldır yavaş büyüyor; mukoza sağlam."),
    dict(t="Son iki ayda damakta karıncalanma ve uyuşma", dur=12, note="Hasta başta söylemedi: son iki ayda damağında karıncalanma ve uyuşma var. Bu bir sinir bulgusu. Tahmininizi yenileyin."),
], size=38, vis_w=900, theme="dark", tag=("pink", "VAKAYA DÖNÜŞ"), cred=NEV)

L.add(title="Vakaya dönüş: şimdi ne diyorsun?", dur=35, theme="dark", q=W7, cred=NEV,
      body=qbody(Q[W7], qsize=36, photo=ph(n("11.38"))),
      notes="Aynı şıklar. Dersin başındaki dağılımı hatırlayın. (İki sonucu yan yana göster.)")

S("En olası tanı: adenoid kistik karsinom", [
    dict(h="Yer", t="Sert damak, lateral: küçük bezlerin en sık yeri; yaklaşık yarısı malign", v=P(n("11.38"), "Sert damakta kitle"), dur=8,
         note="Kanıtları sırayla koyalım. Yer: sert damak; küçük bezlerin en sık yeri ve buradaki tümörlerin yaklaşık yarısı malign."),
    dict(h="Klinik", t="Yavaş büyüyen, ağrısız, sağlam mukoza: pleomorfik adenom gibi", dur=7, note="Klinik pleomorfik adenomu düşündürüyordu ve başta en olası tanı oydu."),
    dict(h="Yeni bulgu", t="Karıncalanma, uyuşma: perinöral invazyon", v=P(n("11.79"), "Perinöral invazyon"), dur=7,
         note="Ama karıncalanma ve uyuşma sinir tutulumu demek; damakta bu adenoid kistik karsinomu, daha az olasılıkla polimorf adenokarsinomu düşündürür."),
    dict(h="Biyopsi", t="İnsizyonel; kribriform yapı ve perinöral invazyon tanıyı koyar", v=P(n("11.77"), "Kribriform desen"), dur=7, note="Tanıyı insizyonel biyopsi koyar: kribriform yapı ve perinöral invazyon."),
    dict(h="Yönetim", t="Geniş cerrahi ± radyoterapi; geç akciğer metastazı için uzun takip", dur=8, note="Tedavi geniş cerrahi, gerekirse radyoterapi. Geç akciğer metastazı için bu hastayı yirmi yıl izleyeceğiz."),
], size=31, gap=10, cred=NEV)

L.add(title="Eski ad, yeni ad: WHO 2022", dur=40, optional=True,
      body=row(col(box("lilac", "Eski ad → güncel ad", None, html_="<table class='t2' style='font-size:28px;border-spacing:0 10px'>"
                       "<tr><td>Polimorf düşük dereceli adenokarsinom</td><td>Polimorf adenokarsinom</td></tr>"
                       "<tr><td>Papiller kistadenoma lenfomatozum</td><td>Warthin tümörü</td></tr>"
                       "<tr><td>Benign lenfoepitelyal lezyon</td><td>Lenfoepitelyal sialadenit</td></tr>"
                       "<tr><td>Malign miks tümör</td><td>Karsinom ex pleomorfik adenom</td></tr>"
                       "<tr><td>Monomorfik adenom</td><td>Önerilmiyor: kanaliküler / bazal hücreli adenom</td></tr>"
                       "<tr><td>Küttner tümörü</td><td>Kronik sklerozan sialadenit (çoğu IgG4 ilişkili)</td></tr>"
                       "<tr><td>MASC</td><td>Sekretuar karsinom</td></tr></table>", style="padding:26px 30px"), style="flex:0 0 1400px")),
      notes="Zaman kalırsa; yoksa atlayın. Adı değişen tümörler; sınavda iki adı da görebilirsiniz.")

L.add(title="Çıkış bileti", dur=30, theme="dark", q=W8,
      body=div("<div class='live'>CANLI · W8 · Kelime bulutu</div><div class='qq' style='font-size:56px;margin-top:60px;max-width:1500px'>%s</div>"
               "<div style='margin-top:60px;font-size:32px;color:%s'>Tek kelime ya da kısa ifade. En büyük çıkan kelimeyle 24 Kasım'da başlıyorum.</div>" % (md(Q[W8]["q"]), C["soft"])),
      notes="Son kelime bulutu. Hangi konu kafanızı karıştırdı? En büyük kelimeyle 24 Kasım'da başlayacağım.")

L.add(title="Liderlik tablosu", dur=20, board=True, notes="Liderlik tablosu. İlk üçü alkışlayalım. Eşit puanda hızlı olan önde.")

L.add(title="Kaynaklar ve evde tekrar", dur=10,
      body=col(bl(["Neville BW, Damm DD, Allen CM, Chi AC. *Oral and Maxillofacial Pathology.* 5. baskı. Elsevier; 2024. Bölüm 11: Tükürük bezi patolojisi.",
                   "WHO Classification of Tumours Editorial Board. *Head and Neck Tumours.* 5. baskı. IARC; 2022. Bölüm 5 (tükürük bezleri).",
                   "Shiboski CH ve ark. 2016 ACR/EULAR primer Sjögren sınıflama ölçütleri. *Arthritis Rheumatol.* 2017;69:35–45.",
                   "Laskaris G. *Color Atlas of Oral Diseases.* 4. baskı. Thieme; 2017. (Klinik fotoğraflar)",
                   "Kahyaoğlu Akkaya Z. Tükürük bezi hastalıkları patolojisi. Fakülte ders slaytı (sıra ve bazı görseller)."], size=28, gap=14),
               div("<div style='display:flex;gap:34px;align-items:center;background:%s;border-radius:16px;padding:22px 28px;margin-top:18px'>"
                   "<img src='file://%s' style='width:190px;height:190px;border-radius:8px'>"
                   "<div style='font-size:30px;line-height:1.35'><b>Evde tekrar: slaytlar ve quiz (isteyen çözsün)</b><br>%s<br>"
                   "<span style='font:700 34px monospace;color:%s'>olgunak.github.io/lam-basinda/quiz</span></div></div>" % (C["lilac"], os.path.join(CANLI, "img", "quiz_qr.png"), "20 soru: Neville'in örnek sınav soruları, Türkçe, cevap açıklamalı.", C["pink"])),
               box("pink", None, html_="<div class='big' style='font-size:34px'>İlk üçü 24 Kasım'da burada anarım.</div>", style="padding:24px 34px;margin-top:18px")),
      notes="Kaynaklar burada. Evde tekrar için quiz: Neville'in örnek sınav soruları Türkçe, cevap açıklamalı; isteyen karekodu okutup çözsün. İlk üçü gelecek derste burada anarım.")

if __name__ == "__main__":
    only = set(int(x) for x in sys.argv[1:]) or None
    L.build(only)
