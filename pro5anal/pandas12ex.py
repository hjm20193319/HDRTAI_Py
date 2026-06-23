# [웹 크롤링 및 데이터 분석 실습]
# 목적: 네이버 금융의 시가총액 페이지를 크롤링하여 CSV 파일로 저장하고 Pandas로 분석함
# 주요 라이브러리: 
# - requests: HTTP 요청을 통해 웹 페이지의 HTML 소스를 가져옴
# - BeautifulSoup: HTML 문서 내의 특정 태그나 CSS 선택자를 이용해 데이터를 추출(파싱)함
# - pandas: 추출된 데이터를 표(DataFrame) 형태로 구조화하고 파일 입출력을 관리함

# https://finance.naver.com/sise/sise_market_sum.naver
# with open(파일 명, mode='w'...)
# csv 파일로 출력
# csv 파일 읽기 후 DataFrame에 저장
# top3 종목명, 시가총액 출력

import requests
from bs4 import BeautifulSoup
import pandas as pd

# 크롤링 대상 URL 설정 (시가총액 1페이지와 2페이지)
url1 = 'https://finance.naver.com/sise/sise_market_sum.naver?&page=1'
url2 = 'https://finance.naver.com/sise/sise_market_sum.naver?&page=2'

# User-Agent 설정: 파이썬 스크립트가 아닌 일반 브라우저를 통한 접속임을 서버에 알려 차단을 방지함
headers = {'User-Agent':'Mozilla/5.0'}

# requests.get(): 해당 URL에 GET 방식의 HTTP 요청을 보내 응답 객체를 받음
sise1 = requests.get(url1, headers=headers)
sise2 = requests.get(url2, headers=headers)

# BeautifulSoup(마크업, 파서): HTML 문자열을 파싱 가능한 객체 구조로 변환함
soup1 = BeautifulSoup(sise1.text, 'html.parser')
soup2 = BeautifulSoup(sise2.text, 'html.parser')

# head1: 테이블의 헤더(컬럼명) 정보 추출 (thead 내의 th 태그들)
head1 = soup1.select('thead th')

head1list = []
for h in head1: 
    for th in h.find_all('th'):
        # .decompose(): 불필요한 태그와 그 내용을 완전히 제거하여 메모리에서 삭제함
        th.decompose()
    # .get_text(strip=True): 태그 내부의 텍스트만 추출하며 앞뒤 공백을 제거함
    head1list = head1list + [h.get_text(strip=True)]
print(head1list)

# n1, n2: 순위(No) 데이터 추출 (class가 no인 td 태그)
n1 = soup1.select('tbody tr>td.no')
# 리스트 컴프리헨션: 반복문을 한 줄로 작성하여 리스트를 생성하는 파이썬 특유의 문법
n1list = [tag.text.strip() for tag in n1]
print(n1list)

n2 = soup2.select('tbody tr>td.no')
n2list = [tag.text.strip() for tag in n2]
print(n2list)

# name1, name2: 종목명 추출 (class가 tltle인 a 태그)
name1 = soup1.select('tbody td>a.tltle')
name1list = [tag.text.strip() for tag in name1]
print(name1list)

name2 = soup2.select('tbody td>a.tltle')
name2list = [tag.text.strip() for tag in name2]
print(name2list)

# price1, price2: 수치 데이터(현재가, 시가총액 등) 추출 (class가 number인 td 태그)
price1 = soup1.select('tbody td.number')
# .replace(',', ''): 천단위 구분 기호를 제거하여 수치 연산이 가능하도록 전처리함
# "".join(...split()): 공백이나 줄바꿈 문자를 모두 제거하여 순수 문자열만 결합함
price1list = ["".join(tag.text.replace(',', '').split()) for tag in price1]
print(price1list)

price2 = soup2.select('tbody td.number')
price2list = ["".join(tag.text.replace(',', '').split()) for tag in price2]
print(price2list)

# 2. 10개씩 쪼개기 (이제 row는 ['하락', '11200', ...] 형태의 리스트가 됩니다)
# 슬라이싱([start:end]): 리스트의 특정 범위를 잘라냄. 여기서는 한 종목당 10개의 지표가 있으므로 10개씩 묶음
price1_rows = [price1list[i:i+10] for i in range(0, len(price1list), 10)]
price2_rows = [price2list[i:i+10] for i in range(0, len(price2list), 10)]

# 3. CSV 저장
# with open(): 파일 입출력 시 사용 후 자동으로 파일을 닫아주는 컨텍스트 매니저
# encoding='utf-8-sig': 윈도우 엑셀에서 CSV를 열 때 한글 깨짐을 방지하기 위해 BOM을 추가함
with open('page1.csv', 'w', encoding='utf-8-sig') as f:
    # ','.join(): 리스트의 요소들을 쉼표로 연결하여 하나의 문자열로 만듦 (CSV 형식)
    f.write(','.join(head1list) + '\n')
    
    # Page 1 처리
    # zip(): 여러 개의 리스트를 병렬로 묶어 동시에 반복문을 돌릴 수 있게 함
    for no, name, row in zip(n1list, name1list, price1_rows):
        # row 안의 요소들이 이미 문자열이므로 바로 join 가능합니다.
        # f-string: 문자열 내에 변수를 직접 삽입하는 포매팅 방식
        line = f"{no},{name}," + ",".join(row)
        f.write(line + '\n')

    # Page 2 처리
    for no, name, row in zip(n2list, name2list, price2_rows):
        line = f"{no},{name}," + ",".join(row)
        f.write(line + '\n')

# pd.read_csv(): 저장된 CSV 파일을 읽어 Pandas의 핵심 자료구조인 DataFrame 객체로 변환함
df = pd.read_csv('page1.csv', encoding='utf-8-sig')
print(df)

# top3 종목명, 시가총액 출력
# .head(3): 상위 3개의 행만 추출함
print("\n--- 시가총액 상위 3개 종목 ---")
print(df[['종목명', '시가총액']].head(3))