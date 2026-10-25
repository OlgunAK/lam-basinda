# -*- coding: utf-8 -*-
"""M3 · Yumuşak Doku Hastalıkları (17 Kasım 2026, blok dersin birincisi, 25 dk)."""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import *
from foto import F

NEV = "Neville ve ark., *Oral and Maxillofacial Pathology*, 5. baskı (Elsevier, 2024)"
LAS = "Laskaris, *Color Atlas of Oral Diseases*, 4. baskı (Thieme, 2017)"
BOTH = NEV + " · " + LAS
n = lambda k, **kw: F("n", k, **kw)
l = lambda k, **kw: F("l", k, **kw)

L = Lesson("M3", "Yumuşak Doku Hastalıkları", "Yumuşak Doku Hastalıkları", "17 Kasım 2026",
           frame="Önce adres: diş etinde mi? Değilse hangi doku?",
           strip=("Önce adres", ["1 Diş eti mi?", "2 Hangi doku?"]),
           cta="24 Kasım'a kadar Neville Bölüm 12'yi (yumuşak doku tümörleri) bir kez okuyun. İlk üçü gelecek derste burada anarım.")

IMG = os.path.join(CANLI, "img")


def save(src, name):
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im.save(os.path.join(IMG, name), quality=88)
    return "img/" + name


# ---------------- questions ----------------
VAKA_OPTS = ["Piyojenik granülom (gebelik tümörü)", "Periferik dev hücreli granülom", "Periferik ossifiye fibrom",
             "Fibrom", "Kaposi sarkomu"]
W1 = L.q(id="W1", type="POLL", label="Açılış vakası: tahminin ne?", q="Bu hastada ön tanın ne?", scored=False,
         img=save(n("12.37"), "m3_vaka.jpg"), opts=VAKA_OPTS, hide=True)
grid_img([l("35.2"), l("34.30"), l("35.12"), n("12.4")], os.path.join(IMG, "m3_dis_eti.jpg"))
W2 = L.q(id="W2", type="IMGMCQ", label="Dört diş eti kitlesi", q="Dört diş eti kitlesi. Hangisi periferik dev hücreli granülom?",
         scored=True, img="img/m3_dis_eti.jpg", opts=["A", "B", "C", "D"], a=2,
         exp="C: koyu, mor-kırmızı kitle; periferik dev hücreli granülom yalnız diş etinde ve dişsiz alveol kretinde görülür. "
             "A piyojenik granülom (parlak kırmızı, lobüler), B periferik ossifiye fibrom (ülserli olunca piyojenik granülom sanılır), "
             "D fibrom. Renk ipucu verir; tanıyı biyopsi koyar.")
W3 = L.q(id="W3", type="MCQ", label="DUS Molası 1/2", scored=True,
         q="Periferik dev hücreli granülom klinik olarak en çok hangi lezyonu taklit eder?",
         opts=["Epulis fissuratum", "İnflamatuvar papiller hiperplazi", "Lenfatik malformasyon", "Piyojenik granülom", "Schwannom"], a=3,
         exp="İkisi de diş etinde, kırmızı ve sıklıkla ülserli kitle. PDHG daha çok mor-mavidir ve yalnız diş eti ya da alveol kretinde görülür; ayırımı mikroskop yapar: çok çekirdekli dev hücreler.")
W4 = L.q(id="W4", type="MCQ", label="DUS Molası 2/2", scored=True,
         q="Tanım gereği 'epulis' kelimesi hangi kitle için kullanılır?",
         opts=["Diş eti ya da alveol kretinde gelişen kitle", "Pürüzlü, çakıl taşı yüzeyli kitle", "Uyumsuz protezle ilişkili kitle",
               "Epitelden köken alan kitle", "Altta yatan bir enfeksiyonla ilişkili kitle"], a=0,
         exp="Epulis bir yer adıdır: diş eti ya da alveol kretinde gelişen kitle. Epulis fissuratum protezle, konjenital epulis yenidoğanla, epulis granulomatosa çekim boşluğuyla ilişkilidir; ortak noktaları adresleri.")
W5 = L.q(id="W5", type="MCQ", label="Patolog gibi düşün", scored=True,
         q="Dil sırtında 1 cm, ağrısız, sarımsı nodül. Yüzeysel biyopsinin raporu: 'Yüzeyde psödoepitelyomatöz hiperplazi; invaziv karsinom dışlanamadı.' İlk adımın ne?",
         opts=["Geniş rezeksiyon ve boyun diseksiyonu planlarım", "Derin insizyonel biyopsiyi tekrarlarım; istek formuna yeri ve kliniği yazarım",
               "Altı ay sonra kontrole çağırırım", "Radyoterapiye yönlendiririm", "İki hafta antifungal veririm"], a=1,
         exp="Dil sırtında ağrısız nodül ve yüzeyde psödoepitelyomatöz hiperplazi: granüler hücreli tümörü düşün. Altındaki granüler hücreleri görmek için derin biyopsi gerekir; yüzeysel parçada PEH karsinom sanılabilir. Dil sırtı ağız kanseri için olağan bir yer değil.")
W6 = L.q(id="W6", type="POLL", label="Vakaya dönüş: şimdi ne diyorsun?", q="Dersin başındaki hasta: şimdi ön tanın ne?", scored=False,
         img=save(n("12.37_2"), "m3_vaka_donus.jpg"), opts=VAKA_OPTS, a=0, compare="W1")
W7 = L.q(id="W7", type="WORDCLOUD", label="Çıkış bileti", q="Bugün en çok kafanı karıştıran konu hangisiydi? (Tek kelime ya da kısa ifade)", scored=False)
Q = L.qmap

