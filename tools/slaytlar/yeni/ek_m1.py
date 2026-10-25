# -*- coding: utf-8 -*-
"""M1'e eklenen "Zaman kalırsa" slaytları (Neville 5. baskı; ders sunumundaki eksik başlıklar)."""
from deck import *
from foto import F

SHORT = "Mukozal Hastalıklar 1"
VER = "4"
NEV = "Neville ve ark., *Oral and Maxillofacial Pathology*, 5. baskı (Elsevier, 2024)"
LAS = "Laskaris, *Color Atlas of Oral Diseases*, 4. baskı (Thieme, 2017)"
n = lambda k: F("n", k)
l = lambda k: F("l", k)
ANCHOR = "Akılda kalacak beş cümle"


def cards(photos, boxes, size=22, extra=None):
    kids = [row(*photos, style="flex:1"), row(*[box("lilac", t, ls, size=size, gap=5, style="flex:1;padding:16px 20px") for t, ls in boxes])]
    if extra:
        kids.append(extra)
    return col(*kids, gap=16)


def table(head, rows, size=22, hot=()):
    h = "<tr>" + "".join("<th>%s</th>" % E(x) for x in head) + "</tr>"
    b = "".join("<tr%s>%s</tr>" % (" class='hot'" if i in hot else "", "".join("<td>%s</td>" % md(c) for c in r)) for i, r in enumerate(rows))
    return "<table class='t2' style='font-size:%dpx;border-spacing:0 6px'>%s%s</table>" % (size, h, b)


