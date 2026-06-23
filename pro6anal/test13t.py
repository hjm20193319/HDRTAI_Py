# Paired Samples t-test 대응 표본 t 검정 (동일 집단 표본 t 검정)
# [개념] 대응 표본 t-검정: 동일한 대상에 대해 두 번 측정하여 전후 차이의 평균이 0인지 검정함.
# [개념] 차이값의 정규성: 엄밀하게는 두 측정값의 '차이(Difference)'가 정규분포를 따라야 함.
# [개념] 등분산성 제외: 동일 인물의 반복 측정이므로 두 시점의 분산이 같아야 한다는 조건은 필요하지 않음.

# < 실습 >
# : 복부 수술 전 9명의 몸무게와 복부 수술 후 몸무게 변화

######################
# 가설 수립
######################
# [개념] 귀무가설(H0): 차이가 없다, 효과가 없다 / 대립가설(H1): 차이가 있다, 효과가 있다.
# 귀무 가설 : 복부 수술 전 몸무게와 복부 수술 후 몸무게의 변화는 없다.
# 대립 가설 : 복부 수술 전 몸무게와 복부 수술 후 몸무게의 변화는 있다.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

######################
# 데이터 수집
######################
# 복부 수술 전 몸무게
baseline = [67.2, 67.4, 71.5, 77.6, 86.0, 89.1, 59.5, 81.9, 105.5]
# 수술 후 몸무게
follow_up = [62.4, 64.6, 70.4, 62.6, 80.1, 73.2, 58.2, 71.0, 101.0]

# [문법] np.mean(data): 데이터의 산술 평균을 계산함
print('수술 전 평균 몸무게:', np.mean(baseline))
print('수술 후 평균 몸무게:', np.mean(follow_up))
print('평균의 차이 : ', np.mean(baseline) - np.mean(follow_up)) # 6.911111111111111

# [추천] : 분석 전 stats.shapiro(np.array(baseline) - np.array(follow_up))를 통해 
# 전후 차이값의 정규성을 먼저 검정하는 것이 통계적으로 더 엄밀합니다.

# 시각화
# [문법] plt.bar(x, height): 막대 그래프를 생성함. np.arange(2)는 x축 위치 [0, 1] 생성
plt.bar(np.arange(2), [np.mean(baseline), np.mean(follow_up)])
plt.xlim(0, 1)
plt.xticks([0, 1], ['수술 전', '수술 후'])
plt.xlabel('수술 전후', fontdict={'size':12, 'fontweight':'bold'})
plt.ylabel('몸무게(kg)')
plt.title('복부 수술 전후 몸무게 변화')
plt.show()

# [추천] : 개별 환자의 변화를 보여주기 위해 plt.plot([baseline, follow_up], marker='o')와 같은 
# 스파게티 플롯(Spaghetti Plot)을 사용하면 데이터의 개별 흐름을 더 잘 파악할 수 있습니다.
plt.figure(figsize=(8, 5))
plt.plot(['수술 전', '수술 후'], [baseline, follow_up], marker='o', color='gray', alpha=0.5)
plt.plot(['수술 전', '수술 후'], [np.mean(baseline), np.mean(follow_up)], marker='s', color='red', linewidth=3, label='평균 변화')
plt.title('개별 환자별 몸무게 변화 (Spaghetti Plot)')
plt.ylabel('몸무게(kg)')
plt.legend()
plt.show()
######################
# t-test
######################
# [문법] stats.ttest_rel(a, b): 동일 집단의 전(a), 후(b) 데이터를 비교하는 대응 표본 t-검정 수행
result = stats.ttest_rel(baseline, follow_up)
print(result)
# statistic=3.6681166519351103, pvalue=0.006326650855933662, df=8
# [개념] 자유도(df): 표본 수(n) - 1 = 9 - 1 = 8

################
# 판정
################
# [판정] 유의 수준 0.05 > p-value 0.0063 이므로, 귀무 가설 기각
# 결론 : 복부 수술 전 몸무게와 복부 수술 후 몸무게의 변화는 있다.