# ---------------- slides ----------------
L.add(title="Yumuşak Doku Hastalıkları", dur=60, lobby=True, nonum=True, raw=title_page(
    "4. Sınıf Patoloji  ·  Diş Hekimliği", "Yumuşak Doku Hastalıkları", "Önce adres, sonra doku: ağızdaki kitlenin peşinde",
    "17 Kasım 2026  ·  Uzm. Dr. M. Olgun Ak", "Yedi aylık gebe, diş etinde üç haftada büyüyen kırmızı kitle.",
    n("12.86"), NEV),
    notes="Günaydın. Bugün iki ders arka arkaya: önce ağzın yumuşak doku kitleleri, sonra tükürük bezleri. Sağdaki pembe hücreleri görüyorsunuz; kim olduklarını dersin ortasında söyleyeceğim, bir tuzak kuruyorlar. Karekod perdede: okutun; hesap yok, uygulama yok. Takma ad isterseniz yazın; dersin sonunda liderlik tablosu var, doğru ve hızlı olan kazanıyor. Herkes girince → ile vakaya geçiyoruz. (L: katılım ekranını gizle/göster.)")

L.add(title="Açılış vakası: diş etinde kanayan kitle", dur=60, theme="dark", qopen=W1, cred=NEV,
      body=row(div(bl(["Genç kadın, yedi aylık gebe",
                       "Üst ön diş etinde üç haftada büyüyen kitle",
                       "Fırçalarken ve dokununca kolayca kanıyor; ağrısız",
                       "Dişlerde diş taşı, diş eti iltihaplı"], size=36, gap=28), "flex:0 0 900px"),
               col(row(ph(n("12.37"), "Üst ön diş eti", pos="50% 45%"), qmark(), style="height:470px"),
                   box("yellow", None, html_="<div class='big' style='font-size:40px'>Tahminini telefondan gir. Cevap dersin sonunda.</div>", style="padding:50px 36px"),
                   style="flex:1"), gap=40),
      notes="Hastamız yedi aylık gebe. Üç haftadır üst ön diş etinde bir kitle büyüyor; fırçalarken kanıyor, ağrı yok. Diş taşı var, diş eti iltihaplı. Fotoğrafa bakın ve tahmininizi girin; şıklar telefonunuzda açık. Cevabı dersin sonunda açacağım, sonraki slaytta yalnız dağılımı göreceğiz.")

L.add(title="Açılış vakası: tahminin ne?", dur=45, theme="dark", q=W1, cont=True, cred=NEV,
      body=qbody(Q[W1], photo=ph(n("12.37"), pos="50% 45%")),
      notes="Sonuçları gösteriyorum ama yorum yapmıyorum. Beş şıkkın dördü diş etinde sık görülen kitleler; biri kötü huylu. Bu dağılımın fotoğrafını çekin, dersin sonunda aynı soruyu yeniden soracağım.")

L.add(title="Önce adres: kitle nerede?", dur=50,
      body=col(row(
          box("navy", "1 · Diş etinde mi?", ["Büyük olasılıkla **reaktif dörtlüden** biri:",
                                             "piyojenik granülom · periferik dev hücreli granülom · periferik ossifiye fibrom · fibrom",
                                             "Tedavi ortak: **periosta kadar** çıkar, komşu dişlerde detertraj yap."], size=29, style="flex:0 0 760px"),
          col(box("lilac", "2 · Değilse: hangi doku?", None, html_=
                  "<table class='t2' style='font-size:26px'>"
                  "<tr><td>Lif</td><td>fibrom, dev hücreli fibrom, protez hiperplazileri</td></tr>"
                  "<tr><td>Sinir</td><td>travmatik nöroma, granüler hücreli tümör, schwannom, nörofibrom</td></tr>"
                  "<tr><td>Damar</td><td>hemanjiyom, vasküler ve lenfatik malformasyon</td></tr>"
                  "<tr><td>Yağ</td><td>lipom</td></tr>"
                  "<tr><td>Kas</td><td>çocukta rabdomiyosarkom</td></tr></table>", style="flex:1;padding:22px 28px"), style="flex:1"),
          style="flex:1"),
          box("pink", None, ["**Ama:** ağız yumuşak dokusuna metastazların da en sık adresi diş eti (%54) ve piyojenik granülom gibi görünebilir. Çıkardığın her doku patolojiye gider."],
              size=28, style="padding:22px 30px")),
      notes="Bütün dersi bir soruya bağlıyorum: önce adres. Kitle diş etindeyse büyük olasılıkla dört reaktif lezyondan biri; tedavileri de ortak: periosta kadar çıkar, komşu dişleri temizle, yoksa nükseder. Diş etinde değilse ikinci soru: hangi doku? Lif, sinir, damar, yağ, kas. Ama bir uyarı: diş eti metastazların da en sevdiği yer ve piyojenik granülom gibi görünebilir. Bu yüzden çıkardığınız her parça patoloğa gelir; bunu birazdan bir hastada göreceğiz.")

