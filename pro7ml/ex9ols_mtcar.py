# [개념] 선형 회귀분석 : mtcars dataset을 활용하여 자동차의 제원(마력, 무게 등)과 연비(mpg) 간의 인과관계를 분석함.
# [개념] 단순 선형 회귀와 다중 선형 회귀 모델을 생성하고 성능(결정계수)을 비교함.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api

# [문법] statsmodels.api.datasets.get_rdataset('mtcars').data: R에서 제공하는 기본 데이터셋인 mtcars를 로드함.
mtcars = statsmodels.api.datasets.get_rdataset('mtcars').data
print(mtcars.head())
print(mtcars.columns) # [문법] 컬럼명 확인
# ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb']
print(mtcars.info()) # [문법] 데이터 타입 및 결측치 확인
print('\n')

# x : hp (마력수), y : mpg(연비)
print(mtcars.corr()) # [문법] 전체 변수 간 상관계수 행렬 출력
print(np.corrcoef(mtcars.hp, mtcars.mpg))   # -0.77616837 [개념] 마력과 연비는 강한 음의 상관관계
print(np.corrcoef(mtcars.wt, mtcars.mpg))   # -0.86765938 [개념] 무게와 연비는 매우 강한 음의 상관관계
print('\n')
# [추천] sns.heatmap(mtcars.corr(), annot=True)를 통해 상관관계를 시각화하면 변수 선택에 도움이 됨.

# 시각화
# plt.scatter(mtcars.hp, mtcars.mpg)
# plt.grid(True)
# plt.xlabel('hp')
# plt.ylabel('mpg')
# plt.show()

##################################################
# 단순 선형회귀
# [문법] smf.ols(formula='종속변수 ~ 독립변수', data=df).fit(): 최소제곱법을 이용한 모델 학습
result = smf.ols(formula='mpg ~ hp', data=mtcars).fit()
print(result.summary()) # [개념] R-squared: 0.602 (약 60% 설명력), Prob (F-statistic): 1.79e-07 (유의함)
print('\n')
# y^ = -0.0682 * x + 30.0989 + (error)
print('마력수 110에 대한 연비 예측값 : \n', -0.0682 * 110 + 30.0989)    # 22.5969
# [문법] predict(pd.DataFrame): 새로운 데이터에 대한 예측 수행. 컬럼명이 학습 시와 동일해야 함.
print('마력수 110에 대한 연비 예측값 : \n', result.predict(pd.DataFrame({'hp':[110]}))) # 22.59375 
# ㄴ> 차이 나는 이유는 수동 계산 시 반올림된 계수를 사용했기 때문 (모델은 더 정밀한 값을 가짐)
print('\n')

######################################################
# 다중선형회귀
# [개념] 두 개 이상의 독립변수(hp, wt)를 사용하여 종속변수(mpg)를 예측함.
result2 = smf.ols(formula='mpg ~ hp + wt', data=mtcars).fit()
print(result2.summary())
# [개념] Adj. R-squared: 0.815 (단순 회귀보다 설명력이 향상됨), Prob (F-statistic): 9.11e-12 (매우 유의함)
print('\n')
print('마력수 110 + 무게 5에 대한 연비 예측값 : \n', (-0.0318 * 110) + (-3.8778 * 5) + 37.2273) # 14.3403
print('마력수 110 + 무게 5에 대한 연비 예측값 : \n', result2.predict(pd.DataFrame({'hp':[110], 'wt':[5]})).values) # 14.34309224
print('\n')
# [추천] result2.params를 통해 각 독립변수의 회귀계수를 확인할 수 있음.

######################################################
# 추정치 구하기 - 차체 무게를 입력해 연비 추정
result3 = smf.ols(formula='mpg ~ wt', data=mtcars).fit()
print(result3.summary())
print('결정계수 : ', result3.rsquared)  # 0.7528327936582646 [개념] 무게 하나만으로도 연비의 약 75%를 설명함.
print('\n')
pred = result3.predict() # [문법] 인자 없이 호출 시 학습 데이터에 대한 예측값(y_hat) 반환
print('result3 연비 예측값 : ', pred[:5])
print('\n')

# 새로운 차체 무게로 연비 추정
# [문법] input()으로 받은 문자열을 float으로 형변환하여 예측용 데이터 생성
user_wt = float(input('차체 무게를 입력하시오 : '))
new_data = pd.DataFrame({'wt': [user_wt]})
new_pred = result3.predict(new_data)
print(f'차체무게 {user_wt}일 때 예상 연비는 {new_pred[0]}')

# [추천] plt.plot(mtcars.wt, result3.predict(), color='red')를 통해 회귀선을 시각화할 수 있음.