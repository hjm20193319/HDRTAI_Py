# 독립 표본 t-검정 (independent samples t-test)
# 서로 독립인 두 집단의 평균에 대한 통계 검정에 사용된다.
# [개념] 독립 표본: 한 집단의 측정값이 다른 집단의 측정값에 영향을 주지 않는 상태 (예: 남성과 여성)

# 비교를 위해 평균과 표준편차 통계량을 사용한다.
# 두 집단의 평균 차이를 표준오차로 나눈 t-통계량을 통해 가설을 검정한다.

# 남녀의 성적, A반과 B반의 키, 경기도와 충청도의 소득 따위의 
# 서로 독립인 두 집단에서 얻은 표본을 독립표본(two sample)이라고 한다.

# <실습> 
# [변수 설정] 독립변수 : 범주형(성별) / 종속변수 : 연속형(시험 점수)
# 남녀 두 집단 간 파이썬 시험의 평균 차이 검정
# 두 가지 교육방법에 따른 평균시험 점수에 대한 검정 수행 two_sample.csv
# 남녀의 시험 평균이 우연히 같을 확률은 얼마나 될까?
# 만약 우연히 발생했다면 평균은 같은 것이고, 우연이 아니면 평균은 다른 것이다.
# 95% 신뢰 구간에서 우연히 발생할 확률이 5% 이상이면, 귀무가설 채택이다.

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 가설 수립
# 귀무가설 : 남녀 두 집단 간 파이썬 시험의 평균의 차이는 없다
# 대립가설 : 남녀 두 집단 간 파이썬 시험의 평균의 차이는 있다

male = [75, 85, 100, 72.5, 86.5]
female = [63.2, 76, 52, 100, 70]
print(np.mean(male), ' ', np.mean(female))  # 83.8   72.24
# [추천] : 데이터의 분포를 시각적으로 먼저 확인하기 위해 sns.boxplot(data=[male, female])을 사용하는 것이 좋습니다.

# 두 개의 표본에 대한 '독립 표본 t-검정' 수행
# [문법] stats.ttest_ind(a, b, equal_var=True): 독립 표본 t-검정 수행. equal_var는 등분산성 여부(기본값 True)
two_sample = stats.ttest_ind(male, female)
print(two_sample)
# TtestResult : statistic=1.233193127514512, pvalue=0.2525076844853278, df=8.0
print('\n')

# [문법] 결과 객체에서 통계량(tv)과 유의확률(pv)을 언패킹하여 할당
tv, pv = two_sample
print('t 검정 통계량 : ', tv)
print('p value : ', pv)
# t 검정 통계량 :  1.233193127514512
# p value :  0.2525076844853278
print('\n')

# 해석
# : 유의 수준(alpha) 0.05 < p-value(0.2525) 이므로 귀무가설 채택
# : 결론 : 남녀 두 집단 간 파이썬 시험의 평균의 차이는 없다

print('-----------------------------------')
# 선행 조건 1)
# : 두 집단이 각각 정규분포를 따라야 한다
# [개념] 정규성 가정: 모집단이 정규분포를 따라야 t-검정의 결과가 유효함

# [문법] stats.shapiro(data): 샤피로-윌크 검정을 통해 데이터의 정규성 확인 (H0: 정규분포를 따른다)
print('male의 정규성 : ', stats.shapiro(male))
print('female의 정규성 : ', stats.shapiro(female))
# male의 정규성 : pvalue=0.6003714029870378
# female의 정규성 : pvalue=0.778043110871599
# [판정] 둘 다 유의 수준 0.05 보다 크다 -> 귀무가설을 채택하여 정규성을 만족한다고 판단함

# [개념] 중심극한정리: 만약 집단의 표본 수가 30개 이상인 경우, 정규성 검정 없이도 정규 분포를 따르는 것으로 가정 가능

# 만약 정규성을 만족하지 못하면(모두 불만족) 비모수 검정인 Mann-whitney test 를 한다
# [문법] stats.mannwhitneyu(group1, group2): 순위합을 이용한 비모수 검정 방법
# [수정] p-value > 0.05 인 경우, 차이 증거 없음(귀무 채택) / p-value < 0.05 인 경우, 두 집단 평균 차이 있음(대립 채택)
print('\n')

# 선행 조건 2) 
# : 두 집단의 분산이 같다는 가정이 필요. '등분산성' (패턴이 비슷하다)
# [개념] 등분산성(Homoscedasticity): 비교하는 두 집단의 분산(흩어짐 정도)이 통계적으로 유의미하게 다르지 않아야 함
from scipy.stats import levene, bartlett, fligner
# [개념] levene : 정규성과 상관없이 사용 가능하며, 이상치에 덜 민감함 (범용적 사용)
# [개념] bartlett : 데이터가 정규성을 확실히 따를 때만 사용하며, 이상치에 매우 민감함

# [문법] 각 함수는 (집단1, 집단2)를 인자로 받아 통계량과 p-value를 반환함
levene_stat, levene_p = levene(male, female)
bartlett_stat, bartlett_p = bartlett(male, female)
print('levene_stat : ', levene_stat)
print('levene_p : ', levene_p)
# [판정] levene_p : 0.4956 > 0.05 -> 귀무가설(분산이 같다)을 채택하여 등분산성 만족
print('bartlett_stat : ', bartlett_stat)
print('bartlett_p : ', bartlett_p)

# [추천] : 만약 등분산성을 만족하지 못할 경우(p < 0.05), stats.ttest_ind(..., equal_var=False) 옵션을 주어 
# 'Welch's t-test'를 수행해야 합니다.