L.add(title="Diş eti dörtlüsü: aynı adres, dört hastalık", dur=80, strip={1}, dus=True, cred=BOTH,
      body=col(row(ph(l("35.8"), "Piyojenik granülom"), ph(n("12.41"), "Periferik dev hücreli granülom"),
                   ph(l("34.29"), "Periferik ossifiye fibrom"), ph(l("34.26"), "Fibrom (yanak)"), style="height:440px"),
               div("<table class='t2'>"
                   "<tr><td style='width:420px'>Piyojenik granülom</td><td>Kırmızı, kolay kanar, hızlı büyür</td><td>Diş etinde %75–85; gebelik, diş taşı</td></tr>"
                   "<tr><td>Periferik dev hücreli granülom</td><td>Mor-mavi</td><td><b>Yalnız</b> diş eti ya da dişsiz alveol kreti</td></tr>"
                   "<tr><td>Periferik ossifiye fibrom</td><td>Pembe-kırmızı, papilladan çıkar</td><td><b>Yalnız</b> diş eti; 10–19 yaş, ⅔ kadın; içinde kemik</td></tr>"
                   "<tr><td>Fibrom</td><td>Pembe, düzgün yüzeyli, sert</td><td>En sık 'tümör'; en sık yeri yanakta ısırma hattı</td></tr>"
                   "</table>")),
      notes="Dört fotoğraf, dört hastalık; üçü diş etinde. Piyojenik granülom kırmızıdır, kolay kanar, hızlı büyür; yüzde 75 ila 85'i diş etinde. Periferik dev hücreli granülom daha koyu, mor-mavidir ve yalnızca diş etinde ya da dişsiz alveol kretinde görülür. Periferik ossifiye fibrom da yalnız diş etinde, interdental papilladan çıkar; çoğu ergen ve genç kadın. Fibrom ağzın en sık 'tümörü' ama aslında reaktif bir hiperplazi; en sık yeri diş eti değil, yanakta ısırma hattı. Bu yüzden dördüncü fotoğraf yanaktan.")

L.add(title="Piyojenik granülom: ne piyojenik ne granülom", dur=75, strip={1}, dus=True, cred=BOTH,
      body=row(ph(n("12.40"), "Lobüler kapiller proliferasyon", "Mikroskop: granülasyon dokusuna benzer damar yumakları", style="flex:0 0 560px"),
               ph(l("35.9"), "Gebelik tümörü", style="flex:0 0 520px"),
               col(bl(["Adı yanıltıcı: irin de granülom da yok; **reaktif damar proliferasyonu**",
                       "Lobüler olanlar: **lobüler kapiller hemanjiyom** (WHO 2022 bu adı öneriyor)",
                       "Gebelikte: ilk üç ayda başlar, yedinci aya kadar artar",
                       "Doğumdan sonra bir kısmı geriler ya da fibroma dönüşür",
                       "Tedavi: periosta kadar eksizyon + detertraj; nüks %3–15"], size=27, gap=14),
                   box("yellow", None, ["**Gebede bekle:** gebelikte çıkarılırsa daha sık nükseder; işlev ya da estetik sorun yoksa doğumu bekle."], size=26, style="padding:20px 24px"),
                   style="flex:1;gap:16px")),
      notes="Adı iki kez yanlış: irin yok, granülom da yok. Aslında hızla çoğalan küçük damarlar; mikroskopta lobüller hâlinde kapiller yumakları görüyorsunuz. WHO 2022 lobüler olanlara lobüler kapiller hemanjiyom diyor ve eski adı önermiyor; ama klinikte herkes hâlâ piyojenik granülom diyor. Hormonlar büyütür: gebelik tümörü ilk üç ayda başlar, yedinci aya kadar artar. Doğumdan sonra bir kısmı kendiliğinden geriler ya da sertleşip fibroma döner. Pratik kural: gebelikte çıkarılırsa daha sık nükseder; işlev ya da estetik sorun yoksa doğumu bekleyin. Çıkarırken periosta kadar inin ve komşu dişlerdeki diş taşını temizleyin; nüks yüzde 3 ila 15.")

L.add(title="Yalnız diş etinde: PDHG ve POF", dur=75, strip={1}, dus=True, cred=NEV,
      body=col(row(
          col(row(ph(n("12.42"), "Periferik dev hücreli granülom"), ph(n("12.44"), "Çok çekirdekli dev hücreler"), style="flex:1"),
              box("lilac", None, ["Ort. 31–46 yaş; alt çenede biraz daha sık", "Altındaki kemikte 'çanak' rezorpsiyonu olabilir; nüks %10–18",
                                  "**Hiperparatiroidinin kahverengi tümörü** aynı görünür: kalsiyum ve PTH iste"], size=27, gap=6, style="padding:20px 24px"),
              style="flex:1;gap:16px"),
          col(row(ph(n("12.45"), "Periferik ossifiye fibrom"), ph(n("12.48_2"), "Fibröz doku içinde kemik"), style="flex:1"),
              box("lilac", None, ["Pik 10–19 yaş; ⅔ kadın; yarıdan fazlası kesici-kanin bölgesinde", "Kemik, sement benzeri madde ya da distrofik kalsifikasyon; nüks %8–16",
                                  "Ülserli olunca piyojenik granülom sanılır"], size=27, gap=6, style="padding:20px 24px"),
              style="flex:1;gap:16px"), style="flex:1"),
          box("navy", None, ["**Üçü için kural:** periosta ya da kemiğe kadar çıkar, komşu dişlerde detertraj yap; yoksa nükseder."], size=27, style="padding:18px 28px")),
      notes="İki lezyon yalnız diş etinde yaşar. Periferik dev hücreli granülom mor-mavidir, mikroskopta kanamalı bir zeminde çok çekirdekli dev hücreler görürüz. Altındaki kemikte çanak gibi bir rezorpsiyon yapabilir; o zaman santral dev hücreli granülomun kemikten taşıp taşmadığını radyografi söyler. Önemli: hiperparatiroidinin kahverengi tümörü mikroskopta aynıdır; tekrarlayan ya da çok sayıda lezyonda kalsiyum ve PTH isteyin. Periferik ossifiye fibrom ergen ve genç kadın hastalığı; adını içindeki kemikten alır. Sağdaki gibi ülserli olunca piyojenik granülom sanılır; bu lezyon iki kez nükset. Kural üçü için aynı: periosta kadar çıkar, dişleri temizle. Sırada telefon: dört diş eti kitlesi.")

