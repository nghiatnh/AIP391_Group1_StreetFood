from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys
import os
from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pickle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

class GUI(Ui_MainWindow):
    '''
    GUI
    ----------

    GUI with actions and triggers
    '''
    
    def __init__(self) -> None:
        '''
        Init and setup window
        '''
        super().__init__()
        # Main window
        self.mainwindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainwindow)

        self.setupSignal()
        self.add_video_widget()

    def add_video_widget(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.mainwindow.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        self.vlo_video_container.addLayout(layout)
        self.vlo_video_container.addLayout(controlLayout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def setupSignal(self) -> None:
        '''
        Add event to buttons and menu items
        '''
        # Buttons
        self.btn_predict.clicked.connect(self.btn_predict_clicked)

        # Actions in Menu File
        self.actionOpen_Video.triggered.connect(
            self.action_open_video_triggered)
        
        self.sld_like_level_1.sliderMoved.connect(self.sld_like_level_1_changed)
        self.sld_like_level_2.sliderMoved.connect(self.sld_like_level_2_changed)
        self.sld_like_level_3.sliderMoved.connect(self.sld_like_level_3_changed)
        self.sld_like_level_4.sliderMoved.connect(self.sld_like_level_4_changed)
        self.sld_like_level_5.sliderMoved.connect(self.sld_like_level_5_changed)

    def show(self) -> None:
        '''
        Show the main window
        '''
        self.mainwindow.show()

    '''
    ---- When buttons click ----
    '''

    def btn_predict_clicked(self, checked) -> None:
        match self.cbb_model.currentIndex():
            case 0:
                model_name = 'KNN_model'
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass
            case _:
                model_name = 'KNN_model'
        clf = pickle.load(open('Model/{}'.format(model_name), 'rb'))
        X = [[self.sld_like_level_1.value(), self.sld_like_level_2.value(), self.sld_like_level_3.value(), self.sld_like_level_4.value(), self.sld_like_level_5.value()]]
        result = clf.predict(X)[0]
        QMessageBox.information(self.mainwindow, 'Prediction Result', 'The attractive level of video is {}'.format(result))

    def sld_like_level_1_changed(self, position) -> None:
        self.lb_like_level_1.setText(str(position))
    def sld_like_level_2_changed(self, position) -> None:
        self.lb_like_level_2.setText(str(position))
    def sld_like_level_3_changed(self, position) -> None:
        self.lb_like_level_3.setText(str(position))
    def sld_like_level_4_changed(self, position) -> None:
        self.lb_like_level_4.setText(str(position))
    def sld_like_level_5_changed(self, position) -> None:
        self.lb_like_level_5.setText(str(position))

    '''
    ---- When actions click ----'''

    def action_open_video_triggered(self, checked) -> None:
        self.openFile()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.mainwindow, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.mainwindow.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.mainwindow.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())