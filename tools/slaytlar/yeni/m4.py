# -*- coding: utf-8 -*-
"""M4 · Tükürük Bezi Hastalıkları ve Tümörleri (17 Kasım 2026, blok dersin ikincisi, 25 dk)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import *
from foto import F

NEV = "Neville ve ark., *Oral and Maxillofacial Pathology*, 5. baskı (Elsevier, 2024)"
LAS = "Laskaris, *Color Atlas of Oral Diseases*, 4. baskı (Thieme, 2017)"
BOTH = NEV + " · " + LAS
n = lambda k, **kw: F("n", k, **kw)
l = lambda k, **kw: F("l", k, **kw)

L = Lesson("M4", "Tükürük Bezi Hastalıkları ve Tümörleri", "Tükürük Bezi Hastalıkları", "17 Kasım 2026",
           frame="Bez küçüldükçe tehlike büyür; ağızda adres tanıyı daraltır.",
           strip=("Adres", ["1 Hangi bez?", "2 Ağızda nerede?"]),
           cta="24 Kasım'a kadar Neville Bölüm 11'in sonundaki örnek soruları çözün. İlk üçü gelecek derste burada anarım.")

IMG = os.path.join(CANLI, "img")


def save(src, name):
    from PIL import Image
    Image.open(src).convert("RGB").save(os.path.join(IMG, name), quality=88)
    return "img/" + name


def bars(rows, size=26):
    """Range bars on a 0–100 % scale: (label, lo, hi, note, hot)."""
    out = ["<div style='display:flex;flex-direction:column;gap:%dpx'>" % int(size * 1.2)]
    for lab, lo, hi, note, hot in rows:
        col_ = C["pink"] if hot else C["purple"]
        out.append(
            "<div style='display:flex;align-items:center;gap:20px'>"
            "<div style='flex:0 0 230px;font:700 %dpx Lato;color:%s'>%s</div>"
            "<div style='flex:1;height:%dpx;background:%s;border-radius:12px;position:relative'>"
            "<div style='position:absolute;left:%g%%;width:%g%%;top:0;bottom:0;background:%s;border-radius:10px'></div>"
            "<div style='position:absolute;%s;top:50%%;transform:translateY(-50%%);font:900 %dpx Lato;color:%s;white-space:nowrap'>%%%d–%d</div></div>"
            "<div style='flex:0 0 420px;font-size:%dpx;line-height:1.25'>%s</div></div>" % (
                size, col_, E(lab), int(size * 2.4), C["lilac"], lo, hi - lo, col_,
                ("left:calc(%g%% + 14px)" % hi) if hi < 70 else ("left:calc(%g%% + 14px)" % lo), size, col_ if hi < 70 else "#fff", lo, hi, size - 2, md(note)))
    out.append("</div>")
    return "".join(out)


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
W6 = L.q(id="W6", type="MATCH", label="Genetik barkod", scored=True,
         q="Her tümörü kendi gen değişikliğiyle eşleştir.",
         left=["Pleomorfik adenom", "Mukoepidermoid karsinom", "Adenoid kistik karsinom", "Sekretuar karsinom"],
         right=["MYB::NFIB", "ETV6::NTRK3", "PLAG1 / HMGA2", "CRTC1/3::MAML2"],
         key=["PLAG1 / HMGA2", "CRTC1/3::MAML2", "MYB::NFIB", "ETV6::NTRK3"],
         exp="Pleomorfik adenom PLAG1 ya da HMGA2; mukoepidermoid karsinom MAML2 füzyonu; adenoid kistik karsinom MYB::NFIB; sekretuar karsinom ETV6::NTRK3. Patolog küçük biyopside tanıyı bu barkodla doğrular.")
W7 = L.q(id="W7", type="POLL", label="Vakaya dönüş: şimdi ne diyorsun?", q="Dersin başındaki hasta damakta karıncalanma ve uyuşma tarifliyor. Şimdi en olası tanı?",
         scored=False, img="img/m4_vaka.jpg", opts=VAKA_OPTS, a=2, compare="W1")
W8 = L.q(id="W8", type="WORDCLOUD", label="Çıkış bileti", q="Bugün en çok kafanı karıştıran konu hangisiydi? (Tek kelime ya da kısa ifade)", scored=False)
Q = L.qmap

# ---------------- slides ----------------
L.add(title="Tükürük Bezi Hastalıkları ve Tümörleri", dur=60, lobby=True, nonum=True, raw=title_page(
    "4. Sınıf Patoloji  ·  Diş Hekimliği", "Tükürük Bezi Hastalıkları ve Tümörleri", "Bez küçüldükçe tehlike büyür",
    "17 Kasım 2026  ·  Uzm. Dr. M. Olgun Ak", "Sert damakta iki yıldır büyüyen, ağrısız bir kitle.", n("11.77"), NEV),
    notes="Sağdaki deliklere bakın: İsviçre peyniri gibi. Bugünün en sinsi tümörü bu desenle tanınıyor; adını dersin ortasında söyleyeceğim. Katılım ekranı bu slaytta açık. İlk dersten gelenler telefondaki 'Sıradaki derse geç' düğmesine dokunur; tekrar kod okutmak gerekmez. Yeni gelenler için kod perdede. Herkes girince L ile kapatıp başlıyoruz.")

L.add(title="Geçen dersin çıkış bileti", dur=25, cloud={"q": "W7", "from": "prev"},
      notes="Az önceki dersin sonunda en çok kafa karıştıran konuyu sormuştum; en büyük kelime bu. (Bir cümleyle cevapla.) Şimdi tükürük bezleri.")

L.add(title="Açılış vakası: damakta kitle", dur=60, theme="dark", qopen=W1, cred=NEV,
      body=row(div(bl(["45 yaşında kadın", "Sert damakta, orta hattın yanında kitle", "İki yıldır yavaş büyüyor; ağrısız",
                       "Üstündeki mukoza sağlam, ülser yok", "Sert, lastiksi; kemiğe yapışık değil"], size=36, gap=28), "flex:0 0 880px"),
               col(row(ph(n("11.38"), "Sert damak, lateral"), qmark(), style="height:470px"),
                   box("yellow", None, html_="<div class='big' style='font-size:40px'>Tahminini telefondan gir. Cevap dersin sonunda.</div>", style="padding:50px 36px"),
                   style="flex:1"), gap=40),
      notes="Kırk beş yaşında bir kadın. Sert damakta, orta hattın yanında bir kitle; iki yıldır yavaş büyüyor, ağrısı yok, üstündeki mukoza sağlam. Fotoğrafa bakın ve tahmininizi girin; şıklar telefonunuzda açık. Cevabı dersin sonunda açacağım.")

L.add(title="Açılış vakası: tahminin ne?", dur=45, theme="dark", q=W1, cont=True, cred=NEV,
      body=qbody(Q[W1], photo=ph(n("11.38"))),
      notes="Dağılımı gösteriyorum, yorum yok. Beş şıktan biri tümör değil, biri iyi huylu, üçü kötü huylu. Dersin sonunda hastanın söylemediği bir şikâyeti öğreneceğiz.")

L.add(title="Bugünün çerçevesi: bez küçüldükçe tehlike büyür", dur=35, tsize="sm", strip={1}, cred=None,
      body=col(div("<div style='font:700 30px Lora;color:%s;margin-bottom:22px'>Tümörün kötü huylu olma olasılığı</div>" % C["purple"] +
                   bars([("Parotis", 15, 32, "Tümörlerin %61–80'i burada", False),
                         ("Submandibuler", 26, 45, "En sık malign: adenoid kistik karsinom", False),
                         ("Küçük bezler", 38, 54, "En sık yer damak", True),
                         ("Sublingual", 70, 97, "Nadir; ama çoğu malign", True)], size=34)),
               box("navy", None, ["**Önce sor:** şişlik mi, tümör mü? Mukosel, taş, iltihap ve Sjögren tümör değil. **Tümörse:** hangi bez, ağızda nerede?"], size=32, style="padding:22px 30px")),
      notes="Bütün dersi iki soruya bağlıyorum. Bir: bu şişlik bir tümör mü? Mukosel, taş, iltihap, Sjögren tümör değil; önce onları göreceğiz. İki: tümörse adresi ne? Kural Neville'den: bez küçüldükçe kötü huylu olma olasılığı artar. Parotiste tümörlerin üçte biri bile malign değil; küçük bezlerde yaklaşık yarısı; sublingual bezde neredeyse hepsi.")

L.add(title="Mukosel, ranula ve tükürük kanalı kisti", dur=75, cred=BOTH,
      body=col(row(ph(l("14.1"), "Mukosel: alt dudak"), ph(n("11.6"), "Dokuya dökülmüş müsin; epitel yok"), ph(n("11.8"), "Ranula: ağız tabanı"),
                   ph(n("11.10"), "Kanal kisti: Wharton üzerinde"), style="flex:1"),
               row(box("lilac", "Mukosel", ["%82 alt dudak; üst dudakta neredeyse hiç yok", "Ekstravazasyon: **epitel yok**, gerçek kist değil",
                                            "Besleyen küçük bezlerle birlikte çıkar"], size=25, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "Ranula", ["Ağız tabanında mukosel; **sublingual** bezden", "Dalan ranula milohyoidi geçer, boyunda şişlik",
                                           "Tedavi: sublingual bezi çıkar"], size=25, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "Tükürük kanalı kisti", ["**Epitelle döşeli** gerçek kist (retansiyon kisti)", "Erişkin; parotis, ağız tabanı, yanak, dudak",
                                                         "Konservatif eksizyon; nüks etmez"], size=25, gap=6, style="flex:1;padding:20px 24px"))),
      notes="Şişliklerin en sığı mukosel. Alt dudağı ısırırsınız, küçük bir kanal yırtılır, müsin dokuya dökülür. Mikroskopta epitel yok, müsin ve köpüklü makrofajlar var; bu yüzden gerçek kist değil. Neville'in 1715 olguluk serisinde yüzde 82'si alt dudakta, üst dudakta bir tane bile yok; birazdan bu cümleye döneceğim. Tedavide besleyen küçük bezleri de çıkarın, yoksa nükseder. Ağız tabanındaki büyük kardeşi ranula; sublingual bezden gelir, milohyoidi geçerse boyunda şişlik yapar. Tedavi sublingual bezi çıkarmak. Tükürük kanalı kisti ise epitelle döşeli gerçek bir kist; erişkinde görülür.")

L.add(title="Taş ve iltihap", dur=60, cred=BOTH,
      body=col(row(ph(n("11.13"), "Wharton kanalı ağzında taş"), ph(n("11.14"), "Panoramikte radyoopak kitle", fit="cover"),
                   ph(l("15.26"), "Kabakulak: parotis"), ph(l("17.25"), "Stensen kanalından irin"), style="flex:1"),
               row(box("lilac", "Siyalolitiazis", ["**%80 submandibuler:** uzun, yukarı kıvrılan Wharton kanalı, koyu salgı", "Yemekte ağrılı şişlik",
                                                   "Okluzal film; panoramikte kemik içi lezyon sanılabilir; her taş radyoopak değil"], size=25, gap=6, style="flex:1;padding:20px 24px"),
                   box("lilac", "Sialadenit", ["Kabakulak: paramiksovirüs; çoğu iki taraflı parotis", "Akut bakteriyel parotit: akış azalır (sıvı kaybı, ameliyat sonrası, ilaç) ya da kanal tıkanır",
                                               "Masajla Stensen kanalından irin; çoğu *S. aureus*"], size=25, gap=6, style="flex:1;padding:20px 24px"))),
      notes="Taşların yüzde 80'i submandibuler bezde. Nedeni anatomi: Wharton kanalı uzun, yukarı doğru kıvrılıyor ve bezin salgısı daha koyu. Hasta yemekte şişen, ağrıyan bir bezle gelir. Okluzal film en iyi gösterir; panoramikte kemiğin üstüne düşen taş kemik içi lezyon sanılabilir ve her taş radyoopak değildir. İltihapta iki tablo: kabakulak, çoğu iki taraflı parotis; ve akut bakteriyel parotit. Bakteriyel parotit akış azalınca olur: sıvı kaybı, ameliyat sonrası, kuruluk yapan ilaçlar. Bezi masaj yapınca Stensen kanalından irin gelir.")

L.add(title="Sjögren: dudaktan alınan biyopsi", dur=75, dus=True, cred=BOTH,
      body=row(col(row(ph(n("11.25"), "Kuru, fissürlü dil"), ph(l("23.18"), "Parotis büyümesi"), style="flex:1"),
                   row(ph(n("11.29"), "Dudak bezi: lenfosit odakları"), ph(n("11.28"), "Lenfoepitelyal sialadenit"), style="flex:1"), style="flex:0 0 760px"),
               col(box("lilac", "ACR/EULAR 2016: toplam ≥4", None, html_="<table class='t2' style='font-size:24px;border-spacing:0 6px'>"
                       "<tr class='hot'><td>Dudak biyopsisi: odak skoru ≥1/4 mm²</td><td style='text-align:center;font:900 30px Lato'>3</td></tr>"
                       "<tr class='hot'><td>Anti-SSA/Ro pozitif</td><td style='text-align:center;font:900 30px Lato'>3</td></tr>"
                       "<tr><td>Göz boyama skoru ≥5</td><td style='text-align:center;font:900 30px Lato'>1</td></tr>"
                       "<tr><td>Schirmer ≤5 mm/5 dk</td><td style='text-align:center;font:900 30px Lato'>1</td></tr>"
                       "<tr><td>Uyarısız tükürük akışı ≤0,1 mL/dk</td><td style='text-align:center;font:900 30px Lato'>1</td></tr></table>", style="padding:20px 24px"),
                   bl(["K:E 9:1; orta yaş", "Odak = ≥50 lenfosit; normal görünen alt dudaktan ≥5 bez", "Yaşam boyu **lenfoma** riski %5–10 (15–20 kat), çoğu MALT",
                       "Kalıcı parotis büyümesi lenfoma uyarısı"], size=27, gap=10), style="flex:1;gap:16px")),
      notes="Sjögren'de diş hekiminin elinde bir tanı aracı var: dudak biyopsisi. Normal görünen alt dudak mukozasından küçük bir kesiyle en az beş küçük tükürük bezi alınır. Patolog her 4 milimetrekarede en az 50 lenfositlik odak sayar; odak skoru 1 ve üstü 3 puan. Anti-SSA da 3 puan; göz ve tükürük testleri birer puan. Toplam 4 ve üstü primer Sjögren. Hastaların onda dokuzu kadın. Akılda tutun: yaşam boyu lenfoma riski yüzde 5 ila 10, genel nüfusun 15 ila 20 katı; parotis sürekli büyükse beklemeyin. Sırada telefon: puanı siz hesaplayacaksınız.")

L.add(title="Sjögren: puanla", dur=45, theme="dark", q=W2, body=qbody(Q[W2], qsize=34, osize=29),
      notes="Hesaplayın. (Sonuç.) Doğru A: biyopsi 3, Schirmer 1, toplam 4. Anti-SSA negatif olabilir; biyopsi bu yüzden değerli. Ama önce dışlama ölçütlerine bakın; ilki bir sonraki slaytta.")

L.add(title="Sjögren'i taklit edenler: IgG4, siyaladenoz, kserostomi", dur=45, tsize="sm", cred=NEV,
      body=col(row(ph(n("11.23"), "IgG4: iki taraflı submandibuler büyüme"), ph(n("11.24"), "Lenfoplazmositer infiltrat, fibrozis"),
                   ph(n("11.30"), "Siyaladenoz: parotis ve submandibuler"), style="flex:1"),
               row(box("lilac", "IgG4 ilişkili hastalık", ["Çoğu submandibuler; iki taraflı sert şişlik", "IgG4+ plazma hücresi >30–50/BBA, IgG4/IgG >%40",
                                                           "Storiform fibrozis, obliteratif flebit; steroide hızlı yanıt"], size=24, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Siyaladenoz", ["İltihapsız, iki taraflı parotis büyümesi", "Diyabet, alkolizm, bulimia, malnütrisyon"], size=24, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Kserostomi", ["Öznel ağız kuruluğu; en sık neden **ilaçlar**", "Kök çürüğü ve kandida; pilokarpin"], size=24, gap=6, style="flex:1;padding:18px 22px"))),
      notes="Üç taklitçi, tek cümleyle. IgG4 ilişkili hastalık: çoğu iki taraflı, sert submandibuler büyüme; plazma hücreleri IgG4 boyar, fibrozis storiform desen yapar; steroide hızlı yanıt verir ve Sjögren'in dışlama ölçütüdür. Siyaladenoz iltihapsız büyüme: diyabet, alkolizm, bulimia. Kserostomi bir yakınma; en sık nedeni ilaçlar.")

L.add(title="Nekrotizan sialometaplazi: karsinom değil", dur=60, dus=True, cred=BOTH,
      body=col(row(ph(n("11.31"), "Erken: arka damakta şişlik"), ph(n("11.32"), "2–3 hafta sonra: krater ülser"), ph(l("36.3"), "İki taraflı olabilir"),
                   ph(n("11.33"), "Nekroz + duktal skuamöz metaplazi"), style="flex:1"),
               row(box("lilac", None, [">%75 arka damak; ort. 46 yaş, erkekte 2 kat", "İskemi: travma, anestezi iğnesi, protez, yakın cerrahi, bulimia",
                                       "Kendiliğinden iyileşir: Neville ort. 5–6 hafta, WHO 6–10 hafta", "WHO 2022: ağız boşluğu bölümünde"], size=24, gap=6, style="flex:0 0 700px;padding:18px 22px"),
                   pato("Formu boş gönderme", "Duktal skuamöz metaplazi ve PEH, **skuamöz hücreli karsinom** ya da **mukoepidermoid karsinom** sanılabilir. İstek formuna yakın cerrahi, protez, travma, anestezi ve hızlı başlangıcı yaz. İyileşmezse yeniden biyopsi.",
                        size=24, style="flex:1;padding:18px 24px 18px 28px"))),
      notes="Bu dersin patoloğun notu burada. Nekrotizan sialometaplazi küçük bezlerin enfarktı: kan akımı kesilir, bez ölür. Çoğu arka damakta; önce şişlik, iki üç hafta içinde krater gibi bir ülser. Hasta 'damağımın bir parçası düştü' diye gelir. Neden olanlar: travma, anestezi iğnesi, protez, yakın bir ameliyat. Klinikte karsinoma benzer; mikroskopta daha da çok: ölen bezlerin kanalları skuamöz metaplazi yapar ve üstteki epitel aşağı dallanır. Bu tablo skuamöz hücreli karsinom ya da mukoepidermoid karsinom sanılabilir. Benim size ricam: istek formunu boş göndermeyin. 'İki hafta önce bu bölgede anestezi yapıldı', 'yeni protez', 'birden başladı' cümleleri patoloğun karşısındaki en değerli bilgidir. Lezyon kendiliğinden iyileşir; iyileşmezse yeniden biyopsi.")

L.add(title="DUS Molası 1/2", dur=45, theme="dark", q=W3, body=qbody(Q[W3]),
      notes="Neville'in bölüm sonu sorularından. 30 saniye. (Sonuç.) Üst dudak. Bu cümleyi birazdan tümörlerde kullanacağız.")

L.add(title="DUS Molası 2/2", dur=40, theme="dark", q=W4, body=qbody(Q[W4]),
      notes="(Sonuç.) Lenfoma; çoğu MALT. Bu ara tümör dışı bloğu kapatıyor; sırada tümörler.")

L.add(title="Ara liderlik: ilk 5", dur=15, board=True, top=5, notes="On saniye: ilk beş. (→ ile devam.)")

L.add(title="Hangi bez? Sayılar kuralı söylüyor", dur=70, strip={1}, dus=True, cred=None,
      body=col(div("<div style='font:700 30px Lora;color:%s;margin-bottom:22px'>Malign oranı (Neville 5, beş büyük seri)</div>" % C["purple"] +
                   bars([("Parotis", 15, 32, "Tümörlerin %61–80'i; en sık malign MEC", False),
                         ("Submandibuler", 26, 45, "Tümörlerin ~%10'u; en sık malign adenoid kistik karsinom", False),
                         ("Küçük bezler", 38, 54, "Tümörlerin %9–28'i; %42–57'si damakta", True),
                         ("Sublingual", 70, 97, "Tümörlerin ~%1'i", True)], size=31)),
               row(box("navy", None, ["Her bezde **en sık tümör pleomorfik adenom**: parotiste %45–63, küçük bezlerde %33–41."], size=27, style="flex:1;padding:20px 26px"),
                   box("yellow", None, ["**Bez küçüldükçe** malign olasılığı artar (sublingual hariç sıralama)."], size=27, style="flex:1;padding:20px 26px"))),
      notes="Rakamlar Neville'in tablolarından, beş büyük serinin aralığı. Tükürük bezi tümörlerinin çoğu parotiste ve parotis tümörlerinin üçte ikisinden fazlası iyi huylu. Submandibuler bezde malign oranı yaklaşık iki kat, en sık malign tümör adenoid kistik karsinom. Küçük bezlerde yaklaşık yarısı malign; en sık yer damak. Sublingual tümör nadirdir ama gördüğünüzde neredeyse hep malign. Her bezde en sık tümör yine pleomorfik adenom.")

L.add(title="Ağızda nerede? Mukosel alt dudağı, tümör üst dudağı sever", dur=60, tsize="xs", strip={2}, dus=True, cred=BOTH,
      body=row(div("<table class='t2' style='font-size:26px'>"
                   "<tr><th>Küçük bez tümörü</th><th>Malign oranı</th><th>Not</th></tr>"
                   "<tr><td>Üst dudak</td><td>%9–25</td><td>Sık; çoğu kanaliküler adenom</td></tr>"
                   "<tr><td>Yanak</td><td>%30–59</td><td></td></tr>"
                   "<tr><td>Damak</td><td>%41–51</td><td>En sık yer; arka-lateral sert damak</td></tr>"
                   "<tr class='hot'><td>Alt dudak</td><td>%43–86</td><td>Nadir; çoğu mukoepidermoid karsinom</td></tr>"
                   "<tr class='hot'><td>Dil · ağız tabanı</td><td>%60–89</td><td>Çoğu malign</td></tr>"
                   "<tr class='hot'><td>Retromolar</td><td>%88–95</td><td>Çoğu mukoepidermoid karsinom</td></tr></table>", "flex:0 0 1100px"),
               col(ph(n("11.50"), "Kanaliküler adenom: üst dudak"), ph(l("39.29"), "Mukoepidermoid karsinom: retromolar"), style="flex:1")),
      notes="Ağızdaki adres de konuşur. Mukoselin tersine, tümör üst dudağı sever; üst dudak tümörlerinin yalnızca dörtte biri ya da daha azı malign, çünkü çoğu kanaliküler adenom. Alt dudakta tümör nadirdir ama çıkarsa yarıdan fazlası malign, çoğu mukoepidermoid karsinom. Dil, ağız tabanı ve retromolar bölgede tümörlerin büyük çoğunluğu malign. Damak ortada: yaklaşık yarı yarıya; bu yüzden açılış vakamız zor bir vaka.")

L.add(title="Pleomorfik adenom: karışık tümör", dur=85, strip={1, 2}, dus=True, cred=NEV,
      body=row(col(row(ph(n("11.34"), "Parotis: kulak altında nodül"), ph(n("11.38"), "Damak, orta hattın yanında"), style="flex:1"),
                   row(ph(n("11.40"), "Kapsüllü, sınırlı kitle"), ph(n("11.43"), "Kondroid madde + epitel"), style="flex:1"), style="flex:0 0 800px"),
               col(bl(["En sık tükürük bezi tümörü; her bezde ilk sırada", "Yavaş büyüyen, ağrısız, sert kitle; hasta yıllarca bekler",
                       "Mikroskop: duktus + miyoepitel + miksoid/kondroid 'stroma'; hücreler pleomorfik değil, **yapı** karışık",
                       "Kapsül eksik ya da delik olabilir (WHO: psödopodlar; tek başına malignite bulgusu değil)",
                       "**Enükleasyon yapma:** tümör yatağına ekilir, nükseder; parotiste yüzeyel parotidektomi",
                       "Malign dönüşüm %3–4'e kadar; süre uzadıkça artar", "PLAG1 / HMGA2"], size=28, gap=16), style="flex:1")),
      notes="En sık tümör, eski adıyla benign miks tümör. Adındaki pleomorfizm hücrelerin değil yapının: kanallar, miyoepitel hücreleri ve bu hücrelerin yaptığı miksoid ya da kıkırdak benzeri bir zemin bir arada. Klinikte yavaş büyüyen, ağrısız, sert bir kitle; parotiste kulak altında, ağızda damakta orta hattın yanında. Kapsül eksik olabilir ve tümör küçük çıkıntılarla kapsülün dışına uzanır. Bu yüzden enükleasyon yapılmaz: tümör yatağına ekilir ve çok odaklı nükseder. Uzun süre bırakılırsa yüzde 3 ila 4'üne kadar malign dönüşür ve risk süreyle artar; buna karsinom ex pleomorfik adenom diyoruz.")

L.add(title="Warthin tümörü: sigara ve parotis kuyruğu", dur=55, strip={1}, cred=NEV,
      body=row(ph(n("11.47"), "Parotis kuyruğunda kitle", pos="50% 30%", style="flex:0 0 420px"),
               col(ph(n("11.48"), "Papiller kistik yapı + lenfoid stroma"), ph(n("11.49"), "İki sıra onkositik epitel"), style="flex:0 0 520px"),
               col(bl(["Neredeyse yalnız parotis; kuyruk bölümü", "Sigara içende **8 kat** risk; 6.–7. dekat", "%5–17 iki taraflı",
                       "Eskiden erkek tümörü; kadınlar sigara içtikçe oran eşitleniyor", "Eski adı papiller kistadenoma lenfomatozum (WHO önermiyor)"], size=31, gap=24), style="flex:1")),
      notes="Parotisin ikinci sık tümörü. Neredeyse yalnız parotiste, mandibula açısının hemen üstünde, kuyruk bölümünde. Sigarayla en güçlü ilişkili tükürük bezi tümörü: risk sekiz kat. Yüzde 5 ila 17'si iki taraflı. Eskiden erkek tümörü denirdi; kadınlar sigara içtikçe oran eşitlendi. Mikroskopta görüntü unutulmaz: iki sıra pembe onkositik hücre ve altında germinal merkezli lenfoid doku.")

L.add(title="Üç iyi huylu tümör, birer cümle", dur=45, strip={1, 2}, cred=NEV,
      body=col(row(ph(n("11.50"), "Kanaliküler adenom"), ph(n("11.51"), "Kanal benzeri hücre dizileri"), ph(n("11.52"), "Bazal hücreli adenom"), style="flex:1"),
               row(box("lilac", "Kanaliküler adenom", ["Neredeyse yalnız küçük bezler; **üst dudakta %66–78**", "7. dekat; kadında biraz sık; mukosel sanılabilir"], size=25, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Bazal hücreli adenom", ["%75'i parotis; 7. dekat", "Bazaloid hücreler; CTNNB1 mutasyonu"], size=25, gap=6, style="flex:1;padding:18px 22px"),
                   box("lilac", "Onkositom", ["Tümörlerin ~%1'i; %85–90'ı parotis", "Mitokondriyle dolu onkositler"], size=25, gap=6, style="flex:1;padding:18px 22px"))),
      notes="Üç küçük iyi huylu tümör. Kanaliküler adenom üst dudağın tümörü; yaşlı hastada mavimsi bir nodül olarak gelir ve mukosel sanılabilir. Bazal hücreli adenom çoğunlukla parotiste. Onkositom nadir, çoğu parotiste. Eskiden 'monomorfik adenom' diye bir torba vardı; artık bu ad önerilmiyor. Sırada telefon: üst dudakta bir nodül.")

L.add(title="Üst dudakta nodül", dur=45, theme="dark", q=W5, body=qbody(Q[W5], qsize=40),
      notes="(Sonuç.) Doğru B: kanaliküler adenom. İki ipucu: üst dudak ve yaş. Mukosel üst dudakta neredeyse hiç olmaz; DUS sorusunu hatırlayın.")

L.add(title="Mukoepidermoid karsinom: en sık malign", dur=75, strip={1, 2}, dus=True, cred=BOTH,
      body=row(col(row(ph(n("11.57"), "Damakta mavimsi kitle"), ph(l("39.29"), "Retromolar bölge"), style="flex:1"),
                   row(ph(n("11.60"), "Mukus hücreleri, kistik alan"), ph(n("11.64"), "Santral MEC: arka mandibula"), style="flex:1"), style="flex:0 0 800px"),
               col(bl(["En sık malign tükürük bezi tümörü; **çocukta da** en sık", "Mukus, epidermoid ve ara hücreler; düşük derecede kistler ve bol mukus hücresi",
                       "Derece prognozu belirler: 5 yıllık sağkalım düşük %90, orta %86, yüksek %55 (WHO)",
                       "Mavi-kırmızı olunca **mukosel** sanılabilir", "Santral MEC: en sık kemik içi tükürük bezi tümörü; arka mandibula, çoğu kadın",
                       "CRTC1/3::MAML2"], size=28, gap=18), style="flex:1")),
      notes="En sık malign tükürük bezi tümörü ve çocukta da en sık malign tümör. Adı hücrelerinden: mukus hücreleri, epidermoid hücreler ve aradaki ara hücreler. Düşük dereceli tümörde kistler ve bol mukus hücresi var; yüksek dereceli olan solid ve skuamöz hücreli karsinoma benzer. Prognozu derece belirler: düşük ve orta derecede beş yıllık sağkalım yüzde 90 dolayında, yüksek derecede yarı yarıya. Ağızda mavi-kırmızı olunca mukosel sanılır. Bir de kemik içinde görülür: santral mukoepidermoid karsinom, en sık kemik içi tükürük bezi tümörü, arka mandibulada çok gözlü radyolüsensi.")

L.add(title="Adenoid kistik karsinom: sinirin peşinde", dur=75, strip={1, 2}, dus=True, cred=NEV,
      body=row(col(ph(n("11.74"), "Damakta silik bir şişlik"), row(ph(n("11.77"), "Kribriform: İsviçre peyniri"), ph(n("11.79"), "Perinöral invazyon"), style="flex:1"),
                   style="flex:0 0 800px"),
               col(bl(["Kribriform, tübüler ve solid desen; solid en kötü", "**Perinöral invazyon:** ağrı ve uyuşma; şişlikten önce ağrı olabilir",
                       "Submandibuler bezin en sık malign tümörü", "Lenf nodu metastazı az; **geç akciğer** metastazı sık",
                       "Sağkalım: 5 yıl %68–89, 20 yıl %25–40: 5 yıl şifa demek değil", "MYB::NFIB"], size=30, gap=22), style="flex:1")),
      notes="Başlık slaytındaki delikler bu tümörün. Kribriform desen, İsviçre peyniri gibi. Bu tümör sinirleri sever: sinir kılıfı boyunca ilerler ve kafa tabanına kadar gidebilir. Bu yüzden hasta şişlikten önce ağrı ya da uyuşma tarif edebilir. Submandibuler bezin en sık malign tümörü. Lenf noduna az gider ama yıllar sonra akciğere gider. Neville'in cümlesi: beş yıllık sağkalım bu tümörde şifa demek değil; yirmi yılda hastaların yarısından fazlası kaybedilir.")

L.add(title="Dört isim daha: PAC, asinik, ex PA, sekretuar", dur=75, tsize="sm", strip={1, 2}, cred=NEV,
      body=col(row(ph(n("11.80"), "Polimorf adenokarsinom: damak"), ph(n("11.66"), "Asinik hücreli karsinom"), ph(n("11.71"), "Karsinom ex PA: damak"),
                   ph(n("11.68"), "Sekretuar karsinom: yanak"), style="flex:1"),
               row(box("lilac", "Polimorf adenokarsinom", ["Neredeyse yalnız küçük bezler; %65 damak; ⅔ kadın", "Tek sıra hücre dizileri; perinöral; prognoz iyi",
                                                           "Eski adı PLGA; PRKD1"], size=22, gap=6, style="flex:1;padding:16px 20px"),
                   box("lilac", "Asinik hücreli karsinom", ["%85–90 parotis", "PAS+, diastaza dirençli zimojen granüller (WHO)", "NR4A3; prognoz iyi"], size=22, gap=6, style="flex:1;padding:16px 20px"),
                   box("rose", "Karsinom ex PA", ["Yıllardır duran kitle **hızla büyümeye** başlarsa", "Hasta PA'dan 10–15 yaş büyük",
                                                  "WHO 2022: invazyon ≥6 mm invaziv"], size=22, gap=6, style="flex:1;padding:16px 20px"),
                   box("lilac", "Sekretuar karsinom", ["ETV6::NTRK3; memenin sekretuar karsinomuna benzer", "TRK inhibitörleri için olası hedef (WHO: geliştiriliyor)"],
                       size=22, gap=6, style="flex:1;padding:16px 20px"))),
      notes="Dört isim, birer cümle. Polimorf adenokarsinom neredeyse yalnız küçük bezlerde, çoğu damakta; eski adı düşük dereceli polimorf adenokarsinom. Perinöral invazyon yapar ama prognozu iyi. Asinik hücreli karsinom parotiste; hücreleri seröz asinüs hücresine benzer. Karsinom ex pleomorfik adenom: yıllardır duran bir kitle birden hızla büyümeye başlarsa. Sekretuar karsinom ETV6::NTRK3 füzyonu taşır; WHO bu füzyonun TRK inhibitörleri için bir hedef olabileceğini söylüyor. Sırada telefon: genetik barkod.")

L.add(title="Genetik barkod", dur=60, theme="dark", q=W6,
      body=div("<div class='live'>CANLI · W6 · Eşleştirme</div><div class='qq'>%s</div>" % md(Q[W6]["q"]) +
               row(col(*[box("navy2", None, [x], size=32, style="padding:22px 28px") for x in Q[W6]["left"]], gap=16, style="flex:1"),
                   col(*[box("navy2", None, [x], size=32, style="padding:22px 28px;font-family:monospace") for x in Q[W6]["right"]], gap=16, style="flex:1"),
                   gap=60, style="margin-top:40px")),
      notes="Telefonda dört tümör, dört gen. Eşleştirin. (Sonuç.) Pleomorfik adenom PLAG1 ya da HMGA2; mukoepidermoid karsinom MAML2; adenoid kistik karsinom MYB::NFIB; sekretuar karsinom ETV6::NTRK3. Neden önemli? Küçük bir biyopside patolog tanıyı bu barkodla doğruluyor.")

L.add(title="Açılış vakası: hastanın söylemediği", dur=30, theme="dark", tag=("pink", "VAKAYA DÖNÜŞ"), cred=NEV,
      body=row(div(bl(["45 yaşında kadın", "Sert damakta, orta hattın yanında kitle", "İki yıldır yavaş büyüyor; mukoza sağlam",
                       "Son iki ayda damakta **karıncalanma ve uyuşma**"], size=36, gap=28), "flex:0 0 880px"),
               col(row(ph(n("11.38"), "Sert damak, lateral"), qmark("Bu bulgu ne anlatıyor?"), style="height:470px"),
                   box("yellow", None, html_="<div class='big' style='font-size:38px'>Yeni bulgu: karıncalanma. Tahminin değişti mi?</div>", style="padding:44px 36px"),
                   style="flex:1"), gap=40),
      notes="Hasta başta söylemedi: son iki ayda damağında karıncalanma ve uyuşma var. Bu bir sinir bulgusu. Şimdi tahmininizi yenileyin.")

L.add(title="Vakaya dönüş: şimdi ne diyorsun?", dur=40, theme="dark", q=W7, cred=NEV,
      body=qbody(Q[W7], qsize=36, photo=ph(n("11.38"))),
      notes="Aynı şıklar. Dersin başındaki dağılımı hatırlayın. (İki sonucu yan yana göster.)")

L.add(title="En olası: adenoid kistik karsinom", dur=40, cred=NEV,
      body=row(div(steps([("Adres", "Sert damak, lateral: küçük bezlerin en sık yeri; yaklaşık yarısı malign"),
                          ("Klinik", "Yavaş büyüyen, ağrısız, sağlam mukoza: pleomorfik adenom gibi"),
                          ("Yeni bulgu", "Karıncalanma, uyuşma: perinöral invazyon"),
                          ("Biyopsi", "İnsizyonel; kribriform yapı ve perinöral invazyon tanıyı koyar"),
                          ("Yönetim", "Geniş cerrahi ± radyoterapi; geç akciğer metastazı için uzun takip")], size=27), "flex:0 0 1180px"),
               ph(n("11.79"), "Perinöral invazyon", style="flex:1")),
      notes="Kanıtlar: adres damak, küçük bez; tümörlerin yaklaşık yarısı malign. Klinik pleomorfik adenomu düşündürüyordu ve en olası tanı oydu. Ama karıncalanma ve uyuşma sinir tutulumu demek; damakta bu adenoid kistik karsinomu, daha az olasılıkla polimorf adenokarsinomu düşündürür. Tanıyı insizyonel biyopsi koyar. Bu hastayı yirmi yıl izleyeceğiz.")

L.add(title="Eski ad, yeni ad: WHO 2022", dur=45, optional=True,
      body=row(col(box("lilac", "Eski ad → güncel ad", None, html_="<table class='t2' style='font-size:25px;border-spacing:0 8px'>"
                       "<tr><td>Polimorf düşük dereceli adenokarsinom</td><td>Polimorf adenokarsinom (eski ad hâlâ kabul edilir)</td></tr>"
                       "<tr><td>Papiller kistadenoma lenfomatozum</td><td>Warthin tümörü</td></tr>"
                       "<tr><td>Benign lenfoepitelyal lezyon</td><td>Lenfoepitelyal sialadenit</td></tr>"
                       "<tr><td>Malign miks tümör</td><td>Karsinom ex pleomorfik adenom</td></tr>"
                       "<tr><td>Monomorfik adenom</td><td>Önerilmiyor: kanaliküler / bazal hücreli adenom</td></tr>"
                       "<tr><td>MASC</td><td>Sekretuar karsinom</td></tr></table>", style="padding:22px 26px"), style="flex:1"),
               col(box("rose", "WHO 2022'de yeni", ["**Malign:** mikrosekretuar adenokarsinom, sklerozan mikrokistik adenokarsinom",
                                                    "**Benign:** keratokistom, interkale kanal adenomu, çizgili kanal adenomu",
                                                    "Sklerozan polikistik adenom artık benign tümör", "Sitoloji için **Milan sistemi** öneriliyor"], size=27, gap=14, style="padding:22px 26px"),
                   style="flex:1")),
      notes="Zaman kalırsa; yoksa atlayın. Solda adı değişenler. Sağda WHO 2022'nin getirdikleri: iki yeni malign, üç yeni benign tümör; sklerozan polikistik adenom benign tümörler arasına alındı; ince iğne sitolojisinde Milan sistemi öneriliyor.")

L.add(title="Çıkış bileti", dur=35, theme="dark", q=W8,
      body=div("<div class='live'>CANLI · W8 · Kelime bulutu</div><div class='qq' style='font-size:56px;margin-top:60px;max-width:1500px'>%s</div>"
               "<div style='margin-top:60px;font-size:32px;color:%s'>Tek kelime ya da kısa ifade. En büyük çıkan kelimeyle 24 Kasım'da başlıyorum.</div>" % (md(Q[W8]["q"]), C["soft"])),
      notes="Son kelime bulutu. Hangi konu kafanızı karıştırdı? En büyük kelimeyle 24 Kasım'da başlayacağım.")

L.add(title="Liderlik tablosu", dur=20, board=True, notes="Liderlik tablosu. İlk üçü alkışlayalım. Eşit puanda hızlı olan önde.")

L.add(title="Kaynaklar ve evde tekrar", dur=10,
      body=col(bl(["Neville BW, Damm DD, Allen CM, Chi AC. *Oral and Maxillofacial Pathology.* 5. baskı. Elsevier; 2024. Bölüm 11: Tükürük bezi patolojisi.",
                   "WHO Classification of Tumours Editorial Board. *Head and Neck Tumours.* 5. baskı. IARC; 2022. Bölüm 5 (tükürük bezleri) ve 6 (ağız boşluğu).",
                   "Shiboski CH ve ark. 2016 ACR/EULAR primer Sjögren sınıflama ölçütleri. *Arthritis Rheumatol.* 2017;69:35–45.",
                   "Laskaris G. *Color Atlas of Oral Diseases.* 4. baskı. Thieme; 2017. (Klinik fotoğraflar)"], size=30, gap=18),
               box("pink", None, html_="<div class='big' style='font-size:36px'>%s</div>" % md(L.cta), style="padding:30px 34px;margin-top:30px")),
      notes="Kaynaklar burada. 24 Kasım'a kadar Neville'in bölüm sonundaki örnek soruları bir kez çözün; ilk üçü gelecek derste burada anarım.")

if __name__ == "__main__":
    only = set(int(x) for x in sys.argv[1:]) or None
    L.build(only)