L.add(title="Dört diş eti kitlesi: hangisi PDHG?", dur=45, theme="dark", q=W2, strip={1}, cred=BOTH,
      body=qbody(Q[W2], qsize=40, photo=col(row(ph(l("35.2"), label="A"), ph(l("34.30"), label="B"), style="flex:1"),
                                            row(ph(l("35.12"), label="C"), ph(n("12.4"), label="D"), style="flex:1"), gap=16, style="flex:1")),
      notes="Dört diş eti kitlesi. Hangisi periferik dev hücreli granülom? Renge bakın. (Sonuç.) Doğru C: koyu, mor-kırmızı. A parlak kırmızı ve lobüler: piyojenik granülom. B kırmızı ve ülserli ama periferik ossifiye fibrom; az önce dediğim gibi ülserli olunca piyojenik granülom sanılır. D pembe ve düzgün: fibrom. Renk ipucu verir; tanıyı biyopsi koyar.")

L.add(title="Dev hücreli fibrom: papillom kılığında", dur=40, strip={2}, cred=NEV,
      body=col(row(ph(n("12.8"), "Dil sırtında nodül"), ph(n("12.9"), "Diş etinde papiller yüzey"), ph(n("12.11_2"), "Yıldızsı, çok çekirdekli fibroblastlar"), style="flex:1"),
               row(box("lilac", None, ["Çoğu ilk 30 yaşta; yarısı diş etinde (alt çene 2 kat)", "Yüzey papiller: **papillom sanılır**"], size=30, style="flex:1"),
                   box("lilac", None, ["Mikroskop: yüzeye yakın büyük, yıldızsı fibroblastlar", "Kronik irritasyonla ilişkili değil; nüks nadir"], size=30, style="flex:1"))),
      notes="Fibromun kardeşi: dev hücreli fibrom. Daha genç hastada, yarısı diş etinde. Yüzeyi pürüzlü olduğu için klinikte papillom sanılır. Mikroskopta adını veren hücreler: yüzeye yakın büyük, yıldızsı, bazen çok çekirdekli fibroblastlar. Sıradan fibromun aksine kronik irritasyonla ilişkili değil. Basit eksizyon yeterli.")

L.add(title="Protezin açtığı kitleler", dur=55, strip={2}, cred=NEV,
      body=col(row(ph(n("12.13"), "Epulis fissuratum", "Protez kenarı iki kıvrım arasındaki yarığa oturur"), ph(n("12.18"), "İnflamatuvar papiller hiperplazi", "Sert damakta çakıl taşı görünümü"),
                   ph(n("12.20"), "Yüzeyde psödoepitelyomatöz hiperplazi", "Karsinom sanılmasın"), style="flex:1"),
               row(box("lilac", "Epulis fissuratum", ["Uyumsuz protez kenarı; çoğu ön vestibülde, orta-ileri yaş kadın",
                                                      "Tedavi: eksizyon + protezi yenile ya da besle"], size=27, gap=6, style="flex:1;padding:20px 26px"),
                   box("lilac", "İnflamatuvar papiller hiperplazi", ["Uyumsuz protez, kötü hijyen, protezi 24 saat takmak (bunların ~%20'si)",
                                                                    "Erken: protezi geceleri çıkar, antifungal; ileri: eksizyon"], size=27, gap=6, style="flex:1;padding:20px 26px"))),
      notes="İki protez lezyonu. Epulis fissuratum uyumsuz bir protez kenarının açtığı kıvrımlar: protezin kenarı iki kıvrımın arasındaki yarığa oturur. Eksizyon yeterli değil; protezi yenilemezseniz geri gelir. İnflamatuvar papiller hiperplazi sert damakta, protezin altında, çakıl taşı gibi kırmızı papiller. Protezi gece gündüz takanların yaklaşık beşte birinde görülür; çoğunda kandida da vardır. Erken dönemde protezi geceleri çıkarmak ve antifungal yeter. Patolog için not: ikisinde de yüzey epiteli psödoepitelyomatöz hiperplazi yapabilir, karsinom sanılmamalı.")

L.add(title="DUS Molası 1/2", dur=45, theme="dark", q=W3, body=qbody(Q[W3]),
      notes="İlk DUS sorusu, Neville'in kitap sonundaki örnek sınav sorularından. 30 saniye. (Sonuç.) Piyojenik granülom: ikisi de diş etinde kırmızı, ülserli kitle. Ayırımı mikroskop yapar.")

L.add(title="DUS Molası 2/2", dur=40, theme="dark", q=W4, body=qbody(Q[W4]),
      notes="İkinci soru bir tanım. (Sonuç.) Epulis bir yer adı: diş eti ya da alveol kreti. Epulis fissuratum, konjenital epulis, epulis granulomatosa; hepsinin ortak noktası adresleri. Bu ara diş eti bloğunu kapatıyor; sırada sinir.")

L.add(title="Ara liderlik: ilk 5", dur=15, board=True, top=5,
      notes="On saniye: ilk beş. (→ ile devam.)")

L.add(title="Travmatik nöroma: kesilen sinirin yarası", dur=50, strip={2}, cred=NEV,
      body=row(ph(n("12.54"), "Mental sinir boyunca nodül", "Ameliyat sırasında", style="flex:0 0 560px"),
               ph(n("12.55"), "Düzensiz sinir demetleri, skar dokusu", style="flex:0 0 560px"),
               col(bl(["En sık: **mental foramen** bölgesi, dil, alt dudak",
                       "Kitaplar 'ağrılı' der; ama yalnız **¼–⅓'i** ağrılı",
                       "Mental sinirdeki nöroma protez bastırınca ağrır",
                       "Tedavi: sinirin proksimal ucuyla birlikte eksizyon"], size=32, gap=26), style="flex:1")),
      notes="İkinci adres sorusu: hangi doku? Önce sinir. Kesilen bir sinir iyileşirken skar içinde düzensiz demetler oluşturur; bu travmatik nöroma. Çekim sonrası mental foramen bölgesinde, dilde ve alt dudakta görülür. DUS 'ağrılı tümör' diye sorar; ama Neville'e göre yalnızca dörtte biri ile üçte biri ağrılı. Mental sinirdekiler protez bastırınca ağrır; hasta protezi takamadığını söyler. Tedavi sinirin proksimal ucuyla birlikte eksizyon.")

