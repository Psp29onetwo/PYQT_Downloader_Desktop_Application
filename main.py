from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys, os, os.path, urllib.request
from pafy import *
from PyQt5.uic import loadUiType

ui, _ = loadUiType("main.ui")

class MainApp(QMainWindow, ui):
    def __init__(self, parent = None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_Buttons()
        # self.pushButton.clicked.connect(self.Download)
        # self.pushButton_2.clicked.connect(self.Handle_Browse)


    def InitUI(self):
        #Contain all ui changes in loading
        pass

    def Handle_Buttons(self):
        #Handle all buttons in the application
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_5.clicked.connect(self.Get_video_Data)

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        #Calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def Handle_Browse(self):
        #Enable browsing to our OS, Help us picking the save location of files or videos
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        # Download Any File(s)
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        # checks the URL and save location is non empty while pressing download button
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data error", "Please provide valid URL or save location")

        else: # Chacks the URL is valid  or not
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handle_Progress)
            except Exception:
                QMessageBox.warning(self, "Download error", "Please provide valid URL or save location")
                return
        QMessageBox.information(self, "Download Completed", "The download is completed successfully")
        self.lineEdit.text('')
        self.lineEdit_2.text('')
        self.progressBar.setValue(0)

    def Save_Browse(self):
        #Save location in the line edit
        pass


#******************************** For downloading single video file************************#


    def Get_video_Data(self):
        video_url = self.lineEdit_4.text()

        if  video_url == '':
            QMessageBox.warning(self, "Data error", "Please provide valid video URL")
        else:
            video = pafy.new(video_url)



    def Download_Video(self):
        pass

    def Video_Progress(self):
        pass





def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()