import cv2
import glob
import os

frame_array=[]
images=sorted(glob.glob('C:/Users/user/Desktop/test/mask/*.jpg'), key=os.path.getctime)
for filename in images:
    frame=cv2.imread(filename)
    height, width, layers = frame.shape
    size = (width,height)
    frame_array.append(frame)

out = cv2.VideoWriter('Desktop/test/output/out.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

for i in range(len(frame_array)):
    out.write(frame_array[i])
out.release()


