import os
import socket
import struct
import json
import hashlib
import threading


class RecvServer:
    def __init__(self):
        self.skt = socket.socket()
        self.recvdir = None
        self.totsize = 0
        self.recved = 0
        self.recved_info={}

    def set_recvdir(self, path):
        self.recvdir = path

    def logout(self, info):
        pass

    def updateprocess(self, recved):
        pass

    def sever_for_ever(self, adr, port, path, maxlisten=5):
        print('ready for connect')
        self.set_recvdir(path)
        self.skt.bind((adr, port))
        self.skt.listen(maxlisten)
        while True:
            conn, adr = self.skt.accept()
            # self.logout('已经连接' + adr[0])
            t = threading.Thread(target=RecvServer.receive, args=[self, conn])
            t.start()

    def receive(self, conn):
        self.recv_all_dir(conn)
        conn.close()

    def recv_file(self, conn):
        s = struct.calcsize('q')
        head_len_byte = conn.recv(s)
        head_len = struct.unpack('q', head_len_byte)[0]
        head_info_byte = conn.recv(head_len)
        head_info = json.loads(head_info_byte)
        name = self.recvdir + '/' + head_info['name']
        size = head_info['file_size']
        md5 = head_info['md5']
        recved = 0
        buffersize = 128*1024*1024
        f = open(name, 'wb+')
        while recved < size:
            if size - recved >= buffersize:
                data = conn.recv(buffersize)
            else:
                data = conn.recv(size - recved)
            f.write(data)
            recved += len(data)
        f.seek(0)
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        remd5 = md5_obj.hexdigest()
        f.close()
        if md5 == remd5:
            conn.send(b'1')
            self.recved += size
            self.updateprocess(self.recved)
            return True
        else:
            conn.send(b'0')
            return False

    def recv_all_dir(self, conn):
        self.recved = 0
        intlen = struct.calcsize('q')
        len_bytes = conn.recv(intlen)
        if len(len_bytes) == 0:
            return
        commit_info_len = struct.unpack('q', len_bytes)[0]
        commit_info_bytes = conn.recv(commit_info_len)
        commit_info = json.loads(commit_info_bytes.decode())
        intlen = struct.calcsize('2q')
        len_bytes = conn.recv(intlen)
        info_len, self.totsize = struct.unpack('2q', len_bytes)
        dir_info_bytes = conn.recv(info_len)
        dir_info = json.loads(dir_info_bytes.decode())
        if os.path.exists(self.recvdir+'/'+dir_info[0]):
            conn.send(b'0')
            return
        else:
            conn.send(b'1')
            for dirname in dir_info:
                os.mkdir(self.recvdir+'/'+dirname)
        len_bytes = conn.recv(intlen//2)
        num = struct.unpack('q', len_bytes)[0]
        for i in range(num):
            while True:
                res = self.recv_file(conn)
                if res:
                    break
        # self.logout(self.recvdir+'/'+dir_info[0] + '接收完成')
        self.logout("{:<15}{:>15}".format("准考号："+commit_info[0], commit_info[1])+"号机 接收完成")
        self.recved_info[commit_info[1]] = commit_info[0]


if __name__ == '__main__':
    server = RecvServer()
    server.sever_for_ever('192.168.2.216', 8888, 'G:')