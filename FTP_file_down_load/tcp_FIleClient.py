#Author:ike yang
import socket,os
from my_socket import tran_recv
import hashlib

def file_trans_my(my_skobj):
    meg=my_skobj.json_data_recv()
    for k,v in enumerate(meg):
        print(k,v)
    while True:
        try:
            file_choose=meg[int(input("请输入选择的文件序号："))]
            break
        except:
            print('invalid input ,please tyr again')
    my_skobj.data_trans(file_choose)
    md5my=my_skobj.file_recv(os.path.join(client_file_path,file_choose))
    md5_server=my_skobj.data_recv()
    if md5_server==md5my:
        print('correct file ')
    else:
        print('wrong file')
def getMd5(filePath,fileName):
    a = hashlib.md5()
    with open(os.path.join(filePath,fileName), mode='rb') as f:
        content = f.read(1024)
        a.update(content)
        while content:
            content = f.read(1024)
            a.update(content)
    return a.hexdigest()



client_file_path=os.path.join(os.getcwd(),'client_file')
sk=socket.socket()
sk.connect(('127.0.0.1',9000))
my_sk=tran_recv(sk)
my_sk.data_trans('ike_yang')
num=sk.recv(1)
if num ==b'1':
    file_trans_my(my_sk)
elif num==b'0':
    name_wrong=my_sk.data_recv()
    print('you have disconnected last time unnormally,the filename is %s'%name_wrong)
    choose_wrong=input('continue download?(Y:1,N:0)')
    if choose_wrong=='0':
        sk.send(b'0')
        file_trans_my(my_sk)
    elif choose_wrong=='1':
        sk.send(b'1')
        file_path=os.path.join(os.path.join(os.getcwd(),'client_file'),name_wrong)
        wrongFileMd5=getMd5(os.path.join(os.getcwd(),'client_file'),name_wrong)
        my_sk.data_trans(wrongFileMd5)
        size_file = os.path.getsize(file_path)
        my_sk.data_trans(str(size_file))
        my_sk.file_recv(os.path.join(client_file_path,name_wrong),'ab')
        md5_server=my_sk.data_recv()
        md5_client=getMd5(client_file_path,name_wrong)
        if md5_server == md5_client:
            print('correct file ')
        else:
            print('wrong file')



sk.close()









