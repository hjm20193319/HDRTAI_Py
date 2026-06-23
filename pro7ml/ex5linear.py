# 전통적 방법의 선형회귀( 기계학습 중 지도학습 )
# [개념] 각 데이터에 대한 잔차 제곱합(RSS)이 최소가 되는 추세선(회귀선)을 만들고
# [개념] 이를 통해 독립변수가 종속변수에 얼마나 영향을 주는지 인과관계를 분석

# [조건] 독립변수 : 연속형 / 종속변수 : 연속형
# [조건] 두 변수는 상관관계 및 인과관계가 있어야 한다
# [목적] 정량적인 모델을 생성
# [추천] 분석 전 산점도(Scatter plot)를 통해 선형성 여부를 먼저 확인하는 것이 좋음

import statsmodels.api as sm
from sklearn.datasets import make_regression
import numpy as np

# 데이터 생성
np.random.seed(12)

# 모델 맛보기
####################################################
# 방법 1) : make_regression 사용, model 생성 X (가상 데이터 생성용)
# [문법] n_samples: 표본 수, n_features: 독립변수 개수, bias: 절편, coef: 기울기 반환 여부
x, y, coef = make_regression(n_samples=50, n_features=1, bias=100, coef=True)
print(x)    # -1.70073563 -0.67794537 0.31866529...
print('\n')
print(y)    # -52.17214291   39.34130801  128.51235594...
print('\n')
print('생성된 기울기:', coef) # 89.47430
# 회귀식 완성
# y^ = wx + b -> y^ = 89.47430 * x + 100 
print('\n')

y_pred = 89.47430 * -1.70073563 + 100
print('예측값 : ', y_pred)  # -52.172129979309005
print('\n')

###################################################
# 방법 2) : LinearRegresion 사용, model 생성 O
from sklearn.linear_model import LinearRegression

xx = x
yy = y

# [문법] LinearRegression(): 사이킷런의 선형 회귀 모델 객체 생성
model = LinearRegression()
# [문법] fit(X, y): 모델 학습. X는 반드시 2차원 배열(Matrix) 형태여야 함.
fit_model = model.fit(xx, yy)   # 최소제곱법(OLS)으로 기울기, 절편을 반환
print('기울기(slope) : ', fit_model.coef_)
print('절편(bias) : ', fit_model.intercept_)
# 기울기 :  [89.47430739]
# 절편 :  100.0
print('\n')

# [문법] predict(X): 학습된 모델로 새로운 데이터에 대한 예측값 산출. 입력은 2차원 배열 형태.
y_newpred = fit_model.predict(xx[[0]])    
print('예측값 : ', y_newpred)
y_newpred2 = fit_model.predict([[0.12345]])    # 입력값 : 2차원 배열, 출력값 : 1차원 -> 차원에 맞는 배열로 넣어줘야한다
# y_newpred2 = fit_model.predict(np.array([[0.12345]]))
print('예측값2 : ', y_newpred2)
y_newpred3 = fit_model.predict([[0.12345], [0.53456], [0.34567]])    # 예측값2 :  [111.04560325]
print('예측값(복수개) : ', y_newpred3)
# 예측값(복수개) :  [111.04560325 147.82938576 130.92858384]
print('\n')

#################################################
# 방법 3) : ols 사용, model 생성 O , 보고서를 작성하기에 좋은 정보 제공
# 잔차제곱합(RSS)을 최소화 하는 가중치 벡터를 행렬 미분으로 구하는 방법

import statsmodels.formula.api as smf

print(xx.ndim)  # 2차원
x1 = xx.flatten()   # 차원 축소 (ols는 1차원을 써야함)
# xx.ravel() 도 가능(속도 더 빠름)
# 차원 확대는 expenddim()
print(x1.ndim)  # 1차원
y1 = yy
print('\n')

import pandas as pd  
data = np.array([x1, y1])
df = pd.DataFrame(data.T)
df.columns = ['x1', 'y1']
print(df.head())
print('\n')

model2 = smf.ols(formula='y1 ~ x1', data=df)
fit_model2 = model2.fit()
print(fit_model2.summary())
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                     y1   R-squared:                       1.000
# Model:                            OLS   Adj. R-squared:                  1.000
# Method:                 Least Squares   F-statistic:                 1.905e+32
# Date:                Fri, 03 Apr 2026   Prob (F-statistic):               0.00
# Time:                        11:01:28   Log-Likelihood:                 1460.6
# No. Observations:                  50   AIC:                            -2917.
# Df Residuals:                      48   BIC:                            -2913.
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    100.0000   7.33e-15   1.36e+16      0.000     100.000     100.000
# x1            89.4743   6.48e-15   1.38e+16      0.000      89.474      89.474
# ==============================================================================
# Omnibus:                        7.616   Durbin-Watson:                   1.798
# Prob(Omnibus):                  0.022   Jarque-Bera (JB):                8.746
# Skew:                           0.516   Prob(JB):                       0.0126
# Kurtosis:                       4.770   Cond. No.                         1.26
# ==============================================================================

# [개념] 독립변수의 p-value 가 유의수준(alpha) 0.05보다 '작으면' 통계적으로 유의미한 인과관계가 있다고 판단함.
# [개념] R-squared(결정계수): 모델의 설명력을 의미함 (1에 가까울수록 데이터에 잘 부합함).
# [개념] 인과관계가 없는(p > 0.05) 독립변수는 모델에서 '제외'하는 것이 일반적임.

print(fit_model2.params['x1'])  # 89.47430739278903 : 기울기
print(fit_model2.params['Intercept'])  # 99.99999999999999 : 절편
print('\n')

# [문법] predict(DataFrame): statsmodels의 predict는 학습 시 사용한 변수명과 동일한 컬럼을 가진 DataFrame을 입력으로 받음.
new_df = pd.DataFrame({'x1':[-1.70073563, -0.67794537]})    # 기존 자료 검증
print('예측값 : \n', fit_model2.predict(new_df))
# 0   -52.172143
# 1    39.341308
new_df2 = pd.DataFrame({'x1':[0.1234, 0.2346]})  # 새로운 자료 검증
print('예측값2 : \n', fit_model2.predict(new_df2))
# 0    111.041130
# 1    120.990673
print('\n')