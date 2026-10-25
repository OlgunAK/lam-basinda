# -*- coding: utf-8 -*-
"""M2'ye eklenen "Zaman kalırsa" slaytları: kalıtsal hastalıklar ve dil (Neville 5. baskı)."""
from deck import *
from foto import F

SHORT = "Mukozal Hastalıklar 2 ve Dil"
VER = "4"
NEV = "Neville ve ark., *Oral and Maxillofacial Pathology*, 5. baskı (Elsevier, 2024)"
LAS = "Laskaris, *Color Atlas of Oral Diseases*, 4. baskı (Thieme, 2017)"
n = lambda k: F("n", k)
l = lambda k: F("l", k)
ANCHOR = "Akılda kalacak beş cümle"


def cards4(photos, boxes, size=22):
    return col(row(*photos, style="flex:1"), row(*[box("lilac", t, ls, size=size, gap=5, style="flex:1;padding:16px 20px") for t, ls in boxes]))


SLIDES = [
 dict(before=ANCHOR, title="Kalıtsal beyaz lezyonlar: çocukluktan beri silinmeyen beyaz", tsize="sm", dur=60, cred=NEV,
      body=cards4([ph(n("16.4"), "Beyaz süngerimsi nevüs"), ph(n("16.7"), "Pap: perinükleer kondansasyon"),
                   ph(n("16.11"), "Pakioniki: tübüler tırnak"), ph(n("16.15"), "Diskeratozis konj.: lökoplaki")],
                  [("Beyaz süngerimsi nevüs", ["OD; **KRT4/KRT13**", "İki taraflı bukkal, kalın, kıvrımlı beyaz plak; ağrısız",
                                               "Spinöz hücrelerde berraklaşma, perinükleer eozinofilik kondansasyon (keratin tonofilamenti)", "Tedavi gerekmez"]),
                   ("Herediter benign intraepitelyal diskeratoz", ["OD; ağızda WSN benzeri plak", "Gözde bulber konjonktivada **jelatinöz plak**",
                                                                   "Mikroskopta 'hücre içinde hücre' diskeratozu"]),
                   ("Pakioniki konjenita", ["Genellikle OD; KRT6A/6B/16/17", "Kalınlaşmış, tübüler tırnaklar; avuç-taban hiperkeratozu",
                                            "Dil kenarı ve sırtında beyaz plak; malign dönüşüm yok"]),
                   ("Diskeratozis konjenita", ["Çoğu X'e bağlı resesif (**DKC1**); telomer hastalığı", "Üçlü: ağ şeklinde deri pigmentasyonu, tırnak distrofisi, **lökoplaki**",
                                               "Lökoplakilerin ~⅓'ü 10–30 yılda malign; aplastik anemi (~%80)"])]),
      notes="Çocukluktan beri olan, iki taraflı, silinmeyen beyaz plak görürseniz kalıtsal bir keratin hastalığını düşünün. Beyaz süngerimsi nevüs otozomal dominant, keratin 4 ya da 13 mutasyonu; yanakta kalın, kıvrımlı beyaz plak, ağrısız, tedavi gerekmez. Mikroskopta spinöz hücreler berrak, yüzeye yakın hücrelerde çekirdek çevresinde pembe bir yoğunlaşma var; Neville bunun keratin tonofilamenti yumağı olduğunu ve Papanicolaou yaymasında daha iyi göründüğünü söylüyor. (Not: bazı kaynaklar bu yapıya Odland cismi diyor; Neville bu terimi kullanmıyor.) Herediter benign intraepitelyal diskeratozda ağız aynı, farkı gözde jelatinöz plaklar. Pakioniki konjenitada tırnaklar kalın, tüp gibi; ağızda dil kenarında beyaz plak ama kanserleşmez. Diskeratozis konjenita farklı: tırnak distrofisi, ağ şeklinde deri pigmentasyonu ve lökoplaki; bu lökoplakinin yaklaşık üçte biri on ila otuz yılda kanserleşir ve hastaların çoğunda kemik iliği yetmezliği gelişir."),
 dict(before=ANCHOR, title="Darier hastalığı ve siğilli diskeratom: bazalin üstünde yarık", tsize="sm", dur=50, cred=NEV,
      body=col(row(ph(n("16.23"), "Darier: damakta papüller"), ph(n("16.24"), "Keratin tıkacı, suprabazal yarık"),
                   ph(n("16.25"), "Siğilli diskeratom: krette papül"), ph(n("16.26"), "Aynı histoloji, tek lezyon"), style="flex:1"),
               row(box("lilac", "Darier hastalığı", ["OD; **ATP2A2** → SERCA2: **hücre içi** kalsiyum pompası; desmozomlar dağılır",
                                                     "Deride seboreik bölgelerde kaşıntılı, keratinli papüller; yazın kötüleşir",
                                                     "Ağız tutulumu %15–50: damak ve alveolde 'kaldırım taşı' papüller; papiller hiperplazi ya da nikotinik stomatit sanılır",
                                                     "Histoloji: suprabazal akantoliz, 'deney tüpü' reteler; **corps ronds** (yuvarlak) ve **grains** (tahıl tanesi) diskeratotik hücreleri"],
                       size=22, gap=5, style="flex:1.4;padding:16px 20px"),
                   box("lilac", "Siğilli diskeratom", ["Tek lezyon; 40 yaş üstü", "Keratinize mukozada (sert damak, alveol kreti) göbekli papül; çoğu <0,5 cm",
                                                       "Darier'le aynı görünüm: tıkaç dolu invajinasyon + suprabazal yarık", "Eksizyon; nüks ve malignite yok"],
                       size=22, gap=5, style="flex:1;padding:16px 20px"))),
      notes="Pemfigusta gördüğümüz suprabazal yarığın kalıtsal bir kuzeni: Darier hastalığı. Otozomal dominant; ATP2A2 geni hücre içindeki kalsiyum pompası SERCA2'yi kodlar, desmozomlar dağılır ve epitel bazal tabakanın üstünden ayrılır. (Bazı ders notlarında 'hücreler arası kalsiyum transportu' yazar; Neville hücre içi pompa diyor.) Ağızda damak ve alveolde küçük beyaz papüller birleşip kaldırım taşı görünümü verir; papiller hiperplazi ya da nikotinik stomatitle karışır. Mikroskopta iki tip ölmüş hücre: yuvarlak olanlar corps ronds, tahıl tanesine benzeyenler grains. Aynı tablonun tek bir lezyonda görüleni siğilli diskeratom: keratinize mukozada ortası çökük küçük papül, basit eksizyon yeterli."),
 dict(before=ANCHOR, title="Ağızda iz bırakan sendromlar (1/2)", dur=50, cred=NEV + " · " + LAS,
      body=cards4([ph(n("16.16"), "Kseroderma pigmentozum", pos="50% 30%"), ph(n("16.21"), "İnkontinensiya pigmenti: konik dişler"),
                   ph(n("16.29"), "HHT: dilde telanjiektazi"), ph(n("16.34"), "Ehlers-Danlos: Gorlin bulgusu")],
                  [("Kseroderma pigmentozum", ["OR; DNA eksizyon onarımı bozuk (UV)", "20 yaşından önce **alt dudak ve dil ucunda SKK**"]),
                   ("İnkontinensiya pigmenti", ["X'e bağlı dominant (IKBKG/NEMO); erkekte çoğu letal", "%70–95'inde hipodonti, **konik dişler**; deride girdap pigmentasyon"]),
                   ("Herediter hemorajik telanjiektazi", ["OD (ENG, ACVRL1)", "Dudak, dil, yanakta bastırınca solan kırmızı papüller; ilk bulgu çoğu kez burun kanaması",
                                                         "AVM varsa invaziv işlemde antibiyotik profilaksisi"]),
                   ("Ehlers-Danlos", ["Heterojen; klasik tip OD (COL5A1/2)", "**Gorlin bulgusu**: dil ucu burna değer (%50)", "Periodontal tipte erken, ağır periodontit"])]),
      notes="Bu sendromların çoğunda tanıyı ilk düşünecek kişi diş hekimi olabilir. Kseroderma pigmentozumda UV hasarı onarılamaz; yirmi yaşından önce alt dudakta ve dil ucunda skuamöz hücreli karsinom görülür. İnkontinensiya pigmentinde konik dişler ve diş eksikliği; deride girdap şeklinde pigmentasyon. Herediter hemorajik telanjiektazide dudak ve dilde bastırınca solan küçük kırmızı noktalar, sık burun kanaması; akciğer ya da beyinde arteriyovenöz malformasyon varsa kanamalı işlemlerden önce antibiyotik profilaksisi. Ehlers-Danlos'ta Gorlin bulgusu: hastaların yarısı dil ucuyla burun ucuna dokunabilir; periodontal tipte genç yaşta ağır periodontit."),
 dict(before=ANCHOR, title="Ağızda iz bırakan sendromlar (2/2)", dur=50, cred=NEV + " · " + LAS,
      body=cards4([ph(l("25.54"), "Tüberoz skleroz: dişeti fibromları"), ph(n("16.41"), "Cowden: dil ve krette papüller"),
                   ph(n("16.46"), "Epidermolizis bülloza: mikrostomi"), ph(n("16.28"), "Peutz-Jeghers: dudakta çiller")],
                  [("Tüberoz skleroz", ["OD; TSC1/TSC2 (mTOR)", "Ön dişlerde **mine çukurcukları** (%50–100), dişetinde fibröz papüller", "Yüzde anjiyofibrom, nöbet"]),
                   ("Cowden (PTEN hamartom)", ["OD; **PTEN**", "Dişeti, dil, yanakta çok sayıda papül (>%80)", "**Meme kanseri** %25–50, tiroid kanseri ~%14"]),
                   ("Epidermolizis bülloza", ["Keratin 5/14, laminin-332, kollajen VII…", "Her lokmada bül, sonra skar, **mikrostomi**, ankiloglossi, yaygın çürük"]),
                   ("Peutz-Jeghers", ["OD; STK11", "Dudakta çil benzeri lekeler + hamartomatöz polipler; kanser riski"])]),
      notes="İkinci grup. Tüberoz sklerozda ön dişlerin labial yüzünde mine çukurcukları ve dişette fibröz papüller; yüzde anjiyofibromlar, nöbet. Cowden sendromunda dişeti ve dilde çok sayıda küçük papül; PTEN mutasyonu ve meme kanseri riski çok yüksek, bu yüzden ağızdaki papüller hastayı kurtarabilir. Epidermolizis büllozada her lokmada bül, iyileşirken skar; ağız daralır, dil yapışır, çürük yaygınlaşır. Peutz-Jeghers'i derste görmüştük: dudakta çil gibi lekeler ve bağırsakta polipler."),
 dict(before=ANCHOR, title="Dil: fissürlü dil, amiloidoz ve kıllı dil", dur=60, cred=NEV + " · " + LAS,
      body=cards4([ph(n("1.22"), "Fissürlü dil"), ph(n("9.21"), "Melkersson-Rosenthal'de fissürlü dil"),
                   ph(l("30.2"), "Amiloidoz: büyük, nodüler dil"), ph(n("17.10"), "Kongo kırmızısı: elma yeşili")],
                  [("Fissürlü (skrotal) dil", ["Dil sırtında 2–6 mm derin oluklar; sıklık %2–5, yaşla artar", "**Coğrafik dille** sık birlikte; Melkersson-Rosenthal'in bileşeni",
                                               "Tedavi gerekmez; dili fırçala"]),
                   ("Dilde amiloidoz", ["AL tipte makroglossi %10–40; kenarı diş izli büyük dil", "Olguların %15–20'si **multipl miyelom**",
                                        "Kongo kırmızısı + polarize ışıkta **elma yeşili**; miyelomu araştır"]),
                   ("Kıllı dil", ["Filiform papillalarda keratin birikir; sirkumvallat papillaların önünde orta hat",
                                  "Sigara, kötü hijyen, kserostomi, antibiyotik; benign", "Kıllı lökoplakiyle (EBV) karıştırma"]),
                   ("Dil SKK", ["Ağız içinde en sık yer dil", "⅔'ü posterior lateral kenarda; dil sırtında yalnız %4"])]),
      notes="Dile hızlı bir tur. Fissürlü dil sık bir varyasyon: dil sırtında derin oluklar, yaşla artar; coğrafik dille sık birlikte görülür ve Melkersson-Rosenthal sendromunun, yani dudak şişliği ve yüz felciyle birlikte, bir bileşenidir. Oluklarda artık birikir, dili fırçalamasını söyleyin. Yaşlı bir hastada kenarları diş izli, büyük, sert bir dil görürseniz amiloidozu düşünün: Kongo kırmızısıyla boyanır, polarize ışıkta elma yeşili çift kırılma verir; sonra miyelomu araştırın. Kıllı dilde filiform papillalar keratin biriktirip uzar; sigara, kötü hijyen, ağız kuruluğu. Benigndir; AIDS'le ilişkili olan isim benzerliği olan kıllı lökoplakidir. (Not: bazı ders notlarındaki 'papilla 1 cm'ye ulaşır' ve 'kanserle birlikte görülür' bilgileri Neville 5'te yok.) Dil kanserinin üçte ikisi arka lateral kenarda, dil sırtında yalnızca yüzde 4."),
]
