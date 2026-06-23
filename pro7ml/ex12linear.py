# LinearRegression 클래스 사용
# : 평가 score 정리 
# [개념] Scikit-learn의 LinearRegression은 통계적 보고서(summary)보다는 예측 성능과 머신러닝 파이프라인 적합성에 초점을 맞춘 클래스임.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.linear_model import LinearRegression       # summary() 지원 안함
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
# [문법] sklearn.preprocessing.MinMaxScaler: 데이터를 0과 1 사이의 범위로 스케일링하여 모델의 수렴 속도와 성능을 향상시킴.
from sklearn.preprocessing import MinMaxScaler
from sympy import Q      # 정규화 클래스

# 데이터 생성
sample_size = 100
np.random.seed(1)

# [문법] np.random.normal(loc, scale, size): 평균(loc), 표준편차(scale)를 따르는 정규분포 난수 생성
x = np.random.normal(0, 10, sample_size)
y = np.random.normal(0, 10, sample_size) + x * 30
print(x[:5])
print(y[:5])
print('상관계수 : ', np.corrcoef(x, y)[0, 1]) # [개념] 두 변수 간의 선형적 관계 강도 측정
# 상관계수 :  0.9993935724865679
print('\n')

# [개념] 정규화(Normalization): 서로 다른 스케일을 가진 독립변수들의 단위를 통일시켜 모델 학습의 왜곡을 방지함.
# 독립변수 x를 정규화 하기(0 ~ 1 범위 내 자료로 변환)
scaler = MinMaxScaler()     # 정규화 수식을 지원
x_scaled = scaler.fit_transform(x.reshape(-1, 1))
print(x[:5])
print(x_scaled[:5].T)
print('\n')

# 시각화
# plt.scatter(x_scaled, y)
# plt.show()

# 모델 생성
# [문법] LinearRegression().fit(X, y): 최소제곱법을 사용하여 회귀 계수(w)와 절편(b)을 학습함.
model = LinearRegression()
model.fit(x_scaled, y)
print('model : ', model)
print('회귀계수 slope : ', model.coef_) # [개념] 독립변수 1단위 증가 시 종속변수의 변화량
print('회귀계수 intercept : ', model.intercept_) # [개념] 모든 독립변수가 0일 때의 종속변수 값
print('결정계수(설명력) R^2 : ', model.score(x_scaled, y)) # [문법] score(): 학습된 모델의 결정계수를 반환함.

y_pred = model.predict(x_scaled) # [문법] predict(): 학습된 파라미터를 사용하여 새로운 데이터에 대한 예측값 산출
print('예측값 : ', y_pred[:5])
print('\n')

# 모델 성능 확인 함수 작성
def myRegScoreFunc(y_true, y_pred):
    print('-----모델 성능 확인-----')

    # 결정계수(설명력) : 실제 관측값의 분산대비 예측값의 분산을 계산하여 데이터 예측의 정확도 성능 측정 지표
    # [개념] 1에 가까울수록 모델이 데이터를 완벽하게 설명함을 의미함.
    print(f'r2_score(결정계수) : {r2_score(y_true, y_pred)}')

    # 모델이 데이터의 분산을 얼마나 잘 설명하는지 나타내는 지표 (오차 분산이 작으면 점수 높음)
    print(f'explained_variance_score(설명분산 점수) : {explained_variance_score(y_true, y_pred)}')

    # 오차를 제곱해서 평균 구함(오차가 커질수록 손실 함수 값이 빠르게 증가, 값이 작을수록 모델 성능 우수)
    print(f'mean_squared_error(MSE, 평균제곱 오차) : {mean_squared_error(y_true, y_pred)}') # [개념] 이상치에 민감한 지표
    imsi = mean_squared_error(y_true, y_pred) # [추천] root_mean_squared_error(y_true, y_pred) 함수를 직접 사용할 수도 있음.
    print(f'root_mean_squared_error(RMSE, 평균제곱근 오차) : {np.sqrt(imsi)}')   # 9.28159 (평균적으로 +- 9 정도의 오차)
    print('\n')


myRegScoreFunc(y, y_pred)   # 실제값, 예측값

# 분산이 크게 다른 x, y 값을 사용
x2 = np.random.normal(0, 1, sample_size)
y2 = np.random.normal(0, 100, sample_size) + x2 * 30
print(x2[:5])
print(y2[:5])
print('상관계수 : ', np.corrcoef(x2, y2)[0, 1])     # 0.2249953961923308
print('\n')

# [개념] 상관계수가 낮은 데이터로 학습할 경우 결정계수(R^2)가 낮게 나타나며 모델의 신뢰도가 떨어짐.
x_scaled2 = scaler.fit_transform(x2.reshape(-1, 1))
model2 = LinearRegression()
model2.fit(x_scaled2, y2)
print('model2 : ', model2)
print('회귀계수 slope : ', model2.coef_)
print('회귀계수 intercept : ', model2.intercept_)
print('결정계수(설명력) R^2 : ', model2.score(x_scaled2, y2))
# [추천] 모델의 성능이 낮을 경우 다항 회귀(Polynomial Regression)나 다른 독립변수 추가를 고려해 볼 것.