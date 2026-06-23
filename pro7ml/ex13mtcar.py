# LinearRegression 클래스 사용 : 평가 score - mtcars dataset 사용
# [개념] Scikit-learn의 LinearRegression을 활용하여 자동차의 마력(hp)이 연비(mpg)에 미치는 영향을 분석하고 모델의 성능을 평가함.

from sklearn.linear_model import LinearRegression
import statsmodels.api
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score, mean_squared_error
from sympy import Line

# [문법] statsmodels.api.datasets.get_rdataset('mtcars').data: R의 기본 데이터셋인 mtcars를 로드함.
mtcars = statsmodels.api.datasets.get_rdataset('mtcars')
mtcars = mtcars.data
print(mtcars.head()) # [문법] 데이터프레임 상위 5개 행 출력
print(mtcars.info()) # [문법] 컬럼 타입 및 결측치 여부 확인
print('\n')

# [문법] corr(method='pearson'): 변수 간 피어슨 상관계수 행렬 계산 (선형적 관계 측정)
print('상관계수 : \n', mtcars.corr(method='pearson')) 
print('\n')

# hp가 mpg에 영향을 주는 인과관계
# [개념] 독립변수(x)는 2차원 배열 형태여야 하므로 대괄호를 두 번 사용하거나 reshape(-1, 1)을 적용함.
x = mtcars[['hp']].values 
y = mtcars['mpg'].values 
print(x[:5])
print(y[:5])
print('\n')

# 모델 생성
# [문법] LinearRegression().fit(X, y): 최소제곱법을 사용하여 회귀 계수와 절편을 학습함.
lmodel = LinearRegression()
lmodel.fit(x, y)
print('회귀 계수 slope : ', lmodel.coef_) # [개념] 마력이 1단위 증가할 때 연비의 변화량
print('회귀 계수 intercept : ', lmodel.intercept_) # [개념] 마력이 0일 때의 추정 연비
print('결정계수(설명력) R^2 : ', lmodel.score(x, y)) # [문법] score(): 학습된 모델의 결정계수를 반환함.
# 회귀 계수 slope :  [-0.06822828]
# 회귀 계수 intercept :  30.098860539622496
# 결정계수(설명력) R^2 :  0.602437341423934
print('\n')

# 시각화
plt.scatter(x, y) # [문법] 실제 데이터 분포를 산점도로 표현
plt.plot(x, lmodel.coef_ * x + lmodel.intercept_, color='red') # [개념] 회귀분석으로 도출된 최적의 추세선
plt.title('마력(hp)에 따른 연비(mpg) 회귀선')
plt.show()

# mpg 예측
# [문법] predict(X): 학습된 파라미터를 사용하여 입력 데이터에 대한 예측값 산출
pred = lmodel.predict(x) 
print('예측값 : ', np.round(pred[:5], 1))
print('실제값 : ', y[:5])
# 예측값 :  [22.6 22.6 23.8 22.6 18.2]
# 실제값 :  [21.  21.  22.8 21.4 18.7]
print('\n')

# 모델 성능 지표
# MSE : 모델 내부 비교용 - 계산 편리(단위가 제곱한 값)
# RMSE : 보고/해석용 - 해석 용이(단위가 원래 단위와 동일)
# 회귀 평가 지표는 고정된 점수 범위가 없다(데이터 스케일에 따라 다름)
#       ㄴ-> 그래서 모델끼리 상대적인 비교를 한다

# [문법] mean_squared_error(y_true, y_pred): 실제값과 예측값 차이의 제곱 평균 계산
print('MSE : ', mean_squared_error(y, pred)) 
print('RMSE : ', np.sqrt(mean_squared_error(y, pred))) # [추천] root_mean_squared_error 함수를 직접 사용할 수도 있음.
print('r2_score : ', r2_score(y, pred)) # [개념] 1에 가까울수록 모델이 데이터를 완벽하게 설명함을 의미함.
# MSE :  13.989822298268805
# RMSE :  3.7402970868994894
# r2_score :  0.602437341423934
# [개념] r2_score 하나만 보고 모델을 판단 X, 설명력만 봄 -> 이상치에 민감, 변수가 많으면 증가하는 경향이 있음.
# 모델 성능은 r2_score와 MSE 또는 r2_score와 RMSE를 사용하도록 한다
print('\n')

########################################
# 새로운 hp로 mpg 예측
new_hp = [[100], [110], [120], [130]]
new_pred = lmodel.predict(new_hp)
print('예측 결과', np.round(new_pred.flatten(), 2)) # [문법] flatten(): 2차원 예측 결과를 1차원으로 변환하여 출력
# [추천] 다중 선형 회귀(wt 등 추가)를 통해 모델의 설명력(R^2)을 높여볼 수 있음.