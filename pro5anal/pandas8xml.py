# XML(Extensible Markup Language) 데이터 파싱 연습
# 계층적 구조를 가진 텍스트 형식의 데이터를 처리하기 위해 내장 라이브러리 사용
import xml.etree.ElementTree as etree

# 1. 로컬 XML 파일 읽기 및 파싱
# parse(): 파일 경로를 인자로 받아 ElementTree 객체를 생성
xmlfile = etree.parse('my.xml')
print(xmlfile)          # <xml.etree.ElementTree.ElementTree object ...>
print(type(xmlfile))    # ElementTree 타입 확인

root = xmlfile.getroot() # XML 문서의 최상위 요소(Root Node)를 가져옴
print(root.tag)         # 루트 태그의 이름 출력

# 인덱싱을 통한 접근 (구조를 정확히 알 때 사용 가능하나, 유연성이 떨어짐)
print(root[0].tag)      # 루트의 첫 번째 자식 요소 태그명
print(root[0][0].tag)   # 첫 번째 자식의 첫 번째 손자 요소 태그명
print()

# find(): 특정 태그를 검색하여 첫 번째 매칭되는 요소를 반환
# .text: 해당 요소 내의 문자열 데이터를 추출
myname = root.find('item').find('name').text  # <item><name>데이터</name></item> 구조 탐색
mytel = root.find('item').find('tel').text    # <item><tel>데이터</tel></item> 구조 탐색
print(f"이름: {myname}")
print(f"전화: {mytel}")
print()

print('------------------')
# 2. 웹상의 실시간 XML 데이터 처리 (기상청 날씨 정보)
import requests

# 기상청 육상 날씨 예보 XML URL
url = 'https://www.kma.go.kr/XML/weather/sfc_web_map.xml'
# 웹 서버에 브라우저인 것처럼 요청하기 위한 헤더 설정
headers = {'User-Agent':'Mozilla/5.0'}

# HTTP GET 요청을 통해 데이터 수신
res = requests.get(url, headers=headers)
res.raise_for_status()              # 응답 코드가 200이 아니면 예외 발생
print(res.text[:200], type(res.text)) # 수신된 데이터는 문자열(str) 타입

# fromstring(): 문자열 형태의 XML 데이터를 파싱하여 Element 객체로 변환
root = etree.fromstring(res.text)
print(root)     # 출력 시 {current}와 같은 네임스페이스가 포함되어 보임

# [네임스페이스 제거 처리]
# XML 태그에 붙은 '{uri}tag' 형태의 네임스페이스 접두사를 제거하여 접근을 용이하게 함
for elem in root.iter():
    if elem.tag.startswith('{'):
        # '}' 문자를 기준으로 분할하여 실제 태그명 부분만 다시 할당
        elem.tag = elem.tag.split('}', 1)[1]

# weather 태그 찾기 및 속성(Attribute) 추출
weather = root.find('weather') 
year = weather.get('year')      # get('속성명'): 태그 내의 속성값을 가져옴
month = weather.get('month')
day = weather.get('day')
hour = weather.get('hour')
print(f'발표 시각: {year}년 {month}월 {day}일 {hour}시 현재 예보')
print()

# findall(): 매칭되는 모든 요소를 리스트 형태로 반환 (반복문 사용)
for local in weather.findall('local'):
    name = local.text.strip()       # 태그 사이의 지역명 텍스트 (공백 제거)
    ta = local.get('ta')            # 해당 지역의 기온(ta) 속성값
    print(f'{name} 지역의 온도는 {ta}도 입니다')
print('------------------')