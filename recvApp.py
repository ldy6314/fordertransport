from recvUi import ReceiveUi
from recvserver import RecvServer
from tkinter import messagebox
from threading import Thread
from tkinter import INSERT, END


class RecvApp(RecvServer, ReceiveUi):
    def __init__(self):
        ReceiveUi.__init__(self)
        RecvServer.__init__(self)

    def start_serve(self):
        if not self.path.get():
            messagebox.showerror('错误', '没有设置接收文件夹')
            return
        self.recvdir = self.path.get().strip('/')
        self.logout(self.recvdir+'文件夹准备接收文件')
        t = Thread(target=self.sever_for_ever, args=[self.ipinfo(), 8888, self.recvdir])
        t.start()

    def logout(self, info):
        self.log.config(state='normal')
        self.log.insert(INSERT, info+'\n')
        self.log.see(END)
        self.log.config(state='disable')

    def updateprocess(self, recved):
        self.precessbar['value'] = int((recved/self.totsize)*100)
        self.percent['text'] = str(self.precessbar['value'])+' %'
        self.precessbar.grid(row=0, column=1, columnspan=3)
        self.secondwin.update()
        self.secondwin.deiconify()
        if self.precessbar['value'] == 100:
            self.secondwin.withdraw()

    def info_out(self):
        with open("提交信息.csv", "w") as fout:
            fout.write("试卷提交信息\n")
            fout.write("机器号,准考证号\n")
            commit_info = list(self.recved_info.items())
            commit_info.sort(key=lambda x: int(x[0]))
            for key in commit_info:
                fout.write(key[0]+','+key[1]+'\n')


if __name__ == '__main__':
    app = RecvApp()
    app.mainloop()
