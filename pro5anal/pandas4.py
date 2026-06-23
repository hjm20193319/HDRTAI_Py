# DataFrame 재구조화 (Reshaping) 및 데이터 구간화(Binning) 연습

import pandas as pd
import numpy as np

# 2행 3열의 데이터프레임 생성 (1000~1005까지의 값)
df = pd.DataFrame(1000 + np.arange(6).reshape(2, 3),
            index=['대전', '서울'], 
            columns=['2020', '2021', '2022']
            )
print("--- 원본 데이터프레임 ---")
print(df) # 행: 지역(대전, 서울), 열: 연도(2020, 2021, 2022)

print('------------------')
# stack / unstack : 데이터의 형태를 재배치 (자료구조의 Stack/LIFO와는 다른 개념)

# stack(): 컬럼(열) 인덱스를 로우(행) 인덱스의 하위 레벨로 쌓아 올림 (Wide -> Long format)
df_row = df.stack()     
print("--- stack() 결과 (Series 형태) ---")
print(df_row)           # 결과는 MultiIndex를 가진 Series 객체가 됨

# unstack(): 행 인덱스의 최하위 레벨을 다시 컬럼으로 되돌림 (Long -> Wide format)
df_col = df_row.unstack()   
print("--- unstack() 결과 (원상 복구) ---")
print(df_col)           # 다시 원래의 DataFrame 형태로 복구됨

print('------------------')
# 데이터 구간화 (Binning / Discretization)
price = [10.3, 5.5, 7.8, 3.6]
cut = [3, 7, 9, 11]     # 구간 경계값 설정 (3~7, 7~9, 9~11)

# pd.cut(): 연속형 데이터를 특정 경계값을 기준으로 나누어 범주형(Categorical) 데이터로 변환
result_cut = pd.cut(price, cut)     
print("--- pd.cut() 결과 ---")
print(result_cut)           # (a, b] 형태: a 초과 b 이하를 의미
print(pd.Series(result_cut).value_counts())  # 각 구간별 데이터 개수(빈도수) 확인

print('------------------')
# qcut(): 데이터의 개수를 기준으로 균등하게 구간을 나눔 (Quantile-based discretization)
datas = pd.Series(np.arange(1, 1001))
print(datas.head(3)) # 상위 3개 확인
print(datas.tail(2)) # 하위 2개 확인

result_cut2 = pd.qcut(datas, 3) # 데이터를 3개의 동일한 크기(개수)를 가진 구간으로 나눔
print("--- pd.qcut() 결과 ---")
print(pd.Series(result_cut2).value_counts()) # 각 구간에 약 333개씩 배분됨

print('------------------')
# agg() 함수 : 그룹화된 데이터에 대해 여러 개의 통계 함수를 한꺼번에 적용
group_col = datas.groupby(result_cut2, observed=True) # 구간별로 그룹화     observed=True : 데이터 있는 것만 작업
print(group_col.agg(['count', 'mean', 'std', 'min', 'max'])) # 개수, 평균, 표준편차, 최소, 최대값 계산

# agg 함수 대신 사용자 함수를 작성
def summaryFunc(gr):
    return {
        'count':gr.count(),
        'mean':gr.mean(),
        'std':gr.std(),
        'min':gr.min(),
        'max':gr.max()
    }

# apply(): 정의한 함수를 각 그룹에 일괄 적용
print("--- apply(summaryFunc) 결과 ---")
print(group_col.apply(summaryFunc))         # 결과가 딕셔너리 형태로 각 행에 들어감

# unstack()을 사용하여 딕셔너리 형태의 결과를 보기 좋게 컬럼으로 펼침
print(group_col.apply(summaryFunc).unstack())       

print('------------------') 
# merge : 데이터 프레임 객체 병합
# SQL의 Join 연산과 유사하게 공통된 열(Key)을 기준으로 두 객체를 병합
df1 = pd.DataFrame({'data1':range(7), 'key':['b', 'b', 'a', 'c', 'a', 'a', 'b']})
print(df1)
df2 = pd.DataFrame({'key':['a', 'b', 'd'], 'data2':range(3)})
print(df2)
print()

# on='key': 병합 기준이 될 컬럼 지정. 생략 시 이름이 같은 컬럼을 자동으로 찾음
print(pd.merge(df1, df2, on='key'))     # 기본값 how='inner' (교집합)
print()
print(pd.merge(df1, df2, on='key', how='inner')) # 양쪽 모두에 키가 존재하는 행만 유지
print()
print(pd.merge(df1, df2, on='key', how='outer')) # 한쪽에만 키가 있어도 포함 (합집합)
print()
print(pd.merge(df1, df2, on='key', how='left'))  # 왼쪽(df1) 기준, 오른쪽 데이터가 없으면 NaN
print()
print(pd.merge(df1, df2, on='key', how='right')) # 오른쪽(df2) 기준, 왼쪽 데이터가 없으면 NaN

print()
# 공통 칼럼명이 없는 경우 : df1 , df3
df3 = pd.DataFrame({'key2':['a', 'b', 'd'], 'data2':range(3)})
print(df3)
print(df1)
# left_on, right_on: 양쪽 프레임의 기준 컬럼명이 다를 때 각각 지정
print(pd.merge(df1, df3, left_on='key', right_on='key2')) 

# concat : 자료 이어 붙이기
# 물리적으로 데이터를 단순히 연결 (Index 기준)
print(pd.concat([df1, df3]))       # 기본값 axis=0 (위아래로 연결)
print(pd.concat([df1, df3], axis=1))   # axis=1 (좌우로 연결)

print('-------------------------')
# pivot_table : pivot과 groupby의 기능을 결합한 형태
# pivot : 데이터의 열을 기준으로 행과 열을 재구성하여 표 형태로 만듦 (중복된 키가 있으면 에러 발생)
# pivot_table : pivot과 달리 중복된 키에 대해 집계(Aggregation) 기능을 제공

data = {
        'city':['강남', '강북', '강남', '강북'],
        'year':[2000, 2001, 2002, 2002],
        'pop':[3.3, 2.5, 3.0, 2.0]
        }
df = pd.DataFrame(data)
print(df)

print()
# pivot(행인덱스, 열인덱스, 데이터값)
print(df.pivot(index='city', columns='year', values='pop'))
print(df.pivot(index='year', columns='city', values='pop'))

print()
# set_index 후 unstack을 통해서도 pivot과 유사한 결과 생성 가능
print(df.set_index(['city', 'year']).unstack())

print()
print(df['pop'].describe())

print()
# pivot_table(index=행, columns=열, values=값, aggfunc=집계함수)
print(df.pivot_table(index='city')) # 기본 aggfunc='mean' (평균)
print(df.pivot_table(index='city', aggfunc='mean'))
print(df.pivot_table(index=['city', 'year'], aggfunc=[len, 'sum']))
print(df.pivot_table(values='pop', index='city', aggfunc=len))

# margins=True: 행/열의 총합(All)을 추가, fill_value: NaN을 특정 값으로 채움
print(df.pivot_table(values='pop', index=['year'], columns=['city'], margins=True, fill_value=0))

print()
# groupby : 특정 컬럼을 기준으로 데이터를 그룹화하여 연산 수행
hap = df.groupby(['city']) # 그룹 객체 생성
print(hap.sum())           # 그룹별 합계
print(df.groupby(['city']).sum()) # 한 줄로 표현