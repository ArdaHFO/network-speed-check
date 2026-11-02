<h1 align="center">Speedtest</h1>

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

**Proje deneysel bir prototiptir.** Bazı ölçüm ve yükleme yolları, çıktıları doğru hız sonuçları olarak kullanılmadan önce düzeltilmelidir. Arayüz ağırlıklı olarak İngilizcedir ve bazı yükleme yanıtları Türkçedir. Belgeler İngilizce ve Türkçe sunulur.

## Yerel olarak çalıştır

| Gereksinim | Amaç |
| --- | --- |
| pip ve venv içeren Python 3 | Yalıtılmış geliştirme ortamı |
| Flask 3.0.0 | Web rotaları ve şablonlar |
| Requests 2.31.0 ve speedtest-cli 2.1.3 | Sunucunun içe aktardığı bağımlılıklar |
| Güncel tarayıcı | JavaScript istek zamanlaması |

Kaynağı klonla ve yeni bir ortam oluştur.

```text
git clone https://github.com/ArdaHFO/speedtest.git
cd speedtest
python -m venv .venv
```

Windows Komut İstemi'nde `.venv\Scripts\activate`, macOS/Linux'ta `source .venv/bin/activate` ile ortamı etkinleştir. Doğrudan çalışma zamanı bağımlılıklarını kur ve yerel önizlemeyi başlat.

```text
python -m pip install Flask==3.0.0 requests==2.31.0 speedtest-cli==2.1.3
python -m flask --app app run --host 127.0.0.1 --port 8000
```

[localhost:8000](http://127.0.0.1:8000) adresini aç. Bu komutlar aktarım testi başlatmadan arayüzü sunar. Daha kapsamlı [requirements.txt](requirements.txt), geçmiş geliştirme ortamının kaydıdır. Repodaki `Scripts/` klasörü ortama özgü çalıştırılabilir dosyalar içerdiğinden yeni oluşturulan ortamı kullan.

## Projede neler var?

- **Tarayıcıda indirme süresi.** Bir düğme uzak görseli ister ve hesaplanan hızı gösterir.
- **Dosya yükleme deneyi.** Dosya seçici, Flask sunucusuna multipart isteği gönderir.
- **HTTP gidiş-dönüş süresi.** Ping düğmesi `/ping` isteğinin süresini ölçer.
- **Sunucu tarafında karşılaştırma.** `POST /measure`, sabit boyutlu indirme, harici yankı hizmetine yükleme, speedtest-cli sonuçları ve sistem ping komutunu birleştirir.
- **Ayrı sonuç ekranı.** Sunucu ölçümleri ve sunucu konumu bilgileri Jinja şablonunda gösterilir.

## Ölçüm yolları

| Yol | Davranış | Ölçüm konumu |
| --- | --- | --- |
| `GET /` | Tarayıcı arayüzünü gösterir | Tarayıcı |
| `GET /ping` | `Pong` döndürür | Tarayıcıdan Flask'a HTTP isteği |
| `POST /upload` | Gönderilen dosyayı `uploads/` altına kaydeder | Tarayıcıdan Flask'a |
| `POST /measure` | Aktarım, speedtest-cli ve sistem ping işlemleri yapar | Flask'ı çalıştıran makine |
| `GET /views/` | Aynı arayüze alternatif giriş | Tarayıcı |

Uzak bir Flask kurulumu, yerel kurulumdan farklı ağ yolunu ölçer. Sunucu tarafındaki rota sunucunun bağlantısını ölçer ve ziyaretçinin internet bağlantısını doğrudan temsil etmez. Tarayıcıdaki “Ping”, ICMP ölçümü değil HTTP gidiş-dönüş süresidir.

## Doğrulama ve mevcut sınırlar

Bu belgeler için Python kaynağı, şablonlar, rotalar ve bağımlılık tanımları incelendi. Ağ ölçümü veya çalışma zamanı entegrasyon testi yapılmadı.

- Tarayıcı indirmesi sabit bir uzak IP adresini ve 1 MiB varsayılan dosya boyutunu kullanır. İstenen dosyanın adı farklı bir boyuta işaret eder. Erişilebilirlik, TLS ve farklı kaynaktan erişim doğrulanmadı.
- Tarayıcı hesapları, gerekli bit dönüşümünü yapmadan bayt temelli değerleri Mbps olarak etiketler. Sunucudaki özel hesapların da incelenmesi gerekir. Görüntülenen sayılar karşılaştırmalı performans sonucu olarak kullanılmamalıdır.
- Yükleme klasörü repoda yoktur. İşleyici, gönderilen dosya adını üretim ortamına uygun bir yükleme politikası olmadan kaydeder. Prototipi yerelde tut ve hassas olmayan test dosyaları kullan.
- Sunucunun özel yükleme hesabı, gönderilen dosya yerine yanıt gövdesindeki baytları sayar.
- Sunucu ölçüm formunun gönderme düğmesi yorum satırına alınmıştır. Sistem ping işlemi işletim sistemi davranışına da bağlıdır.
- Harici isteklerde açık zaman aşımı ve kapsamlı durum denetimi yoktur. `POST /measure` çalıştırmak gerçek ağ trafiği oluşturur.

Düzeltilmiş bir uygulamada önce ölçülen ağ yolu tanımlanmalı, HTTP başarısı denetlenmeli, gerçek dosya boyutu kullanılmalı ve ondalık Mbps değeri `bayt × 8 / saniye / 1.000.000` olarak hesaplanmalıdır. Sonuçlarla birlikte tekrarlanabilirlik ve önbellek davranışı da açıklanmalıdır.

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

Birimlerin düzeltilmesi, indirme dosyalarının yapılandırılabilmesi, yükleme güvenliğinin geliştirilmesi ve rota ile hesaplar için yalıtılmış testler yararlı sonraki adımlardır.

## Lisans ve kaynaklar

[MIT lisansı](LICENSE) ile dağıtılır. Harici uç noktalar ve speedtest-cli, kendi koşulları ve erişilebilirlikleri olan ayrı hizmetler ve bağımlılıklardır.

