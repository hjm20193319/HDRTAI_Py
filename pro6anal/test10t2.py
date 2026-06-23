# 독립 표본 t-검정 (independent samples t-test)
# [개념] 독립 표본 t-검정: 서로 다른 두 집단의 평균이 통계적으로 유의미하게 차이가 있는지 검정함
# [전제 조건] 독립성(두 집단은 서로 무관함), 정규성(각 집단은 정규분포를 따름), 등분산성(두 집단의 분산이 유사함)

# <실습 예제>
# 두 가지 교육방법에 따른 평균시험 점수에 대한 검정 수행 two_sample.csv

#################
# 가설수립
#################
# 귀무가설 : 두 가지 교육방법에 따른 평균시험 점수에 차이가 없다.
# 대립가설 : 두 가지 교육방법에 따른 평균시험 점수에 차이가 있다.

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

#################
# 데이터 수집
#################
# [문법] pd.read_csv: 외부 URL의 CSV 데이터를 읽어와 데이터프레임 생성
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/two_sample.csv')
print(data.head())
# [문법] .isnull().sum(): 각 컬럼별 결측치(NaN)의 개수를 합산하여 출력
print(data.isnull().sum())

# 교육 방법별 분리
ms = data[['method', 'score']]
# [문법] 불리언 인덱싱: 특정 조건을 만족하는 행만 추출하여 새로운 데이터프레임 생성
m1 = ms[ms['method'] == 1]  # 교육 방법 1 집단
m2 = ms[ms['method'] == 2]  # 교육 방법 2 집단
print(m1.head())
print(m2.head())
print('\n')

# 교육방법에서 score 만 별도 기억
score1 = m1['score']
score2 = m2['score']
print('score1 결측치 : ', score1.isnull().sum())        # 0개
print('score2 결측치 : ', score2.isnull().sum())        # 2개
print('\n')

# [문법] .fillna(value): 결측치(NaN)를 특정 값으로 채움. 여기서는 해당 집단의 평균값으로 대체함
score2 = score2.fillna(score2.mean())       # NaN을 평균으로 대체
# [추천] : 결측치가 많지 않다면 .dropna()를 사용하여 해당 행을 제거하는 것이 분석의 왜곡을 줄이는 더 깔끔한 방법일 수 있습니다.

##############################
# 정규성 검정 : p-value가 유의수준(0.05)보다 커야 정규성을 따른다고 판단함
##############################
# [문법] stats.shapiro(data): 샤피로-윌크 검정을 통해 데이터가 정규분포를 따르는지 확인 (H0: 정규분포를 따른다)
print(stats.shapiro(score1))
print(stats.shapiro(score2))
# [판정] 두 집단 모두 p-value > 0.05 이므로 귀무가설을 채택하여 정규성을 만족함
print('\n')

###############
# 시각화
###############
# [문법] sns.histplot: 데이터의 빈도를 막대 형태로 나타내며, kde=True 옵션으로 밀도 곡선을 추가함
sns.histplot(score1, kde=True)
sns.histplot(score2, kde=True, color='blue')
plt.show()

##############################
# 등분산성 검정 : 두 집단의 분산(흩어짐 정도)이 같은지 확인
##############################
from scipy.stats import levene
# [문법] stats.levene(sample1, sample2): 레빈 검정을 통해 두 집단의 등분산성 확인 (H0: 분산이 같다)
leven_p = stats.levene(score1, score2).pvalue
print(leven_p)      # 0.4568427112977608
# [판정] 유의 수준 0.05 < p-value 이므로 귀무가설을 채택하여 등분산성을 만족함
# [추천] : 데이터가 정규성을 확실히 따른다면 stats.bartlett()을 사용할 수도 있으나, 일반적으로 levene 검정이 더 범용적입니다.

# 독립 표본 t-검정
# [문법] stats.ttest_ind(a, b, equal_var=True): 독립 표본 t-검정 수행. equal_var=True는 등분산성을 만족할 때 사용
result = stats.ttest_ind(score1, score2, equal_var=True)
print(result)
# pvalue=0.8450532207209545

#######################
# 결론
#######################
# [판정] 유의 수준 0.05 < p-value(0.845) 이므로 귀무가설을 채택함
# 결론 : 두 가지 교육방법에 따른 평균시험 점수에 통계적으로 유의미한 차이가 없다.
# [추천] : 만약 등분산성을 만족하지 못했다면(p < 0.05), equal_var=False 옵션을 주어 Welch's t-test를 수행해야 합니다.