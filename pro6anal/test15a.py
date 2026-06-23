# 일원분산분석으로 평균 차이 검정
# 강남구에 있는 GS편의점 3개 지역 알바생의 급여에 대한 평균 차이 검정
# 요인 : GS 편의점
# [개념] 일원분산분석(One-way ANOVA): 세 개 이상의 집단 간 평균 차이가 통계적으로 유의미한지 검정하는 기법.

# 가설 수립
# 귀무 가설(H0) : GS편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 없다.
# 대립 가설(H1) : GS편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 있다.

import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.formula.api import ols 
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 수집
# [문법] 외부 URL의 텍스트 데이터를 읽어오기 위한 경로 설정
uri = 'https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3.txt'

# 읽기 1 - DataFrame type -> 배열로 변환
# data = pd.read_csv(uri, header=None)
# data = data.values    # 배열로 바꾸기
# print(data)
# print('\n')

# 읽기 2 - 배열로 읽기 (추천 방식)
import urllib.request as req
data = np.genfromtxt(req.urlopen(uri), delimiter=',')
print(data, type(data))     #  <class 'numpy.ndarray'>
print(data.shape)       # (22, 2)
print('\n')

# 세 개 집단의 월급 자료 읽기, 평균
# [문법] 불리언 인덱싱: data[:, 1] == 1 조건을 만족하는 행의 0번째 열(급여) 데이터를 추출
gr1 = data[data[:, 1] == 1, 0]
gr2 = data[data[:, 1] == 2, 0]
gr3 = data[data[:, 1] == 3, 0]
print(gr1, ' ', np.mean(gr1))   # 316.625
print(gr2, ' ', np.mean(gr2))   # 256.444
print(gr3, ' ', np.mean(gr3))   # 278.0
print('\n')

# 정규성 확인
# [문법] stats.shapiro(data): 샤피로-윌크 검정을 통해 데이터가 정규분포를 따르는지 확인 (H0: 정규분포를 따른다)
print(stats.shapiro(gr1).pvalue)
print(stats.shapiro(gr2).pvalue)
print(stats.shapiro(gr3).pvalue)
# 0.3336828974377483
# 0.6561053962402779
# 0.8324811457153043
# [판정] 모든 집단의 p-value > 0.05 이므로 정규성 가정을 충족함
print('\n')

# 등분산성
# [문법] stats.levene: 이상치에 강한 등분산성 검정 / stats.bartlett: 정규성을 따르는 데이터에 적합한 등분산성 검정
print(stats.levene(gr1, gr2, gr3).pvalue)       # 0.0458
print(stats.bartlett(gr1, gr2, gr3).pvalue)     # 0.3508
# [판정] bartlett 검정 결과 p-value > 0.05 이므로 등분산성 가정을 충족하는 것으로 간주함

# 데이터 퍼짐 정도 시각화
# plt.boxplot([gr1, gr2, gr3], labels=['gr1', 'gr2', 'gr3'], showmeans=True)
# plt.show()
# [추천] : sns.violinplot을 사용하면 박스플롯보다 데이터의 밀도 분포를 더 상세하게 확인할 수 있습니다.

# 일원분산분석 - 방법 1 : anova_lm() - 유도되는 과정을 알고 싶을 때
# [문법] pd.DataFrame: 넘파이 배열을 판다스 데이터프레임으로 변환
df = pd.DataFrame(data=data, columns=['pay', 'group'])
print(df)

# [문법] ols('종속변수 ~ 독립변수', data).fit(): 최소제곱법 회귀 모델 생성. C()는 해당 변수가 범주형임을 명시함
lmodel = ols('pay ~ C(group)', data=df).fit()       
# [문법] anova_lm(model, typ=1): 적합된 모델을 바탕으로 분산분석표(ANOVA Table)를 생성함
result = anova_lm(lmodel, typ=1)
print(result)
# [해석] PR(>F)는 p-value를 의미함
# p-value = 0.043589 < alpha 0.05 이므로, 귀무가설 기각
# 결론 : GS편의점 3개 지역 알바생의 급여에 대한 평균은 차이가 있다.
print('\n')

# 일원분산분석 - 방법 2 : f_oneway() - 결과만 알고 싶을 때
f_stat, p_val = stats.f_oneway(gr1, gr2, gr3)
print('f_stat : ', f_stat)
print('p_val : ', p_val)
# f_stat :  3.711335988266977
# p_val :  0.043589334959178244
print('\n')

# 사후 검정
from statsmodels.stats.multicomp import pairwise_tukeyhsd
# [개념] 사후분석(Post Hoc): ANOVA 결과가 유의미할 때, 구체적으로 어떤 집단 간에 차이가 있는지 확인하는 절차
# [문법] pairwise_tukeyhsd(endog, groups): Tukey의 HSD 검정 수행
tukResult = pairwise_tukeyhsd(endog=df['pay'], groups=df['group'])
print(tukResult)
#  Multiple Comparison of Means - Tukey HSD, FWER=0.05  
# ======================================================
# group1 group2 meandiff p-adj    lower    upper  reject
# ------------------------------------------------------
#    1.0    2.0 -60.1806 0.0355  -116.619 -3.7421   True
#    1.0    3.0  -38.625 0.3215 -104.8404 27.5904  False
#    2.0    3.0  21.5556 0.6802  -43.2295 86.3406  False
# ------------------------------------------------------

# 시각화
tukResult.plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()

# 참고
# anva_lm() : 정규성, 등분성이 깨지면 p-value 신뢰 불가
# f_oneway() : 정규성 깨지면 stats.kruskal(), 등분산성이 깨지면 welch ANOVA 사용