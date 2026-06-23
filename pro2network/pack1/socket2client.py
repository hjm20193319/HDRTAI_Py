# client

from socket import *

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect(('127.0.0.1', 7788))     # 능동적으로 연결을 시도
clientsock.send('안녕 잘지내'.encode(encoding='utf_8', errors = 'strict'))      # 인코딩한것을 보냄

print('수신자료 : ', clientsock.recv(1024).decode())

clientsock.close()
clientsock.close()
