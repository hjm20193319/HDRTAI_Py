# Pandas DataFrame의 다양한 파일 형식 저장(Export) 및 엑셀 파일 입출력 연습

import pandas as pd
import numpy as np

# 1. 딕셔너리를 이용한 데이터프레임 생성
# 중첩 딕셔너리 사용 시 바깥쪽 키('apple', 'orange')는 컬럼명이 되고, 
# 안쪽 키('count', 'price')는 행 인덱스가 됨
items = {
        'apple':{'count':10, 'price':1500},
        'orange':{'count':5, 'price':800},
        }
df = pd.DataFrame(items)
print("--- 원본 데이터프레임 ---")
print(df) 

# 2. DataFrame 저장 (다양한 포맷)

# to_clipboard(): 데이터를 클립보드에 복사. 엑셀이나 메모장에 바로 붙여넣기(Ctrl+V) 가능
df.to_clipboard()       

# to_html(): 데이터를 HTML <table> 태그 형태의 문자열로 변환 (웹 페이지 삽입용)
print("\n--- HTML 변환 결과 ---")
print(df.to_html())     

# to_json(): 데이터를 JSON 형식의 문자열로 변환 (REST API나 Ajax 통신 시 활용)
print("\n--- JSON 변환 결과 ---")
print(df.to_json())     

# to_csv(): CSV(Comma Separated Values) 파일로 저장
df.to_csv('result1.csv', sep=',') # 기본 저장 (인덱스, 헤더 포함)
df.to_csv('result2.csv', sep=',', index=False) # 인덱스(행 번호/라벨) 제외하고 저장
df.to_csv('result3.csv', sep=',', index=False, header=False) # 인덱스와 헤더(컬럼명) 모두 제외
print()

# T (Transpose): 행과 열을 바꿈 (전치)
df2 = df.T 
print(df2)

# encoding='utf-8-sig': 엑셀에서 CSV를 열 때 한글 깨짐 방지를 위해 BOM(Byte Order Mark) 추가
df2.to_csv('result4.csv', sep=',', index=False, header=False, encoding='utf-8-sig')     

redata = pd.read_csv('result4.csv')
print(redata)

print('------------------')

# 3. 엑셀(Excel) 파일 처리
df3 = pd.DataFrame({
    'name':['Alice', 'Bob', 'Oscar'],
    'age':[24, 22, 29],
    'city':['seoul', 'suwon', 'incheon']
})
print(df3)

# to_excel(): DataFrame을 엑셀 파일(.xlsx)로 저장. sheet_name으로 시트 이름 지정 가능
df3.to_excel('result5.xlsx', index=False, sheet_name='work1')

# pd.ExcelFile(): 엑셀 파일을 로드하여 시트 정보 등을 확인하거나 특정 시트를 읽을 때 사용
exdf = pd.ExcelFile('result5.xlsx')
print(f"엑셀 시트 목록: {exdf.sheet_names}")
print()

# parse(): ExcelFile 객체에서 특정 시트의 데이터를 DataFrame으로 파싱(추출)
df4 = exdf.parse('work1') 
print(df4)

print('------------------')