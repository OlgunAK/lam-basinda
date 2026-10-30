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

# ---------------- slides ----------------
L.add(title="Yumuşak Doku Hastalıkları", dur=60, lobby=True, nonum=True, raw=title_page(
    "4. Sınıf Patoloji  ·  Diş Hekimliği", "Yumuşak Doku Hastalıkları",
    "Neoplastik olmayan kitleler, iyi huylu tümörler ve sarkomlar",
    "17 Kasım 2026  ·  Uzm. Dr. M. Olgun Ak", "42 yaşında kadın, dil sırtında bir yıldır büyüyen ağrısız nodül.",
    n("12.61"), NEV),
    notes="Günaydın. Bugün iki ders arka arkaya: önce ağzın yumuşak doku hastalıkları, sonra tükürük bezleri. Sağdaki görüntü bir schwannom; dersin ortasında mikroskopta tanıyacaksınız. Karekod perdede: okutun; hesap yok, uygulama yok. Takma ad isterseniz yazın; dersin sonunda liderlik tablosu var, doğru ve hızlı olan kazanıyor. Herkes girince → ile vakaya geçiyoruz. (L: katılım ekranını gizle/göster.)")

L.add(title="Açılış vakası: dil sırtında nodül", dur=60, theme="dark", qopen=W1, cred=NEV,
      body=row(div(bl(["42 yaşında kadın",
                       "Dil sırtında 1 cm, sert, sarımsı nodül",
                       "Bir yıldır yavaş büyüyor; ağrısız",
                       "Üstündeki mukoza sağlam; travma öyküsü yok",
                       "Sigara ve alkol kullanmıyor"], size=36, gap=26), "flex:0 0 900px"),
               col(row(ph(n("12.84"), "Dil sırtı"), qmark(), style="height:470px"),
                   box("yellow", None, html_="<div class='big' style='font-size:40px'>Tahminini telefondan gir. Cevap dersin sonunda.</div>", style="padding:50px 36px"),
                   style="flex:1"), gap=40),
      notes="Hastamız 42 yaşında bir kadın. Dil sırtında bir santimetrelik, sert, sarımsı bir nodül var; bir yıldır yavaş büyüyor ve ağrımıyor. Üstündeki mukoza sağlam, travma öyküsü yok, sigara içmiyor. Fotoğrafa bakın ve tahmininizi girin; şıklar telefonunuzda açık. Cevabı dersin sonunda açacağım, sonraki slaytta yalnız dağılımı göreceğiz.")

L.add(title="Açılış vakası: tahminin ne?", dur=40, theme="dark", q=W1, cont=True, cred=NEV,
      body=qbody(Q[W1], photo=ph(n("12.84"))),
      notes="Sonuçları gösteriyorum ama yorum yapmıyorum. Şıklardan biri kötü huylu, dördü iyi huylu ya da reaktif. Bu dağılımın fotoğrafını çekin; dersin sonunda biyopsi sonucuyla birlikte aynı soruyu yeniden soracağım.")

