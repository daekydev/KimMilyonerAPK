# Kim Bir Milyon İster - Özel Sunucu & APK Düzenleme Rehberi

Bu proje, kapanmış olan **Kim Bir Milyon İster (com.wenetix.kimbirmilyonister)** Android oyununun sunucularını yeniden canlandırmak ve oyunu tekrar oynanabilir kılmak için hazırlanmış tam bağımsız özel sunucu (backend) ve APK yama (patcher) araçlarını içerir.

---

## 1. Sistem ve Mimari Özeti

Oyun istemcisi (`Assembly-CSharp.dll`) sunucuyla HTTP üzerinden `http://api.wenetix.com/kbi/` adresinde haberleşmektedir. Orijinal sunucu kapandığı için oyun soru çekememekte, skor kaydedememekte ve liderlik tablosunu yükleyememektedir.

Yeniden yazılan sunucu aşağıdaki 9 uç noktayı (endpoint) birebir orijinal protokol ve JSON şemasına uygun olarak sağlar:
1. `POST /kbi/Logingoogle.php`: Kullanıcı giriş doğrulaması
2. `POST /kbi/Creategoogle.php`: Kullanıcı profili oluşturma ve güncelleme
3. `POST /kbi/EncokKazananlar.php`: Liderlik tablosu / En çok kazanan 12 kişi
4. `POST /kbi/DusukSorular.php`: 1-4. Seviye kolay sorular
5. `POST /kbi/OrtaSorular.php`: 5-8. Seviye orta seviye sorular
6. `POST /kbi/UstSorular.php`: 9-12. Seviye zor sorular
7. `POST /kbi/Kazanc.php`: Kullanıcının toplam kazancını getirme
8. `POST /kbi/Update_Kazanc.php`: Oyun sonu kazanılan ödülü kaydetme
9. `POST /kbi/Update_Resim.php`: Profil resmini güncelleme

---

## 2. Sunucuyu Kurma ve Çalıştırma

### Gereksinimler
- Python 3.8 veya üzeri
- `pip install -r server/requirements.txt`

### Adım 1: Bağımlılıkları Yükleyin
```bash
pip install -r server/requirements.txt
```

### Adım 2: Veritabanını Başlatın (İlk Kurulum)
Sunucuda Türkçe soruları ve varsayılan liderlik tablosunu SQLite veritabanına yüklemek için:
```bash
python3 server/init_db.py
```
*(Bu işlem `server/kbi_game.db` dosyasını oluşturur ve hazır soruları yükler.)*

### Adım 3: Sunucuyu Çalıştırın
```bash
python3 server/app.py
```
Sunucu varsayılan olarak `0.0.0.0:5000` portunda çalışacaktır.
Farklı bir portta çalıştırmak isterseniz:
```bash
PORT=8080 python3 server/app.py
```

Tarayıcınızdan `http://localhost:5000/` adresine girdiğinizde `Kim Bir Milyon İster? Game Server is running.` mesajını görebilirsiniz.

---

## 3. APK'yı Kendi Sunucunuza Bağlama (Patching)

Oyun APK'sı varsayılan olarak `http://api.wenetix.com` adresine bağlanmayı dener. Hazırladığımız otomatik patcher aracı ile APK içindeki C# kütüphanesini kendi sunucu IP adresinize yönlendirebilirsiniz.

### Android Emülatör İçin (Örn: Android Studio Emülatörü)
Android emülatörleri geliştirici bilgisayarının localhost'una `10.0.2.2` IP'si üzerinden erişir:
```bash
python3 patcher/patch_apk.py \
  --apk "Kim+Bir+Milyon+İster_1.5.7_APKPure.apk" \
  -o "KimMilyoner_Patched.apk" \
  --host "http://10.0.2.2:5000"
```

### Gerçek Android Cihaz İçin (Wi-Fi / Yerel Ağ)
Telefonunuz ve bilgisayarınız aynı Wi-Fi ağına bağlıyken, bilgisayarınızın yerel IP adresini (örneğin `192.168.1.50`) kullanın:
```bash
python3 patcher/patch_apk.py \
  --apk "Kim+Bir+Milyon+İster_1.5.7_APKPure.apk" \
  -o "KimMilyoner_Patched.apk" \
  --host "http://192.168.1.50:5000"
```

### Yalnızca DLL Dosyasını Güncellemek İsterseniz
```bash
python3 patcher/patch_apk.py \
  --dll "yol/Assembly-CSharp.dll" \
  -o "yol/Assembly-CSharp.patched.dll" \
  --host "http://192.168.1.50:5000"
```

Patcher aracı:
- Assembly içerisindeki 9 adet API URL'ini yeni adrese yönlendirir.
- APK'yı otomatik olarak debug sertifikası ile yeniden imzalar.
- İmzalanmış APK dosyasını doğrudan cihazınıza veya emülatörünüze (`adb install KimMilyoner_Patched.apk`) kurup oynayabilirsiniz.

---

## 4. Yeni Soru Ekleme ve Düzenleme

Soru havuzunu genişletmek için `server/init_db.py` dosyasındaki `DUSUK_SORULAR`, `ORTA_SORULAR` ve `UST_SORULAR` listelerine yeni sorular ekleyip `python3 server/init_db.py` komutunu tekrar çalıştırabilirsiniz.

Her soru formatı:
```python
{
    "Soru": "Soru metni buraya gelecek?",
    "DogruCevap": "Doğru Şık",
    "Cevap": "Yanlış Şık 1",
    "Cevap2": "Yanlış Şık 2",
    "Cevap3": "Yanlış Şık 3"
}
```

---

## 5. Testleri Çalıştırma

Sunucu API'lerinin ve veritabanının doğru çalıştığından emin olmak için otomatik birim testleri çalıştırabilirsiniz:
```bash
python3 -m unittest tests/test_server.py
```
Tüm testler başarıyla geçmelidir.
