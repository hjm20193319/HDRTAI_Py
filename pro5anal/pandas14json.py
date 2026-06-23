# JSON(JavaScript Object Notation) 자료 : xml에 비해 경량이며 텍스트 기반의 데이터 교환 표준임
# 배열(Array)과 객체(Object) 구조만 있으면 처리가 가능하여 대부분의 프로그래밍 언어에서 지원함

import json # JSON 데이터를 처리하기 위한 파이썬 내장 모듈

# 파이썬의 Dictionary 객체 생성
dict = {
    'name':'tom',
    'age':25,
    'score':['90','80','88']
}       # dict type (Key-Value 쌍으로 구성)
print(dict)
print(type(dict))

# json.dumps(): 파이썬 객체(dict, list 등)를 JSON 형식의 문자열(str)로 변환 (Serialization/직렬화)
print('json 인코딩 : dict -> str (직렬화)')
# indent=4: 출력되는 문자열에 들여쓰기를 적용하여 가독성을 높임
str_val = json.dumps(dict, indent=4)
print(str_val)
print(type(str_val))        # str
print(str_val[0:20])        # 문자열이므로 슬라이싱 가능

# json.loads(): JSON 형식의 문자열을 파이썬 객체(주로 dict)로 변환 (Deserialization/역직렬화)
print('json 디코딩 : str -> dict (역직렬화)')
json_val = json.loads(str_val)
print(json_val)
print(type(json_val))
print(json_val['name'])     # 딕셔너리 키를 이용한 데이터 접근

# 반복문을 이용한 데이터 탐색
for k in json_val.keys():
    print(k)                # 모든 키(Key) 출력
for v in json_val.values():
    print(v)                # 모든 값(Value) 출력

print('------------------')
# [공공데이터 활용] 서울시 제공 도서관 정보 JSON 샘플 자료 -> dict 로 가져오면 됨
# urllib.request: URL을 통해 네트워크 상의 데이터를 가져오기 위한 모듈
import urllib.request as req
import pandas as pd

url = 'http://openapi.seoul.go.kr:8088/sample/json/SeoulLibraryTimeInfo/1/5/'
plainText = req.urlopen(url).read().decode()
# print(plainText, type(plainText))  str
# print('---')

# 수신된 JSON 문자열을 파이썬 딕셔너리로 변환
jsonData = json.loads(plainText)
# print(jsonData, type(jsonData))  dict
# 계층 구조 접근: 딕셔너리 내의 리스트, 다시 그 안의 딕셔너리 순으로 접근
print(jsonData['SeoulLibraryTimeInfo']['row'][0]['LBRRY_NAME'])

# dict의 get() 메소드 사용: 해당 키가 없을 경우 에러 대신 None을 반환하여 안정적인 접근 가능
print()
libData = jsonData.get('SeoulLibraryTimeInfo').get('row')
# print(libData)
name = libData[0].get('LBRRY_NAME')
addr = libData[0].get('ADRES')
print('도서관명 : ' + name + ', 주소 : ' + addr) # 문자열 결합을 통한 출력

print()
# 데이터 프레임(DataFrame)에 넣기 위해 리스트에 딕셔너리 형태로 저장
datas = []
for ele in libData:
    name = ele.get('LBRRY_NAME')
    tel = ele.get('TEL_NO')
    addr = ele.get('ADRES')
    print('도서관명 : ' + name + ', 전화번호 : ' + tel + ', 주소 : ' + addr)
    print()
    datas.append({'도서관명':name, '전화번호':tel, '주소':addr})

print('------------------')
# pd.DataFrame(list_of_dicts): 딕셔너리 리스트를 기반으로 표 형태의 데이터프레임 생성
df = pd.DataFrame(datas)
print(df)
print('건수 : ', len(df)) # 데이터프레임의 행(Row) 개수 출력