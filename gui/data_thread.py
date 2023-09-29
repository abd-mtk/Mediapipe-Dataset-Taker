import os
import shutil
import time

import cv2
import mediapipe as mp
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from gui.stream_data import StreamData
from utility.draw import Draw
from utility.tools import DetectionData


class DataThread(QThread):
    frame = QtCore.pyqtSignal(np.ndarray)
    noSample = QtCore.pyqtSignal(str)
    mode, path, movmentsName = "live", "Data", ""
    keypoints, fps, pause, collection, stauts = True, False, False, False, True
    noSamples, noframe, fromFile = 30, 30, 0
    flip, rotation = 1, 0

    def __init__(self, camId=0, videopath=None, image_view=None, width=1080, hight=720, lcdView=None):
        super().__init__()
        self.pTime = time.time()
        self.mp_holistic = mp.solutions.holistic
        self.mp_pose = mp.solutions.pose
        self.draw = Draw()
        self.detectionData = DetectionData()

        if videopath is None:
            self.capture = cv2.VideoCapture(camId)
        else:
            self.capture = cv2.VideoCapture(videopath)
            self.frameCount = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)

        self.stram = StreamData(image_view, width, hight, lcdView)
        self.frame.connect(self.stram.updateImagepixmap)
        self.noSample.connect(self.stram.updateLcd)

    def camera(self):
        while self.stauts:
            try:
                cTime = time.time()
                success, image = self.capture.read()
                height, width = image.shape[:2]
                M = cv2.getRotationMatrix2D(
                    (width / 2, height / 2), self.rotation, 1)
                image = cv2.warpAffine(image, M, (width, height))
                image = cv2.flip(image, self.flip)

                if success:
                    fps = 1 / (cTime - self.pTime)
                    if self.fps:
                        cv2.putText(image, f"FPS: {int(fps)}", (int(width - 100), 20), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1,
                                    (255, 0, 0), 2)
                    if self.keypoints:
                        image, results = self.detectionData.mediapipeDetection(
                            image)
                        self.draw.drawStyledLandmarks(image, results)
                    self.frame.emit(image)
                    self.pTime = cTime
                    if self.collection:
                        if not os.path.exists(os.path.join(self.path, self.movmentsName, str(self.fromFile))):
                            os.makedirs(os.path.join(
                                self.path, self.movmentsName, str(self.fromFile)))
                        for frame in range(self.noframe):
                            cTime = time.time()
                            image, results = self.detectionData.mediapipeDetection(
                                image)
                            if results.pose_landmarks:
                                if self.keypoints:
                                    self.draw.drawStyledLandmarks(
                                        image, results)
                                if self.fps:
                                    cv2.putText(image, f"FPS: {int(fps)}", (int(width - 100), 50),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                                (255, 0, 0), 2)
                                cv2.putText(image, f"Collecting frames for {self.fromFile} start", (25, 25),
                                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                                keypoints = self.detectionData.extractKeypoints(
                                    results)
                                try:

                                    npy_path = os.path.join(
                                        self.path, self.movmentsName, str(self.fromFile), str(frame))
                                    np.save(npy_path, keypoints)
                                except Exception:
                                    cv2.putText(image, "ERROR: Failed to Save a Data", (25, 25),
                                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                                    pass
                                self.frame.emit(image)
                                self.noSample.emit(str(frame))
                                success, image = self.capture.read()
                                M = cv2.getRotationMatrix2D(
                                    (width / 2, height / 2), self.rotation, 1)
                                image = cv2.warpAffine(
                                    image, M, (width, height))
                                image = cv2.flip(image, self.flip)
                                self.pTime = cTime
                        if len(os.listdir(os.path.join(self.path, self.movmentsName, str(self.fromFile)))) != self.noframe:
                            shutil.rmtree(os.path.join(
                                self.path, self.movmentsName, str(self.fromFile)))
                            cv2.putText(image, "ERROR: Failed to Save a Data", (25, 25),
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                        self.collection = not self.collection
            except Exception as e:
                # print(e)
                pass

    def getData(self):
        # print(self.frameCount)
        while self.stauts and self.frameCount > 0:
            try:
                _, image = self.capture.read()
                self.frameCount -= 1
                height, width = image.shape[:2]
                M = cv2.getRotationMatrix2D(
                    (width / 2, height / 2), self.rotation, 1)
                image = cv2.warpAffine(image, M, (width, height))
                image = cv2.flip(image, self.flip)
                cTime = time.time()
                fps = 1 / (cTime - self.pTime)
                if self.keypoints:
                    image, results = self.detectionData.mediapipeDetection(
                        image)
                    self.draw.drawStyledLandmarks(image, results)

                if self.fps:
                    cv2.putText(image, f"FPS: {int(fps)}", (int(width - 190), 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                (255, 0, 0), 2)
                    self.pTime = cTime
                if self.pause:
                    cv2.putText(image, "PAUSED", (int(width / 3), int(height / 2)),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                    self.frame.emit(image)
                    while self.pause:
                        pass
                if self.collection and self.frameCount > self.noframe:
                    if not os.path.exists(os.path.join(self.path, self.movmentsName, str(self.fromFile))):
                        os.makedirs(os.path.join(
                            self.path, self.movmentsName, str(self.fromFile)))
                    for frame in range(self.noframe):
                        cTime = time.time()
                        fps = 1 / (cTime - self.pTime)
                        image, results = self.detectionData.mediapipeDetection(
                            image)
                        if results.pose_landmarks:
                            if self.keypoints:
                                self.draw.drawStyledLandmarks(image, results)
                            if self.fps:
                                cv2.putText(image, f"FPS: {int(fps)}", (int(width - 190), 50),
                                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
                            cv2.putText(image, f"Collecting frames for {self.fromFile} start", (25, 25),
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                            keypoints = self.detectionData.extractKeypoints(
                                results)
                            try:

                                npy_path = os.path.join(
                                    self.path, self.movmentsName, str(self.fromFile), str(frame))
                                np.save(npy_path, keypoints)
                            except Exception:
                                cv2.putText(image, "ERROR: Failed to Save a Data", (25, 25),
                                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                                pass
                            self.frame.emit(image)
                            self.pTime = cTime
                            self.noSample.emit(str(frame))
                            success, image = self.capture.read()
                            self.frameCount -= 1
                            M = cv2.getRotationMatrix2D(
                                (width / 2, height / 2), self.rotation, 1)
                            image = cv2.warpAffine(image, M, (width, height))
                            image = cv2.flip(image, self.flip)
                    if len(os.listdir(os.path.join(self.path, self.movmentsName, str(self.fromFile)))) != self.noframe:
                        shutil.rmtree(os.path.join(
                            self.path, self.movmentsName, str(self.fromFile)))
                        cv2.putText(image, "ERROR: Failed to Save a Data", (25, 25),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                    self.collection = not self.collection
                self.frame.emit(image)
            except Exception as e:
                print(e)
                pass

    def run(self):
        if self.mode == "live":
            self.camera()
        elif self.mode == "video":
            self.getData()

    def stop(self):
        self.stauts = False
        self.capture.release()
