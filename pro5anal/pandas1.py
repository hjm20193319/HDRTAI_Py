# Pandas : 
# 고수준의 자료 구조 ( Series, DataFrame )와 빠르고 쉬운 데이터 분석용 함수 제공
# 통합된 시계열 연산, 축약연산, 누락 데이터 처리, SQL, 시각화 .... 등을 제공
# Data Wrangling, Data Munging 을 효율적으로 처리 가능

import pandas as pd
from pandas import Series, DataFrame
import numpy as np

# Series : 일련의 객체를 담을 수 있는 1차원 배열과 같은 자료구조 / 색인(index)을 갖는다
obj = pd.Series([3, 7, -5, 4])      # Series 객체 생성 - list를 가지고
print(obj)          # index가 자동으로 붙는다
obj = pd.Series((3, 7, -5, 4))
print(obj)          # tuple
# obj = pd.Series({3, 7, -5, 4})      # Error
# print(obj)          # set - 순서가 없기 때문에
obj = pd.Series([3, 7, -5, '사'])       # 요소 값은 object type -> 모든 값이 들어갈 수 있음
print(obj)          # 다양한 타입 가능
print(obj, type(obj))   # Series type

print('-----------------')
obj2 = pd.Series([3, 7, -5, 4], index=['a', 'b', 'c', 'd'])     # 인덱스 직접 지정 가능
print(obj2)
print(obj2.sum(), ' ', np.sum(obj2), ' ', sum(obj2))    # 판다스(넘파이), 넘파이, 파이썬
print(obj2.std())   # 표준편차

print('-----------------')
print(obj2.values)      # 순수한 값을 리스트 형태로 얻을 수 있다
# 인덱싱
print(obj2.index)
print(obj2['a'])        # 3
print(obj2[['a']])      # a  3
# 슬라이싱
print(obj2[['a', 'b']])
print(obj2['a':'c'])

print(obj2[2])          # 인덱스 사용
print(obj2.iloc[2])
print(obj2[1:4])

print(obj2[[2, 1]])
print(obj2.iloc[[2, 1]])

print('a' in obj2)
print('k' in obj2)

print('------------------')
print('파이썬 dict 자료를 Series 객체로 생성\n')
names = {'mouse':5000, 'keyboard':25000, 'monitor':450000}
print(names)            # dict 타입
obj3 = Series(names)
print(obj3, ' ', type(obj3))        # Series 타입
obj3.index = ['마우스', '키보드', '모니터']     # 인덱스 값 수정 가능
print(obj3)

obj3.name = '상품가격'      # Series 객체 자체에 이름을 부여 (데이터 열의 제목 역할)
obj3.index.name = '상품명'  # Series의 인덱스(색인) 영역에 이름을 부여 (행 라벨의 제목 역할)
print(obj3)

print('------------------')
print('<DataFrame 객체>\n')
df = pd.DataFrame(obj3)     # Series로 데이터프레임을 만듦
print(df, ' ', type(df))

data = {
    'irum':['홍길동', '한국인', '신기해', '공기밥', '한가해'],
    'juso':('역삼동', '신사동', '역삼동', '신사동', '역삼동'),
    'nai':[23, 25, 33, 32, 18]
}
frame = pd.DataFrame(data)      # dict로 데이터프레임을 만듦, 프레임 내부의 데이터는 벡터 취급
print(frame)

print('------------------')
print(frame['irum'])        # 결과는 똑같지만, 개발자들이 더 많이 쓰는 방식
print(frame.irum)
print(type(frame.irum))     # Series 타입

print(DataFrame(data=data, columns=['juso', 'irum', 'nai']))    # 칼럼의 순서를 변경할 수 있다(Table 이랑 비슷)

print('------------------\n')
# NaN (결측치)
frame2 = pd.DataFrame(data, columns=['irum', 'nai', 'juso', 'tel'])
print(frame2)       # 여기까지 하면 NaN 하고 나옴

frame2 = pd.DataFrame(data, columns=['irum', 'nai', 'juso', 'tel'], index=['a', 'b', 'c', 'd', 'e'])
print(frame2)       # index 변경

# 칼럼 tel에 값 대입 ( 수정 가능 )
frame2['tel'] = '1111-1111'     # 모든 행에 적용 됨
print(frame2)

val = pd.Series(['2222-2222', '3333-3333', '4444-4444'], index=['b', 'c', 'e'])     # 특정 인덱스만 지정
print(val)      # val 은 Series 임
frame2['tel'] = val         # Series로 덮어쓰기(일부만 수정이 아니라, val로 덮어쓴 것)
print(frame2)       # 'a' 와 'd' 에는 NaN 표시(111-1111이 아니다)

print('------------------\n')
# 전치
print(frame2.T)     # 행과 열 바꿈

print('------------------\n')
print(frame2.values)        # 결과는 list 타입, 값만 꺼내는 것
print(frame2.values[0, 1])      # 인덱싱
print(frame2.values[0:2])       # 슬라이싱

print('------------------')
# 행, 열 삭제
frame3 = frame2.drop('d')       # 행 삭제
# frame3 = frame2.drop('d', axis = 0)      axis 생략된 것
print(frame3)

frame4 = frame2.drop('tel', axis=1)     # 열 삭제
print(frame4)

print('------------------')
# 정렬
print(frame2)   # 원본 데이터는 유지됨 (drop 등은 복사본을 반환)
print(frame2.sort_index(axis=0, ascending=False))   # 행 인덱스를 기준으로 내림차순 정렬
print(frame2.sort_index(axis=1, ascending=True))    # 열 이름을 기준으로 오름차순 정렬

print(frame2.rank(axis=0))      # 각 열 내에서 값의 순위(Rank)를 매김 (기본값: 오름차순 순위)

# 'juso' 열의 데이터별 빈도수(출현 횟수)를 계산하여 Series 객체로 반환
counts = frame2['juso'].value_counts()
print(counts)

print('------------------')
# 문자열 자르기 (데이터 가공)
data = {
    'juso':['강남구 역삼동', '중구 신당동', '강남구 대치동'],
    'inwon':[23, 25, 33]
}
fr = pd.DataFrame(data)
print(fr)

# '강남구'는 몇명인지?
# 리스트 컴프리헨션을 사용하여 'juso' 열의 각 문자열을 공백으로 분리한 후, 첫 번째 요소(구)만 추출하여 Series 생성
result1 = Series([x.split()[0] for x in fr['juso']])
# 두 번째 요소(동)만 추출하여 Series 생성
result2 = Series([x.split()[1] for x in fr['juso']])

print(result1) # 추출된 구 단위 출력
print(result2) # 추출된 동 단위 출력
print(result1.value_counts()) # 각 구별 데이터 빈도수(인원수) 출력