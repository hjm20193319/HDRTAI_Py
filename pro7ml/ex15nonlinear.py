# 비선형회귀분석(Non-linear regression)
# [개념] 비선형회귀란 직선의 회귀선을 곡선으로 변환해 보다 더 정확하게 데이터 변화를 예측하는 데 목적이 있다.
# [개념] 선형 가정이 어긋날 때(비정규성, 비선형성) 대처할 수 있는 방법으로, 다항식 항을 추가한 다항 회귀(Polynomial Regression) 모델을 사용함.

# 입력 데이터 특징 변환으로 선형 모델을 개선

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score

x = np.array([1,2,3,4,5])
y = np.array([4,2,1,3,7])

plt.scatter(x, y)
plt.title('데이터')
plt.show()
print('상관계수 : ', np.corrcoef(x, y)[0,1]) # [문법] np.corrcoef: 두 변수 간의 피어슨 상관계수 행렬 반환
# 0.48076

# 선형회귀모델을 적용
from sklearn.linear_model import LinearRegression

# [문법] np.newaxis: 1차원 배열을 2차원 배열(Matrix) 형태로 변환 (사이킷런 모델 입력 조건)
x = x[:, np.newaxis]    
model = LinearRegression()
# [문법] fit(X, y): 최소제곱법을 사용하여 선형 모델 학습
model.fit(x, y) 
ypred = model.predict(x) # [문법] predict(X): 학습된 모델로 예측값 산출
print('예측값 : ', ypred)
# 예측값 :  [2.  2.7 3.4 4.1 4.8]
print('결정계수 : ', r2_score(y, ypred)) # [개념] r2_score: 모델의 설명력(1에 가까울수록 우수)

# 시각화
plt.scatter(x, y)
plt.plot(x, ypred, 'r')
plt.title('선형회귀모델')
plt.show()

# 비선형회귀모델 작성
# 여러 방법 중 가장 일반적인 방법을 사용(PolynomialFeatures, Log 변환, Curve_fit ...)
# [문법] PolynomialFeatures: 주어진 차수(degree)에 따라 독립변수의 다항식 특징을 생성함.
from sklearn.preprocessing import PolynomialFeatures    

# [문법] degree=2: x^2 항을 추가, include_bias=False: 상수항(1)을 생성하지 않음.
poly = PolynomialFeatures(degree=2, include_bias=False)     
x2 = poly.fit_transform(x)  # [문법] fit_transform: 데이터를 학습하고 다항식 특징 행렬로 변환
print(x)    # (5, 1)
print(x2)   # [개념] 기존의 x 에 x²항의 열이 추가 됨
print(x2.shape) # (5, 2)
print('\n')

model2 = LinearRegression()
model2.fit(x2, y)   # [개념] 변환된 다항 특징 행렬을 사용하여 선형 회귀 모델 학습(결과적으로 곡선 형태)
ypred2 = model2.predict(x2)
print('예측값 : ', ypred2)
# 예측값 :  [4.14285714 1.62857143 1.25714286 3.02857143 6.94285714]
print('결정계수 : ', r2_score(y, ypred2))
# 결정계수 :  0.9892183288409704
# [개념] 차수가 높아질수록 결정계수는 올라가나 과적합(Overfitting)의 위험이 있음.
print('\n')

# 시각화
plt.scatter(x, y)
plt.plot(x, ypred2, 'r')
plt.title('비선형회귀모델')
plt.show()
# [추천] 더 복잡한 비선형 관계는 scipy.optimize.curve_fit을 사용하여 사용자 정의 함수로 피팅할 수 있음.