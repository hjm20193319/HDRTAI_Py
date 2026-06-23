# Pandas의 재색인(Reindexing) 및 데이터 필터링 연습
from pandas import DataFrame, Series
import numpy as np


# Series의 재색인: 기존 객체의 데이터를 새로운 색인에 맞게 재배열함
data = Series([1, 3, 2], index = (1, 4, 2))
print(data) # 인덱스 순서가 1, 4, 2인 상태
data2 = data.reindex((1, 2, 4)) # 인덱스 순서를 1, 2, 4로 재배치
print(data2) # 데이터 값이 인덱스에 맞춰 정렬됨

print('------------------')
print('재색인할 때 값 채워넣기\n')

# 존재하지 않는 인덱스로 재색인하면 기본적으로 NaN(결측치)이 채워짐
data3 = data2.reindex([0, 1, 2, 3, 4, 5]) 
print(data3)        # 0, 3, 5번 인덱스는 원래 없었으므로 NaN 발생

# fill_value 옵션: 대응값이 없는 인덱스에 NaN 대신 특정 값을 채움
data3 = data2.reindex([0, 1, 2, 3, 4, 5], fill_value=777)
print(data3)

print('------------------')
# method='ffill' 또는 'pad': NaN을 앞(이전)에 있는 유효한 값으로 채움 (Forward Fill)
data3 = data2.reindex([0, 1, 2, 3, 4, 5], method='ffill')
print(data3)
data3 = data2.reindex([0, 1, 2, 3, 4, 5], method='pad')
print(data3)

print('------------------')
# method='bfill' 또는 'backfill': NaN을 뒤(다음)에 있는 유효한 값으로 채움 (Backward Fill)
data3 = data2.reindex([0, 1, 2, 3, 4, 5], method='bfill')
print(data3)
data3 = data2.reindex([0, 1, 2, 3, 4, 5], method='backfill')
print(data3)

print('------------------')
print('DataFrame : Boolean indexing 및 값 변경\n')

# 4행 3열의 DataFrame 생성
df = DataFrame(np.arange(12).reshape(4, 3),
            index = ['1월', '2월', '3월', '4월'],
            columns=['강남', '강북', '서초']
            )
print(df)
print(df['강남'])           # '강남' 열만 추출 (Series)
print(df['강남'] > 3)       # '강남' 열의 값이 3보다 큰지 비교 (Boolean Series)
print(df[df['강남'] > 3])   # '강남' 열의 값이 3보다 큰 행들만 필터링하여 출력

print(df < 3)               # 전체 요소에 대해 3보다 작은지 여부를 True/False로 반환
df[df < 3] = 0              # 3보다 작은 모든 요소를 0으로 일괄 변경
print(df)                   # 원본 데이터프레임의 값이 수정됨

print('------------------')
print('슬라이싱 관련 메소드 : loc() : label-based, iloc() : position-based, 숫자 지원\n')
print(df.loc['3월', :])      # '3월' 행의 모든 열 출력 (라벨 기준)
print(df.loc[:'2월',['서초']]) # 처음부터 '2월' 행까지, '서초' 열만 출력 (라벨 슬라이싱은 끝점 포함)
print()
print(df.iloc[2, :])        # 2번 인덱스(3번째) 행의 모든 열 출력 (위치 기준)
print(df.iloc[:2])          # 0번부터 1번 인덱스까지의 행 출력
print(df.iloc[:2, 2])       # 0~1번 행의 2번 열 데이터 출력
print(df.iloc[:3, 1:3])     # 0~2번 행의 1~2번 열 데이터 출력 (위치 슬라이싱은 끝점 제외)