L.add(title="Dersin planı: üç grup", dur=45,
      body=col(row(
          box("navy", "1 · Neoplastik olmayan kitleler", ["Hamartom ve koristom", "Juvenil hiyalen fibromatozis", "Fibromatozis colli (tortikollis)",
                                                          "Keloid ve hipertrofik skar", "Nodüler fasiitis", "Oral fokal müsinozis", "Travmatik nöroma"], size=30, gap=12, style="flex:1"),
          box("lilac", "2 · İyi huylu tümörler", None, html_=table([
              ["Lif, histiyosit", "fibröz histiyositom, fibromatozis, miyofibrom, soliter fibröz tümör"],
              ["Yağ", "lipom"],
              ["Sinir", "palizatlı kapsüllü nöroma, schwannom, nörofibrom, paragangliom, granüler hücreli tümör, konjenital epulis"],
              ["Damar", "hemanjiyom, lenfanjiyom, nazofarengeal anjiyofibrom"],
              ["Kas", "leiomiyom, rabdomiyom"]], size=26, w1=170), style="flex:0 0 760px;padding:22px 24px"),
          box("rose", "3 · Sarkomlar", ["Pleomorfik sarkom, fibrosarkom, liposarkom", "Malign periferik sinir kılıfı tümörü, olfaktör nöroblastom",
                                        "Anjiyosarkom, Kaposi sarkomu", "Leiomiyosarkom, rabdomiyosarkom", "Sinovyal sarkom, alveoler yumuşak doku sarkomu"],
              size=29, gap=16, style="flex:1"), style="flex:1"),
          box("yellow", None, ["Her hastalıkta aynı dört soruyu soruyoruz: **hangi dokudan** köken alıyor, **kaç yaşında**, **ağızda nerede**, **mikroskopta ne görülür**."],
              size=28, style="padding:20px 30px")),
      notes="Ders fakültemizin resmi slaytıyla aynı sırada ilerliyor: üç grup. Birincisi neoplastik olmayan kitleler; tümör gibi görünürler ama gerçek tümör değildirler. İkincisi iyi huylu tümörler; köken aldıkları dokuya göre sıraladım: lif, yağ, sinir, damar, kas. Üçüncüsü sarkomlar, yani yumuşak dokunun kötü huylu tümörleri. Her hastalıkta aynı dört soruyu soracağız: hangi dokudan köken alıyor, kaç yaşında görülüyor, ağızda en sık nerede, mikroskopta ne görülüyor. Rakamlar Neville 5. baskıdan; resmi slaytla Neville'in ayrıldığı yerleri ayrıca söyleyeceğim.")

# ---- 1. Neoplastik olmayan kitleler ----
L.add(title="Hamartom ve koristom", dur=40, strip={1}, dus=True, cred=NEV,
      body=col(row(ph(n("12.127"), "Koristom: dil kökünde sert nodül"), ph(n("12.128"), "Epitel altında olgun lameller kemik"),
                   ph(n("12.116"), "Leiomiyomatöz hamartom", "7 yaşında çocuk, üst alveol kreti"), style="flex:1"),
               row(box("lilac", "Hamartom", ["O bölgede **normalde bulunan** dokuların düzensiz büyümesi", "Tümör gibi sürekli büyümez",
                                             "Örnek: leiomiyomatöz hamartom; üst ön diş eti (insiziv papilla) ya da dil sırtı orta hat; doğumda varsa konjenital epulis sanılır"],
                       size=25, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "Koristom", ["Normal doku, **olmaması gereken** bir yerde", "Ağızda en sık kemik ve kıkırdak; ayrıca mide mukozası, glial doku, yağ bezi",
                                             "Kemik-kıkırdak koristomlarının %85'i dilde, çoğu foramen çekum çevresinde; 0,5–2 cm",
                                             "Tedavi: eksizyon; nüks bildirilmemiş"], size=25, gap=6, style="flex:1;padding:20px 24px"))),
      notes="İki tanım, sınavda sık karıştırılır. Hamartom: o bölgede normalde bulunan dokuların düzensiz büyümesi; tümör gibi sürekli büyümez. Ağızdaki örneği leiomiyomatöz hamartom: üst ön diş etinde insiziv papilla bölgesinde ya da dil sırtının orta hattında küçük bir kabarıklık; doğumda varsa konjenital epulis sanılabilir. Koristom: normal doku ama olmaması gereken bir yerde. Ağızda en sık kemik ve kıkırdak koristomu görülür; Neville'e göre bunların yüzde 85'i dilde, çoğu dil kökünde foramen çekum çevresinde. Hasta öğürme ya da yutma güçlüğünden yakınabilir. Eksizyon yeterli, nüks bildirilmemiş.")

