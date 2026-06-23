# 선형 회귀분석 모형의 적절성 선행 조건
# [개념] 선형 회귀 모델이 통계적으로 타당하기 위해서는 정규성, 선형성, 등분산성, 독립성 등의 가정을 만족해야 함.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf

advdf = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv', usecols=[1,2,3,4])
print(advdf.head()) # [문법] 데이터프레임의 상위 5개 행 출력
print(advdf.info()) # [문법] 컬럼명, 데이터 타입, 결측치 여부 확인
print('\n')
print('상관계수 : \n', advdf.corr()) # [문법] 변수 간 피어슨 상관계수 행렬 계산
print('\n')
# [추천] sns.pairplot(advdf)를 통해 모든 변수 간의 산점도와 분포를 한눈에 파악할 수 있음.

# 단순 선형 회귀 모델 - OLS 사용
# x : tv / y : sales

# [문법] smf.ols(formula='y ~ x', data=df).fit(): 최소제곱법을 이용한 선형 회귀 모델 생성 및 학습
lm = smf.ols(formula='sales ~ tv', data=advdf).fit()
print(lm.summary())
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                  sales   R-squared:                       0.612
# Model:                            OLS   Adj. R-squared:                  0.610
# Method:                 Least Squares   F-statistic:                     312.1
# Date:                Mon, 06 Apr 2026   Prob (F-statistic):           1.47e-42
# Time:                        09:54:14   Log-Likelihood:                -519.05
# No. Observations:                 200   AIC:                             1042.
# Df Residuals:                     198   BIC:                             1049.
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      7.0326      0.458     15.360      0.000       6.130       7.935
# tv             0.0475      0.003     17.668      0.000       0.042       0.053
# ==============================================================================
# Omnibus:                        0.531   Durbin-Watson:                   1.935
# Prob(Omnibus):                  0.767   Jarque-Bera (JB):                0.669
# Skew:                          -0.089   Prob(JB):                        0.716
# Kurtosis:                       2.779   Cond. No.                         338.
# ==============================================================================
print('\n')
print(lm.summary().tables[1])
print('\n')
# [문법] params: 회귀계수(기울기, 절편), pvalues: 유의확률, rsquared: 결정계수
print(f'coefficients : \n{lm.params}\np-value : \n{lm.pvalues}\nr-squared : \n{lm.rsquared}') 
print('\n')

# 예측
x_new = pd.DataFrame({'tv':advdf['tv'][:3]})
print(x_new)
print('실제값 : ', advdf['sales'][:3].values)
# [문법] predict(DataFrame): 학습된 모델을 사용하여 새로운 독립변수에 대한 종속변수 예측값 계산
print('예측값 : ', lm.predict(x_new).values) 
print('직접 계산 : \n', lm.params.tv * x_new + lm.params.Intercept)
print('\n')

# 경험하지 않은 tv 광고비에 따른 상품 판매량 예측
my_new = pd.DataFrame({'tv':[100, 350, 780]})
print('예측 상품 판매량 : ', lm.predict(my_new).values)
print('\n')

# 시각화
plt.scatter(advdf['tv'], advdf['sales'])
plt.grid(True)
plt.xlabel('tv광고비')
plt.ylabel('상품 판매량')
ypred = lm.predict(advdf[['tv']])
plt.plot(advdf['tv'], ypred, c='r') # [개념] 회귀분석을 통해 도출된 최적의 추세선
plt.title('단순 선형 회귀')
plt.show()

print('--------------------------------')
# 단순 선형 회귀모델이므로 적절성 선행조건 중 잔차의 정규성, 선형성 확인

# 잔차(Residual)
# [개념] 실제 값과 모델이 예측한 값의 차이 (e = y - y_hat)
fitted = lm.predict(advdf)      # lm.predict(advdf.tv)
print('실제값 : \n', advdf['sales'][:5].values)
print('예측값 : \n', fitted[:5].values)
residual = advdf['sales'] - fitted # [추천] lm.resid 속성을 사용하면 잔차를 바로 얻을 수 있음.
print('잔차 : \n', residual[:5].values)
print('잔차 평균값 : \n', np.mean(residual[:5]))
print('\n')

# 잔차의 정규성 : 잔차가 정규성을 따르는지 확인
from scipy.stats import shapiro
stat, p = shapiro(residual)
# [개념] Shapiro-Wilk 검정: p-value > 0.05이면 정규 분포를 따른다는 귀무가설을 채택함.
print(f'통계량 : {stat}, p-value : {p}')
# 통계량 : 0.9905306561484953, p-value : 0.21332551436720226
print('정규성 만족' if p > 0.05 else '정규성 불만족')
print('\n')

# Q-Q plot으로 시각화
import statsmodels.api as sm
sm.qqplot(residual, line='s') # [개념] 점들이 직선상에 위치할수록 잔차가 정규성을 만족함.
plt.title('Q-Q plot으로 정규성 만족 확인')
plt.show()

