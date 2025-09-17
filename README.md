\# 🎬 YouTube Playlist Downloader 2025  



برنامج بواجهة رسومية (GUI) باستخدام Python + PyQt6 لتحميل فيديوهات YouTube أو Playlists كاملة بجودة عالية مع إمكانية اختيار الجودة ومكان الحفظ.  



---



\## 📝 المتطلبات (Requirements)



قبل تشغيل السكربت تأكد من الآتي:



1\. \*\*Python 3.9 أو أعلى\*\*  

&nbsp;  - \[تحميل Python](https://www.python.org/downloads/)



2\. \*\*تثبيت المكتبات المطلوبة\*\*  

&nbsp;  - كل المكتبات مكتوبة في ملف `requirements.txt`.  

&nbsp;  - بعد تحميل المشروع، نفّذ الأمر التالي في مجلد المشروع:

&nbsp;    ```bash

&nbsp;    pip install -r requirements.txt

&nbsp;    ```



3\. \*\*FFmpeg\*\* (ضروري لدمج الصوت مع الفيديو):

&nbsp;  - نزّل FFmpeg من الموقع الرسمي: \[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)  

&nbsp;  - فك الضغط وضع مجلد `ffmpeg` في مسار مثل: `C:\\ffmpeg`  

&nbsp;  - تأكد أن الملف التنفيذي موجود في:

&nbsp;    ```

&nbsp;    C:\\ffmpeg\\bin\\ffmpeg.exe

&nbsp;    ```

&nbsp;  - \*\*(اختياري لكن يُفضل)\*\*: أضف المسار `C:\\ffmpeg\\bin` إلى متغير البيئة `PATH` حتى يمكن تشغيله من أي مكان.



---



\## ⚙️ طريقة التشغيل



1\. حمّل المشروع أو انسخه:

&nbsp;  ```bash

&nbsp;  git clone https://github.com/USERNAME/YoutubePlaylistDownloader.git

&nbsp;  cd YoutubePlaylistDownloader



