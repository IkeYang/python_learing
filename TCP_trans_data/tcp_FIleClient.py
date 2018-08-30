#Author:ike yang
import socket,os
from my_socket import tran_recv
client_file_path=os.path.join(os.getcwd(),'client_file')
sk=socket.socket()
sk.connect(('127.0.0.1',8086))
my_sk=tran_recv(sk)
meg=my_sk.json_data_recv()
for k,v in enumerate(meg):
    print(k,v)
while True:
    try:
        file_choose=meg[int(input("请输入选择的文件序号："))]
        break
    except:
        print('invalid input ,please tyr again')
my_sk.data_trans(file_choose)
my_sk.file_recv(os.path.join(client_file_path,file_choose))
sk.close()









