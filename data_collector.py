# Script containing a function that starts a recording using the webcam of the
# laptop. The function takes "fps", "seconds" and "scale_factor" as arguments
# where fps determines the number of frames saved per second, seconds
# determines the length of the video (implemented through saving a set
# number of frames at a specified frame rate) and a scale_factor of
# eg. 0.5 halves the width and height of the video.


import cv2
import pandas as pd
from datetime import datetime
import os
from ssh_connection import SSHConnection
from sql_connection import SQLConnection

class DataCollector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.ssh_connection = SSHConnection(service='RockPaperScissors',
                                            username='srd290_lab1',
                                            server='10.8.128.233',
                                            port=22)
        self.sql_connection = SQLConnection(service='RockPaperSciccors',
                                            username='SA',
                                            server='10.8.128.233',
                                            database='RockPaperScissors')

    def close(self):
        self.ssh_connection.close()
        self.sql_connection.close()
        self.cap.release()
        cv2.destroyAllWindows()

    def record_video(self, meta_data, scale_factor=1):
        """Records a video, length specified in meta_data.

        Args:
            meta_data (dictionary): Contains all meta data associated with the video
            scale_factor (number > 0): Width and height of video is multiplied
            by this value
        """

        local_name = meta_data['movie_file_path']
        fps = meta_data['fps']

        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)*scale_factor) # 640
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*scale_factor) # 480
        writer = cv2.VideoWriter(local_name, fourcc, fps, (width, height))

        meta_data['file_format'] = '.mp4'
        meta_data['pixel_width'] = width
        meta_data['pixel_height'] = height
        meta_data['record_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        total_of_frames = meta_data['number_frames']
        counter_of_frames = 0
        while counter_of_frames < total_of_frames:
            counter_of_frames += 1

            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (0,0), fx=scale_factor, fy=scale_factor)
            writer.write(frame)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        writer.release()

    def transfer_video(self, meta_data):
        """Transfers the video to the sql-database.

        Args:
            meta_data (dictionary): Contains all meta data associated with the video

        """
        local_name = meta_data['movie_file_path']
        hand = meta_data['left_or_right_hand']
        name = meta_data['photo_model']
        dt = meta_data['record_time']
        remote_name = os.sep.join(['home',
                                    'srd290_lab1',
                                    'Documents',
                                    'RockPaperScissors',
                                    'data',
                                    f'{hand}_{name}_{dt}.mp4'])
        self.ssh_connection.transfer_local_file(local_name, remote_name)
        self.remove_video(meta_data)
        meta_data['movie_file_path'] = remote_name
        dataframe = pd.DataFrame(meta_data, index=[0])
        self.sql_connection.add_new_dataframe('movie_data', dataframe)

    def remove_video(self, meta_data):
        local_name = meta_data['movie_file_path']
        os.remove(local_name)
