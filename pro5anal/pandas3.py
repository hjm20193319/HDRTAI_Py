# Pandas 객체의 산술 연산 및 결측치(NaN) 처리 연습

from pandas import DataFrame, Series
import numpy as np

# Series 간의 연산
s1 = Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = Series([4, 5, 6, 7], index=['a', 'b', 'd', 'c'])
print(s1)
print(s2)

# 인덱스가 일치하는 요소끼리 연산됨. 한쪽이라도 인덱스가 없으면 NaN(Not a Number) 반환
print(s1 + s2)      
print(s1.add(s2))      # 더하기 메소드 (s1 + s2와 동일)
print(s1.mul(s2))      # 곱하기 메소드 (sub: 빼기, div: 나누기 등 지원)

print('------------------')
# DataFrame 간의 연산
df1 = DataFrame(np.arange(9).reshape(3, 3), columns = list('kbs'), index=['서울', '대전', '부산'])
df2 = DataFrame(np.arange(12).reshape(4, 3), columns = list('kbs'), 
                index=['서울', '대전', '제주', '광주']
                )
print(df1)
print(df2)

print(df1 + df2)        
# 행/열 인덱스가 모두 일치해야 연산됨. 불일치 시 NaN
# fill_value 옵션: 한쪽에만 데이터가 존재할 경우, NaN 대신 특정 값(0)으로 간주하여 연산 수행
print(df1.add(df2, fill_value=0))       
print(df1.sub(df2))     # 뺄셈
print(df1.mul(df2))     # 곱셈
print(df1.div(df2))     # 나눗셈

print('------------------')
print('NaN(결측값) 처리\n')

# 결측치가 포함된 데이터프레임 생성
df = DataFrame([[1.4, np.nan], [7,-4.5], [np.nan, np.nan], [0.5, -1]],
            columns=['one', 'two']
            )
print(df)
print()

print(df.isnull())      # 각 요소가 NaN인지 확인 (NaN이면 True)
print(df.notnull())     # 각 요소가 유효한 값인지 확인 (NaN이 아니면 True)

print(df.dropna())      # NaN이 하나라도 포함된 행은 모두 제거 (기본값 how='any')
print(df.dropna(how = 'any')) # 위와 동일
print(df.dropna(how = 'all')) # 행의 모든 값이 NaN인 경우에만 해당 행 삭제
print(df.dropna(subset=['one'])) # 'one' 열에 NaN이 있는 행만 골라서 삭제
print(df.dropna(subset=['two'])) # 'two' 열에 NaN이 있는 행만 골라서 삭제
print(df.dropna(axis='rows'))    # 행 방향으로 삭제 (기본값)
print(df.dropna(axis='columns')) # NaN이 포함된 열(Column) 자체를 삭제

print('------------------')
print(df)               # 현재 데이터프레임 상태 출력
imsi = df.drop(1)       # 인덱스 1번 행 삭제 (원본은 유지되고 삭제된 복사본 반환)
print(imsi)             # 삭제된 결과 출력
print(df)               # 원본 데이터프레임은 그대로임

# df.drop(1, inplace=True)        # 원본 삭제 됨
# print(df)

print('------------------')
# 계산 관련 메소드
print(df.sum())             # 각 열의 합계 계산 (기본값 axis=0)
print(df.sum(axis=0))       # 열 단위 합계 - NaN은 무시하고 계산
print(df.sum(axis=1))       # 행 단위 합계 - NaN은 무시하고 계산

print(df.mean())            # 각 열의 평균 계산
print(df.mean(axis=0))      # 열 단위 평균

print(df.describe())        # 주요 기술 통계량(개수, 평균, 표준편차 등) 요약 출력
print(df.info())            # 데이터프레임의 구조, 인덱스, 컬럼 타입, 메모리 등 정보 출력

words = Series(['봄', '여름', '가을', '겨울'])      # 문자열 데이터를 가진 Series 생성
print(words.describe())     # 문자열 데이터의 경우 빈도수, 고유값 수 등의 요약 정보 출력