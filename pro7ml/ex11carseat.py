# 다중 선형 회귀 분석 및 모델 적합성 진단 실습
# [개념] 여러 독립변수가 종속변수(Sales)에 미치는 영향을 분석하고, 회귀 분석의 5대 기본 가정(정규성, 선형성, 등분산성, 독립성, 다중공선성)을 검증함.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf
from sympy import Q

# [문법] pd.read_csv(): 카시트 판매량 데이터를 DataFrame으로 로드
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Carseats.csv')
print(df.head()) # [문법] 상위 5개 행 출력
print(df.info()) # [문법] 컬럼 타입 및 결측치 확인
print('\n')

# [문법] drop(columns, axis=1): 수치형 데이터 분석을 위해 범주형 컬럼(ShelveLoc, Urban, US) 제거
df = df.drop(df.columns[[6,9,10]], axis=1)
print(df.head())
print(df.info())
print(df.corr()) # [문법] 변수 간 피어슨 상관계수 행렬 계산
#                 Sales  
# Sales        1.000000   
# CompPrice    0.064079   
# Income       0.151951  
# Advertising  0.269507  
# Population   0.050471  
# Price       -0.444951   
# Age         -0.231815  
# Education   -0.051955   
# [개념] 상관계수가 매우 낮은 CompPrice, Population, Education은 모델의 단순화를 위해 제외함.
print('\n')

# [문법] smf.ols(formula, data).fit(): 최소제곱법을 이용한 다중 선형 회귀 모델 생성 및 학습
lm = smf.ols(formula='Sales ~ Income + Advertising + Price + Age', data=df).fit()
print(lm.summary()) # [개념] R-squared(0.371), F-통계량 유의확률(1.33e-38), 각 변수의 p-value 확인
# [추천] 모델의 설명력(Adj. R-squared)을 높이기 위해 유의미한 상호작용 항을 추가해 볼 수 있음.
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                  Sales   R-squared:                       0.371
# Model:                            OLS   Adj. R-squared:                  0.364
# Method:                 Least Squares   F-statistic:                     58.21
# Date:                Mon, 06 Apr 2026   Prob (F-statistic):           1.33e-38
# Time:                        12:10:15   Log-Likelihood:                -889.67
# No. Observations:                 400   AIC:                             1789.
# Df Residuals:                     395   BIC:                             1809.
# Df Model:                           4
# Covariance Type:            nonrobust
# ===============================================================================
#                   coef    std err          t      P>|t|      [0.025      0.975]
# -------------------------------------------------------------------------------
# Intercept      15.1829      0.777     19.542      0.000      13.656      16.710
# Income          0.0108      0.004      2.664      0.008       0.003       0.019
# Advertising     0.1203      0.017      7.078      0.000       0.087       0.154
# Price          -0.0573      0.005    -11.932      0.000      -0.067      -0.048
# Age            -0.0486      0.007     -6.956      0.000      -0.062      -0.035
# ==============================================================================
# Omnibus:                        3.285   Durbin-Watson:                   1.931
# Prob(Omnibus):                  0.194   Jarque-Bera (JB):                3.336
# Skew:                           0.218   Prob(JB):                        0.189
# Kurtosis:                       2.903   Cond. No.                     1.01e+03
# ==============================================================================
print('\n')

# <선형 회귀모델의 적절성 조건 체크 후 모델 사용>

# 잔차항 구하기
df_lm = df[['Sales', 'Income', 'Advertising', 'Price', 'Age']]
# df_lm = df.iloc[:,[0,2,3,5,6]]
print(df_lm.head())
print('\n')
# [문법] predict(): 학습 데이터에 대한 예측값 계산
fitted = lm.predict(df_lm) 
# [개념] 잔차(Residual): 실제값과 모델 예측값의 차이 (e = y - y_hat)
residual = df_lm['Sales'] - fitted 
print(residual.head())
print('잔차의 평균 : ', np.mean(residual))    # [개념] OLS 모델의 잔차 평균은 이론적으로 0에 수렴함.
print('\n') 

# 1. 잔차의 정규성 : 잔차가 정규성을 따르는지 확인
from scipy.stats import shapiro
import statsmodels.api as sm
stat, p = shapiro(residual)
print(f'통계량 : {stat:.5f}, p-value : {p:.5f}')
print('정규성 만족' if p > 0.05 else '정규성 불만족')
# [개념] Shapiro-Wilk 검정: p-value > 0.05이면 잔차가 정규 분포를 따른다는 귀무가설을 채택함.
print('\n')

# Q-Q plot으로 시각화
sm.qqplot(residual, line='s') # [문법] 점들이 직선(s)에 가까울수록 정규성을 만족함.
plt.title('Q-Q plot으로 정규성 만족 확인')
plt.show()

# 정규성 만족 완료