L.add(title="Çocukta iki fibröz lezyon; keloid", dur=45, strip={1}, dus=True,
      body=col(row(box("lilac", "Juvenil hiyalen fibromatozis", ["Otozomal resesif; akraba evliliğinde sık", "Başlangıç 2–5 yaş; baş-boyunda mm'den 5 cm'ye kadar papül ve nodüller",
                                                               "Ağızda en sık bulgu **diş eti büyümesi**", "Eklem kontraktürleri eşlik edebilir",
                                                               "Mikroskop: hücreden fakir, hiyalinize matriks; **PAS ve Alcian mavisi** ile boyanır"],
                           size=30, gap=16, style="flex:1;padding:22px 26px"),
                       box("lilac", "Fibromatozis colli (tortikollis)", ["Sternokleidomastoid kasın alt bölümünde", "Doğumdan sonraki 2.–4. haftada boyunda şişlik",
                                                                        "Zor doğumda travma ve kanamayla ilişkili; neoplazi değil, onarım süreci",
                                                                        "Kas çekince baş lezyon tarafına eğilir", "Tedavi: fizik tedavi; kendiliğinden gerileyebilir; tedavisiz kalırsa yüzde asimetri"],
                           size=30, gap=16, style="flex:1;padding:22px 26px"),
                       box("lilac", "Keloid ve hipertrofik skar", ["İkisi de yara iyileşmesinde aşırı kollajen birikimi",
                                                                  "Hipertrofik skar yaranın sınırları içinde kalır, zamanla yumuşar",
                                                                  "Keloid yaranın sınırını aşar; çıkarılınca sık nükseder",
                                                                  "Mikroskop: keloidde kalın, camsı (hiyalinize) kollajen demetleri"],
                           size=30, gap=16, style="flex:1;padding:22px 26px"), style="flex:1"),
               div("Kaynak: fakültenin resmi ders slaytı. Bu üç konu Neville 5'te ayrı başlık olarak yok.", GREY)),
      notes="Üç lezyon, resmi slaytımızda var ama Neville'de ayrı başlık olarak yok; bu yüzden fotoğraf koymadım, bilgiler resmi slayttan. Juvenil hiyalen fibromatozis otozomal resesif bir hastalık; 2 ile 5 yaş arasında başlar, baş-boyunda nodüller yapar ve ağızda en sık bulgu diş eti büyümesidir. Mikroskopta hücreden fakir, camsı bir matriks görürüz; PAS ve Alcian mavisi ile boyanır. Fibromatozis colli yenidoğanda sternokleidomastoid kasın alt bölümünde şişlik; zor doğumla ilişkili bir onarım süreci, gerçek tümör değil. Kas kısalınca baş o tarafa eğilir; fizik tedaviyle düzelir. Keloid ve hipertrofik skar: hipertrofik skar yaranın sınırında kalır, keloid sınırı aşar ve çıkarılınca sık nükseder.")

L.add(title="Nodüler fasiitis: hızlı büyür ama iyi huyludur", dur=50, strip={1}, dus=True,
      body=row(col(box("navy", "Klinik", ["Genç erişkin (WHO: en sık 3.–4. dekat); cinsiyet farkı yok", "Birkaç haftada hızla büyür; ameliyata kadar çoğu 2–3 ay",
                                          "Çoğu **≤3 cm**; sıklıkla ağrılı", "Baş-boyunda olguların %25'ine kadarı; ağızda herhangi bir yerde",
                                          "Hızlı büyüdüğü için klinikte **sarkom sanılır**"], size=33, gap=18, style="padding:24px 30px"), style="flex:1"),
               col(box("lilac", "Mikroskop", ["Gevşek miksoid ya da kollajenli zeminde düzensiz demetler yapan, iğsi-yıldızsı fibroblast ve miyofibroblastlar",
                                              "Mitoz bol olabilir, **atipik mitoz yok**; pleomorfizm yok",
                                              "Ekstravaze eritrositler, lenfosit ve makrofajlar",
                                              "SMA pozitif"], size=30, gap=14, style="padding:24px 30px"),
                   box("yellow", "Resmi slayt ile WHO 2022", ["Resmi slayt neoplastik olmayan grupta sayar. WHO 2022 ise **USP6** gen yeniden düzenlenmesi bulunduğu için 'kendiliğinden geçen bir neoplazi' olarak tanımlar.",
                                                             "İkisinde de sonuç aynı: yerel eksizyon yeterli, nüks nadir."], size=27, gap=10, style="padding:20px 26px"),
                   style="flex:1;gap:18px"), gap=30),
      notes="Nodüler fasiitis bu grubun en önemli lezyonu, çünkü sarkomla karışır. Genç erişkinde birkaç haftada hızla büyüyen, çoğu 3 santimetreden küçük, sıklıkla ağrılı bir kitle. Mikroskopta iğsi ve yıldızsı fibroblastlar düzensiz demetler yapar; mitoz bol olabilir. Sarkomdan ayıran: atipik mitoz yok, hücrelerde pleomorfizm yok; zeminde ekstravaze eritrositler ve iltihap hücreleri var. Resmi slaytımız bunu neoplastik olmayan grupta sayıyor; WHO 2022 ise USP6 geninde yeniden düzenleme bulunduğu için kendiliğinden geçen bir neoplazi diyor. Tedavi açısından fark yok: yerel eksizyon yeterli, nüks nadir. Şimdi telefon: bir biyopsi raporu okuyacaksınız.")

