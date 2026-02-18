🎣 Metin2 Fish Jigsaw Bot (Balık Yapboz Botu)

🚧 DİKKAT: GELİŞTİRME AŞAMASINDA / WARNING: UNDER DEVELOPMENT



\[TR] Metin2 Balık Yapboz etkinliği için geliştirilmiş, görüntü işleme (OpenCV) ve deterministik yapay zeka algoritmaları kullanan tam otomatik, ban korumalı bir bottur.



\[EN] A fully automated, ban-safe bot for the Metin2 Fish Jigsaw event, powered by Computer Vision (OpenCV) and deterministic AI solving algorithms.



🌟 Özellikler / Features

* 👁️ Gelişmiş Görüntü İşleme: OpenCV ile oyun ekranındaki parçaları anlık olarak tanır ve analiz eder.



* 🧠 Kusursuz Yapay Zeka: deterministic.py içindeki algoritma sayesinde her hamle için matematiksel olarak en yüksek puanı alacak kombinasyonu hesaplar.



* 🛡️ Akıllı Hata Kontrolü: Parça yerleşmediğinde veya lag olduğunda bunu algılar, hafızasını düzeltir ve oyunu bozmadan devam eder.



* 📏 Esnek Grid Sistemi: Farklı ekran çözünürlükleri veya oyun penceresi boyutları için Grid boyutunu (örn: 32px) arayüzden ayarlayabilirsiniz.



* ⚙️ Kolay Kalibrasyon: Tek tuşla (F1) ekran koordinatlarını otomatik ayarlar.



🛠️ Kurulum / Installation

Gereksinimler / Requirements

* Python 3.8 veya üzeri





* 1\. Projeyi İndirin / Clone the Repository



* 2\. Kütüphaneleri Yükleyin / Install Dependencies

Gerekli Python kütüphanelerini yüklemek için terminali proje klasöründe açın ve şu komutu girin:



pip install -r requirements.txt

(Eğer requirements.txt dosyanız yoksa manuel olarak şunları yükleyin:)





pip install opencv-python numpy pyautogui pydirectinput keyboard pillow

🚀 Kullanım / Usage

* Oyunu Açın: Metin2 istemcisini başlatın ve "Balık Yapboz" (Fish Jigsaw) penceresini açın.



* Botu Başlatın: main.pyw dosyasını Yönetici Olarak çalıştırın (Mouse kontrolü için gereklidir).



Kalibrasyon (Calibration):



* Mouse imlecini oyun tahtasındaki sol üstteki ilk kutunun SOL ÜST KÖŞESİNE getirin.



* Klavyeden F1 tuşuna basın. Bot "Kilitlendi" diyecektir.



Ayarlar (Settings):



* Varsayılan Grid boyutu 32'dir. Eğer bot parçaları çizgilere koyuyorsa bu değeri 37.4 gibi değerlerle değiştirip "Test Et" butonunu kullanabilirsiniz.



Başlat (Start):



* F5 tuşuna basarak botu başlatın.



Durdur (Stop):



* İstediğiniz zaman F6 tuşuna basarak durdurabilirsiniz.





📂 Dosya Yapısı / File Structure

* main.pyw: Botun ana arayüzü, mouse kontrolü ve görüntü işleme döngüsü.



* core/: Yapay zeka motoru.



* &nbsp;	jigsaw.py: Oyun kuralları ve tahta mantığı.



* &nbsp;	deterministic.py: En iyi hamleyi hesaplayan çözümleyici algoritma.



* assets/: Parça görsellerinin bulunduğu klasör (fish\_1.png vb.).



⚠️ Yasal Uyarı / Disclaimer

\[TR] Bu yazılım tamamen eğitim ve hobi amaçlı geliştirilmiştir (Görüntü işleme ve otomasyon algoritmaları üzerine çalışmak için). Oyun sunucularında kullanmak hesabınızın yasaklanmasına (ban) neden olabilir. Kullanımdan doğacak tüm sorumluluk kullanıcıya aittir. Geliştirici, oluşabilecek hesap kayıplarından sorumlu tutulamaz.



\[EN] This software is developed for educational purposes only (to study Computer Vision and automation algorithms). Using it on official game servers may result in account suspension (ban). The user assumes full responsibility for its use. The developer is not responsible for any account losses.



🤝 Katkıda Bulunma / Contributing

Hataları bildirmek veya yeni özellikler eklemek için "Issue" açabilir veya "Pull Request" gönderebilirsiniz.