# 잔차의 선형성 검정
# : 독립변수의 변화에 종속변수도 변화하나, 특정한 패턴이 있으면 안됨
# : 독립변수와 종속변수 간에 선형형태로 적절하게 모델링 되었는지 확인
from statsmodels.stats.diagnostic import linear_reset       # 선형성 확인 모듈
# [개념] Ramsey's RESET test: 모델의 선형 결합이 적절한지 검정. p-value > 0.05이면 선형성 만족.
reset_result = linear_reset(lm, power=2, use_f=True)
print('reset_result : \n', reset_result.pvalue)
print('선형성 만족' if reset_result.pvalue > 0.05 else '선형성 위배')
print('\n')

# 시각화
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color':'red'}) # [개념] 잔차가 0을 중심으로 무작위하게 분포해야 함.
plt.title('잔차의 선형성 검정')
plt.plot([fitted.min(), fitted.max()], [0,0], '--', color='gray')
plt.show()

# 잔차의 등분산성 검정

# 등분성 검정 : 모든 x 값에서 오차의 퍼짐이 유사해야 한다 
from statsmodels.stats.diagnostic import het_breuschpagan
# [개념] Breusch-Pagan test: 잔차의 분산이 일정한지 검정. p-value > 0.05이면 등분산성 만족.
bp_test = het_breuschpagan(residual, sm.add_constant(advdf['tv']))
print('bp_test : \n', bp_test)
print('등분산성 만족' if bp_test[1] > 0.05 else '등분상성 위배')
print('\n')

# 참고
# Cook's distance 
# [개념] 특정 데이터가 회귀모델에 얼마나 영향을 주는지 확인
# [개념] 영향력 있는 관측치(이상치)를 탐지하는 진단 방법
# [개념] 데이터가 적을 때, 이상치가 의심스러울 때, 모델 결과가 이상하게 나올 때 사용
from statsmodels.stats.outliers_influence import OLSInfluence
cd, _ = OLSInfluence(lm).cooks_distance     # 쿡 거리, 인덱스 반환

# 쿡 거리가 가장 큰 5개 확인
print(cd.sort_values(ascending=False).head())
# 35     0.060494
# 178    0.056347
# 25     0.038873
# 175    0.037181
# 131    0.033895

# 쿡 거리가 가장 큰 -> 영향력이 가장 큰 관측지 원본 확인
print(advdf.iloc[[35, 178, 25, 175, 131]])
#         tv  radio  newspaper  sales
# 35   290.7    4.1        8.5   12.8
# 178  276.7    2.3       23.7   11.8
# 25   262.9    3.5       19.5   12.0
# 175  276.9   48.9       41.8   27.0
# 131  265.2    2.9       43.0   12.7

# 대부분 tv 광고비는 매우 높으나, sales가 낮음 
# - 모델이 예측하기 어려운 포인트들

# 시각화
# [문법] influence_plot: 레버리지(Leverage)와 잔차를 시각화하여 영향력 있는 관측치를 식별함.
fig = sm.graphics.influence_plot(lm, alpha=0.05, criterion='cooks') 
plt.tight_layout()
plt.show()
print('\n')

print('--------------------------------')
# 다중 선형 회귀 모델 - OLS 사용
# x : tv, radio, newspaper / y : sales

lm_mul = smf.ols(formula='sales ~ tv + radio + newspaper', data=advdf).fit()
print(lm_mul.summary())
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                  sales   R-squared:                       0.897
# Model:                            OLS   Adj. R-squared:                  0.896
# Method:                 Least Squares   F-statistic:                     570.3
# Date:                Mon, 06 Apr 2026   Prob (F-statistic):           1.58e-96
# Time:                        11:55:46   Log-Likelihood:                -386.18
# No. Observations:                 200   AIC:                             780.4
# Df Residuals:                     196   BIC:                             793.6
# Df Model:                           3
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      2.9389      0.312      9.422      0.000       2.324       3.554
# tv             0.0458      0.001     32.809      0.000       0.043       0.049
# radio          0.1885      0.009     21.893      0.000       0.172       0.206
# newspaper     -0.0010      0.006     -0.177      0.860      -0.013       0.011
# ==============================================================================
# Omnibus:                       60.414   Durbin-Watson:                   2.084
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):              151.241
# Skew:                          -1.327   Prob(JB):                     1.44e-33
# Kurtosis:                       6.332   Cond. No.                         454.
# ==============================================================================
# [개념] newspaper의 p-value(0.860)가 0.05보다 크므로 sales에 미치는 영향이 유의하지 않음.
# [추천] 유의하지 않은 변수인 newspaper를 제거하고 모델을 재학습하여 성능(Adj. R-squared)을 비교해 볼 것.