from tkinter import *
from tkinter import ttk

class DataCollection:
    def __init__(self, root):
        self.frame_header = ttk.Frame(root)
        self.frame_header.pack()
        ttk.Label(self.frame_header, text='Rock Paper Scissors Data Collection').pack()
        ttk.Label(self.frame_header, text='Set your meta data, record, play, save').pack()

        self.frame_meta = ttk.Frame(root)
        self.frame_meta.pack()
        
        self.result = StringVar()
        ttk.Radiobutton(self.frame_meta, text='Rock', variable=self.result, value='Rock').grid(row=0,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Paper', variable=self.result, value='Paper').grid(row=1,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Scissors', variable=self.result, value='Scissors').grid(row=2,column=0, sticky='w')
        
        ttk.Label(self.frame_meta,text='Name:').grid(row=0,column=1,sticky='w')
        ttk.Label(self.frame_meta,text='Angle:').grid(row=1,column=1,sticky='w')
        ttk.Label(self.frame_meta,text='Counts:').grid(row=2,column=1,sticky='w')

        self.entry_name = ttk.Entry(self.frame_meta).grid(row=0,column=2,sticky='w')
        self.angle_of_hand = StringVar()
        self.angle = ttk.Combobox(self.frame_meta, textvariable=self.angle_of_hand,
                                  values=('inside','in front','outside')).grid(row=1,column=2,sticky='w')
        self.count = ttk.Label(self.frame_meta, text='There are no data points with this meta combo').grid(row=2,column=2,sticky='w')
        
        self.frame_record = ttk.Frame(root)
        self.frame_record.pack()

        self.logo = PhotoImage(file=r'C:\Users\emnixa\Documents\RockPaperScissors\Data Collection\peace.png').subsample(10,10)
        self.video = ttk.Label(self.frame_record,image=self.logo).grid(row=0,column=0,sticky='w')

        ttk.Button(self.frame_record,text='Play',command=self.play).grid(row=0,column=1,sticky='se')
    
    def play(self):
        print('Play!')

def main():
    root = Tk()
    data_collection = DataCollection(root)
    root.mainloop()

if __name__ == '__main__':
    main()