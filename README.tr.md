Bu uygulama tarayıcıdaki dosya aktarımlarını ölçer ve sunucudan ayrı hız kontrolleri yapar.

# Network Speed Check

[English](README.md) · [Türkçe](README.tr.md)

Ana sayfa, tarayıcı ile Flask arasındaki indirme, yükleme ve HTTP isteklerinin süresini ölçer. Ayrı bir `POST /measure` rotası harici dosya aktarımlarını, speedtest-cli ölçümlerini ve sistem ping sonucunu birleştirir.

## Yerel kurulum

pip ve venv içeren Python 3 ile bir web tarayıcısı gerekir.

```text
git clone https://github.com/ArdaHFO/network-speed-check.git
cd network-speed-check
python -m venv .venv
```

Windows Komut İstemi'nde `.venv\Scripts\activate`, macOS/Linux'ta `source .venv/bin/activate` ile ortamı etkinleştir.

```text
python -m pip install Flask==3.0.0 requests==2.31.0 speedtest-cli==2.1.3
python -m flask --app app run --host 127.0.0.1 --port 8000
```

[localhost:8000](http://127.0.0.1:8000) adresini aç. Sunucunun açılması aktarım başlatmaz.

[requirements.txt](requirements.txt), daha geniş bir eski bağımlılık listesi içerir. Repodaki `Scripts/` klasörü o Python ortamına aittir. Yukarıdaki yeni sanal ortamı kullan.

## Tarayıcı ölçümleri

Sayfa, `GET /download` ile repodaki `20MB.png` dosyasını indirir, seçilen dosyayı `POST /upload` adresine gönderir ve `GET /ping` isteğinin süresini ölçer.

Sunucu, dosyanın bir kopyasını kaydetmeden alınan bayt sayısını doğrular. Yükleme istekleri multipart ek yükü dahil **32 MiB** ile sınırlıdır. İndirme ve ping yanıtları önbelleğe alınmaz.

## Sunucu ölçümleri

`POST /measure`, Flask'ın çalıştığı makinede şu işlemleri yapar:

1. thinkbroadband'den 5 MB dosya indirmeyi ister.
2. Repodaki `5MB.png` dosyasını httpbin'e yükler.
3. speedtest-cli ile indirme ve yükleme ölçümleri yapar.
4. İşletim sisteminin ping komutunu çalıştırır.

Sonuçlar, speedtest-cli'nin seçtiği sunucu bilgileriyle birlikte `templates/measure.html` içinde gösterilir. Formun gönderme düğmesi şu anda yorum satırındadır; bu rota doğrudan POST isteği gerektirir. Harici ağ istekleri yapar ve adı geçen iki dosyanın toplamından daha fazla veri aktarabilir.

## Sonuçları yorumlama

Özel aktarım hesapları, ondalık Mbps değeri için `bayt × 8 / saniye / 1.000.000` formülünü kullanır. Süreye istek işleme de dahildir. httpbin yüklemesinde yanıt süresi de hesaba katılır.

Tarayıcıdaki Ping düğmesi HTTP gidiş-dönüş süresini ölçer. Sunucu raporundaki sistem ping sonucu ayrı bir ölçümdür. Tarayıcı sonuçları tarayıcı ile Flask arasındaki bağlantıyı, sunucu sonuçları ise uygulamayı çalıştıran makinenin harici hizmetlere bağlantısını gösterir. Localhost aktarımları internet sağlayıcısının bant genişliğini ölçmez.

Uçtan uca davranış ve ölçüm doğruluğu henüz doğrulanmadı. Harici hizmetler erişilemez olabilir; sistem ping çıktısı işletim sistemine göre değişir.

## Kod ve lisans

Rotalar ve sunucu ölçümleri [app.py](app.py), tarayıcı zamanlaması [templates/index.html](templates/index.html) içindedir. [views.py](views.py) alternatif sayfa rotalarını sağlar.

[MIT lisansı](LICENSE). Bağımlılıklar ve harici hizmetler kendi lisanslarına ve koşullarına tabidir.
