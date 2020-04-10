from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys, os, os.path, urllib.request
from PyQt5.uic import loadUiType
from pafy import *
import humanize
ui, _ = loadUiType("main.ui")


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_Buttons()



    def InitUI(self):
        # Contain all ui changes in loading
        pass

    def Handle_Buttons(self):
        # Handle all buttons in the application
        #single files
        self.pushButton.clicked.connect(self.Download)
        # self.pushButton2.clicked.connect(self.Handle_Browse)
        #Single videos
        self.pushButton_5.clicked.connect(self.Get_video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)

        #playlist
        # self.pushButton_7.clicked.connect(self.Playlist_Download)
        self.pushButton_8.clicked.connect(self.Save_Browse)


    def Handle_Progress(self, blocknum, blocksize, totalsize):
        # Calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def Handle_Browse(self):
        # Enable browsing to our OS, Help us picking the save location of files or videos
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        # Download Any File(s)
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        # checks the URL and save location is non empty while pressing download button
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data error", "Please provide valid URL or save location")

        else:  # Checks the URL is valid  or not
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handle_Progress)
            except Exception:
                QMessageBox.warning(self, "Download error", "Please provide valid URL or save location")
                return
        QMessageBox.information(self, "Download Completed", "The download is completed successfully")
        self.lineEdit.text('')
        self.lineEdit_2.text('')
        self.progressBar.setValue(0)



    # ******************************** For downloading single video file************************#


    def Save_Browse(self):
        # Save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.lineEdit_3.setText(str(save_location[0]))


    def Get_video_Data(self):
        video_url = self.lineEdit_4.text()

        if video_url == '':
            QMessageBox.warning(self, "Data error", "Please provide valid video URL")
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            video_streams = video.streams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                # size = str(size / 1024)
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)


                self.comboBox.addItem(data)
                print(data)

    def Download_Video(self):
        video_url = self.lineEdit_4.text()
        save_location = self.lineEdit_3.text()
        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data error", "Please provide valid video URL or save location")
        else:
            video = pafy.new(video_url)
            video_stream = video.streams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath = save_location, callback = self.Video_Progress)
        QMessageBox.information(self, "Download Completed", "The download is completed successfully")
        self.lineEdit_4.text('')
        self.lineEdit_3.text('')
        self.progressBar_2.setValue(0)

    def Video_Progress(self, total, recived, ratio, rate, time):
        readed_data = recived
        if total > 0:
            download_percentage = int(readed_data * 100 /total)
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time/60, 2)
            self.label_8.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()


#******************************** Downloading playlist videos ********************************#



    def Playlist_Download(self):
        playlist_url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()

        # if playlist_url == '' or save_location == '':
        #     QMessageBox.warning(self, "Data error", "Please provide valid Playlist URL or save location")

        # else:
        playlist = pafy.get_playlist(playlist_url)
        print(playlist)
        playlist_videos = playlist['items']

        self.lcdNumber_2.display(len(playlist_videos))



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