L.add(title="Granüler hücreli tümör ve konjenital epulis", dur=75, strip={2}, dus=True, cred=BOTH,
      body=col(row(ph(l("34.47"), "Dil sırtında nodül"), ph(n("12.86"), "Granüler hücreler"), ph(n("12.87"), "Yüzeyde PEH", pos="50% 30%"),
                   ph(n("12.88"), "Konjenital epulis", "Yenidoğan, üst alveol kreti"), style="flex:1;min-height:330px"),
               row(box("lilac", "Granüler hücreli tümör", ["Dil sırtı (⅓–½); 4.–6. dekat; K:E 3:1", "S100+ (WHO: SOX10+); granüller CD68+",
                                                          "En sık yeri ağız boşluğu ve deri"], size=24, gap=6, style="flex:0 0 520px;padding:20px 24px"),
                   box("rose", "Konjenital epulis", ["Yenidoğan; üst alveol kreti", "~%90 kız; **S100 negatif**", "Nüksetmez; kendiliğinden gerileyebilir"],
                       size=24, gap=6, style="flex:0 0 470px;padding:20px 24px"),
                   pato("Yüzeysel biyopsi tuzağı", "Olguların yarısına kadarında yüzey epiteli psödoepitelyomatöz hiperplazi yapar; yüzeysel biyopside karsinom sanılıp gereksiz kanser ameliyatı yapılabilir. **Derin al**, istek formuna yeri yaz.",
                        size=23, style="flex:1;padding:18px 24px 18px 28px"))),
      notes="Başlık slaytındaki pembe hücreler bunlardı: granüler hücreli tümör. Dil sırtında ağrısız, sarımsı, sert bir nodül; kadında üç kat sık. Hücreler iri, sitoplazmaları granüllerle dolu; S100 pozitif, Schwann hücresi kökenli. Yenidoğandaki kuzeni konjenital epulis: doğumda üst alveol kretinde polipoid kitle, yaklaşık yüzde 90'ı kız bebek. Mikroskopta benzer ama S100 negatif; nüksetmez, hatta kendiliğinden küçülebilir. Patoloğun notu: granüler hücreli tümörün üstündeki epitel olguların yarısına kadarında aşağı doğru uzanan dallar yapar; buna psödoepitelyomatöz hiperplazi diyoruz. Yüzeysel bir parçada bu karsinoma çok benzer ve Neville gereksiz kanser ameliyatı yapılan hastalardan söz ediyor. Biyopsiyi derin alın ve istek formuna 'dil sırtı, ağrısız nodül' yazın; dil sırtı ağız kanserinin olağan yeri değil. Sırada telefon: patolog gibi düşüneceksiniz.")

L.add(title="Patolog gibi düşün", dur=60, theme="dark", q=W5, body=qbody(Q[W5], qsize=34, osize=29),
      notes="Rapor geldi: yüzeyde psödoepitelyomatöz hiperplazi, invaziv karsinom dışlanamadı. Ne yaparsınız? (Sonuç.) Doğru B: derin biyopsiyi tekrarlayın ve formu doldurun. Dil sırtında ağrısız nodül granüler hücreli tümörü düşündürür; altındaki granüler hücreleri görürsem tanı biter. Geniş rezeksiyon bu hastaya yapılabilecek en kötü şey.")

L.add(title="Schwannom, nörofibrom ve NF1", dur=60, strip={2}, dus=True, cred=BOTH,
      body=col(row(ph(n("12.60"), "Schwannom: ağız tabanı"), ph(n("12.61"), "Antoni A, Verocay cisimcikleri"),
                   ph(l("25.43"), "NF1: dil kenarında nörofibrom"), ph(n("12.68"), "Café-au-lait lekeleri"), style="flex:1;min-height:330px"),
               row(box("lilac", "Schwannom", ["Kapsüllü; ağızda en sık dil ve dudak", "Antoni A (palizat, Verocay cisimcikleri) + Antoni B (gevşek)",
                                              "Yaygın S100+; malign dönüşüm yok denecek kadar nadir"], size=27, gap=6, style="flex:1;padding:20px 26px"),
                   box("lilac", "Nörofibrom ve NF1", ["Nörofibrom görürsen hastayı **NF1** için muayene et", "Otozomal dominant; yarısı yeni mutasyon",
                                                      "Café-au-lait, aksiller çillenme, Lisch nodülleri; MPNST riski %8–13"], size=27, gap=6, style="flex:1;padding:20px 26px"))),
      notes="Sinirin iki iyi huylu tümörü. Schwannom kapsüllüdür; ağızda en sık dilde. Mikroskopta iki desen var: Antoni A'da hücre çekirdekleri palizat yapar, aralarındaki pembe alanlara Verocay cisimciği denir; Antoni B gevşek ve miksoiddir. DUS bunu sever. Nörofibrom kapsülsüzdür ve önemli bir soru sordurur: bu hastada NF1 var mı? NF1 otozomal dominant; deride café-au-lait lekeleri, koltuk altında çillenme, gözde Lisch nodülleri. Hastaların yüzde 8 ila 13'ünde malign periferik sinir kılıfı tümörü gelişir; bu yüzden büyüyen ya da ağrıyan bir nörofibrom beklemez.")

