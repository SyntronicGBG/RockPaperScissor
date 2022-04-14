from tkinter import *
from tkinter import ttk
import data_collector

class DataCollection:
    def __init__(self, root):
        # configure the root Tk window
        root.title('Data Collection')
        root.minsize(640,150)
        root.resizeable=(False,False)
        root.configure(background='#e1d8b9')

        # set all styles for the different ttk object types
        style = ttk.Style()
        style.configure('TFrame', background='#e1d8b9', font=('Arial',11))
        style.configure('TLabel', background='#e1d8b9', font=('Arial',11))
        style.configure('Header.TLabel', font=('Arial',18,'bold'))
        style.configure('TButton', background='#e1d8b9', font=('Arial',11))
        style.configure('TCombobox', background='#e1d8b9', font=('Arial',11))
        style.configure('TRadiobutton', background='#e1d8b9', font=('Arial',11))
        style.configure('Message.TLabel', background='#e1d8b9', font=('Arial',10))

        # set up a frame for the title and short description of how to play
        self.frame_header = ttk.Frame(root)
        self.frame_header.pack()
        ttk.Label(self.frame_header, text='Rock Paper Scissors Data Collection',style='Header.TLabel').pack()
        ttk.Label(self.frame_header, text='Set your meta data, choose number of recordings, press record, play!').pack()

        # set up a frame for all meta data
        self.frame_meta = ttk.Frame(root)
        self.frame_meta.pack()
        
        # add radiobuttons for each of the three end results
        self.result = StringVar(None, 'Rock')
        ttk.Radiobutton(self.frame_meta, text='Rock', variable=self.result, value='Rock').grid(row=0,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Paper', variable=self.result, value='Paper').grid(row=1,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Scissors', variable=self.result, value='Scissors').grid(row=2,column=0, sticky='w')
        
        # add labels for each meta data column
        ttk.Label(self.frame_meta,text='Name:').grid(row=0,column=1,sticky='e',padx=5)
        ttk.Label(self.frame_meta,text='Angle:').grid(row=1,column=1,sticky='e',padx=5)
        ttk.Label(self.frame_meta,text='Hand:').grid(row=2,column=1,sticky='e',padx=5)

        # set the entry name
        self.name = StringVar()
        self.entry_name = ttk.Entry(self.frame_meta, textvariable=self.name)
        self.entry_name.grid(row=0,column=2,sticky='w')

        # set the combobox for the angle of the hand toward the camera
        self.angle_of_hand = StringVar(None,'Outside')
        self.angle = ttk.Combobox(self.frame_meta, textvariable=self.angle_of_hand,
                                  values=('Inside','Frontal','Outside'))
        self.angle.grid(row=1,column=2,sticky='w')

        # set the combobox for which hand is used
        self.l_r_hand = StringVar(None,'Right')
        self.hand = ttk.Combobox(self.frame_meta, textvariable=self.l_r_hand,
                                 values=('Left','Right'))
        self.hand.grid(row=2, column=2,sticky='w')
        
        # set up a frame for the recording actions
        self.frame_record = ttk.Frame(root)
        self.frame_record.pack()

        #self.logo = PhotoImage(file=r'C:\Users\emnixa\Documents\RockPaperScissors\Data Collection\peace.png')
        #self.video = ttk.Label(self.frame_record,image=self.logo).grid(row=0,column=0,sticky='w',padx=10)

        ttk.Label(self.frame_record,text='Number of recordings:').grid(row=0,column=0,sticky='e',padx=5)
        self.n_recordings = IntVar(None, 1)
        self.spinbox_recordings = ttk.Spinbox(self.frame_record, textvariable=self.n_recordings,
                                              from_=0, to=50).grid(row=0,column=1,sticky='w',padx=10)
        # set up the button for recording
        self.button_record = ttk.Button(self.frame_record,text='Record',command=self.record)
        self.button_record.grid(row=0,column=2,sticky='e',padx=10)

        # set up message of recording status
        self.status = StringVar()
        self.label_record = ttk.Label(self.frame_record,style='Message.TLabel', textvariable=self.status)
        self.label_record.grid(row=0,column=3,sticky='w')

    
    def record(self):
        self.button_record.state(['disabled'])
        if not self.name.get():
            self.status.set('Must enter a name of the player')
            self.label_record.configure(foreground='red')
        elif not self.n_recordings.get():
            self.status.set('Must enter number of recordings')
            self.label_record.configure(foreground='red')
        else:
            print(self.get_meta_data())
            try:
                n_recs = self.n_recordings.get()
                for i in range(n_recs):
                    # record and save the video
                    data_collector.record_video(30, 2, 1, self.get_meta_data())
                    # let the user know it was successful
                    self.status.set('Recording ' + str(i+1) + '/' + str(n_recs) + ' successful!')
                    self.label_record.configure(foreground='green')
            except:
                # let the user know something went wrong
                self.status.set('Recording unsuccessful!')
                self.label_record.configure(foreground='red')
        self.button_record.state(['!disabled'])
    
    def get_meta_data(self):
        meta_data = {'RPS': self.result.get(),
                     'Angle': self.angle.get(),
                     'Name': self.entry_name.get(),
                     'Hand': self.hand.get()}
        return meta_data

def main():
    root = Tk()
    DataCollection(root)
    root.mainloop()

if __name__ == '__main__':
    main()