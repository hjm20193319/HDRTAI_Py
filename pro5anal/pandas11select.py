# BeautifulSoup의 select() 및 select_one() 메소드를 이용한 데이터 추출
# CSS Selector: HTML 요소를 선택하기 위해 사용하는 스타일 시트 언어의 문법을 그대로 활용
# find/find_all 보다 복잡한 계층 구조를 직관적으로 표현 가능 (예: 자식, 후손, 아이디, 클래스 조합)
from bs4 import BeautifulSoup
import requests

html_page = """
<html>
<body>
<div id='hello'>
    <a href='https://www.naver.com'>네이버</a><br/>
    <span>
        <a href='https://www.google.com'>구글</a><br/>
    </span>
    <ul class='world'>
        <li>hello</li>
        <li>world</li>
    </ul>
</div>
<div id='hi' class='good'>
    두번째 div
</div>
</body>
</html>
"""
# 'lxml' 파서는 C언어로 작성되어 'html.parser'보다 속도가 빠르고 유연한 처리가 가능함
soup = BeautifulSoup(html_page, 'lxml')

# select_one(): CSS 셀렉터 조건에 맞는 첫 번째 요소 하나만 반환 (find()와 유사)
aa = soup.select_one('div')
print('aa : ', aa, ' ', aa.string)      # 첫번째 div 출력. .string은 태그 내에 문자열만 있을 때 추출
print('--')

aa = soup.select_one('div#hello')       # '#' 기호는 id 속성을 의미 (div 태그 중 id가 hello인 것)
print('aa : ', aa, ' ', aa.string)     # id가 hello인 div 출력
print('--')

aa = soup.select_one('div.good')        # '.' 기호는 class 속성을 의미 (div 태그 중 class가 good인 것)
print('aa : ', aa, ' ', aa.string)     # class가 good인 div 출력
print('--')

aa = soup.select_one('div#hello > a')   # '>' 기호는 자식(Direct Child) 선택자. hello 바로 아래의 a 태그
print('aa : ', aa, ' ', aa.string)
print('--')

# select(): 조건에 맞는 모든 요소를 리스트(ResultSet) 형태로 반환 (find_all()과 유사)
bb = soup.select('div') 
# bb = soup.select('div#hello > ul.world')
# bb = soup.select('div#hello ul.world') # 공백은 후손(Descendant) 선택자. 하위 계층 어디든 있으면 선택
# bb = soup.select('div#hello > ul.world > li')

print('bb : ', bb)
for i in bb:
    # .text: 태그 내의 모든 텍스트(자식 태그 포함)를 하나의 문자열로 합쳐서 반환
    print(i, ' ', i.text) 

print('------------------')

# 위키 백과 사이트에서 이순신으로 검색된 자료 읽기
url = 'https://ko.wikipedia.org/wiki/이순신'
headers = {'User-Agent':'Mozilla/5.0'}
wiki = requests.get(url, headers=headers)
soup = BeautifulSoup(wiki.text, 'html.parser')

# select('p#mwHw'): p 태그 중 id가 mwHw인 요소를 선택
result = soup.select('p#mwHw')
# print(result)
for s in result: # 선택된 각 문단(p 태그)에 대해 반복
    for sup in s.find_all('sup'): # 문단 내에 포함된 모든 <sup> 태그(주석 번호 등)를 찾음
        sup.decompose()     # .decompose(): 추출 대상에서 제외하기 위해 해당 태그와 그 내용을 완전히 삭제
    
    print(s.get_text(strip=True)) # 불필요한 태그가 제거된 순수 텍스트만 추출 (앞뒤 공백 제거)

print('------------------')

# 여러 문단을 읽어오고 싶을 때: id가 mw-content-text인 요소 하위의 모든 p 태그 선택
result = soup.select('#mw-content-text p')
for s in result:
    for sup in s.find_all('sup'):
        sup.decompose()     # 태그 삭제
    
    print(s.get_text(strip=True))

print('------------------')

# 교촌치킨 사이트에서 메뉴, 가격 자료 읽기 및 데이터 분석(Pandas 활용)
import pandas as pd

url = 'https://www.kyochon.com/menu/chicken.asp'
headers = {'User-Agent':'Mozilla/5.0'}
kyochon = requests.get(url, headers=headers)
soup2 = BeautifulSoup(kyochon.text, 'html.parser')

# 메뉴명 얻기: dl 태그의 class가 txt인 것 내부의 dt 태그들
names = soup2.select('dl.txt > dt')
# 리스트 컴프리헨션을 사용하여 텍스트만 추출하고 공백 제거
names_text = [tag.text.strip() for tag in names]
# print(names_text)

# 가격 얻고 활용하기: p 태그의 class가 money인 것 내부의 strong 태그들
prices = soup2.select('p.money strong')
# replace(',', ''): 천단위 구분 쉼표 제거 후 int()로 형변환하여 수치 연산 가능하게 처리
prices_text = [int(tag.text.strip().replace(',', '')) for tag in prices]
# print(prices_text)      # 문자열 -> 정수화

# 추출한 리스트들을 딕셔너리 형태로 묶어 DataFrame 생성
df = pd.DataFrame({
    '메뉴명':names_text,
    '가격':prices_text
})

print(df.head(10))
print()
print(f'가격 평균 : {df["가격"].mean():.2f}')
print(f'가격 표준편차 : {df["가격"].std():.2f}')
print(f'제일 비싼 메뉴 가격 : {df["가격"].max()}')
print(f'제일 싼 메뉴 가격 : {df["가격"].min()}')

# 변동계수(Coefficient of Variation, CV) 구하기: 표준편차를 평균으로 나눈 값
# 데이터의 상대적인 흩어짐 정도를 파악할 때 사용 (단위가 다른 집단 간 비교 시 유용)
cv = df['가격'].std() / df['가격'].mean() * 100
print(f'가격 변동계수(CV) : {cv:.2f}%')