L.add(title="Patolog gibi düşün", dur=60, theme="dark", q=W5, strip={1}, body=qbody(Q[W5], qsize=32, osize=29),
      notes="Rapor geldi. Ne dersiniz, ne yaparsınız? (Sonuç.) Doğru B: nodüler fasiitis, yerel eksizyon yeterli. Hızlı büyüme ve bol mitoz sizi sarkoma götürebilir; ama atipik mitoz yok, pleomorfizm yok ve ekstravaze eritrositler var. Bu hastaya geniş rezeksiyon yapmak en büyük hata olur.")

L.add(title="Oral fokal müsinozis ve travmatik nöroma", dur=55, strip={1}, dus=True, cred=NEV,
      body=col(row(ph(n("12.31"), "Oral fokal müsinozis", "Alt azı dişleri arasında diş eti"), ph(n("12.33"), "Gevşek, miksoid bağ dokusu"),
                   ph(n("12.54"), "Travmatik nöroma", "Mental sinir boyunca nodül; ameliyatta"), ph(n("12.55"), "Skar içinde düzensiz sinir demetleri"), style="flex:1"),
               row(box("lilac", "Oral fokal müsinozis", ["Derinin fokal müsinozisinin ağızdaki karşılığı", "Genç erişkin; K:E 2:1; yarıdan fazlası **diş etinde**, sonra sert damak",
                                                         "Yüzeyi normal renkte nodül", "Mikroskop: iyi sınırlı miksoid alan; hiyalüronik asit, Alcian mavisi pozitif", "Eksizyon; nüks yok"],
                       size=24, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "Travmatik nöroma", ["Kesilen sinirin düzensiz rejenerasyonu: akson, Schwann hücresi ve fibroblastlardan oluşan skar",
                                                     "En sık **mental foramen** bölgesi, dil, alt dudak; diş çekimi ya da cerrahi öyküsü",
                                                     "Kitaplar 'ağrılı' der; Neville'e göre yalnız **¼–⅓'i** ağrılı; mental sinirdeki protez bastırınca ağrır",
                                                     "Kemik içindeyse radyolüsent; tedavi: sinirin proksimal ucuyla birlikte eksizyon"],
                       size=24, gap=6, style="flex:1;padding:20px 24px"))),
      notes="Bu grubun son iki lezyonu. Oral fokal müsinozis derinin fokal müsinozisinin ağızdaki karşılığı: genç erişkinde, kadında iki kat sık, yarıdan fazlası diş etinde. Üstündeki mukoza normal renkte. Mikroskopta iyi sınırlı, gevşek, miksoid bir alan; içindeki hiyalüronik asit Alcian mavisiyle boyanır. Nüks etmez. Travmatik nöroma kesilen bir sinirin düzensiz iyileşmesi: akson, Schwann hücresi ve fibroblastlardan oluşan bir skar. En sık mental foramen bölgesinde, dilde ve alt dudakta; hastada diş çekimi ya da cerrahi öyküsü vardır. Resmi slayt ağrılı der; Neville'e göre ancak dörtte biri ile üçte biri ağrılı. Mental sinirdekiler protez bastırınca ağrır. Tedavi sinirin proksimal ucuyla birlikte eksizyon. Sırada iyi huylu tümörler.")