L.add(title="MEN 2B: dildeki nöromalar tiroidi haber verir", dur=50, strip={2}, dus=True, cred=NEV,
      body=row(col(row(ph(n("12.74"), "Dil ucunda çok sayıda nöroma"), ph(n("12.73"), "Kalın, çıkık dudaklar", pos="50% 30%"), style="flex:1"),
                   style="flex:0 0 900px"),
               col(bl(["**RET** mutasyonu; otozomal dominant",
                       "Medüller tiroid karsinomu %100 · ağız nöromaları %88 · marfanoid yapı %73 · feokromositoma %50",
                       "Ağız nöromaları çoğu zaman **ilk bulgu**; bebeklikte bile görülebilir",
                       "Tiroidektomi mümkünse ilk yaşta"], size=29, gap=16),
                   box("navy", "Diş hekimi için", ["Dudak ve dil ucunda nodüller, uzun ince yapı: endokrinolojiye yönlendir.",
                                                   "Feokromositoma varsa genel anestezide hipertansif kriz riski."], size=27, gap=8, style="padding:22px 26px"),
                   box("rose", None, ["**Bebeğin melanotik nöroektodermal tümörü:** <1 yaş, üst çene ön bölge, mavi-siyah kitle; idrarda VMA yüksek."], size=26, style="padding:18px 24px"),
                   style="flex:1;gap:14px")),
      notes="Bu slayt bir hayat kurtarabilir. MEN 2B'de dil ucunda, dudaklarda, ağız köşelerinde çok sayıda küçük nöroma olur; dudaklar kalın ve çıkıktır. Neville'e göre ağız nöromaları çoğu zaman hastalığın ilk bulgusu ve bebeklikte bile görülebilir. Arkasındaki tehlike medüller tiroid karsinomu: hastaların hepsinde gelişir. Prognoz ağızdaki bulguların erken tanınmasına bağlı; tiroidektomi mümkünse ilk yaşta yapılır. Yani bu dili ilk gören kişi siz olabilirsiniz. Bir satır da bebeğin melanotik nöroektodermal tümörü: bir yaşın altında, üst çene ön bölgede, mavi-siyah, hızla büyüyen kitle; idrarda vanilmandelik asit yüksek.")

L.add(title="Hemanjiyom mu, vasküler malformasyon mu?", dur=90, strip={2}, dus=True, cred=NEV,
      body=row(col(ph(n("12.93"), "İnfantil hemanjiyom", "4 yaşında çocuk, üst dudak"), ph(n("12.94"), "Venöz malformasyon", "Dil, mor-mavi"), style="flex:0 0 520px"),
               col(div("<table class='t2' style='font-size:25px'>"
                       "<tr><th></th><th>Hemanjiyom (tümör)</th><th>Malformasyon</th></tr>"
                       "<tr><td>Doğumda</td><td>Çoğu yok; ilk haftalarda çıkar</td><td>Var</td></tr>"
                       "<tr><td>Seyir</td><td>Hızlı büyür, sonra geriler: 5 yaşta %50, 9 yaşta %90</td><td>Çocukla birlikte büyür, gerilemez</td></tr>"
                       "<tr><td>GLUT1</td><td>Pozitif</td><td>Negatif</td></tr>"
                       "<tr><td>Bastırınca</td><td>Kan boşalmaz; sert, lastiksi</td><td>Venöz olan kolayca söner</td></tr>"
                       "<tr><td>Tedavi</td><td>Bekle; gerekirse propranolol</td><td>Lazer, skleroterapi, embolizasyon</td></tr></table>"),
                   box("pink", None, ["**Dikkat:** tanısı konmamış kemik içi lezyonda biyopsiden ya da çekimden önce **iğne aspirasyonu** yap. Malformasyonun yanında diş çekiminden sonra ölümcül kanamalar bildirildi."],
                       size=25, style="padding:18px 26px"),
                   div("Sınıflama: ISSVA · vasküler tümör ile vasküler malformasyonu ayırır", "font-size:21px;color:%s" % C["grey"]),
                   style="flex:1;gap:14px"), gap=30),
      notes="Damar lezyonlarında iki ayrı aile var; ISSVA sınıflaması bunu ayırır. Hemanjiyom bir tümör: çoğu doğumda yoktur, ilk haftalarda çıkar, hızla büyür, sonra geriler; yarısı beş yaşında, yüzde 90'ı dokuz yaşında kaybolur. GLUT1 pozitiftir; çoğunu bekleriz, gerekirse propranolol. Malformasyon ise damar yapısının bozukluğu: doğumda vardır, çocukla birlikte büyür ve hiç gerilemez; GLUT1 negatif. Venöz olan mor-mavidir ve bastırınca kolayca söner. Pratik uyarı Neville'den: tanısı konmamış kemik içi bir lezyonda biyopsiden önce iğneyle aspirasyon yapın; malformasyonun yanında diş çekiminden sonra ölümcül kanamalar bildirildi.")

