# Script containing a function that starts a recording using the webcam of the
# laptop. The function takes "fps", "seconds" and "scale_factor" as arguments
# where fps determines the number of frames saved per second, seconds
# determines the length of the video (implemented through saving a set
# number of frames at a specified frame rate) and a scale_factor of
# eg. 0.5 halves the width and height of the video.


import cv2
import srd290_lab1_connect as srd
import pandas as pd
from datetime import datetime
import os

def record_video(fps, seconds, scale_factor=1, meta_data={}):
    number_of_frames = int(fps * seconds)

    # write something that makes the video go to server
    cap = cv2.VideoCapture(0)

    local_name = 'basicvideo.mp4'
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)*scale_factor) # 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*scale_factor) # 480
    writer = cv2.VideoWriter(local_name, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width, height))

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
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    remote_name = f'/home/srd290_lab1/Documents/RockPaperScissors/data/'+meta_data['Hand']+'_'+meta_data['Name']+'_'+dt+'.mp4'
    srd.transfer_local_file(local_name,remote_name)
    data = {
        'hand_sign': meta_data['RPS'],
        'left_or_right_hand': meta_data['Hand'],
        'record_time': dt,
        'movie_file_path': remote_name,
        'pixel_width': int(width),
        'pixel_height': int(height),
        'fps':fps,
        'number_frames': number_of_frames,
        'photo_model': meta_data['Name'],
        'angle': meta_data['Angle'],
        'file_format':'.mp4'
    }
    dataframe = pd.DataFrame(data,index=[0])
    srd.add_new_movie(dataframe)

    os.remove(local_name)