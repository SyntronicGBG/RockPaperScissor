import cv2
def record_video(fps, seconds, crop_width=640, crop_height=480, scale_factor=1, ):
    number_of_frames = int(fps * seconds)
    
    # write something that makes the video go to server
    cap = cv2.VideoCapture(0)
    
    width= int(crop_width * scale_factor) # max 640
    height= int(crop_height * scale_factor) # max 480
    writer= cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))
    
    counter = 0
    while True:
        counter += 1
        
        ret,frame = cap.read()
        # enables cropping and resizing, commented out until further notice
        frame = cv2.resize(frame[:,80:560], (0,0), fx=scale_factor, fy=scale_factor)
        writer.write(frame)
    
        cv2.imshow('frame', frame)
    
        if (cv2.waitKey(1) & 0xFF == ord('q')) or counter == number_of_frames: 
            break
        
    
    cap.release()
    writer.release()
    cv2.destroyAllWindows()