
# BeautifulSoup 객체를 이용한 웹 문서 처리
# BeautifulSoup: HTML 및 XML 문서를 파싱하여 원하는 데이터를 쉽게 추출할 수 있게 돕는 파이썬 라이브러리

import requests
from bs4 import BeautifulSoup
import requests # HTTP 요청을 보내기 위한 라이브러리
from bs4 import BeautifulSoup # HTML 파싱 및 데이터 추출을 위한 클래스

baseurl = "https://www.naver.com"
# 접속할 대상 URL 설정
baseurl = "https://www.naver.com" 
# User-Agent 설정: 서버 측에서 봇(Bot)으로 인식하여 차단하는 것을 방지하기 위해 브라우저 정보를 헤더에 포함
headers = {'User-Agent':'Mozilla/5.0'}

# requests.get(): 해당 URL에 GET 요청을 보냄
source = requests.get(baseurl, headers=headers)
print(source, type(source))
# <Response [200]> <class 'requests.models.Response'>
print(source.status_code)
# status_code: HTTP 상태 코드 (200은 성공, 404는 페이지 없음, 500은 서버 에러 등)
print(source.status_code) 

# print(source.text, type(source.text))       # <class 'str'> - 단순 문자열->원하는 작업을 할 수 없음
# print(source.content, type(source.content))     # <class 'bytes'> - binary 데이터가 넘어옴

conv_data = BeautifulSoup(source.text, 'lxml')      # parser는 선택(html.parser 또는 lxml)
# BeautifulSoup(마크업문자열, 파서): 문자열 형태의 HTML을 구조화된 객체로 변환
# 'lxml' 파서: 속도가 빠르고 유연한 파싱 능력을 가진 외부 라이브러리 파서 (설치 필요)
conv_data = BeautifulSoup(source.text, 'lxml')      # parser는 선택(html.parser 또는 lxml)
# print(conv_data, type(conv_data))   # <class 'bs4.BeautifulSoup'> 객체 -> 명령어 적용 가능(작업 가능)

# <a> tag 잡아오기
# find_all('태그명'): 문서 내에서 해당 태그를 모두 찾아 리스트 형태로 반환
for atag in conv_data.find_all('a'):
    href = atag.get('href')
    title = atag.get_text(strip=True)
    if title:
# .get('속성명'): 태그 내의 특정 속성값(여기서는 링크 주소인 href)을 추출
        href = atag.get('href') 
# .get_text(): 태그 사이의 텍스트 노드만 추출
# strip=True: 텍스트 앞뒤의 공백 및 줄바꿈 제거
        title = atag.get_text(strip=True) 
        if title: # 텍스트 내용이 존재하는 경우에만 출력
            print(href)
            print(title)
            print('------------------')