# -*- coding: utf-8 -*-   
# 한글 깨짐 현상 해결 - 위 명령 안 먹으면 아래 방법 사용
import sys
sys.stdout.reconfigure(encoding='utf-8')   

import os
import urllib.parse

# --- get / post 요청 받을 때 ---------
method = os.environ.get("REQUEST_METHOD", "GET")

if method == "POST":                                # post 방식일때
    length = int(os.environ.get("CONTENT_LENGTH", 0))   # POST 데이터의 길이를 환경 변수에서 가져옵니다.
    body_bytes = sys.stdin.buffer.read(length)          # 표준 입력(stdin)에서 해당 길이만큼 데이터를 읽습니다.
    body = body_bytes.decode('utf-8')                   # 데이터는 바이트(bytes) 형태이므로, .decode('utf-8')로 문자열로 변환합니다.
else:
    body = os.environ.get("QUERY_STRING", "")       # get 방식일때

params = urllib.parse.parse_qs(body)                # 읽어온 데이터를 딕셔너리로 파싱합니다. (이 부분은 GET과 동일)

irum = params.get("name", [""])[0]
junhwa = params.get("phone", [""])[0]
gen = params.get("gen", [""])[0]

print("Content-Type: text/html; charset=utf-8")
print()
print("""
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>world</title>
</head> 
<body>
    입력한 값은 : 이름은 {0} 전화는 {1} 성별은 {2} 
</body>
</html>
""".format(irum, junhwa, gen))