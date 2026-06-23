# 단순선형회귀 : ols의 Regression Results의 이해
# [개념] statsmodels의 ols(Ordinary Least Squares)는 최소제곱법을 사용하여 선형 회귀 모델을 생성하고 상세한 통계 보고서를 제공함.
 
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np


df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv')
print(df.head()) # [문법] 데이터프레임의 상위 5개 행을 출력하여 데이터 구조 확인
print(df.corr()) # [문법] 변수 간의 피어슨 상관계수 행렬을 계산함.
print('\n')
# 만족도 ~ 적절성의 상관계수가 제일 높으므로 변수 설정

# [문법] smf.ols(formula='종속변수 ~ 독립변수', data=데이터프레임): R 스타일의 포뮬러를 사용하여 모델 정의
model = smf.ols(formula='만족도 ~ 적절성', data=df)
# [문법] fit(): 정의된 모델을 데이터를 바탕으로 학습시켜 회귀 계수를 추정함.
fit_model = model.fit() 
print(fit_model.summary()) # [개념] 모델의 결정계수(R-squared), F-통계량, 회귀계수, p-value 등 상세 통계 정보를 출력함.
print('\n')

print('parameters : \n', fit_model.params) # [문법] 추정된 회귀 계수(절편과 기울기)를 반환함.
print('R-squared : ', fit_model.rsquared)   # 0.5880630629464404 [개념] 모델이 종속변수의 변동을 약 58.8% 설명함.
print('p-value : ', fit_model.pvalues)  # [개념] 각 독립변수의 유의성을 검정함. 0.05보다 작으면 통계적으로 유의함.
print('예측값 : \n', fit_model.predict()[:5]) # [문법] 학습 데이터에 대한 예측값(y_hat)을 반환함.
print('실제값 : \n', df['만족도'][:5].values)
print('\n')

# [개념] 주요 통계 지표 해석:
# 1. R-squared (결정계수): 1에 가까울수록 모델의 설명력이 높음.
# 2. Adj. R-squared (수정된 결정계수): 독립변수의 개수를 고려하여 보정된 결정계수.
# 3. Prob (F-statistic): 모델 전체의 유의성. 0.05보다 작으면 모델이 유의미함.
# 4. P>|t| (p-value): 각 독립변수가 종속변수에 미치는 영향의 유의성.

# 시각화(추세선)
# [문법] np.polyfit(x, y, deg): 데이터를 다항식에 적합시킴. deg=1은 1차 선형 회귀를 의미함.
slope, intercept = np.polyfit(df['적절성'], df['만족도'], 1)

# [추천] plt.style.use('ggplot') # 그래프의 시각적 품질을 높이기 위해 스타일 설정 권장

# [문법] plt.plot(x, y): 선 그래프를 그림. 여기서는 회귀식(y = ax + b)을 이용해 추세선을 그림.
plt.plot(df['적절성'], slope * df['적절성'] + intercept, c='blue', label='회귀선')

# [문법] plt.scatter(x, y): 산점도를 그림. 실제 데이터의 분포를 확인하는 용도.
plt.scatter(df['적절성'], df['만족도'])
plt.grid(True)
plt.xlabel('적절성')
plt.ylabel('만족도')
plt.title('적절성에 따른 만족도 회귀 분석')
plt.legend()
plt.show()

# [추천] seaborn의 regplot을 사용하면 산점도와 회귀선을 동시에 쉽게 그릴 수 있음.
# import seaborn as sns
# sns.regplot(x='적절성', y='만족도', data=df)
# plt.show()

# 새로운 데이터 예측 예시
# [문법] predict(pd.DataFrame): 새로운 독립변수 값을 DataFrame 형태로 전달하여 예측값을 얻음.
# new_data = pd.DataFrame({'적절성': [3.5, 4.2]})
# print('새로운 데이터 예측값:\n', fit_model.predict(new_data))

# [개념] 잔차(Residual) 분석: 실제값과 예측값의 차이를 분석하여 모델의 가정을 검토함.
# residuals = fit_model.resid
```