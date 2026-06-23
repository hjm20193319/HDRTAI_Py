# socket : 소켓은 프로세스가 드넓은 네트워크 세계로 데이터를 내보내거나 혹은 그 세계로부터 데이터를 받기 위한 실제적인 창구역할을 한다
# 그러므로 프로세스가 데이터를 보내거나 받기 위해서는 반드시 소켓을 열어서 소켓에 데이터를 써보내거나 소켓으로부터 데이터를 읽어들여야한다

# socket이란 TCP / IP 의 프로그래머 인터페이스이다
# 통신 기기간 대화가 가능하도록 하는 통신 방식으로 클라이언트 / 서버 모델에 기초한다

# 연결지향 : TCP/IP
# 비연결지향 : UDP

# socket 통신 확인

import socket

# 서로 목적과 용도가 다름 / 내부적으로는 모두 TCP 사용중
# port number 확인하기 -- 0 ~ 1024는 사용하지 않아야 한다(8080, 1521, 3306, 5421 등도 이미 사용중)
print(socket.getservbyname('http', 'tcp'))          # www환경 전송 규약
print(socket.getservbyname('ssh', 'tcp'))           # 원격 컴 접속 규약
print(socket.getservbyname('ftp', 'tcp'))           # 파일 전송 proto
print(socket.getservbyname('smtp', 'tcp'))          # 메일 송수신 proto
print(socket.getservbyname('pop3', 'tcp'))          # 이메일 Proto

print(socket.getaddrinfo('www.daum.net', 80, proto = socket.SOL_TCP))













