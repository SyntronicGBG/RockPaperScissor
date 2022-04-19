# from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import StringVar
# import data_collector
from data_collector import DataCollector


class DataCollectionGUI:
    def __init__(self, root):
        self.dc = DataCollector()

        root.title('Data Collection')
        root.resizeable=(False,False)
        root.configure(background='#e1d8b9')

        style = ttk.Style()
        style.configure('TFrame', background='#e1d8b9', font=('Arial',11))
        style.configure('TLabel', background='#e1d8b9', font=('Arial',11))
        style.configure('Header.TLabel', font=('Arial',18,'bold'))
        style.configure('TButton', background='#e1d8b9', font=('Arial',11))
        style.configure('TCombobox', background='#e1d8b9', font=('Arial',11))
        style.configure('TRadiobutton', background='#e1d8b9', font=('Arial',11))

        self.frame_header = ttk.Frame(root)
        self.frame_header.pack()
        ttk.Label(self.frame_header, text='Rock Paper Scissors Data Collection',style='Header.TLabel').pack()
        ttk.Label(self.frame_header, text='Set your meta data, record, play, save').pack()

        self.frame_meta = ttk.Frame(root)
        self.frame_meta.pack()

        self.result = StringVar(None, 'Rock')
        ttk.Radiobutton(self.frame_meta, text='Rock', variable=self.result, value='Rock').grid(row=0,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Paper', variable=self.result, value='Paper').grid(row=1,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Scissors', variable=self.result, value='Scissors').grid(row=2,column=0, sticky='w')

        ttk.Label(self.frame_meta,text='Name:').grid(row=0,column=1,sticky='e',padx=5)
        ttk.Label(self.frame_meta,text='Angle:').grid(row=1,column=1,sticky='e',padx=5)
        ttk.Label(self.frame_meta,text='Counts:').grid(row=2,column=1,sticky='e',padx=5)

        self.name = StringVar(None, 'NoName')
        self.entry_name = ttk.Entry(self.frame_meta, textvariable=self.name)
        self.entry_name.grid(row=0,column=2,sticky='w')
        self.angle_of_hand = StringVar(None,'inside')
        self.angle = ttk.Combobox(self.frame_meta, textvariable=self.angle_of_hand,
                                  values=('inside','in front','outside'))
        self.angle.grid(row=1,column=2,sticky='w')
        self.l_r_hand = StringVar(None,'Left')
        self.hand = ttk.Combobox(self.frame_meta, textvariable=self.l_r_hand,
                                 values=('Left','Right'))
        self.hand.grid(row=2, column=2,sticky='w')
        #self.count = ttk.Label(self.frame_meta, text='There are no data points with this meta combo')
        #self.count.config(wraplength=180)
        #self.count.grid(row=2,column=2,sticky='sw')

        self.frame_record = ttk.Frame(root)
        self.frame_record.pack()

        #self.logo = PhotoImage(file=r'C:\Users\emnixa\Documents\RockPaperScissors\Data Collection\peace.png')
        #self.video = ttk.Label(self.frame_record,image=self.logo).grid(row=0,column=0,sticky='w',padx=10)

        ttk.Button(self.frame_record,text='Play',command=self.play_action).grid(row=0,column=1,sticky='e',padx=10)

    def close(self):
        self.dc.close()

    def play_action(self):
        meta_data = {
                'hand_sign': self.result.get(),
                'left_or_right_hand': self.hand.get(),
                'photo_model': self.entry_name.get(),
                'angle': self.angle.get(),
                'movie_file_path': 'basicvideo.mp4',
                'fps': 30,
                'number_frames': 30*2,
                }
        print(meta_data)
        self.dc.record_video(meta_data)
        print(meta_data)
        self.dc.transfer_video(meta_data)
        print(meta_data)


def main():
    root = Tk()
    dcg = DataCollectionGUI(root)
    root.mainloop()
    dcg.close()

if __name__ == '__main__':
    main()