L.add(title="Lenfatik malformasyon, Sturge-Weber, lipom", dur=80, strip={2}, cred=NEV,
      body=col(row(ph(n("12.110"), "Dilde lenfatik malformasyon"), ph(n("12.109"), "Kistik higroma", pos="50% 30%"),
                   ph(n("12.103"), "Sturge-Weber", pos="50% 25%"), ph(n("12.50"), "Lipom (yanak)"), style="flex:1;min-height:330px"),
               row(box("lilac", "Lenfatik malformasyon", ["Eski adı lenfanjiyom (WHO hâlâ 'lymphangioma' der)", "Ağızda en sık dilin ön ⅔'ü: makroglossi; 'kurbağa yumurtası' yüzey",
                                                          "Boyunda kistik higroma: havayolunu tıkayabilir"], size=23, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Sturge-Weber", ["Trigeminal dağılımda porto şarabı lekesi; V1 lekesinde risk %15–20", "Aynı tarafta leptomeninks: nöbet, zihinsel yetersizlik",
                                                 "Ağızda cerrahide ciddi kanama olabilir"], size=23, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Lipom", ["Ağızda en sık yanak ve vestibül (~yarısı)", "Yumuşak, sarımsı; çoğu 40 yaş üstü", "Basit eksizyon; nüks nadir"],
                       size=23, gap=6, style="flex:1;padding:18px 22px"))),
      notes="Üç hızlı tablo. Lenfatik malformasyon, eski adıyla lenfanjiyom: ağızda en sık dilin ön üçte ikisinde; yüzey kurbağa yumurtası gibi küçük kabarcıklarla kaplı, dil büyür. Boyunda büyük kistli formuna kistik higroma deniyor; yenidoğanda havayolunu tıkayabilir. Sturge-Weber: yüzde trigeminal dağılımda porto şarabı lekesi; lekesi birinci dalı tutan çocukların yüzde 15 ila 20'sinde beyin zarında aynı taraflı damar anomalisi, nöbet ve zihinsel yetersizlik. Ağızda o bölgede cerrahi yaparken ciddi kanama olabilir. Lipom: yanakta yumuşak, sarımsı kitle; basit eksizyon.")

L.add(title="Kötü huylu üç hikâye", dur=120, strip={2}, dus=True, cred=BOTH,
      body=col(row(ph(l("39.54"), "Kaposi sarkomu", "Damak ve diş eti"), ph(n("12.142"), "Rabdomiyosarkom", "Çocukta maksillada kitle"),
                   ph(l("39.68"), "Metastaz", "Diş etinde; birincil tümör rektumda"), style="flex:1"),
               row(box("lilac", None, ["**HHV-8**; dört form: klasik, endemik, iatrojenik (nakil), AIDS", "AIDS'li hastaların ~%70'inde ağız lezyonu; en sık sert damak",
                                       "Bastırınca solmaz"], size=26, gap=8, style="flex:1;padding:20px 24px"),
                   box("lilac", None, ["Çocuk yumuşak doku sarkomlarının **yarısı**", "En sık baş-boyun (%26); çoğu embriyonal tip", "Ağız içinde en sık damak"],
                       size=26, gap=8, style="flex:1;padding:20px 24px"),
                   box("rose", None, ["Ağız yumuşak dokusunda en sık **diş eti** (%54)", "Erkekte akciğer (~⅓), kadında meme (~%25)",
                                      "Hastaların %25'inde kanserin **ilk bulgusu**; piyojenik granülom gibi görünebilir"], size=26, gap=8, style="flex:1;padding:20px 24px"))),
      notes="Kötü huylu üç kısa hikâye. Kaposi sarkomu: HHV-8 ile ilişkili; dört formu var: klasik, Afrika'da endemik, organ naklinden sonra iatrojenik ve AIDS'e eşlik eden. AIDS'li hastaların yaklaşık yüzde 70'inde bir noktada ağız lezyonu olur, en sık sert damakta; mor lekeler bastırınca solmaz. Rabdomiyosarkom çocukların sarkomu: çocukluk çağı yumuşak doku sarkomlarının yarısı; en sık baş-boyunda, ağız içinde en sık damakta. Üçüncü hikâye en önemlisi: metastaz. Ağız yumuşak dokusuna gelen metastazların yarısından fazlası diş etine gelir ve piyojenik granülom gibi görünür. Erkekte en sık akciğerden, kadında memeden. Hastaların dörtte birinde ağızdaki lezyon kanserin ilk bulgusu. Dersin başında 'çıkardığın her doku patolojiye' dememin nedeni bu.")

L.add(title="Açılış vakası: doğumdan sonra", dur=30, theme="dark", tag=("pink", "VAKAYA DÖNÜŞ"), cred=NEV,
      body=row(div(bl(["Genç kadın, yedi aylık gebe", "Üst ön diş etinde üç haftada büyüyen, kanayan kitle",
                       "Doğumdan üç ay sonra: kitle **küçüldü**, rengi soldu, sertleşti"], size=36, gap=28), "flex:0 0 860px"),
               col(row(ph(n("12.37"), "Doğumdan önce", pos="50% 45%"), ph(n("12.37_2"), "Doğumdan 3 ay sonra", hl=True, pos="50% 45%"), style="height:380px"),
                   box("yellow", None, html_="<div class='big' style='font-size:38px'>Küçüldü ama kaybolmadı. Tahminin değişti mi?</div>", style="padding:44px 36px"),
                   style="flex:1"), gap=40),
      notes="Hastamız doğurdu. Üç ay sonra kitle küçülmüş, rengi solmuş, sertleşmiş. Hormon etkisi çekilince lezyon olgunlaştı. Şimdi tahmininizi yenileyin; sıradaki slaytta ilk tahminle karşılaştıracağız.")

L.add(title="Vakaya dönüş: şimdi ne diyorsun?", dur=40, theme="dark", q=W6, cred=NEV,
      body=qbody(Q[W6], photo=ph(n("12.37_2"), "Doğumdan 3 ay sonra", pos="50% 45%")),
      notes="Aynı soru, aynı şıklar. Dersin başındaki dağılımı hatırlayın. (İki sonucu yan yana göster.)")

