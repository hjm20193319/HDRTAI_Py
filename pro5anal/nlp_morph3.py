# 웹(동아 일보)에서 특정 단어 관련 문서들 검색 후 명사만 추출
# 워드 클라우드그리기
# [필수 라이브러리 설치]
# pip install pygame : pytagcloud의 의존성 라이브러리 (그래픽 처리)
# pip install simplejson : JSON 데이터 처리를 위한 라이브러리
# pip install pytagcloud : 텍스트 데이터를 시각적인 워드클라우드로 변환하는 라이브러리

from bs4 import BeautifulSoup # HTML/XML 파싱 라이브러리
from urllib.parse import quote # 한글 키워드를 URL 인코딩(UTF-8)하기 위한 함수
# urllib.request: URL을 통해 네트워크 데이터를 읽어오기 위한 모듈
import urllib.request
from konlpy.tag import Okt # 한국어 형태소 분석기 (Open Korean Text)
import pytagcloud # 워드클라우드 생성 라이브러리
from collections import Counter # 요소의 개수를 세어 딕셔너리 형태로 반환하는 클래스
import webbrowser # 생성된 이미지를 브라우저로 자동 실행하기 위한 모듈
import matplotlib.pyplot as plt # 데이터 시각화 라이브러리
import koreanize_matplotlib # matplotlib 한글 폰트 깨짐 방지 자동 설정
import matplotlib.image as mpimg # 이미지를 읽어서 배열로 변환하는 모듈

# keyword = input('검색어 : ')
# print(quote(keyword)) # URL에 포함될 수 없는 한글을 %ED%98%84... 형태의 16진수로 변환

keyword = '현대자동차'

# 동아일보 검색 결과 페이지 URL 생성
target_url = 'https://www.donga.com/news/search?query=' + quote(keyword)
# urlopen().read(): 해당 URL의 전체 HTML 소스를 바이트(bytes) 형태로 가져옴
source_code = urllib.request.urlopen(target_url).read()
# print(source_code)
# BeautifulSoup(마크업, 파서): HTML 소스를 파싱 가능한 트리 구조 객체로 변환
soup = BeautifulSoup(source_code, 'lxml', from_encoding='utf-8')
# print(soup)

msg = '' # 기사 본문 텍스트를 누적할 변수
# find_all(): 검색 결과 리스트에서 기사 제목에 해당하는 h4 태그(class='tit')를 모두 추출
for title in soup.find_all('h4', class_='tit'):
    title_link = title.find('a') # h4 태그 내의 하이퍼링크(a) 태그 찾기
    # print(title_link)
    article_url = title_link['href'] # a 태그의 href 속성값(기사 상세 주소) 추출
    # print(article_url)    # 각 기사의 url을 모두 긁어옴

    try:
        # 각 기사 상세 페이지 접속
        source_article = urllib.request.urlopen(article_url)
        soup2 = BeautifulSoup(source_article, 'lxml', from_encoding='utf-8')
        # print(soup2)
        # select(): CSS 선택자를 사용하여 본문 영역(section.news_view) 추출
        contents = soup2.select('section.news_view')
        # print(contents)
        for imsi in contents:
            # find_all(string=True): 태그를 제외한 순수 텍스트 노드만 추출
            item = str(imsi.find_all(string=True))
            msg += item # 추출된 텍스트를 전체 메시지에 추가
    except Exception as err:
        # 접속 오류나 파싱 에러 발생 시 해당 기사는 건너뜀
        pass

    # print(msg)

# 형태소 분석 후 명사 추출
okt = Okt() # Okt 객체 생성
nouns = okt.nouns(msg) # 수집된 전체 텍스트에서 명사만 추출하여 리스트로 반환

result = [] # 의미 있는 단어(2글자 이상)만 담을 리스트
for imsi in nouns:
    if len(imsi) > 1: # 한 글자 단어(은, 는, 이, 가 등)는 분석에서 제외
        result.append(imsi)
    
print(result)

# Counter(): 리스트 내 단어별 빈도수를 계산하여 딕셔너리 형태로 반환
count = Counter(result) 
print(count)

# most_common(n): 빈도수가 높은 상위 n개의 단어와 빈도수를 튜플 리스트로 반환
tag = count.most_common(50) 
print(tag)

# 워드 클라우드 작성
# make_tags(): 단어와 빈도수 데이터를 pytagcloud에서 사용하는 태그 객체 리스트로 변환
taglist = pytagcloud.make_tags(tag, maxsize=100)

# create_tag_image(): 워드클라우드 이미지 파일 생성
# fontname='korean': pytagcloud 설정 폴더 내에 'korean'으로 등록된 폰트 사용 (사전 설정 필요)
pytagcloud.create_tag_image(taglist, 'word.png', size=(1000, 600), background=(0,0,0), rectangular=False, fontname='korean')

# 생성된 이미지를 화면에 출력
img = mpimg.imread('word.png') # 이미지 파일을 수치 데이터(배열)로 읽기
plt.imshow(img) # 이미지 표시
plt.axis('off') # 그래프의 축(x, y축 눈금)을 숨김
plt.show() # 윈도우 창에 그래프 출력

# 시스템 기본 브라우저를 통해 이미지 파일 열기
webbrowser.open('word.png')