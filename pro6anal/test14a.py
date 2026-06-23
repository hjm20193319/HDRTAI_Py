# 세 개 이상의 모집단에 대한 가설검정 – 분산분석
# 분산이 발생한 과정을 분석하여 요인에 의한 분산과 요인을 통해 나누어진 
# 각 집단 내의 분산으로 나누고 요인에 의한 분산이 의미 있는 크기를 가지는지를 검정하는 것을 의미한다.
# [개념] 분산분석(ANOVA): 세 개 이상의 집단 간 평균 차이가 통계적으로 유의미한지 검정하는 기법.

# 세 집단 이상의 평균비교에서는 독립인 두 집단의 평균 비교를 반복하여 실시할 경우에 
# 제1종 오류가 증가하게 되어 문제가 발생한다.
# 이를 해결하기 위해 Fisher가 개발한 분산분석(ANOVA, ANalysis Of Variance)을 이용하게 된다.
# [개념] 제1종 오류: 귀무가설이 참임에도 불구하고 이를 기각할 확률. 집단이 많아질수록 t-검정 반복 시 이 오류가 누적됨.

# f 값 = 집단 간 분산 / 집단 내 분산
# [개념] F-통계량: 집단 간 차이(변동)를 집단 내 우연한 차이(변동)로 나눈 값. 이 값이 클수록 평균 차이가 유의미할 가능성이 높음.
 
# 서로 독립인 세 집단의 평균 차이 검정
# 일원 분산 분석 (One way ANOVA)
# < 실습 > 
# : 세 가지 교육방법을 적용하여 1개월 동안 교육받은 교육생 80명을 대상으로 실기시험을 실시.
# 독립 변수(범주형) - 한 개의 요인 : 교육 방법
# 방법의 종류(3가지-그룹 3개)
# 종속 변수(연속형) - 실기시험 평균 점수

# 가설 수립
# 귀무가설 : 3가지 교육 방법에 따른 시험 점수의 차이가 없다.
# 대립가설 : 3가지 교육 방법에 따른 시험 점수의 차이가 있다.

import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.formula.api import ols     # 추정 및 검정, 회귀, 시계열 분석 등의 기능 제공
# [문법] ols: Ordinary Least Squares 최소 제곱법 회귀 모델을 생성하는 함수
# from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 수집
# [문법] pd.read_csv: 외부 URL의 CSV 데이터를 읽어와 데이터프레임 생성
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/three_sample.csv')
print(data.head())
# [문법] .describe(): 수치형 데이터의 주요 기술 통계량(개수, 평균, 표준편차 등) 요약
print(data.describe())
print('\n')

# 이상치 Outlier 를 시각화
# plt.boxplot(data.score)
# plt.show()
# [추천] : sns.boxplot(x='method', y='score', data=data)를 사용하여 그룹별 분포와 이상치를 동시에 확인하는 것이 좋습니다.

# [문법] .query(): 조건식을 문자열로 입력받아 데이터프레임을 필터링함
data = data.query('score <= 100')       # 이상치 처리 (100점 이하만 추출)
print(data.describe())

# 교차표 (교육 방법별 건수) - 참고용
# [문법] pd.crosstab: 범주형 변수의 빈도를 집계하여 교차표 생성
data2 = pd.crosstab(index=data['method'], columns='count')
data2.index = ['방법1', '방법2', '방법3']
print(data2)

# 교차표 (교육 방법별 만족 건수) - 참고용
data3 = pd.crosstab(index=data['method'], columns=data['survey'])
# [추천] : 결측치가 포함되어 있다면 dropna=False 옵션을 주어 결측치 빈도도 함께 확인하는 것이 좋습니다.

data3.index = ['방법1', '방법2', '방법3']
data3.columns = ['만족', '불만족']
print(data3)
print('\n')

# ANOVA 검정
# F 통계값을 얻기 위해 회귀분석 결과를 사용 -> linear model이 필요함
import statsmodels.api as sm

# [문법] ols('종속변수 ~ 독립변수', data).fit(): 선형 회귀 모델을 적합(Fitting)시킴
# [주의] : method가 범주형(1, 2, 3)이므로 'score ~ C(method)'와 같이 C()를 사용하여 범주형임을 명시하는 것이 통계적으로 더 정확합니다.
lin_model = ols('data["score"] ~ data["method"]', data=data).fit()     # 회귀분석 모델 생성

# [문법] sm.stats.anova_lm(model, typ=1): 적합된 모델을 바탕으로 분산분석표를 생성함
result = sm.stats.anova_lm(lin_model, typ=1)
print(result)
print('\n')
#                   df(자유도)    sum_sq(제곱합)     mean_sq(제곱 평균)    F(F값)    PR(>F)-pvalue
# data["method"]       1.0         27.980888            27.980888        0.122228    0.727597
# Residual(잔차)       76.0       17398.134497          228.922822          NaN         NaN
# 해석 : p-value 0.7275 > alpha 0.05 이므로 귀무 채택
# 결론 : 3가지 교육 방법에 따른 시험 점수의 차이가 없다.

# F값, p값 확인
# [문법] .loc[행, 열]: 인덱스 이름을 사용하여 특정 위치의 데이터를 추출
f_value = result.loc['data["method"]', 'F']
p_value = result.loc['data["method"]', 'PR(>F)']
print('f_value : ', f_value)
print('p_value : ', p_value)
print('\n')

# 하지만 정확히 어느 그룹의 평균값이 의미가 있는지는 알려주지는 않는다.
# 그룹 간 평균 차이를 구체적으로 알려 주지 않음
# 그러므로 그룹 간의 관계를 보기 위해 추가적인 사후분석(Post Hoc Analysis)이 필요하다.
# [개념] 사후분석: ANOVA 결과가 유의미할 때(p < 0.05), 구체적으로 어떤 집단들 사이에 차이가 있는지 검정하는 절차.

# 사후분석(Post Hoc Analysis) 하기
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# [문법] pairwise_tukeyhsd(endog, groups): Tukey의 HSD(Honestly Significant Difference) 검정 수행
tukResult = pairwise_tukeyhsd(endog=data['score'], groups=data['method'])
# [개념] reject: True면 두 집단 간 평균 차이가 유의미함, False면 유의미한 차이가 없음.
print(tukResult)
# Multiple Comparison of Means - Tukey HSD, FWER=0.05 
# ====================================================
# group1 group2 meandiff p-adj   lower   upper  reject
# ----------------------------------------------------
#      1      2   0.9725 0.9702 -8.9458 10.8909  False : 유의미한 차이가 없으면 False (있으면 True)
#      1      3   1.4904 0.9363 -8.8183  11.799  False
#      2      3   0.5179 0.9918 -9.6125 10.6483  False
# ----------------------------------------------------

# Tukey HSD 결과 시각화
# [문법] .plot_simultaneous(): 각 집단의 신뢰구간을 시각화하여 겹치지 않으면 유의미한 차이가 있음을 보여줌
tukResult.plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()

# Tukey HSD : 원래 반복 수가 동일하다는 가정하에 고안된 방법
# 집단 간 평균 차이를 정밀하게 확인 가능
# 각 집단의 표본수의 차이가 크면, 결과의 신뢰가 떨어진다
# [추천] : 표본 크기가 다를 경우 Scheffe 검정이나 Bonferroni 교정 등을 대안으로 고려할 수 있습니다.
# [추천] : ANOVA 수행 전 stats.shapiro(정규성)와 stats.levene(등분산성) 검정을 먼저 수행하여 선행 조건을 확인하는 것이 좋습니다.