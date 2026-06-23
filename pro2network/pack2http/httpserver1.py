# html이 가능한 http server
# 💡 소프트웨어에서의 HTTP Server ( 웹서버 ) 란, 웹 브라우저와 같은 "클라이언트" 로 부터 HTTP 프로토콜로 요청을 받고,
# 요청에 대해 HTML 문서와 같은 정적인 웹 페이지를 응답해주는 소프트웨어 입니다.

# 웹 사용자가 어떻게 호스트 파일들에 접근하는지를 관리
# HTTP 서버는 URL(Web address)과 HTTP의 소프트웨어 일부임

# 단순한 HTTP Server 구축 - 기본적인 socket 연결 관리

from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 7777

handler = SimpleHTTPRequestHandler      # get 요청에 대해 문서를 읽어, 클라이언트로 전송하는 역할

# HTTP 서버 객체 생성
serv = HTTPServer(('127.0.0.1', PORT), handler)
print('웹 서비스 시작...')
serv.serve_forever()        # 웹 서비스 무한 루핑