# Script containing a function that starts a recording using the webcam of the 
# laptop. The function takes "fps", "seconds" and "scale_factor" as arguments
# where fps determines the number of frames saved per second, seconds
# determines the length of the video (implemented through saving a set 
# number of frames at a specified frame rate) and a scale_factor of 
# eg. 0.5 halves the width and height of the video.


import cv2
def record_video(fps, seconds, scale_factor=1):
    number_of_frames = int(fps * seconds)
    
    # write something that makes the video go to server
    cap = cv2.VideoCapture(0)
    

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 480
    writer = cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))
    
    counter = 0
    while True:
        counter += 1
        
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx=scale_factor, fy=scale_factor)
        writer.write(frame)
    
        cv2.imshow('frame', frame)
    
        if (cv2.waitKey(1) & 0xFF == ord('q')) or counter == number_of_frames: 
            break
        
    
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    