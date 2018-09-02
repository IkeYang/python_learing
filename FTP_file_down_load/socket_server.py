#Author:ike yang
import socketserver
import os
import hashlib
import pickle
from my_socket import tran_recv
server_file_path=os.path.join(os.getcwd(),'server_file')
db_file_path=os.path.join(os.getcwd(),'db')

# print(server_file_path)
file_list=os.listdir(server_file_path)
client_choose=None
def getMd5(file_path,file_name,size_file=None):
    a=hashlib.md5()
    if size_file==None:
        size_file = os.path.getsize(os.path.join(file_path,file_name))
    with open(os.path.join(file_path,file_name), 'rb') as f:
        while size_file:
            if size_file >= 1024:
                content = f.read(1024)

                size_file -=1024

                a.update(content)
            else:
                content = f.read(size_file)
                a.update(content)
                break
    return a.hexdigest()
class my_socket(socketserver.BaseRequestHandler):
    def downLoadFile(self,my_sk):
        my_sk.json_data_trans(file_list)
        client_choose = my_sk.data_recv()
        md5 = my_sk.file_trans(server_file_path, client_choose)
        my_sk.data_trans(md5)
        return client_choose
    def handle(self):
        while True:
            try:
                # msg = self.request.recv(1024).decode('utf-8')
                # if msg =='q':
                #     print(msg)
                #     break
                # print(msg)
                # my_send = input('>>>')
                # self.request.send(my_send.encode('utf-8'))  # conn

                my_sk = tran_recv(self.request)
                addr = self.client_address
                name=my_sk.data_recv()
                if os.path.exists(os.path.join(db_file_path,name)):
                    with open(db_file_path + '\%s' % (name), mode='rb') as f:
                        meg = pickle.load(f)
                    if meg['filename']!=None:
                        self.request.send(b'0')#告诉客户端存在上次非正常退出
                        with open(db_file_path + '\%s' % (name), mode='rb') as f:
                            meg=pickle.load(f)
                        my_sk.data_trans(meg['filename'])
                        num=self.request.recv(1)
                        if num ==b'0':#客户端拒绝重新下载文件
                            self.downLoadFile(my_sk)
                        elif num==b'1': #客户端接收重新下载文件
                            file_clent_md5=my_sk.data_recv()
                            file_clent_size=int(my_sk.data_recv())
                            file_server_md5=getMd5(server_file_path,meg['filename'],file_clent_size)
                            if file_server_md5==file_clent_md5:
                                my_sk.file_trans(server_file_path, meg['filename'],seek=file_clent_size)
                                md5=getMd5(server_file_path,meg['filename'])
                                my_sk.data_trans(md5)
                                os.remove(os.path.join(db_file_path,name))
                        # else:
                        #     md5 = my_sk.file_trans(server_file_path, meg['filename'])
                        #     my_sk.data_trans(md5)
                    else:
                        self.request.send(b'1')
                        my_sk.json_data_trans(file_list)
                        client_choose = my_sk.data_recv()
                        md5 = my_sk.file_trans(server_file_path, client_choose)
                        my_sk.data_trans(md5)

                else:
                    self.request.send(b'1')
                    my_sk.json_data_trans(file_list)
                    client_choose = my_sk.data_recv()
                    md5 = my_sk.file_trans(server_file_path, client_choose)
                    my_sk.data_trans(md5)

            except ConnectionResetError:
                print('\nclient disconnected')
                with open(db_file_path+'\%s'%(name),mode='wb') as f:
                    wrong_message={'addr':addr,'filename':client_choose}
                    pickle.dump(wrong_message,f)
                break



server=socketserver.ThreadingTCPServer(('192.168.1.106',9000),my_socket)
server.serve_forever()













