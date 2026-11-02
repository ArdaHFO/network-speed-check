Bu proje, dosya aktarımı ve bağlantı isteklerinin sürelerini inceleyerek internet hızını ölçmeyi araştırır.

<h1 align="center">Network Speed Lab</h1>

<p align="center"><strong>Ağ ölçümlerini tarayıcının iki tarafından incele.</strong></p>
<p align="center">Tarayıcı istek sürelerini, sunucu tarafındaki dosya aktarımını ve speedtest-cli ölçümlerini bir araya getiren Python ve Flask deneyi.</p>

<p align="center">
  <a href="README.md">English</a> · <strong>Türkçe</strong><br />
  <a href="#yerel-olarak-çalıştır"><strong>Yerel olarak çalıştır</strong></a> ·
  <a href="#ölçüm-yolları">Ölçüm yolları</a> ·
  <a href="#doğrulama-ve-mevcut-sınırlar">Mevcut sınırlar</a>
</p>

---

Bu proje bağlantı ölçümü için iki yaklaşımı inceler. Tarayıcı sayfası HTTP isteklerinin süresini ölçerken ayrı bir Flask rotası dosya aktarımını, speedtest-cli sonuçlarını ve sistem ping komutunu birleştirir. İki yaklaşım, ölçümün yapıldığı konumun, aktarılan bayt sayısının ve zamanlama yönteminin önemini gösterir.

**Proje deneysel bir prototiptir.** Aktarım yollarına ve hesaplara statik düzeltmeler uygulandı. Uçtan uca davranış ve ölçüm doğruluğu henüz doğrulanmadı. Arayüz ağırlıklı olarak İngilizcedir. Belgeler İngilizce ve Türkçe sunulur.

## Yerel olarak çalıştır

| Gereksinim | Amaç |
| --- | --- |
| pip ve venv içeren Python 3 | Yalıtılmış geliştirme ortamı |
| Flask 3.0.0 | Web rotaları ve şablonlar |
| Requests 2.31.0 ve speedtest-cli 2.1.3 | Sunucunun içe aktardığı bağımlılıklar |
| Güncel tarayıcı | JavaScript istek zamanlaması |

Kaynağı klonla ve yeni bir ortam oluştur.

```text
git clone https://github.com/ArdaHFO/network-speed-lab.git
cd network-speed-lab
python -m venv .venv
```

Windows Komut İstemi'nde `.venv\Scripts\activate`, macOS/Linux'ta `source .venv/bin/activate` ile ortamı etkinleştir. Doğrudan çalışma zamanı bağımlılıklarını kur ve yerel önizlemeyi başlat.

```text
python -m pip install Flask==3.0.0 requests==2.31.0 speedtest-cli==2.1.3
python -m flask --app app run --host 127.0.0.1 --port 8000
```

