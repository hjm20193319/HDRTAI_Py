# <선호도 분석 실습>
# [개념] 일원 카이제곱 검정(One-way Chi-square Test): 
# 하나의 범주형 변수에 대해 각 범주별 관찰 빈도가 특정 기대 빈도와 일치하는지 검정합니다.
# 여기서는 5개의 스포츠 음료에 대한 선호도(빈도)가 균등한지(기대치)를 확인합니다.

# [목적] 5개의 스포츠 음료에 대한 선호도에 차이가 있는지 검정하기
# (모든 음료의 선호도가 같다면 기대 빈도는 '전체 합계 / 5'가 됩니다.)

##########################
# 가설 수립
##########################
# 귀무가설 : 기대치와 관찰치는 차이가 없다. 스포츠 음료의 선호도에 차이가 없다.
# 대립가설 : 기대치와 관찰치는 차이가 있다. 스포츠 음료의 선호도에 차이가 있다.

import pandas as pd
import scipy.stats as stats

#################
# 데이터 수집
#################
# [문법] pd.read_csv: 외부 URL의 CSV 데이터를 읽어와 데이터프레임 생성
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinkdata.csv')
print(data) # 음료종류와 관측도수 컬럼 확인

# [문법] stats.chisquare(f_obs): 관측 빈도 리스트를 인자로 받아 카이제곱 통계량과 p-value 반환
# f_exp(기대 빈도)를 생략하면 모든 범주의 확률이 동일하다고 가정하고 자동 계산함
print(stats.chisquare(data['관측도수']))
# 결과 : statistic=20.488, pvalue=0.0003999

# [개념] 기대 빈도 계산: 전체 관측값의 합을 범주의 수(5)로 나눈 값
exp = [data['관측도수'].sum() / 5] 
print(exp)
# 기대 빈도 : 50.8

# [문법] f_obs(관측값), f_exp(기대값)를 명시적으로 전달하여 검정 수행
stat, p = stats.chisquare(f_obs=data['관측도수'], f_exp=exp)
print('stat : ', stat)
print('p : ', p)

# 판정 : 유의수준 0.05 > p-value 0.0003999 이므로, 귀무 가설을 기각하고 대립 가설을 채택
# 결론 : 스포츠 음료의 선호도에 차이가 있다.

###################
# 시각화
################### 
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np

# 기대도수
total = data['관측도수'].sum()
expected = [total / len(data)] * len(data)
x = np.arange(len(data))        # [문법] np.arange: 음료 종류 개수만큼의 인덱스 배열 생성 (0~4)
width = 0.35                    # [개념] 막대 그래프의 너비 설정

plt.figure(figsize=(10, 5))
# [문법] plt.bar: 막대 그래프 생성. x축 위치를 조절하여 관측도수와 기대도수를 나란히 배치(Grouped Bar Chart)
plt.bar(x -width/2, data['관측도수'], width=width, label='관측도수')
plt.bar(x +width/2, expected, width=width, label='기대도수', alpha=0.6)

plt.xticks(x, data['음료종류']) # x축 눈금을 음료 이름으로 변경
plt.ylabel('빈도수')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#########################

#########################
# 카이제곱 검정 결과와 그래프를 근거로 어떤 음료가 더 인기 있는지 분석
data['기대도수'] = expected # 분석을 위해 데이터프레임에 기대도수 컬럼 추가
data['차이(관측 - 기대)'] = data['관측도수'] - data['기대도수'] # 잔차(Residual) 계산
data['차이비율(%)'] = round(data['차이(관측 - 기대)'] / expected * 100, 2) # 기대치 대비 증감 비율

pd.set_option('display.max_rows', None) # [문법] 데이터프레임 출력 시 모든 행을 표시하도록 설정
# print(data)

# [문법] sort_values: 특정 컬럼을 기준으로 정렬. ascending=False는 내림차순(큰 값부터)
data.sort_values(by='차이(관측 - 기대)', ascending=False, inplace=True)     
data.reset_index(drop=True, inplace=True) # 정렬 후 인덱스를 0부터 다시 재설정
print(data)
# [추천] : 분석 결과에서 '차이(관측-기대)'가 양수인 항목은 선호도가 높은 음료, 음수인 항목은 낮은 음료로 해석할 수 있습니다.