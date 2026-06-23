# BeautifulSoup 모듈로 XML 문서 처리
# BeautifulSoup은 HTML뿐만 아니라 XML 파싱도 지원하며, lxml-xml(또는 xml) 파서를 통해 구조화된 데이터 추출이 가능함
from bs4 import BeautifulSoup

# open() 함수를 이용해 로컬 XML 파일을 읽기 모드('r')로 열기
with open('my.xml', 'r', encoding='utf-8') as f:
    xmlfile = f.read() # 파일의 전체 내용을 문자열로 읽어옴
    print(xmlfile, type(xmlfile))

# BeautifulSoup(마크업, 파서): 문자열을 파싱하여 BeautifulSoup 객체 생성
# 'lxml' 파서는 속도가 빠르며 XML 처리에 적합함
soup = BeautifulSoup(xmlfile, 'lxml') 
print(soup, type(soup))

# find_all(): 해당 태그명을 가진 모든 요소를 찾아 리스트(ResultSet) 형태로 반환
itemTag = soup.find_all('item')
print(itemTag, type(itemTag))
print()

# 특정 태그의 속성값 접근: 태그객체['속성명'] 또는 태그객체.get('속성명')
nameTag = soup.find_all('name')
print(nameTag[0]['id'], type(nameTag[0]['id'])) # 첫 번째 name 태그의 id 속성값 출력

print('------------------')
# 계층 구조 순회: 각 item 태그 내부를 탐색
for i in itemTag:
    nameTag = i.find_all('name') # 현재 item 내부의 모든 name 태그 찾기
    for j in nameTag:
        # .string: 태그 내부에 자식 태그 없이 문자열만 있을 때 해당 텍스트를 추출
        print('id : ' + j['id'] + 'name : ' + j.string)
        tel = i.find('tel') # find(): 조건에 맞는 첫 번째 요소만 반환
        print('tel : ' + tel.string)

    # 속성 기반 데이터 추출: 태그 내의 속성(Attribute) 값을 가져옴
    for j in i.find_all('exam'):
        print('kor : ' + j['kor'] + ' eng : ' + j['eng'])
    print()

print('------------------')

# [공공데이터 활용]
# urllib.request: URL을 통해 네트워크 데이터를 가져오기 위한 모듈
# pandas: 추출한 데이터를 표 형태(DataFrame)로 관리하기 위한 라이브러리

# 서울시 제공 도서관 정보 xml 샘플 자료 5개 읽기
import urllib.request as req
import pandas as pd

url = 'http://openapi.seoul.go.kr:8088/sample/xml/SeoulLibraryTimeInfo/1/5/'
plainText = req.urlopen(url).read().decode('utf-8')
print(plainText)
print('---')

# 'xml' 파서 명시: XML 전용 파싱 모드로 동작하여 대소문자 구분 및 구조를 정확히 파악
xmlObj = BeautifulSoup(plainText, 'xml') 
# select(): CSS 선택자 문법을 사용하여 요소 선택 (row 태그들 선택)
libData = xmlObj.select('row') 
print(libData)
print('---')

rows = []
for data in libData:
    name = data.find('LBRRY_NAME').string # 하위 태그의 텍스트 노드 추출
    addr = data.find('ADRES').string
    print('도서관명 : ' + name + ', 주소 : ' + addr)
    print()
    rows.append({'도서관명':name, '주소':addr}) # 딕셔너리 형태로 리스트에 저장

df = pd.DataFrame(rows)
print(df)
print('건수 : ', len(df))