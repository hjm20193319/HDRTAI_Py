# BeautifulSoup 객체 메소드 활용
# BeautifulSoup: HTML/XML 파일에서 데이터를 추출하기 위한 파이썬 라이브러리
# 파서(Parser)를 통해 트리 구조의 객체(DOM)를 생성하여 탐색 및 수정을 용이하게 함
from bs4 import BeautifulSoup 

html_page = """
<html>
<body>
<h1>제목 태그</h1>
<p>웹문서 연습</p>
<p>원하는 자료 확인</p>
</body>
</html>
"""
print(type(html_page))  # <class 'str'>
# 문자열(str) 상태로는 HTML 태그 단위의 데이터 추출이 어려움

# BeautifulSoup(마크업, 파서): 문자열을 파싱하여 BeautifulSoup 객체 생성
soup = BeautifulSoup(html_page, 'html.parser')
print(type(soup))       # <class 'bs4.BeautifulSoup'>  : 클래스가 지원하는 메소드 명령을 활용하기 위해서
print()

# DOM 구조를 이용한 자료 접근
# 계층 구조(Tree)를 따라 직접 접근하는 방식
h1 = soup.html.body.h1 
print("h1 : ", h1.string)       # h1 :  제목 태그

p1 = soup.html.body.p # 동일한 태그가 여러 개일 경우 가장 첫 번째 요소만 반환
print("p1 : ", p1.string)       # p1 :  웹문서 연습     * 최초의 p 태그

# .next_sibling: 형제 노드(같은 레벨의 다음 요소)로 이동. 
p2 = p1.next_sibling.next_sibling       # p1.next_sibling은 태그 사이의 줄바꿈/공백(Text 노드)일 수 있음
print("p2 : ", p2.string)       # p2 :  원하는 자료 확인
print()

# find() method 사용한 자료 접근
html_page2 = """
<html>
<body>
<h1 id = "title">제목 태그</h1>
<p>웹문서 연습</p>
<p id = "my" class = "our">원하는 자료 확인</p>
</body>
</html>
"""
soup2 = BeautifulSoup(html_page2, 'html.parser')
# find(tag 명, attrs속성, recursive, string)
# 조건에 맞는 첫 번째 태그 하나만 반환
print(soup2.p, ' ', soup2.p.string)      # <p>웹문서 연습</p>  웹문서 연습
print(soup2.find('p').string)      # 웹문서 연습
print(soup2.find('p', id='my').string)      # 원하는 자료 확인
print(soup2.find('p', class_='our').string)    # 원하는 자료 확인       클래스에는 _ 붙여야 함!! (Python 예약어 class와 충돌 방지)
print(soup2.find(id='title').string)    # 태그명 없이 속성(id)만으로도 검색 가능
print(soup2.find(attrs={'class':'our'}).string)    # attrs 인자에 딕셔너리 형태로 속성 명시 가능
print()

# find_all() method 사용한 자료 접근
html_page3 = """
<html>
<body>
<h1 id = "title">제목 태그</h1>
<p>웹문서 연습</p>
<p id = "my" class = "our">원하는 자료 확인</p>
<div>
    <a href='https://www.naver.com'>네이버</a><br/>
    <a href='https://www.google.com'>구글</a>
</div>
</body>
</html>
"""
soup3 = BeautifulSoup(html_page3, 'html.parser')
# find_all(): 조건에 맞는 모든 태그를 리스트(ResultSet) 형태로 반환
print(soup3.find_all(['a']))    # 리스트 안에 a 태그 잡힘 (복수 태그 선택 가능)
print(soup3.find_all(['a','p'])) # a 태그와 p 태그를 모두 찾아 리스트로 반환
print()
links = soup3.find_all('a')
# print(links)
for link in links:
    # .attrs: 태그의 모든 속성을 딕셔너리 형태로 반환
    href = link.attrs['href'] 
    # .text 또는 .get_text(): 태그 내부의 텍스트만 추출
    text = link.text 
    print(href, ' ', text)
print('------------------')

# 정규 표현식 사용
import re # Regular Expression 모듈
# href 속성값이 'https'로 시작하는(^ 기호) 모든 a 태그 검색
links2 = soup3.find_all(href=re.compile(r'^https'))
# print(links2)
for link in links2:
    href = link.attrs['href']
    text = link.text # 태그 사이의 문자열
    print(href, ' ', text)
print('------------------')

# bugs 사이트 음악 순위 읽기
import requests # HTTP 요청 처리를 위한 라이브러리

url = 'https://music.bugs.co.kr/chart'
response = requests.get(url) # 해당 URL의 HTML 소스 가져오기
# print(response.text)
bsoup = BeautifulSoup(response.text, 'html.parser')
musics = bsoup.find_all('td', class_='check') # 곡 정보가 포함된 td 태그들 추출

for idx, music in enumerate(musics):
    # music.input["title"]: td 태그 하위의 input 태그에서 title 속성값(곡명) 추출
    print(f'{idx + 1}위 : {music.input["title"]}')