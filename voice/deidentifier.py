import sys
import moviepy.editor as mp
from PyQt5 import uic
from PyQt5.QtWidgets import *
import ffmpeg
# from voice_extractor import voice_extractor

from voice_de_identification import voice_de_identification
# from video_de_identification import video_de_identification


form_class = uic.loadUiType("ui_deidentification.ui")[0]


class WindowClass(QMainWindow, form_class):
    global flag
    flag = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fileselectBtn.clicked.connect(self.btn_fileselect)
        self.convertBtn.clicked.connect(self.btn_convert)


    def btn_fileselect(self):
        global fname
        fname=QFileDialog.getOpenFileName(self,'파일 선택','.\\','영상(*.avi *.asf *.mov *.wmv *.mp4 *.mpeg *.webm)')       
        if fname[0]:
            global flag
            flag = 1
            self.label.setText(fname[0])    


    def btn_convert(self):
        if flag:
                #음성 추출 data_voice = ...
                clip = mp.VideoFileClip(fname[0])
                clip.audio.write_audiofile("data_voice.mp3")
                voice_de_identification("data_voice.mp3", 1.3)


                QMessageBox.information(self, "알림", "변환이 완료되었습니다")
        else:
            QMessageBox.warning(self, "Error", "파일을 선택하십시오")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
