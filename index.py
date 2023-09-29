import os
import sys

import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from gui.data_thread import DataThread
from utility.setup_folder import SetupFolder

PATH = f"gui//main.ui"
FORM_CLASS, _ = loadUiType(PATH, "main.ui")


class MainApp(QMainWindow, FORM_CLASS):
    angle, fliper = 0, 0

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent, flags=Qt.WindowStaysOnTopHint)
        QMainWindow.__init__(self, parent, flags=Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.saveLoc_btn.clicked.connect(self.saveLocation)
        self.brows_btn.clicked.connect(self.browsLocation)
        self.showFps.stateChanged.connect(self.showFPS)
        self.showKeypoint.stateChanged.connect(self.showKeypoints)
        self.apply_btn.clicked.connect(self.apply)
        self.clean_btn.clicked.connect(self.clean)
        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.pause_btn.clicked.connect(self.pause)
        self.flip_btn.clicked.connect(self.flip)
        self.rotation_btn.clicked.connect(self.rotation)
        self.collection_btn.clicked.connect(self.collection)
        self.ports = self.list_ports()
        self.cam_num.addItems([str(i) for i in self.ports])
        self.cam_num.addItems(["video"])
        self.cameraPort = self.ports[0]
        self.runCamera = DataThread(
            camId=self.cameraPort, image_view=self.dataShow, lcdView=self.noSample_num)
        self.runCamera.start()

    def list_ports(self):
        ports = []
        for i in range(10):
            cap_ = cv2.VideoCapture(i)
            if cap_.read()[0]:
                ports.append(i)
            cap_.release()
        return ports

    def saveLocation(self):
        try:
            dir_ = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select project folder:',
                                                              os.chdir(
                                                                  f"C:\\Users\\{os.getlogin()}\\Desktop"),
                                                              options=QtWidgets.QFileDialog.ShowDirsOnly)
            self.saveLoc_txt.setText(dir_)
            self.fromFile_num.setValue(
                len(os.listdir(dir_+f"\\{self.movment_txt.text()}")))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def browsLocation(self):
        videopath = QtWidgets.QFileDialog.getOpenFileName(self, 'Select video file:',
                                                          os.chdir(
                                                              f"C:\\Users\\{os.getlogin()}\\Desktop"),
                                                          'Video Files (*.mov *.flv *.wmv *.webm *.mp4 *.avi *.MTS)')
        try:
            self.vidPath_txt.setText(videopath[0])
            self.cam_num.setCurrentText("video")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def apply(self):
        if self.saveLoc_txt.text() == "" or self.movment_txt.text() == "" or not os.path.isdir(self.saveLoc_txt.text()):
            QtWidgets.QMessageBox.critical(
                self, "Error", "Please select save location")
            return
        else:
            movments = self.movment_txt.text()
            try:
                SetupFolder(self.saveLoc_txt.text(), movments,
                            int(self.noSample_num.text()))
                QtWidgets.QMessageBox.information(
                    self, "Success", "Setup folder successfully")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def collection(self):
        if self.saveLoc_txt.text() == "" or self.movment_txt.text() == "" or not os.path.isdir(self.saveLoc_txt.text()):
            QtWidgets.QMessageBox.critical(
                self, "Warning", "Please Enter All Fields")
        else:
            self.runCamera.path = self.saveLoc_txt.text().replace("/", "\\")
            self.runCamera.fromFile = int(self.fromFile_num.text())
            self.runCamera.collection = not self.runCamera.collection
            self.fromFile_num.setValue(int(self.fromFile_num.text()) + 1)

    def clean(self):
        self.vidPath_txt.setText("")
        self.saveLoc_txt.setText("")
        self.movment_txt.setText("")

    def start(self):
        if self.vidPath_txt.text() == "" and self.cam_num.currentText() == "video":
            QtWidgets.QMessageBox.critical(
                self, "Error", "Please select video source")
            return
        if self.vidPath_txt.text() == "" and self.cam_num.currentText() != "video":
            self.runCamera.action = self.movment_txt.text()
            if self.runCamera.isRunning():
                self.runCamera.stop()
            self.runCamera = DataThread(camId=int(self.cam_num.currentText()), image_view=self.dataShow,
                                        lcdView=self.dataCollected_num)
            self.runCamera.movmentsName = self.movment_txt.text()
            self.runCamera.noSamples = int(self.noSample_num.text())
            self.runCamera.noframe = int(self.noFrame_num.text())
            self.runCamera.path = self.saveLoc_txt.text()
            self.runCamera.mode = "live"
            self.runCamera.start()

        elif os.path.isfile(self.vidPath_txt.text()) and self.cam_num.currentText() == "video":
            if os.path.isfile(self.vidPath_txt.text()):
                if self.runCamera.isRunning():
                    self.runCamera.stop()
                self.runCamera = DataThread(videopath=self.vidPath_txt.text(), image_view=self.dataShow,
                                            lcdView=self.dataCollected_num)
                self.runCamera.movmentsName = self.movment_txt.text()
                self.runCamera.noSamples = int(self.noSample_num.text())
                self.runCamera.noframe = int(self.noFrame_num.text())
                self.runCamera.path = self.saveLoc_txt.text()
                self.runCamera.mode = "video"
                self.runCamera.start()
            else:
                QtWidgets.QMessageBox.critical(
                    self, "Error", "Please select video source")

    def stop(self):
        if self.runCamera.isRunning():
            self.runCamera.stop()
        self.dataShow.setPixmap(QPixmap())

    def pause(self):
        if self.runCamera.isRunning():
            self.runCamera.pause = not self.runCamera.pause
        else:
            QtWidgets.QMessageBox.information(
                self, "warning", "Please Run the video first")

    def flip(self):
        try:
            fliparray = [0, 1, -1]
            if self.runCamera.isRunning():
                if self.fliper == 3:
                    self.fliper = 0
                self.runCamera.flip = fliparray[self.fliper]
                self.fliper += 1
            else:
                QtWidgets.QMessageBox.information(
                    self, "warning", "Please Run the video first")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def rotation(self):
        angle = [0, 90, 180, 270]
        if self.runCamera.isRunning():
            if self.angle == 4:
                self.angle = 0
            self.runCamera.rotation = angle[self.angle]
            self.angle += 1
        else:
            QtWidgets.QMessageBox.information(
                self, "warning", "Please Run the video first")

    def showKeypoints(self):
        self.runCamera.keypoints = self.showKeypoint.isChecked()

    def showFPS(self):
        self.runCamera.fps = self.showFps.isChecked()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
