import sys
import moviepy.editor as mp
from PyQt5 import uic
from PyQt5.QtWidgets import *
import ffmpeg


from voice import *
#from video.TDDFA_video import main as TDDFA

from video.deidentified_video_to_image import main as vid2img
#from FaceSwap.swap_merge import main as merge
from video.combine import main as combine
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
        fname=QFileDialog.getOpenFileName(self,'파일 선택','./','영상(*.avi *.asf *.mov *.wmv *.mp4 *.mpeg *.webm)')       
        if fname[0]:
            global flag
            flag = 1
            self.label.setText(fname[0])    
            print(fname[0])
            


    def btn_convert(self):
        if flag:
                #음성 추출 data_voice = ...
                clip = mp.VideoFileClip(fname[0])
                clip.audio.write_audiofile("data_voice.mp3")
                voice_de_identification("data_voice.mp3", 1.3)
 #               TDDFA(fname[0])

                vid2img('1차변환.mp4')
#                merge(self, '0.jpg', "chap.mp4")
#                merge(self, 'sample/1.jpg', 'swapped.mp4')


                import os
                from os import system, chdir
                chdir("FaceSwap")
                os.system("python main_video.py --src_img ../0.jpg --video_path ../원본.mp4 --show --correct_color --save_path ../2차변환.mp4")
                os.system("python main_video.py --src_img ../sample/1.jpg --video_path ../2차변환.mp4 --show --correct_color --save_path ../de_identified_video.mp4")
                
                
                chdir("..")
                chdir("video")
                combine('../de_identified_video.mp4', '../de_identified_audio.mp3')
                QMessageBox.information(self, "알림", "변환이 완료되었습니다")
        else:
            QMessageBox.warning(self, "Error", "파일을 선택하십시오")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