SLIDES = [
 dict(before=ANCHOR, title="Elementer lezyonlar: muayenenin dili", dur=45,
      body=row(div(table(["Lezyon", "Tanım"], [
                   ["Makül (leke)", "<1 cm, mukozayla aynı düzeyde düz renk değişikliği"], ["Yama (patch)", ">1 cm makül"],
                   ["Papül", "<1 cm kabarık, solid"], ["Nodül", ">1 cm kabarık, solid"], ["Plak", ">1 cm, hafif kabarık, yüzeyi geniş"],
                   ["Püstül", "İçinde püy olan kabarık lezyon"]], size=31), "flex:1"),
               div(table(["Lezyon", "Tanım"], [
                   ["Vezikül", "<1 cm, içi şeffaf sıvı dolu kabarcık"], ["Bül", ">1 cm vezikül"], ["Erozyon", "Epitelin yüzeyel kaybı"],
                   ["Ülser", "Epitelin **tam kat** kaybı; bağ dokusu açıkta"], ["Fissür", "Epitelde çizgisel çatlak"], ["Ekskoriasyon", "Epitelin soyulması"]], size=31)
                   + box("yellow", None, ["**Ağızda bül neredeyse hiç sağlam yakalanmaz:** çatı patlar, geriye erozyon ve ülser kalır. Pemfigusta çatı ince; pemfigoidde subepitelyal ve daha kalın."],
                         size=28, style="margin-top:20px;padding:22px 26px"), "flex:1"), gap=30),
      notes="Raporda ve sınavda kullandığımız kelimeler. Eşik bir santimetre: makül ve vezikül bir santimden küçük, yama ve bül büyük; papül küçük, nodül büyük kabarıklık. Erozyon epitelin yüzeyel kaybı, ülser tam kat kaybı. (Not: Neville bu tanımlar için eşik vermiyor; bazı dermatoloji kaynakları 0,5 cm kullanır. Ders notlarındaki 1 cm eşiğini kullanıyoruz.) Pratik ipucu: ağızda bül sağlam kalmaz; ülser görünce 'bu önce kabarcık mıydı?' diye sorun."),
 dict(before=ANCHOR, title="Muayenede yardımcı bulgular", dur=55, cred=NEV + " · " + LAS,
      body=row(col(ph(n("9.13"), "Paterji: 24–48 saatte steril püstül"), ph(l("26.30"), "Sürtünmeyle epitel soyuluyor"), style="flex:0 0 560px"),
               div(table(["Bulgu", "Nasıl", "Ne düşündürür"], [
                   ["Nikolsky", "Normal görünen mukozaya yana doğru sıkı basınç → bül ya da soyulma", "**Pemfigus vulgaris**; pemfigoidde de epitel kolay soyulur"],
                   ["Paterji", "Steril iğne deriye oblik batırılır; 24–48 saatte papül ya da **steril püstül**", "**Behçet** (Orta Doğu'da ~%60 pozitif)"],
                   ["Koebner", "Travma bölgesinde yeni lezyon çıkması", "Psoriazis, liken planus, lupus"],
                   ["Yama (patch) testi", "Şüpheli madde deriye kapalı uygulanır", "Kontakt alerji; amalgam likenoid reaksiyonunda %70'e kadar (+)"],
                   ["Bastırınca solma", "Cam ya da parmakla bas", "Solarsa kan damar içinde: vasküler lezyon; solmazsa kanama"],
                   ["Silinme", "Gazlı bez ya da spatülle sil", "Silinir: kandida, yanık; silinmez: lökoplaki, liken planus"]], size=22), "flex:1"), gap=30),
      notes="Altı küçük test. Nikolsky: normal görünen mukozaya yana doğru bastırınca epitel kayıyor ya da bül çıkıyorsa pemfigus. Paterji: steril iğneyle deriye batırılır, bir iki gün sonra papül ya da steril püstül çıkarsa pozitif; Behçet'in ölçütlerinden biri, bizim coğrafyada sık pozitif. Koebner: travma bölgesinde yeni lezyon; psoriazis ve liken planusta tarif edilir (Neville metninde tanımlanmıyor). Yama testi kontakt alerjiyi gösterir; amalgama komşu likenoid reaksiyonda yüzde 70'e kadar pozitif. Bastırınca soluyorsa kan damarın içinde; solmuyorsa damar dışına çıkmış, yani kanama. Silinen beyaz kandida ya da yanık; silinmeyen lökoplaki ya da liken planus. Hiçbiri tek başına tanı koymaz; sizi doğru biyopsiye götürür."),
 dict(before=ANCHOR, title="Enfeksiyonlar ağızda iz bırakır", dur=55, cred=NEV,
      body=col(row(ph(n("7.29"), "Kızamık: Koplik lekeleri"), ph(n("5.5"), "Kızıl: beyaz çilek dil"), ph(n("5.10"), "Sekonder sifiliz: mukoz plak"),
                   ph(n("5.33"), "Noma"), style="flex:1"),
               div(table(["Hastalık", "Ağızda", "İpucu"], [
                   ["Kızamık", "Bukkal mukozada mavi-beyaz 'tuz taneleri' (**Koplik**)", "Döküntüden **önce** çıkar"],
                   ["Kızıl", "Önce **beyaz**, 4–5. günde **kırmızı çilek dil**; damakta peteşi", "A grubu streptokok; 3–12 yaş"],
                   ["Sifiliz", "Primer: **ağrısız**, temiz tabanlı şankr (en sık dudak); sekonder: **mukoz plak**; tersiyer: gumma, damak perforasyonu", "Spiroket boyası; VDRL ilk haftalarda negatif olabilir"],
                   ["Difteri", "Tonsil ve damakta **yapışık gri psödomembran**; kaldırınca kanar", "Antitoksin ilk 48 saatte"],
                   ["Noma", "Nekrotizan gingivitle başlar, yanağı delen gangren", "Beslenmesi bozuk çocuk; en sık öncül kızamık"]], size=21)), gap=14),
      notes="Ağız çocukluk enfeksiyonlarının vitrini. Kızamıkta döküntüden önce yanakta mavi-beyaz noktalar çıkar: Koplik lekeleri. Kızılda önce beyaz, sonra kırmızı çilek dil. Sifilizde primer şankr ağrısız, temiz tabanlı bir ülserdir; sekonder evrenin ağız lezyonu mukoz plaktır; tersiyer evrede damakta gumma ve perforasyon. (Not: bazı ders notlarında 'aftöz şankr' yazar; Neville'e göre şankr ağrısızdır ve yalnız primer evrededir.) Difteride tonsil ve damakta yapışık gri zar; kaldırmaya çalışınca kanar. Noma ise kızamıklı, beslenmesi bozuk çocukta nekrotizan diş eti iltihabıyla başlayıp yanağı delen bir gangren."),
 dict(before=ANCHOR, title="Granülom yapan şişlik ve ülserler", dur=55, cred=NEV,
      body=cards([ph(n("9.20"), "Orofasiyal granülomatoz: dudak"), ph(n("9.17"), "Sarkoidoz: sıkı granülomlar"),
                  ph(n("5.21"), "Tüberküloz: dilde ülser"), ph(n("9.26"), "GPA (Wegener): çilek dişeti")],
                 [("Orofasiyal granülomatoz", ["En sık dudakta ağrısız, kalıcı şişlik; yanakta kaldırım taşı", "**Melkersson-Rosenthal:** dudak şişliği + yüz felci + fissürlü dil",
                                              "Crohn'u araştır: ağız bulgusu bağırsaktan önce çıkabilir"]),
                  ("Sarkoidoz", ["Ağızda en sık bukkal mukoza", "**Nekrozsuz**, sıkı epiteloid granülom; Schaumann, asteroid cisimcik", "Serum ACE yalnız ~%60'ında yüksek"]),
                  ("Tüberküloz", ["Ağız lezyonu nadir; **en sık dilde** kronik ülser", "**Kazeifiye** granülom, Langhans dev hücresi", "Ülser + lenf nodu: karsinom sanılabilir"]),
                  ("Granülomatozis polianjiitis", ["**Çilek dişeti:** kanayan granüler hiperplazi; çoğu kez böbrekten önce", "Vaskülit + dev hücre; PR3-ANCA (c-ANCA)"])],
                 extra=box("navy", None, ["**Rapor 'granülomatöz inflamasyon' diyorsa iş bitmedi:** tüberküloz, mantar ve yabancı cismi dışla (özel boyalar, polarize ışık), sonra Crohn ve sarkoidozu araştır."],
                           size=24, style="padding:16px 24px")),
      notes="Granülom bir tanı değil, bir yanıt. Orofasiyal granülomatoz en sık dudakta ağrısız, kalıcı bir şişlik yapar; dudak şişliği, yüz felci ve fissürlü dil birlikteyse Melkersson-Rosenthal sendromu. Bu hastalarda Crohn'u mutlaka sorun; ağız bulgusu bağırsaktan önce çıkabilir. Sarkoidozda granülomlar sıkı ve nekrozsuz. Tüberkülozda ağız lezyonu nadirdir, en sık dilde kronik bir ülser; mikroskopta kazeifikasyon. Granülomatozis polianjiitiste, eski adıyla Wegener, dişeti çilek gibi kırmızı ve granülerdir; bu bulgu böbrek tutulumundan önce gelebilir, yani hastanın hayatını siz kurtarabilirsiniz. Patolog granülom yazdıysa organizma ve yabancı cisim mutlaka dışlanmalı."),
 dict(before=ANCHOR, title="İlaç ve temas reaksiyonları", dur=55, cred=NEV,
      body=cards([ph(n("9.50"), "ACE inhibitörü anjiyoödemi"), ph(n("9.36"), "Likenoid ilaç reaksiyonu"),
                  ph(n("9.42"), "Tarçına bağlı kontakt stomatit"), ph(n("9.48"), "Amalgama komşu likenoid lezyon")],
                 [("ACE inhibitörü anjiyoödemi", ["Bradikinin aracılı: **antihistaminiğe yanıt vermez**", "Yıllarca kullanılan ilaçla bile çıkabilir; diş tedavisi tetikleyebilir",
                                                 "Dil ve ağız tabanı tutulursa havayolu acili"]),
                  ("Likenoid ilaç reaksiyonu", ["ACE inhibitörleri, antimalaryaller, β-blokerler, NSAİİ, allopurinol…", "Aylar ya da yıllar sonra başlar; DİF ayırt ettirmez",
                                                "Lupus benzeri reaksiyon: ANA ve anti-histon (+)"]),
                  ("Alerjik kontakt stomatit", ["Gerçek ağız alerjisi nadir; en sık yakınma **yanma**", "**Tarçın** (sakız, diş macunu): yanakta beyaz zeminli eritem",
                                                "Bırakınca ~1 haftada geçer, yeniden kullanınca 24 saatte döner"]),
                  ("Amalgam teması", ["Lezyon dolguya komşu, iki taraflı değil", "Yama testi %70'e kadar (+); dolguyu değiştirince geriler"])]),
      notes="İlaç ve temas reaksiyonları diş hekimini doğrudan ilgilendirir. ACE inhibitörü anjiyoödemi alerjik değildir, bradikinin birikir; bu yüzden antihistaminik işe yaramaz. Yıllardır aynı ilacı kullanan hastada bile çıkabilir ve diş tedavisi tetikleyebilir; dil ve ağız tabanı şişerse havayolu acili. Likenoid ilaç reaksiyonu liken planusa benzer; ilacı sorun. Lupus benzeri ilaç reaksiyonunda anti-histon pozitif. Gerçek kontakt alerji nadirdir; en sık yakınma yanmadır. Tarçınlı sakız ya da diş macunu yanakta beyaz zeminli kırmızılık yapar; ürünü bırakınca bir haftada geçer. Amalgama komşu likenoid lezyon dolguya değer, iki taraflı değildir; dolguyu değiştirince geriler."),
 dict(before=ANCHOR, title="Liken planus patoloğun gözüyle", dur=55, cred=NEV,
      body=row(col(ph(n("16.101"), "Testere dişi reteler, bant infiltrat"), ph(n("16.102_2"), "Bazal tabaka yıkımı, lenfosit göçü"), style="flex:0 0 640px"),
               col(bl(["Hiperkeratoz ya da parakeratoz; reteler **sivri, testere dişi**",
                       "Bazal tabakada **hidropik (vakuoler) dejenerasyon**",
                       "Hemen altında **bant tarzında T lenfosit** infiltratı",
                       "Arayüzde ölmüş keratinositler: **Civatte (kolloid) cisimcikleri**",
                       "DİF: bazal membran boyunca tüylü **fibrinojen** bandı (spesifik değil)"], size=27, gap=12),
                   pato("'Liken planus ile uyumlu' ne demek?", ["Aynı tabloyu likenoid ilaç reaksiyonu, amalgam teması, GVHD, lupus ve erken proliferatif verrüköz lökoplaki da verir. Patolog bu yüzden 'uyumlu' yazar; ayırımı öyküyle sen yaparsın.",
                                                                "Malign dönüşüm: Neville rakam vermiyor, risk 'varsa küçük'; tek ve kalıcı erozyon biyopsiye gider."], size=23),
                   style="flex:1;gap:16px"), gap=30),
      notes="Liken planusu mikroskopta beş bulguyla tanırız: sivri, testere dişi reteler; bazal tabakada vakuoler dejenerasyon; hemen altında bant gibi T lenfosit infiltratı; arayüzde ölmüş keratinositler, yani Civatte cisimcikleri; ve immünofloresanda bazal membran boyunca tüylü fibrinojen. Ama bu bir reaksiyon kalıbı: likenoid ilaç reaksiyonu, amalgam teması, GVHD, lupus aynı resmi verebilir. Bu yüzden raporda 'liken planus ile uyumlu' görürsünüz. Malign dönüşüm tartışmalı: bazı ders notlarında yüzde 2,5 geçer; Neville rakam vermiyor ve riskin varsa küçük olduğunu söylüyor. Kalıcı, tek bir erozyon ya da plak biyopsiye gider."),
 dict(before=ANCHOR, title="Büllöz hastalıklar: yarık nerede, floresan ne diyor?", tsize="sm", dur=60, cred=None,
      body=div(table(["Hastalık", "Ayrışma düzeyi", "DİF", "Akılda kalsın"], [
                   ["Pemfigus vulgaris", "Epitel içi, **suprabazal**; mezar taşı, Tzanck", "Hücreler arası **ağ** (IgG, C3)", "Ağız ilk bulgu; Dsg3"],
                   ["Pemfigus foliaseus", "Epitel içi, **yüzeyel**", "Hücreler arası", "Yalnız Dsg1: **ağız korunur**"],
                   ["Paraneoplastik pemfigus", "Epitel içi + subepitelyal, likenoid", "Hücreler arası ± bazal membran", "Lenfoma, KLL; ağır ağız ülserleri"],
                   ["Müköz membran pemfigoidi", "**Subepitelyal**", "Bazal membranda **lineer** IgG, C3", "Deskuamatif gingivit; skar **gözde**"],
                   ["Büllöz pemfigoid", "Subepitelyal; bülde eozinofil", "Lineer IgG, C3", "Yaşlı; deri ön planda; ağız %10–20"],
                   ["Lineer IgA dermatozu", "Subepitelyal", "Bazal membranda lineer **yalnız IgA**", "Çoğu deri; ilaç sonrası olabilir"],
                   ["Dermatitis herpetiformis", "Subepitelyal; papillada nötrofil mikroapsesi", "Papilla uçlarında **granüler IgA**", "Gluten, çölyak; dapson"],
                   ["(Liken planus)", "Ayrışma yok; bazal yıkım", "Tüylü fibrinojen", "Karşılaştırma için"]], size=25, hot=(0, 3)),
               "display:flex;flex-direction:column;justify-content:center;height:100%"),
      notes="Bütün büllöz hastalıkları tek tabloya koyalım; M1'in 3D çerçevesi burada da işliyor: düzey ve desen. Pemfigus ailesinde yarık epitelin içinde, floresan ağ şeklinde. Foliaseusta yalnız desmoglein 1'e antikor var; ağızda desmoglein 1 az olduğu için ağız korunur. Paraneoplastik pemfigus lenfoma ya da kronik lenfositik lösemiyle gelir, ağız ülserleri çok ağırdır. Pemfigoid ailesinde yarık epitelin altında, floresan çizgi. Müköz membran pemfigoidinde asıl skar gözde; büllöz pemfigoid yaşlı hastada deriyi tutar, ağız yüzde 10 ila 20. Lineer IgA dermatozunda çizgi yalnız IgA'dan oluşur; dermatitis herpetiformiste IgA papilla uçlarında granüler, hasta glutene duyarlı. (Not: dermatitis herpetiformis Neville 5'te ayrı başlık olarak yok; bilgiler ders notlarından.)"),
 dict(before=ANCHOR, title="Pemfigus ve pemfigoidin akrabaları", dur=50, cred=NEV + " · " + LAS,
      body=cards([ph(n("16.60"), "Paraneoplastik pemfigus"), ph(n("16.74"), "Büllöz pemfigoid: damakta"),
                  ph(l("26.38"), "Lineer IgA: bukkal bül"), ph(l("26.44"), "Dermatitis herpetiformis")],
                 [("Paraneoplastik pemfigus", ["Lenfoma, KLL, Castleman; ~⅓'ünde tümör henüz bilinmiyor", "Yaygın ağrılı ülser, EM benzeri dudak kabukları",
                                              "Bronşiolitis obliterans; mortalite %60–90"]),
                  ("Büllöz pemfigoid", ["En sık otoimmün bül hastalığı; 75–80 yaş", "Kaşıntı, sonra gergin büller; skarsız iyileşir", "BP180/BP230 (hemidesmozom)"]),
                  ("Lineer IgA dermatozu", ["Bazal membranda lineer yalnız IgA", "Çoğunlukla deri; mukozada skar yapabilir"]),
                  ("Dermatitis herpetiformis", ["Gluten duyarlılığı, çölyak", "Papillada nötrofil mikroapsesi, granüler IgA", "Glutensiz diyet, dapson"])]),
      notes="Dört akraba. Paraneoplastik pemfigus ağır ağız ülserleri ve dudak kabuklarıyla gelir; hastaların üçte birinde altta yatan lenfoma henüz bilinmiyordur, yani ağız tanıyı ilk koyabilir. Büllöz pemfigoid yaşlıların hastalığı: önce kaşıntı, sonra gergin büller, skarsız iyileşme. Lineer IgA dermatozu ve dermatitis herpetiformis deri ağırlıklıdır; birincide IgA çizgi, ikincide papillalarda granüler; ikincisinde glutensiz diyet ve dapson."),
 dict(before=ANCHOR, title="Deriden ağza: psoriazis, lupus, skleroderma, GVHD", tsize="sm", dur=55, cred=NEV,
      body=cards([ph(n("16.113"), "Psoriazis: damakta"), ph(n("16.116"), "SLE: likenoid bukkal ülser"),
                  ph(n("16.126"), "Skleroderma: periodontal aralık"), ph(n("16.109"), "GVHD: likenoid lezyon")],
                 [("Psoriazis", ["Parakeratoz, uzamış reteler, **Munro mikroapsesi**", "Ağız lezyonu **nadir** ve tartışmalı", "Coğrafik dil psoriazislilerde biraz daha sık"]),
                  ("Sistemik lupus", ["Ağız lezyonu %5–25: damak, yanak, dişeti", "LP'ye benzer; ayıran: bazal membranda **PAS (+)** kalınlaşma, derin perivasküler infiltrat",
                                      "DİF: bazal membranda granüler IgG, IgM, C3"]),
                  ("Sistemik skleroz", ["Mikrostomi: ~%70'inde ağız açıklığı kısıtlı", "Röntgende **yaygın periodontal aralık genişlemesi**; %10–20'sinde ramus/kondil rezorpsiyonu"]),
                  ("GVHD", ["Allojenik nakil sonrası; kronikte ağız tutulumu ≥%80", "LP benzeri çizgiler, kserostomi, yüzeyel mukoseller"])]),
      notes="Deri hastalıklarının ağızdaki izleri. Psoriazisin mikroskobunda parakeratoz içinde nötrofil kümeleri var, Munro mikroapsesi; ama ağız lezyonu nadirdir ve tartışmalıdır. (Not: ders notlarındaki Kogoj püstülü ve Auspitz bulgusu deri bulgularıdır; Neville'de geçmiyor.) Coğrafik dil psoriazislilerde biraz daha sık. Lupusun ağız lezyonu liken planusa benzer; ayıran bulgu bazal membranda PAS pozitif kalınlaşma ve daha derine inen, damar çevresi infiltrat. Sistemik sklerozda ağız daralır; periapikal filmde bütün dişlerde periodontal aralık genişlemişse ve ağız üç parmak açılmıyorsa sklerodermayı düşünün. GVHD nakil sonrası liken planus gibi görünür; kronik formda hastaların çoğunda ağız tutulur."),
]