# 2. 잔차의 선형성 검정
from statsmodels.stats.diagnostic import linear_reset       # 선형성 확인 모듈
# [개념] Ramsey's RESET test: 모델에 비선형 항이 필요한지 검정. p-value > 0.05이면 선형 모델이 적절함.
reset_result = linear_reset(lm, power=2, use_f=True)
print('reset_result : \n', reset_result.pvalue)
print('선형성 만족' if reset_result.pvalue > 0.05 else '선형성 위배')
print('\n')

# 시각화
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color':'red'}) # [문법] lowess=True: 국소 회귀선을 그려 잔차의 패턴 확인
plt.title('잔차의 선형성 검정')
plt.plot([fitted.min(), fitted.max()], [0,0], '--', color='gray')
plt.show()

# 3. 잔차의 등분산성 검정
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residual, sm.add_constant(df_lm['Sales']))
# [개념] Breusch-Pagan test: 잔차의 분산이 독립변수와 무관하게 일정한지 검정. p-value > 0.05이면 등분산성 만족.
bp_stat, bp_pvalue = bp_test[0], bp_test[1]
print(f'breuschpagan 통계량 : {bp_stat:.5f}, p-value : {bp_pvalue:.5f}')
print('등분산성 만족' if bp_pvalue > 0.05 else '등분산성 위배')
print('\n')

# 시각화
fig = sm.graphics.influence_plot(lm, alpha=0.05, criterion='cooks') # [문법] 레버리지와 잔차를 통해 영향력 있는 이상치 탐색
plt.tight_layout()
plt.show()
print('\n')

# 4. 독립성 검정
# : 다중회귀 분석 시 독립변수의 값이 서로 관련되지 않아야 한다
# : 잔차가 자기상관(인접 관측치의 오차가 상관됨)이 있는지 확인

# Durbin-Watson
# : 잔차의 자기상관(autocorrelation) 검정 지표. 
# : 잔차들이 서로 독립적인가? 시간 흐름 데이터에서 중요 (시계열)
# : 값의 범위는 0 ~ 4 이고   
# : 2이면 정상 (자기상관 없음)
# : < 2이면 양의 자기상관
# : > 2이면 음의 자기상관
# : model.summary()로 확인 가능
import statsmodels.stats.api as sm
# [문법] durbin_watson(): 인접한 오차항 간의 상관관계를 측정함.
print('Durbin-Watson : ', sm.stattools.durbin_watson(residual))
# Durbin-Watson :  1.9314981270829592       ==> 독립성 만족(자기상관이 없다)
print('\n')

# 5. 잔차의 다중공선성 검정
# : 독립변수 간에 강한 상관관계가 있어서는 안된다
# VIF (Variance Inflation Factor) : 분산 인플레이션 요인, 분산 팽창 지수
#                                 : 값이 10을 넘으면 다중 공선성이 발생하는 변수라고 할 수 있다
from statsmodels.stats.outliers_influence import variance_inflation_factor
# [개념] 다중공선성: 독립변수들끼리 강한 상관관계를 가져 회귀 계수 추정의 신뢰도가 떨어지는 현상.
df_ind = df[['Income', 'Advertising', 'Price', 'Age']]  # 독립변수들
vifdf = pd.DataFrame()
vifdf['변수'] = df_ind.columns
vifdf['vif_value'] = [variance_inflation_factor(df_ind.values, i) for i in range(df_ind.shape[1])] # [문법] 리스트 컴프리헨션으로 각 변수의 VIF 계산
print(vifdf)
#    vif_value
# 0   5.971040
# 1   1.993726
# 2   9.979281
# 3   8.267760
# ㄴ--> 10을 초과하지 않았으므로 모두 만족
print('\n')

# 시각화
sns.barplot(x='변수', y='vif_value', data=vifdf) # [문법] VIF 수치를 막대 그래프로 시각화
plt.axhline(y=10, color='red', linestyle='--', linewidth=2, label='Threshold (10)')
plt.title('VIF')
plt.show()


# 유의한 모델이므로 생성된 모델을 파일로 저장하고 이를 재사용
# 방법 1)
# import pickle
# with open('carseat.pickle', 'wb') as obj:   # 저장
#     pickle.dump(lm, obj)

# with open('carseat.pickle', 'rb') as obj:   # 불러오기
#     mymodel = pickle.load(obj)

# 방법 2) - pickle은 binary로 i/o 해야 하므로, 번거롭다
import joblib
# [문법] joblib.dump(model, filename): 학습된 모델 객체를 파일로 저장
joblib.dump(lm, 'carseat.joblib') 
# 이후 부터는 아래 처럼 읽어 사용하면 됨
mymodel = joblib.load('carseat.joblib') # [문법] 저장된 모델 파일을 로드하여 객체 복원

# 새로운 값으로 Sales 예측
new_df = pd.DataFrame({'Income':[35, 62], 'Advertising':[6, 3], 'Price':[105, 88], 'Age':[32, 55]})
# [문법] predict(DataFrame): 새로운 독립변수 조합에 대한 종속변수(Sales) 예측값 도출
pred = mymodel.predict(new_df) 
print('Sales 예측값 : \n', pred.values)