L.add(title="Tanı: gebelik tümörü (piyojenik granülom)", dur=60, cred=NEV,
      body=row(div(steps([("Adres", "Üst ön diş eti: reaktif dörtlünün yeri"),
                          ("Klinik", "Kırmızı, kolay kanayan, hızlı büyüyen; gebelik ve diş taşı"),
                          ("Seyir", "Doğumdan sonra küçüldü ve fibröz olgunlaştı"),
                          ("Mikroskop", "Lobüler kapiller proliferasyon"),
                          ("Yönetim", "Küçülmezse periosta kadar eksizyon + detertraj; doku patolojiye")], size=27), "flex:0 0 1180px"),
               ph(n("12.40"), "Lobüler kapiller damarlar", style="flex:1")),
      notes="Kanıtları sırayla koyalım. Adres: üst ön diş eti. Klinik: kırmızı, kolay kanayan, hızlı büyüyen kitle, gebelik ve diş taşı. Seyir: doğumdan sonra küçüldü, sertleşti; Neville'in fotoğrafı tam bu. Mikroskop: lobüler kapiller damarlar. Yönetim: doğumdan sonra tamamen gerilemezse periosta kadar çıkarın, komşu dişleri temizleyin ve dokuyu mutlaka patolojiye gönderin; diş etindeki her kırmızı kitle piyojenik granülom değildir.")

L.add(title="Eski ad, yeni ad ve atladıklarımız", dur=45, optional=True,
      body=row(col(box("lilac", "Eski ad → güncel ad", None, html_="<table class='t2' style='font-size:26px;border-spacing:0 8px'>"
                       "<tr><td>Piyojenik granülom</td><td>Lobüler kapiller hemanjiyom (WHO 2022)</td></tr>"
                       "<tr><td>Lenfanjiyom</td><td>Lenfatik malformasyon (Neville 5; WHO hâlâ lymphangioma)</td></tr>"
                       "<tr><td>Malign fibröz histiyositom</td><td>İndiferansiye pleomorfik sarkom</td></tr>"
                       "<tr><td>Hemanjiyoperisitom</td><td>Soliter fibröz tümör</td></tr>"
                       "<tr><td>Nazofarengeal anjiyofibrom</td><td>Sinonazal anjiyofibrom (WHO 2022)</td></tr>"
                       "<tr><td>Damar lezyonları</td><td>ISSVA: tümör ile malformasyon ayrı</td></tr></table>", style="padding:22px 26px"), style="flex:1"),
               col(box("rose", "Bugün tek satır", ["**Paraganglioma:** karotis cisimciği; zellballen", "**Olfaktör nöroblastom:** burun tavanı, rozetler",
                                                   "**Alveoler yumuşak doku sarkomu:** çocukta dil ve orbita", "**Sinonazal anjiyofibrom:** ergen erkek, burun kanaması; biyopsi kanatır",
                                                   "**Koristomalar:** dilde kemik ya da kıkırdak (foramen çekum çevresi)", "**Ektomezenkimal kondromiksoid tümör:** dil sırtının ön kısmı",
                                                   "**Fibrohistiyositik tümörler:** ağızda nadir"], size=27, gap=14, style="padding:22px 26px"), style="flex:1")),
      notes="Zaman kalırsa; yoksa atlayın. Solda adı değişenler: piyojenik granülom WHO'da lobüler kapiller hemanjiyom, lenfanjiyom Neville'de lenfatik malformasyon, malign fibröz histiyositom artık indiferansiye pleomorfik sarkom, hemanjiyoperisitomların çoğu soliter fibröz tümör. Sağda bugün yalnız adını andıklarımız; DUS'ta çıkarsa tek satırlık ipucu bu.")

L.add(title="Çıkış bileti", dur=40, theme="dark", q=W7,
      body=div("<div class='live'>CANLI · W7 · Kelime bulutu</div><div class='qq' style='font-size:56px;margin-top:60px;max-width:1500px'>%s</div>"
               "<div style='margin-top:60px;font-size:32px;color:%s'>Tek kelime ya da kısa ifade. En büyük çıkan kelimeyle bir sonraki derse başlıyorum.</div>" % (md(Q[W7]["q"]), C["soft"])),
      notes="Son kelime bulutu. Hangi konu kafanızı karıştırdı? En büyük çıkan kelimeyle hemen sonraki derse, tükürük bezlerine başlayacağım.")

L.add(title="Liderlik tablosu", dur=25, board=True,
      notes="Liderlik tablosu. İlk üçü alkışlayalım. Eşit puanda hızlı olan önde.")

L.add(title="Kaynaklar ve evde tekrar", dur=15,
      body=col(bl(["Neville BW, Damm DD, Allen CM, Chi AC. *Oral and Maxillofacial Pathology.* 5. baskı. Elsevier; 2024. Bölüm 12: Yumuşak doku tümörleri.",
                   "WHO Classification of Tumours Editorial Board. *Head and Neck Tumours.* 5. baskı. IARC; 2022. Bölüm 6 (ağız boşluğu) ve 10 (yumuşak doku).",
                   "Laskaris G. *Color Atlas of Oral Diseases.* 4. baskı. Thieme; 2017. (Klinik fotoğraflar)"], size=30, gap=18),
               box("pink", None, html_="<div class='big' style='font-size:36px'>%s</div>" % md(L.cta), style="padding:30px 34px;margin-top:30px")),
      notes="Kaynaklar burada. 24 Kasım'a kadar Neville'in 12. bölümünü bir kez okuyun; ilk üçü gelecek derste burada anarım. On dakika ara; sonra tükürük bezleri. Telefonlarınızı kapatmayın: aynı adla 'Sıradaki derse geç' düğmesi çıkacak.")

if __name__ == "__main__":
    only = set(int(x) for x in sys.argv[1:]) or None
    L.build(only)
