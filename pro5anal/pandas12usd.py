# 일정 간격으로 데이터를 읽어오기
# 네이버 - 증권 - 시장지표 : 환율 값 출력 (일정시간에 한번씩 주기적으로 읽기)
import requests # HTTP 요청을 보내기 위한 라이브러리 (GET, POST 등 지원)
from bs4 import BeautifulSoup # HTML/XML 파싱 및 데이터 추출을 위한 라이브러리
import time # 시간 지연(sleep) 기능을 사용하기 위한 모듈
import sys # 시스템 관련 파라미터와 함수를 제어하기 위한 모듈

# sys.stdout.reconfigure: 표준 출력의 인코딩을 설정. 
# 특히 윈도우 환경의 터미널에서 한글 깨짐 방지를 위해 utf-8로 재설정함
sys.stdout.reconfigure(encoding='utf-8')

# 크롤링 대상 URL (네이버 금융 시장지표 페이지)
url = 'https://finance.naver.com/marketindex/'
# User-Agent: 서버에 브라우저를 통한 접속임을 알려 차단을 방지하는 헤더 정보
headers = {'User-Agent':'Mozilla/5.0'}

# 무한 루프를 통해 주기적으로 데이터를 수집 (실시간 모니터링 흉내)
while True: 
    time.sleep(5) # 5초 동안 실행을 일시 중단 (서버 부하 방지 및 주기 설정)

    # requests.get(): 해당 URL의 HTML 소스 코드를 가져옴
    res = requests.get(url, headers=headers)
    # BeautifulSoup(마크업, 파서): HTML 객체 생성. 
    # res.content는 바이너리(bytes) 형태의 데이터를 반환하며, 인코딩 문제를 최소화하기 위해 사용함
    soup = BeautifulSoup(res.content, 'html.parser')       # binary로 읽음 

    # select_one(): CSS 선택자를 사용하여 조건에 맞는 첫 번째 요소만 반환
    # nation: 국가명 추출 (h3 태그의 class가 h_lst인 요소 하위의 span.blind)
    nation = soup.select_one('h3.h_lst > span.blind').get_text(strip=True)
    # price: 현재 환율 수치 추출 (class가 value인 요소)
    price = soup.select_one('.value').get_text(strip=True)
    # unit: 통화 단위 추출 (txt_krw 클래스 내부의 blind 클래스)
    unit = soup.select_one('.txt_krw .blind').get_text(strip=True)
    # change: 전일 대비 변동 금액 추출
    change = soup.select_one('.change').get_text(strip=True)
    # updown: 상승/하락 여부 추출. select()는 리스트를 반환하므로 [-1]로 마지막 요소 선택
    updown = soup.select('div.head_info.point_up span.blind')[-1].get_text(strip=True)

    print('환율 알아보기')
    # f-string: 문자열 포매팅 방식. 변수를 중괄호{} 안에 넣어 직관적으로 출력
    print(f'{nation.replace(' ','')} : {price}{unit} ({change} {updown})')

    print('------------------')