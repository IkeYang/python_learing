#Author:ike yang
import socket
from processBar import processBar
class tran_recv():
    '''
    在建立连接后实现数据，文件，的传输

    '''
    def __init__(self,sk):
        '''

        :param sk: a socket object or a conn
        '''
        self.sk=sk

    def data_trans(self,data):
        '''

        :param data: utf-8 style data
        :return:
        '''
        # self.sk=socket.socket()
        # print(str(len(data)))
        self.sk.send(str(len(str(data).encode('utf-8'))).encode('utf-8'))
        self.sk.recv(1024)
        self.sk.send(data.encode('utf-8'))
    def data_recv(self):
        '''

        :return: data utf-8 style
        '''

        len_data=int(self.sk.recv(1024).decode('utf-8'))
        self.sk.send(b'ok')
        return self.sk.recv(len_data).decode('utf-8')
    def json_data_trans(self,data):
        '''

        :param data: utf-8 style data list
            direction ect..
        :return:
        '''
        # self.sk=socket.socket()
        # print(str(len(data)))
        import json
        json_data=json.dumps(data)
        self.sk.send(str(len(json_data.encode('utf-8'))).encode('utf-8'))
        self.sk.recv(1024)
        self.sk.send(json_data.encode('utf-8'))
    def json_data_recv(self):
        '''

        :return: data utf-8 style json to bytes data
        '''
        import json
        len_data=int(self.sk.recv(1024).decode('utf-8'))
        self.sk.send(b'ok')
        json_data=self.sk.recv(len_data).decode('utf-8')
        return json.loads(json_data)
    def file_trans(self,path,name,buffer=1024,seek=0):
        '''

        :param path: the filedir which your file stored in
        :param name: the file's name
        :param buffer: the amount of bytes to be sent as once
        :param seek: the begining of the file to read
        :return: the md5 of file
        '''
        import hashlib
        import os,json,struct
        a = hashlib.md5()
        file_path=os.path.join(path,name)
        size_file=os.path.getsize(file_path)
        init_size=size_file
        size_file -= seek
        head={'filename':'name','size':size_file}
        json_head=json.dumps(head)
        bytes_head=json_head.encode('utf-8')
        head_len=len(bytes_head)
        pack_len_by=struct.pack('i',head_len)
        self.sk.send(pack_len_by)
        self.sk.send(bytes_head)
        print(size_file)
        with open(file_path,'rb') as f:
            f.seek(seek)

            while size_file:
                if size_file>=buffer:
                    content=f.read(buffer)
                    self.sk.send(content)
                    size_file-=buffer
                    processBar( init_size-size_file,init_size)
                    a.update(content)
                else:
                    content=f.read(size_file)
                    self.sk.send(content)
                    processBar(init_size, init_size)
                    a.update(content)
                    break
        return a.hexdigest()
    def file_recv(self,path,pattern='wb',buffer=1024):
        '''

        :param path:the dir you want to store file
        :param buffer: the amount of bytes to be received as once (mak sure equal to file_trans's buffer)
        :return:the md5 of file
        '''
        import  json, struct
        import hashlib
        a = hashlib.md5()
        json_head=self.sk.recv(struct.unpack('i',self.sk.recv(4))[0]).decode('utf-8')
        file_head=json.loads(json_head)
        size_file=int(file_head['size'])
        init_size=size_file
        print(size_file,buffer)
        with open(path,pattern) as f:
            while size_file:
                if size_file >= buffer:
                    content=self.sk.recv(buffer)
                    f.write(content)
                    a.update(content)
                    size_file -= buffer
                    processBar(init_size - size_file, init_size)
                else:
                    content = self.sk.recv(size_file)
                    f.write(content)
                    a.update(content)
                    processBar(init_size , init_size)
                    break
        return a.hexdigest()




