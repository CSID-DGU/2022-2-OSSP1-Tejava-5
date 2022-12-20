from video import *

def main(video):
    capture = cv2.VideoCapture(video)
    num=0
    if (capture.isOpened()== False): 
        print("Error opening video stream or file")
    
    while(num < 5):
        ret, frame = capture.read()
      
        if ret == True:
            cv2.imshow('Frame', frame)
            path='./' + str(num) + '.jpg'
            cv2.imwrite(path,frame)
        else:
            break
        num += 1
    capture.release()
    cv2.destroyAllWindows()
 
 