# ---- 2. İyi huylu tümörler ----
L.add(title="Lif ve histiyosit kökenli iyi huylu tümörler", dur=55, strip={2}, dus=True, cred=NEV,
      body=col(row(ph(n("12.21"), "Fibröz histiyositom", "Dil sırtı"), ph(n("12.26"), "Fibromatozis", "Alt çene lingual diş eti"),
                   ph(n("12.28"), "Miyofibrom", "Üst çene diş eti"), ph(n("12.24"), "Soliter fibröz tümör", "Retromolar bölge"), style="flex:1;min-height:300px"),
               div(table([
                   ["Fibröz histiyositom (dermatofibrom)", "Deride sık, ağızda nadir; ağrısız küçük nodül", "İğsi hücreler girdap gibi (**storiform**) dizilir; dev hücre, köpüksü makrofaj"],
                   ["Fibromatozis (desmoid tip)", "Çocuk ve genç erişkin; **lokal agresif**, sınırları düzensiz; metastaz yapmaz", "Nükleer β-katenin; nüks ~%30"],
                   ["Miyofibrom", "Ort. 23 yaş; ağızda en sık **alt çene**; çok odaklı formu miyofibromatozis (bebek)", "Fibroblast ve düz kas özellikli iğsi hücreler; SMA+"],
                   ["Soliter fibröz tümör", "Ağızda en sık yanak (~%45); eski 'hemanjiyoperisitomların' çoğu", "'Geyik boynuzu' damarlar; CD34, **STAT6** pozitif"]],
                   size=23, w1=360))),
      notes="İkinci grup, iyi huylu tümörler; önce lif ve histiyosit kökenliler. Fibröz histiyositom deride dermatofibrom adıyla sık, ağızda nadir; mikroskopta iğsi hücreler girdap gibi dizilir, buna storiform desen diyoruz. Fibromatozis, desmoid tip: iyi huylu ama lokal agresif; sınırları düzensiz olduğu için tam çıkarmak zor ve yaklaşık üçte birinde nükseder, metastaz yapmaz. Resmi slayt 'gingival fibromatozis' diyor; kalıtsal diş eti büyümesiyle karıştırmayın, burada kastedilen diş etine yerleşen desmoid tip fibromatozis. Miyofibrom genç hastada, ağızda en sık alt çenede; bebeklerde çok odaklı formu var. Soliter fibröz tümör: eskiden hemanjiyoperisitom denen tümörlerin çoğu bu; geyik boynuzu gibi dallanan damarlar ve STAT6 pozitifliği tanı koydurur.")

L.add(title="Lipom", dur=45, strip={2}, dus=True, cred=NEV,
      body=row(ph(n("12.50"), "Yanak mukozasında nodül", style="flex:0 0 560px"),
               ph(n("12.52"), "Olgun yağ hücreleri", "Normal yağ dokusundan ayırt edilemez", style="flex:0 0 520px"),
               col(bl(["Ağız-çene tümörlerinin yalnız **%1–4**'ü", "Yumuşak, sarımsı, ağrısız nodül; çoğu **40 yaş üstü**",
                       "Ağızda en sık **yanak ve vestibül** (~yarısı); sonra dil, ağız tabanı, dudak",
                       "Mikroskop: ince kapsüllü olgun yağ dokusu", "Tipler: fibrolipom (en sık), iğsi hücreli (CD34+), anjiyolipom, miksoid, pleomorfik",
                       "Tedavi: eksizyon; nüks nadir"], size=27, gap=12),
                   box("yellow", None, ["Atipik hücre varsa **MDM2/CDK4** ile iyi diferansiye liposarkom dışlanır."], size=25, style="padding:18px 24px"),
                   style="flex:1;gap:16px")),
      notes="Lipom, yağ dokusunun iyi huylu tümörü. Ağızda beklenenden az: ağız-çene tümörlerinin yüzde 1 ila 4'ü. Yumuşak, sarımsı, ağrısız bir nodül; çoğu 40 yaşın üstünde. Resmi slayt en sık yeri dil olarak sıralıyor; Neville'e göre yanak ve vestibül olguların yaklaşık yarısını oluşturuyor. Mikroskopta ince bir kapsülle çevrili olgun yağ dokusu görürüz. Tiplerinden en sık fibrolipom; iğsi hücreli lipom CD34 pozitif. Hücrelerde atipi görürsek MDM2 ve CDK4 boyalarıyla iyi diferansiye liposarkomu dışlarız; buna sarkomlar bölümünde döneceğiz.")

