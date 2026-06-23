# 일회용 서버

from socket import *

# 소켓 객체 생성
serversock = socket(AF_INET, SOCK_STREAM)       # socekt 유형 중 stream
serversock.bind(('127.0.0.1', 8888))            # socket을 주소(특정 컴)에 바인딩 , 튜플 타입
serversock.listen(5)        # 클라이언트와 연결 정보수, 리스너 설정
print('서버서비스 중...')

conn, addr = serversock.accept()        # 수동적으로 연결을 받아들임
print('client addr : ', addr)
print('from client message : ', conn.recv(1024).decode())       # 인코딩 된 것을 디코딩 함
conn.close()
serversock.close()
