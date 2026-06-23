# 집단간 차이분석 : 평균 또는 비율 차이를 분석
#                : 모집단에서 추출한 표본정보를 이용하여 모집단의 다양한 특성을 과학적으로 추론할 수 있다.
# [개념] 추론 통계(Inferential Statistics): 표본을 통해 모집단의 특성을 확률적으로 추측하는 과정

# 단일 분포 t 검정(One- Sample t-test)
# : 정규분포의 표본에 대한 기댓값을 조사하는 검정 방법
# : 예상 평균값과 표본 자료 간에 평균의 차이를 검정
# [개념] t-분포: 표본의 크기가 작을 때(보통 30미만) 사용하는 분포로, 정규분포보다 양 끝단(Tail)이 두꺼운 형태임

# [변수 설정] 독립변수 : 범주형(집단) / 종속변수 : 연속형(수치 데이터)

# 하나의 집단에 대한 표본 평균이 예측된 평균(모집단)과 같은지 여부를 확인

# <실습 1> - 어느 남성 집단의 키 검정
# [문법] 필요한 라이브러리 임포트
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

#########################
# 가설 수립
#########################
# [개념] 귀무가설(H0): 차이가 없다, 효과가 없다 (해당 집단의 평균 키가 177이다.)
# [개념] 대립가설(H1): 차이가 있다, 효과가 있다 (해당 집단의 평균 키가 177이 아니다.)

one_sample = [167.0, 182.7, 169.6, 176.8, 185.0]
print(np.array(one_sample).mean())      # 표본 평균 계산: 176.219

# [문법] stats.ttest_1samp(a, popmean): 단일 표본 t-검정 수행
# a: 표본 데이터, popmean: 비교하고자 하는 모집단의 기대 평균값
result = stats.ttest_1samp(one_sample, popmean=177)
print(result)
print('\n')
# 결과 해석: statistic(t-통계량)=-0.221, pvalue(유의확률)=0.835, df(자유도)=4
# [개념] 자유도(df): 표본 수(n) - 1 = 5 - 1 = 4

################
# 판정
################
# [판정] 유의 수준 0.05 < p-value(0.8356) 이므로, 귀무가설을 기각할 수 없음(채택)
# 결론 : 해당 집단의 평균 키가 177이라고 볼 수 있다. (통계적으로 유의미한 차이가 없음)

#########################
# [실습 2] 예상 평균을 165로 설정했을 때의 검정
result2 = stats.ttest_1samp(one_sample, popmean=165)
print(result2)
print('\n')
# 결과 해석: statistic=3.184, pvalue=0.033

################
# 판정
################
# [판정] 유의 수준 0.05 > p-value(0.0333) 이므로, 귀무가설 기각, 대립가설 채택
# 결론 : 해당 집단의 평균 키는 165라고 할 수 없다. (통계적으로 유의미한 차이가 있음)

###############
# 시각화
###############
# [문법] sns.displot: 데이터의 분포를 히스토그램과 밀도 곡선(KDE)으로 시각화
# bins: 막대 개수, kde=True: 커널 밀도 추정 곡선 표시
sns.displot(one_sample, bins=10, kde=True)
plt.xlabel('data')
plt.ylabel('value')
plt.title('남성 집단 키 분포')

# [추천] : 표본의 크기가 매우 작을 때는 정규성 검정(stats.shapiro)을 먼저 수행하여 
# 데이터가 정규분포를 따르는지 확인하는 과정이 선행되는 것이 좋습니다.

plt.show()