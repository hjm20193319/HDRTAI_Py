# 웹 문서를 읽어 형태소 분석 : 위키백과에서 단어 검색 결과
# 단어 출형 횟수 DataFrame으로 저장

import requests # HTTP 요청을 보내기 위한 라이브러리
from bs4 import BeautifulSoup # HTML/XML 파싱 라이브러리
import pandas as pd # 데이터 분석 및 조작을 위한 라이브러리
from konlpy.tag import Okt # Open Korean Text: 트위터에서 개발한 한국어 형태소 분석기
from urllib import parse    # 한글 인코딩 라이브러리 (URL에 한글 포함 시 필요)

okt = Okt() # Okt 형태소 분석기 객체 생성

# url = 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%88%9C%EC%8B%A0'     -> 이미 인코딩이 된 상태

para = '이순신' # 검색 키워드
url = 'https://ko.wikipedia.org/wiki/' + parse.quote(para)      # 인코딩이 되어서 표시된다 (URL Safe 문자열로 변환)
# 프로그램에서 검색해서 결과를 받을 수 있다
print(url)

# User-Agent: 봇(Bot) 차단을 방지하기 위해 브라우저 정보를 헤더에 포함
headers = {'User-Agent':'Mozilla/5.0'} 
wiki = requests.get(url, headers=headers) # 해당 URL의 HTML 소스 가져오기

if wiki.status_code == 200: # HTTP 응답 코드가 200(성공)인 경우 실행
    page = wiki.text # 응답받은 HTML 소스 문자열
    print(page, type(page))     # <class 'str'>  : 객체로 만들어서 원하는 값을 뽑아야 함
    
    # BeautifulSoup(마크업, 파서): lxml 파서는 속도가 빠르고 유연함
    soup = BeautifulSoup(page, 'lxml') 

    wordlist = []   # 형태소 분석으로 명사를 추출해 기억

    # select(): CSS 선택자를 사용하여 id가 mw-content-text인 요소 하위의 모든 p 태그 선택
    for item in soup.select('#mw-content-text p'):
        if item.string != None: # 태그 내에 텍스트가 존재하는 경우만 처리
            # okt.nouns(): 텍스트에서 명사만 추출하여 리스트로 반환
            # extend(): 리스트 끝에 다른 리스트의 모든 요소를 추가 (리스트 병합)
            wordlist.extend(okt.nouns(item.string))

    print('wordlist : ', wordlist)
    print('단어 수 : ', len(wordlist))
    print('중복 제거 후 단어 수 : ', len(set(wordlist))) # set 자료형은 중복을 허용하지 않음
    print('\n')

    word_dict = {}      # 단어의 발생 횟수를 dict로 저장
    for i in wordlist:
        if i in word_dict: # 이미 딕셔너리에 키가 있다면 카운트 증가
            word_dict[i] += 1
        else: # 처음 발견된 단어라면 1로 초기화
            word_dict[i] = 1    # 처음 나온 것
    print('word_dict : ', word_dict)
    print('\n')

    # Series로 출력
    # Series: Pandas의 1차원 배열 자료구조 (인덱스와 값으로 구성)
    seri_list = pd.Series(wordlist) 
    print(seri_list[:3])
    # value_counts(): 각 값의 출현 빈도를 계산하여 내림차순으로 정렬된 Series 반환
    print(seri_list.value_counts()[:5])
    print('\n')

    seri_dict = pd.Series(word_dict)
    print(seri_dict[:3])
    # 딕셔너리로 만든 Series의 경우 value_counts()는 '빈도수 값' 자체의 빈도를 세므로 주의
    print(seri_dict.value_counts()[:5])
    print('\n')

    # DataFrame으로 출력
    df1 = pd.DataFrame(wordlist, columns=['단어'])
    print(df1.head(3))
    print(df1['단어'].value_counts()[:5]) # 특정 열의 빈도수 확인
    
    # .T (Transpose): 행과 열을 바꿈. keys()와 values() 리스트를 행으로 쌓은 후 전치하여 열로 만듦
    df2 = pd.DataFrame([word_dict.keys(), word_dict.values()]).T
    df2.columns = ['단어', '출현 횟수']
    print(df2.head())

    # to_csv(): DataFrame을 CSV 파일로 저장. index=False는 행 번호 저장을 생략함
    df2.to_csv('nlp_morph2.csv', index=False)

    # read_csv(): 저장된 CSV 파일을 다시 읽어와서 확인
    df3 = pd.read_csv('nlp_morph2.csv')
    print(df3.head())