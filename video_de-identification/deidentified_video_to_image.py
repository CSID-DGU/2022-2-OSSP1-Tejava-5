import cv2
 
def main():
    capture = cv2.VideoCapture('Desktop/test/mask.mp4')
    num=0
    if (capture.isOpened()== False): 
        print("Error opening video stream or file")
    
    while(capture.isOpened()):
        ret, frame = capture.read()
      
        if ret == True:
            cv2.imshow('Frame', frame)
            path='Desktop/test/mask/mask_' + str(num) + '.jpg'
            cv2.imwrite(path,frame)
          
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
        num += 1
     
    capture.release()
     
    cv2.destroyAllWindows()
 
 
if __name__ == '__main__':
    main()
