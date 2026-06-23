# 단일 모집단의 평균에 대한 가설 검정 (One-Samples t-test)
# [개념] 단일 표본 t-검정: 연속형 변수로 구성된 한 집단의 평균이 특정 기준값(모집단 평균)과 차이가 있는지 검정함
# [개념] t-검정의 전제조건: 독립성(표본은 독립적이어야 함), 정규성(표본이 정규분포를 따라야 함), 등분산성(두 집단 이상일 때 해당)

# <실습 예제>
# A중학교 1학년 1반 학생들의 시험 결과가 담긴 파일을 읽어 처리
# 국어 점수 평균검정 (80) -- student.csv

#######################
# 가설 수립
#######################
# 귀무가설 : 학생들의 국어점수 평균은 80이다.
# 대립가설 : 학생들의 국어점수 평균은 80이 아니다.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from scipy.stats import wilcoxon # [문법] wilcoxon: 정규성 가정을 만족하지 못할 때 사용하는 비모수 검정 함수

#################
# 데이터 수집
################
# [문법] pd.read_csv: 외부 URL의 CSV 데이터를 읽어와 데이터프레임 생성
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/student.csv')
print(data.head())
# [문법] .describe(): 수치형 데이터의 주요 기술 통계량(개수, 평균, 표준편차, 사분위수 등)을 요약 출력
print(data.describe())  # mean : 72.900000 
print(data['국어'].mean())
print('\n')

##############################
# 정규성 검정 : p-value는 alpha보다 커야 정규성을 따른다고 할 수 있다.
##############################
# [개념] 중심극한정리(Central Limit Theorem): 표본의 크기가 충분히 크면(보통 n >= 30), 모집단의 분포와 상관없이 표본 평균의 분포는 정규분포를 따름
# [개념] 샤피로-윌크 검정(Shapiro-Wilk Test): 데이터가 정규분포로부터 추출되었는지 확인하는 검정 (H0: 정규분포를 따른다)
print(len(data))       # 건수 : 20  -> 30행 미만이므로 정규성 확인이 필수적임

# 30개가 넘지 않으므로, 정규성 검정 실시
# [문법] stats.shapiro(data): 샤피로-윌크 검정을 통해 데이터가 정규분포를 따르는지 확인 (귀무: 정규분포를 따른다)
print(stats.shapiro(data['국어']))
# pvalue = 0.0129597
# [판정] 유의 수준 0.05 > p-value(0.0129) 이므로 귀무가설 기각 -> 정규성을 만족하지 않음
print('\n')

####################################################################################################
# 정규성을 만족하지 않은 경우 대안 
# -> Wilcoxon matched paired t-test : 비모수 검정 방법으로 정규성이 없을 때 적절한 선택이 될 수 있다.
####################################################################################################
# [개념] 비모수 검정(Non-parametric test): 모수(평균, 분산 등)에 대한 가정을 하지 않고 순위(Rank)나 빈도를 이용하는 검정 방식
# [개념] 윌콕슨 부호순위 검정: 데이터의 정규성이 보장되지 않을 때, 중앙값을 기준으로 차이의 순위를 매겨 검정함
# from scipy.stats import wilcoxon
# [문법] wilcoxon(x - popmean): 단일 표본의 중앙값과 특정 값의 차이를 검정
wilcoxon_result = wilcoxon(data['국어'] - 80)
print('wilcoxon_result : ', wilcoxon_result)
# statistic=74.0, pvalue=0.3977762065889890
# [판정] 유의 수준 0.05 < p-value(0.3977) 이므로 귀무가설을 채택함
print('\n')

# [문법] stats.ttest_1samp(a, popmean): 단일 표본 t-검정 수행
# a: 표본 데이터, popmean: 비교할 모집단의 평균값
result = stats.ttest_1samp(data['국어'], popmean=80)
print(result)
# statistic=-1.3321801667713216, pvalue=0.19856051824785262, df=19
# [판정] 유의 수준 0.05 < p-value(0.1985) 이므로 귀무가설을 채택함

#######################
# 결론
#######################
# 정규성은 부족하나, 귀무가설 채택이라는 동일 결론을 얻음
# 표본 수가 크다면 ttest_1samp() 사용 가능
# 보고서 작성시에는 
# "shapiro-wilk test 결과, 정규성 가정이 다소 위배되었으나
# 비모수 검정(wilcoxon) 결과도 동일하므로 ttest_1samp() 결과를 신뢰할 수 있다" 
# 라고 명시한다.