L.add(title="Palizatlı kapsüllü nöroma ve schwannom", dur=55, strip={2}, dus=True, cred=NEV,
      body=col(row(ph(n("12.57"), "Palizatlı kapsüllü nöroma", "Sert damakta ağrısız nodül"), ph(n("12.58"), "İyi sınırlı nöral proliferasyon"),
                   ph(n("12.60"), "Schwannom", "Ağız tabanı"), ph(n("12.61"), "Antoni A ve B alanları"), style="flex:1;min-height:320px"),
               row(box("lilac", "Palizatlı kapsüllü nöroma (soliter sınırlı nöroma)", ["Olguların %90'ı yüzde; ağızda sert damak, diş eti, dudak", "Çoğu <1 cm; **travma öyküsü yok**",
                                                                                        "NF ya da MEN 2B ile ilişkisi yok", "Mikroskop: kapsüllü Schwann hücresi proliferasyonu, içinde aksonlar"],
                       size=24, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "Schwannom", ["Schwann hücresinden; **kapsüllü**, yavaş büyür", "Baş-boyunda %25–48; ağızda en sık **dil** ve dudak",
                                              "Kemik içinde: alt çene arka bölge, mandibular kanal", "**Antoni A** (palizat, Verocay cisimcikleri) + **Antoni B** (gevşek, miksoid)",
                                              "Yaygın S100+; malign dönüşüm yok denecek kadar nadir"], size=24, gap=6, style="flex:1;padding:20px 24px"))),
      notes="Sinir kökenli tümörlere geçiyoruz. Palizatlı kapsüllü nöroma küçük, ağrısız, kapsüllü bir nodül; çoğu yüzde, ağızda sert damakta ve diş etinde. Travmatik nöromadan farkı: travma öyküsü yok. NF ve MEN 2B ile ilişkisi yok. Schwannom Schwann hücresinden köken alan kapsüllü bir tümör; ağızda en sık dilde. Mikroskopta iki alan var: Antoni A'da hücre çekirdekleri sıra sıra dizilir, buna palizat diyoruz; iki sıra çekirdek arasındaki pembe alana Verocay cisimciği denir. Antoni B gevşek ve miksoiddir. S100 yaygın pozitiftir; kötü huylu dönüşüm neredeyse hiç olmaz.")

L.add(title="Nörofibrom ve nörofibromatozis tip 1", dur=60, strip={2}, dus=True, cred=NEV,
      body=col(row(ph(n("12.62"), "Nörofibrom", "Üst çene diş eti"), ph(n("12.65"), "Dalgalı çekirdekli iğsi hücreler"),
                   ph(n("12.69"), "NF1: dilin tek taraflı büyümesi"), ph(n("12.68"), "Café-au-lait lekeleri"), style="flex:1;min-height:320px"),
               row(box("lilac", "Nörofibrom", ["Periferik sinir kılıfının **en sık** tümörü; Schwann hücresi + perinöral fibroblast", "Kapsülsüz, sinirle devamlı; ağrısız, yavaş büyür",
                                               "Ağızda dil, damak, yanak; kemik içinde radyolüsent", "Mikroskop: gevşek miksoid zeminde dalgalı çekirdekli iğsi hücreler, mast hücreleri"],
                       size=24, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "NF1", ["Nörofibrom görürsen hastayı **NF1** için muayene et", "Otozomal dominant; yarısı yeni mutasyon",
                                        "Café-au-lait lekeleri, aksiller çillenme, Lisch nodülleri; pleksiform nörofibrom tanı koydurur",
                                        "Malign periferik sinir kılıfı tümörü riski **%8–13**"], size=24, gap=6, style="flex:1;padding:20px 24px"),
                   box("rose", "Ayrıca: MEN 2B", ["Dil ucu ve dudaklarda çok sayıda mukozal nöroma; çoğu zaman ilk bulgu",
                                                  "Medüller tiroid karsinomu hastaların hepsinde: endokrinolojiye yönlendir"], size=23, gap=6, style="flex:0 0 430px;padding:20px 24px"))),
      notes="Nörofibrom periferik sinir kılıfının en sık tümörü. Schwannomdan farkları: kapsülü yok, sinirle iç içe büyür, mikroskopta dalgalı çekirdekli iğsi hücreler ve aralarda mast hücreleri görülür. Tek başına olabilir; ama bir nörofibrom gördüğünüzde hastayı nörofibromatozis tip 1 için muayene edin. NF1 otozomal dominant; deride café-au-lait lekeleri, koltuk altında çillenme, gözde Lisch nodülleri. Pleksiform nörofibrom tek başına tanı koydurur. Hastaların yüzde 8 ila 13'ünde malign periferik sinir kılıfı tümörü gelişir; bu yüzden büyüyen ya da ağrıyan bir nörofibrom beklemez. Sağda bir not: dil ucunda ve dudaklarda çok sayıda küçük nöroma MEN 2B'yi düşündürür; bu hastaların hepsinde medüller tiroid karsinomu gelişir. Resmi slaytta yok, ama Neville'de önemli bir konu.")

