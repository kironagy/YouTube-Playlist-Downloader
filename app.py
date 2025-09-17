import os
import sys
import yt_dlp
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QLineEdit, QComboBox, QListWidget, QListWidgetItem, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


# ---------------- Worker (تحميل الفيديوهات) ---------------- #
class DownloadThread(QThread):
    progress = pyqtSignal(str, int)  # filename, percent
    finished = pyqtSignal(str)

    def __init__(self, videos, output_path, quality):
        super().__init__()
        self.videos = videos
        self.output_path = output_path
        self.quality = quality

    def run(self):
        # تحديد الجودة مع ضمان وجود الصوت
        if self.quality == "Best":
            format_string = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        else:
            # استخدام format selector أكثر ذكاءً لضمان الحصول على الجودة المطلوبة مع الصوت
            quality_num = self.quality
            format_string = f"(bestvideo[height<={quality_num}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={quality_num}]+bestaudio)/best[height<={quality_num}]/best"

        ydl_opts = {
            "format": format_string,
            "merge_output_format": "mp4",  # دمج الفيديو والصوت في MP4
            "ffmpeg_location": r"C:\ffmpeg\bin",  # تأكد من أن ffmpeg موجود في هذا المسار
            "outtmpl": os.path.join(self.output_path, "%(title)s.%(ext)s"),
            "progress_hooks": [self.my_hook],
            "postprocessors": [{  # إضافة معالج لضمان دمج الصوت
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            # خيارات إضافية لضمان جودة التحميل
            "writesubtitles": False,
            "writeautomaticsub": False,
            "ignoreerrors": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for video in self.videos:
                try:
                    print(f"🔄 Downloading: {video}")
                    ydl.download([video])
                except Exception as e:
                    print(f"❌ Error downloading {video}: {e}")
                    # يمكنك إضافة signal هنا لإشعار الـ GUI بالخطأ

    def my_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent_str = d.get("_percent_str", "0%").replace("%", "").strip()
                percent = int(float(percent_str))
                filename = os.path.basename(d.get("filename", "Unknown"))
                self.progress.emit(filename, percent)
            except:
                pass
        elif d['status'] == 'finished':
            filename = os.path.basename(d.get("filename", "Unknown"))
            self.finished.emit(filename)


# ---------------- Main App ---------------- #
class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 YouTube Playlist Downloader 2025")
        self.setGeometry(300, 150, 700, 500)

        layout = QVBoxLayout()

        # رابط الـ Playlist
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("ضع رابط Playlist هنا...")
        layout.addWidget(QLabel("📌 Playlist Link:"))
        layout.addWidget(self.url_input)

        # مكان الحفظ
        self.path_btn = QPushButton("📂 اختر مكان الحفظ")
        self.path_btn.clicked.connect(self.select_path)
        self.path_label = QLabel("لم يتم اختيار مجلد بعد")
        layout.addWidget(self.path_btn)
        layout.addWidget(self.path_label)

        # الجودة
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Best", "1080", "720", "480", "360"])
        layout.addWidget(QLabel("🎥 اختر الجودة:"))
        layout.addWidget(self.quality_combo)

        # Load playlist button
        self.load_btn = QPushButton("📑 Load Playlist Videos")
        self.load_btn.clicked.connect(self.load_playlist)
        layout.addWidget(self.load_btn)

        # قائمة الفيديوهات
        layout.addWidget(QLabel("✅ اختر الفيديوهات:"))
        self.video_list = QListWidget()
        layout.addWidget(self.video_list)

        self.select_all_btn = QPushButton("🔘 Select All")
        self.select_all_btn.clicked.connect(self.select_all)
        layout.addWidget(self.select_all_btn)

        # Progress
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("جاهز للتحميل")
        layout.addWidget(self.status_label)

        # زر تحميل
        self.download_btn = QPushButton("⬇️ بدء التحميل")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        self.setLayout(layout)
        self.output_path = os.getcwd()

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, "اختر مكان الحفظ")
        if path:
            self.output_path = path
            self.path_label.setText(path)

    def load_playlist(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "⚠️", "من فضلك ضع رابط Playlist")
            return

        self.video_list.clear()
        self.status_label.setText("🔄 جاري تحميل قائمة الفيديوهات...")
        
        try:
            ydl_opts = {"extract_flat": True, "quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if "entries" in info:
                    for entry in info["entries"]:
                        if entry:  # تأكد من أن الـ entry ليس None
                            item = QListWidgetItem(entry.get("title", "Unknown Title"))
                            item.setData(Qt.ItemDataRole.UserRole, entry.get("url", entry.get("id")))
                            item.setCheckState(Qt.CheckState.Unchecked)
                            self.video_list.addItem(item)
                    self.status_label.setText(f"✅ تم تحميل {self.video_list.count()} فيديو")
                else:
                    self.status_label.setText("❌ لم يتم العثور على فيديوهات في هذا الرابط")
        except Exception as e:
            QMessageBox.critical(self, "❌ خطأ", f"فشل في تحميل الـ Playlist:\n{str(e)}")
            self.status_label.setText("❌ فشل في تحميل الـ Playlist")

    def select_all(self):
        for i in range(self.video_list.count()):
            item = self.video_list.item(i)
            if item.checkState() == Qt.CheckState.Unchecked:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

    def start_download(self):
        videos = []
        for i in range(self.video_list.count()):
            item = self.video_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                videos.append(item.data(Qt.ItemDataRole.UserRole))

        if not videos:
            QMessageBox.warning(self, "⚠️", "اختر فيديوهات أولا")
            return

        # تحقق من وجود ffmpeg
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
        if not os.path.exists(ffmpeg_path):
            reply = QMessageBox.question(self, "⚠️ تحذير", 
                                       "لم يتم العثور على ffmpeg في المسار المحدد.\n"
                                       "هذا مطلوب لدمج الفيديو والصوت.\n"
                                       "هل تريد المتابعة؟",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        quality = self.quality_combo.currentText()
        self.status_label.setText(f"🔄 جاري التحميل بجودة {quality}...")
        self.download_btn.setEnabled(False)
        
        self.thread = DownloadThread(videos, self.output_path, quality)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def update_progress(self, filename, percent):
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"🔄 تحميل: {filename} - {percent}%")

    def on_finished(self, filename):
        self.status_label.setText(f"✅ تم التحميل: {filename}")
        
        # تحقق إذا انتهت كل التحميلات
        if not self.thread.isRunning():
            self.download_btn.setEnabled(True)
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "✅ تم", "انتهى التحميل بنجاح!")


# ---------------- Run ---------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())