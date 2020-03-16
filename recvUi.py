import tkinter
import socket
import tkinter.filedialog
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import W, E


class ReceiveUi:
    def __init__(self):
        self.win = tkinter.Tk()
        self.win.geometry('700x450')
        self.win.resizable(width=False, height=False)
        self.win.title('信息学收卷客户端')
        self.label1 = ttk.Label(text='收卷ip').grid(row=0, column=0)
        self.iplebel = ttk.Label(text=self.ipinfo()).grid(row=0, column=1)
        self.label2 = ttk.Label(text='接收文件夹').grid(row=1, column=0, padx=10)
        self.path = tkinter.StringVar()
        self.ent = ttk.Entry(text=self.path, width=60, state='readonly').grid(row=1, column=1)
        self.choosebutton = ttk.Button(text='设置文件夹', command=self.dirask).grid(row=1, column=2)
        self.startbutton = ttk.Button(text='开始接收', command=self.start_serve).grid(row=1, column=3)
        self.info_outbutton = ttk.Button(text='导出信息', command=self.info_out).grid(row=4, column=3)
        # self.label31 = ttk.Label().grid(row=2, column=0)
        self.label3 = ttk.Label(text='传输详情').grid(row=2, column=1)
        self.log = scrolledtext.ScrolledText(state='disable')
        self.log.grid(row=3, column=0, columnspan=4, padx=10, sticky=W+E)
        self.secondwin = tkinter.Toplevel()
        self.secondwin.title('传输进度')
        self.secondwin.withdraw()
        self.percent = ttk.Label(self.secondwin, text='')
        self.percent.grid(row=0, column=0)
        self.precessbar = ttk.Progressbar(self.secondwin, length=500, mode='determinate', value=0)

    def dirask(self):
        path = tkinter.filedialog.askdirectory()
        self.path.set(path)

    def info_out(self):
        pass

    def start_serve(self):
        pass

    def ipinfo(self):
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        return ip

    def mainloop(self):
        self.win.mainloop()


if __name__ == '__main__':
    rcv = ReceiveUi()
    rcv.mainloop()