L.add(title="Dört mikroskop görüntüsü: hangisi schwannom?", dur=40, theme="dark", q=W2, strip={2}, cred=NEV,
      body=qbody(Q[W2], qsize=40, photo=col(row(ph(n("12.65"), label="A"), ph(n("12.61"), label="B"), style="flex:1"),
                                            row(ph(n("12.118"), label="C"), ph(n("12.33"), label="D"), style="flex:1"), gap=16, style="flex:1")),
      notes="Dört mikroskop görüntüsü. Hangisi schwannom? (Sonuç.) Doğru B: çekirdeklerin sıra sıra dizildiği Antoni A alanı. A nörofibrom: dalgalı çekirdekli, düzensiz iğsi hücreler. C leiomiyom: küt uçlu çekirdekli düz kas demetleri. D oral fokal müsinozis: gevşek, miksoid bağ dokusu.")

L.add(title="Granüler hücreli tümör ve konjenital epulis", dur=70, strip={2}, dus=True, cred=NEV,
      body=col(row(ph(n("12.85"), "Granüler hücreli tümör", "Yanak, ağız köşesine yakın"), ph(n("12.86"), "İri, granüler sitoplazmalı hücreler"),
                   ph(n("12.88"), "Konjenital epulis", "Yenidoğan, üst alveol kreti"), ph(n("12.89"), "Yüzey epiteli ince, reteler atrofik"), style="flex:1;min-height:320px"),
               row(box("lilac", "Granüler hücreli tümör", ["Ağız (deriyle birlikte) en sık yeri; ağızda olguların **⅓–½'i dil sırtında**", "4.–6. dekat; K:E 3:1; çoğu <2 cm, kapsülsüz",
                                                          "Poligonal hücreler, geniş granüler eozinofilik sitoplazma; **PAS+**, **S100+** (WHO: SOX10+)",
                                                          "Yüzeyde psödoepitelyomatöz hiperplazi: olguların yarısına kadar"],
                       size=24, gap=6, style="flex:1;padding:20px 24px"),
                   box("rose", "Konjenital epulis", ["Yenidoğanın alveol mukozası; üst çene alt çeneden 2–3 kat sık", "Olguların ~%90'ı **kız**; doğumda var",
                                                     "Benzer granüler hücreler ama **S100 negatif**; yüzeyde hiperplazi yok, reteler atrofik",
                                                     "Nüksetmez; kendiliğinden gerileyebilir"], size=24, gap=6, style="flex:1;padding:20px 24px"))),
      notes="Granüler hücreli tümör: hücreler iri, poligonal ve sitoplazmaları ince pembe granüllerle dolu; PAS ve S100 pozitif, yani Schwann hücresi özellikleri taşıyor. Vücutta en sık ağızda ve deride görülür; ağızda olguların üçte biri ile yarısı dil sırtında. Kadında üç kat sık, çoğu 40 ile 60 yaş arasında. Önemli bir ayrıntı: olguların yarısına kadarında üstteki epitel aşağı doğru uzanan dallar yapar; buna psödoepitelyomatöz hiperplazi diyoruz. Yenidoğandaki benzeri konjenital epulis: doğumda alveol kretinde polipoid bir kitle, yaklaşık yüzde 90'ı kız bebek. Hücreleri benzer ama S100 negatif, yüzeyde hiperplazi yok, reteler incelmiş. Nüksetmez, hatta kendiliğinden küçülebilir.")

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