# [추천] : 데이터의 분포를 시각적으로 확인하기 위해 sns.histplot(data['국어'], kde=True)나 
# stats.probplot(data['국어'], plot=plt) (Q-Q plot)을 병행하면 정규성 위배 정도를 더 직관적으로 파악할 수 있습니다.

###############
# 시각화
###############
# [문법] sns.histplot: 데이터의 빈도를 막대 형태로 나타내며, kde=True 옵션으로 밀도 곡선을 추가함
sns.histplot(data['국어'], kde=True)
plt.title('국어 점수 분포')
plt.show()

print('-------------------------------------------')

#######################################################################################################
# <실습 2>
# 여아 신생아 몸무게의 평균 검정 수행
# 여아 신생아의 몸무게는 평균이 2800g으로 알려져 왔으나 이보다 더 크다는 주장이 나왔다.
# 표본으로 여아 18명을 뽑아 체중을 측정하였다고 할 때 새로운 주장이 맞는지 검증해보자

# [변수 설정] 독립변수 : 범주형(성별) / 종속변수 : 연속형(몸무게)
# [개념] 단측 검정(One-tailed test): '크다' 또는 '작다'와 같이 한쪽 방향의 차이만을 검정함

############################
# 가설 수립
############################
# 귀무가설 : 여아 신생아의 몸무게는 평균이 2800g 이다.
# 대립가설 : 여아 신생아의 몸무게는 평균이 2800g 보다 크다

############################
# 데이터 수집
############################
data2 = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/babyboom.csv')
print(data2.head())
# [문법] .describe(): 데이터프레임의 수치형 컬럼들에 대한 요약 통계 정보 제공
print(data2.describe())
print('\n')

fdata = data2[data2.gender == 1]    # 여아 : 1, 남아 : 2
print(fdata)
print('여아 신생아 수 : ', len(fdata))      # 18
print('여아 몸무게 평균 : ', np.mean(fdata['weight']))  # 3132.44
# 2800 과 3132는 평균에 차이가 있는가?
print('여아 몸무게 표준편차 : ', np.std(fdata.weight))  # 613.787
print('\n')

################################
# One sample t-test 
################################
# [문법] stats.ttest_1samp: 표본 평균과 모집단 평균(2800) 간의 차이를 검정
result2 = stats.ttest_1samp(fdata['weight'], popmean=2800)
print('result2 : ',result2)
# statistic=2.233, pvalue=0.0392, dof=17

############################
# 판정 1 - pvalue 사용
############################
# alpha 0.05 > p-value=0.0392 이므로 귀무가설 기각
# 결론 : 여아 신생아의 몸무게는 평균이 2800g 보다 크다.

############################
# 판정 2 - t 분포표 사용
############################
# t 값 : statistic=2.233, dof=17, alpha=0.05
# [문법] stats.t.ppf(0.95, 17): 유의수준 0.05, 자유도 17에서의 임계값(Critical Value) 계산
# cv = 1.740
# t value > cv 이므로 귀무기각 영역에 존재, 귀무가설 기각
# 결론 : 여아 신생아의 몸무게는 평균이 2800g 보다 크다.

print('-------------------------------------------')

##################################
# 선행 조건인 정규성 검정을 한 경우
##################################
print(stats.shapiro(fdata['weight']))   # p-value=0.017984789994719325
# alpha 0.05 > p-value=0.017984789994719325 이므로 정규성을 만족하지 않음

##############################
# 시각화 - 정규성 만족 여부
##############################
# histplot
# [추천] : 표본 수가 적을 때는 히스토그램의 bin(구간) 개수를 적절히 조절하여 분포 왜곡을 방지해야 합니다.
sns.histplot(fdata['weight'], kde=True)
plt.title('여아 신생아 몸무게 분포')
plt.show()

# Quantile- Quantile plot (QQ plot)
# [개념] Q-Q Plot: 수집된 데이터의 분위수와 이론적 정규분포의 분위수를 비교하여 직선에 가까울수록 정규성을 띰
stats.probplot(fdata['weight'], plot=plt)
plt.title('여아 신생아 몸무게 분포')
plt.show()
# Q-Q plot 상에서 점들이 직선을 크게 벗어나므로 정규성을 만족하지 못한다고 판단함

###########################
# 비모수 검정 - wilcoxon
###########################
result3 = wilcoxon(fdata['weight'] - 2800)
print('result3 : ', result3)
# statistic=37.0, pvalue=0.03423

#######################
# 판정
#######################
# alpha 0.05 > p-value=0.03423 이므로, 귀무가설 기각
# 결론 : 여아 신생아의 몸무게는 평균이 2800g 보다 크다.
