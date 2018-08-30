#Author:ike yang
import socket
import os
import json
from my_socket import tran_recv
server_file_path=os.path.join(os.getcwd(),'server_file')
# print(server_file_path)
file_list=os.listdir(server_file_path)

sk=socket.socket()

sk.bind(('127.0.0.1',8086))
sk.listen()
conn,addr=sk.accept()
my_sk=tran_recv(conn)

my_sk.json_data_trans(file_list)
client_choose=my_sk.data_recv()
my_sk.file_trans(server_file_path,client_choose)




conn.close()
sk.close()












