#Based on 'FaceSwap.main_video.py'
import os
import cv2
import logging

from ..FaceSwap.face_detection import select_face
from ..FaceSwap.face_swap import face_swap


#class VideoHandler(object):
def main(self, src, vid):
    self.src_points, self.src_shape, self.src_face = select_face(cv2.imread())
    if self.src_points is None:
        print('No face detected in the source image !!!')
        exit(-1)
    #self.args = args
    self.video = cv2.VideoCapture(vid)
    self.writer = cv2.VideoWriter('./swapped.mp4', cv2.VideoWriter_fourcc(*'MJPG'), self.video.get(cv2.CAP_PROP_FPS),
                                    (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

#def start(self):
    while self.video.isOpened():
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        _, dst_img = self.video.read()
        dst_points, dst_shape, dst_face = select_face(dst_img, choose=False)
        if dst_points is not None:
            dst_img = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, dst_img, self.args, 68)
        self.writer.write(dst_img)

#       os.remove(vid)
 #           if self.args.show:
 #               cv2.imshow("Video", dst_img)

#        self.video.release() 
#        self.writer.release()
#        cv2.destroyAllWindows()


# 아랫줄 코드 없애고 최종코드에 합치기
#    VideoHandler(args.video_path, args.src_img, args).start()