[localhost:8000](http://127.0.0.1:8000) adresini aç. Bu komutlar aktarım testi başlatmadan arayüzü sunar. Daha kapsamlı [requirements.txt](requirements.txt), geçmiş geliştirme ortamının kaydıdır. Repodaki `Scripts/` klasörü ortama özgü çalıştırılabilir dosyalar içerdiğinden yeni oluşturulan ortamı kullan.

## Projede neler var?

- **Tarayıcıda indirme süresi.** Bir düğme paketlenmiş aktarım dosyasını ister ve alınan bayt sayısından hız hesaplar.
- **Dosya yükleme deneyi.** Dosya seçici multipart isteği gönderir. Sunucu uygulama dosyası kaydetmeden alınan bayt sayısını doğrular.
- **HTTP gidiş-dönüş süresi.** Ping düğmesi `/ping` isteğinin süresini ölçer.
- **Sunucu tarafında karşılaştırma.** `POST /measure`, sabit boyutlu indirme, harici yankı hizmetine yükleme, speedtest-cli sonuçları ve sistem ping komutunu birleştirir.
- **Ayrı sonuç ekranı.** Sunucu ölçümleri ve sunucu konumu bilgileri Jinja şablonunda gösterilir.

## Ölçüm yolları

| Yol | Davranış | Ölçüm konumu |
| --- | --- | --- |
| `GET /` | Tarayıcı arayüzünü gösterir | Tarayıcı |
| `GET /ping` | `Pong` döndürür | Tarayıcıdan Flask'a HTTP isteği |
| `GET /download` | Paketlenmiş `20MB.png` dosyasını önbelleksiz sunar | Flask'tan tarayıcıya |
| `POST /upload` | Uygulama dosyası kaydetmeden alınan baytları sayar | Tarayıcıdan Flask'a |
| `POST /measure` | Aktarım, speedtest-cli ve sistem ping işlemleri yapar | Flask'ı çalıştıran makine |
| `GET /views/` | Aynı arayüze alternatif giriş | Tarayıcı |

Uzak bir Flask kurulumu, yerel kurulumdan farklı ağ yolunu ölçer. Sunucu tarafındaki rota sunucunun bağlantısını ölçer ve ziyaretçinin internet bağlantısını doğrudan temsil etmez. Tarayıcıdaki “Ping”, ICMP ölçümü değil HTTP gidiş-dönüş süresidir.

## Doğrulama ve mevcut sınırlar

Kaynak statik olarak incelendi. Bu değişiklikler için uygulama, otomatik test, ağ ölçümü veya performans deneyi çalıştırılmadı.

- Tarayıcı zamanlaması artık başarılı HTTP yanıtlarını, gerçek bayt sayısını, geçen saniyeyi ve ondalık Mbps dönüşümünü kullanır. İndirme ve ping yanıtlarında önbellekleme kapatılır. Bu düzeltmeler tarayıcıda denenmedi.
- Tarayıcı indirmesi paketlenmiş `20MB.png` dosyasını kullanır. Ölçülen yol tarayıcı ile bu Flask sunucusu arasındadır. Yerel önizleme internet sağlayıcısının bant genişliğini ölçmez.
- Yükleme istekleri multipart ek yükü dahil 32 MiB ile sınırlıdır. İşleyici dosya baytlarını saymak için tüketir ve kalıcı bir uygulama dosyası kaydetmez.
- Sunucu yükleme hızı, istek ve yanıt süresini birlikte içerir. HTTP işleme, ağ koşulları ve uzak hizmetler gözlenen değeri etkiler.
- İsteğe bağlı sunucu ölçüm rotası hâlâ harici aktarım hizmetlerini ve speedtest-cli kullanır. Formunun gönderme düğmesi yorum satırındadır. Sağlayıcıların güncel erişilebilirliği iddia edilmez.
- Sistem ping çıktısı işletim sistemine bağlı kalır. Komutlarda ve özel HTTP isteklerinde süre sınırları vardır, ancak harici hizmet akışının tamamı doğrulanmadı.

Hızlar `bayt × 8 / saniye / 1.000.000` olarak hesaplanır. Anlamlı performans raporu için kontrollü dosyalar, tekrarlar ve ölçülen ağ yolunun açıkça belirtilmesi gerekir.

## Proje yapısı

```text
app.py                 Flask rotaları ve sunucu ölçümleri
views.py               Ek sayfa rotaları
templates/index.html   Tarayıcı kontrolleri ve JavaScript zamanlaması
templates/measure.html Sunucu sonuç ekranı
5MB.png, 10MB.png,
20MB.png               Aktarım örnek dosyaları
requirements.txt       Geçmiş bağımlılık kaydı
Scripts/               Repoya eklenmiş eski Python ortamı
```

## Geliştirme ve katkı

Değişikliklerde tarayıcı ve sunucu ölçümlerini açıkça ayır. Hata bildirimine işletim sistemi, Python sürümü, istenen rota, HTTP durum kodu ve ilgili hesabı ekle. Doğrulamanın statik inceleme, yerel HTTP testi veya gerçek aktarım ölçümü olduğunu belirt.

Rota ve hesaplar için yalıtılmış testler ile kontrollü bir sunucuya karşı tekrarlanabilir ölçümler yararlı sonraki adımlardır.

## Lisans ve kaynaklar

[MIT lisansı](LICENSE) ile dağıtılır. Harici uç noktalar ve speedtest-cli, kendi koşulları ve erişilebilirlikleri olan ayrı hizmetler ve bağımlılıklardır.
