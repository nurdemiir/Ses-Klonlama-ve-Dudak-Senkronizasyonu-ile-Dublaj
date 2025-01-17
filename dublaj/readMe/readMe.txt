KODU ÇALIŞTIRIRKEN DİKKAT EDİLMESİ GEREKENLER
BU KISIM DİKKATE ALINMAZSA KOD DÜZGÜN BİR  ÇIKTI ÜRETMEYEBİLİR
##################################################################


KULLANILACAK VİDEODA DİKKAT EDİLMESİ GEREKENLER
###############################################
(Wav2Lip/videolar) klasöründe denemek için örnek bir video bıraktık.

1. İşlem yapılacak videonu uzuluğu 15 saniye uzunluğu civarında olmalı. 
2. Sesin düzgün bir şekilde taklit edilmesi için videodaki sesin sadece bir kişiye ait olması gerekiyor. 
3. Videodaki seste arka plan gürültüleri olmaması gerekiyor ve videodaki kişinin takılmadan akıcı bir şekilde konuşması gerekiyor.
4. Videodaki kişinin ana videoda, çevirilecek dilde kullanılacak sesleri çıkarması gerekiyor. 
   Örneğin çevirilecek dilde "k" harfi kullanılması gerekiyor ve ana videoda bu ses çıkarılmamışsa çevirilmiş ses "k" harfini çıkaramaz.
   Eğer bu işleme dikkat edilmezse çevirilip taklit edilmiş seste bozukluklar olabilir. 
5. Ana videodaki kişinin konuşurken kafasını aşağı, yukarı, sağa,sola çevirmesi senkronizasyon modelinin yüzü algılayamamasına sebep olur ve bu durumda kod çıktı üretmez. 
   Videodaki kişi kafasını bu yönlere direkt çevirmediği sürece kafasını oynatabilir.


GUI EKRANI 
#############

1. Kod çalıştırıldığında açılan GUI ekranında "Ses Tanıma Dilini Seçin" kısmında ana videonun dilini seçmemiz gerekiyor.
2. "Çeviri Dilini Seçin" kısmında ana videomuzu hangi dile çevirmek istediğimizi seçiyoruz.
3. "Video Yükle" kısmından yükleyeceğimiz videonun 1. maddede belirttiğimiz dilde bir video olması gerekiyor. 
4. "Ses Tanıma" butonu videoyu metne döküyor.
5. "Çevir" butonuyla çeviri işlemini sağlıyoruz.
6. "Metni Sese Dönüştür" butonuyla videodaki kişinin sesi istenen dilde taklit ediliyor.
7. "Sesi Çal" butonu taklit edilen sesi dinlememizi sağlıyor.
8. "Videoyu Kaydet" butonu ise taklit edilmiş sesi ana videoyu dudak senkronizasyonlarıyla birlikte ekliyor.
(Kaydedilen video senkronize_video klasörünün içine kaydoluyor. Bu çıktıyı üretmesi uzun sürebilir)
(Kaydedilen video visual studio code içinde sesli bir şekilde açılmıyor sesli sonucu görmek için videoyu klasörden açmak gerekiyor.)











