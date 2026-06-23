# 최소제곱 해를 선형 행렬 방정식으로 얻기
# [개념] 최소제곱법(Ordinary Least Squares, OLS)은 잔차 제곱합을 최소화하는 가중치 벡터를 구하는 방법임.

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

x = np.array([0, 1, 2, 3])
y = np.array([-1, 0.2, 0.5, 2.1])

# [추천] plt.style.use('ggplot') # 그래프의 시각적 품질을 높이기 위해 스타일 설정 권장
# plt.scatter(x, y)
# plt.grid(True)
# plt.show()

# [문법] np.vstack: 배열을 수직으로 쌓음. 독립변수 x와 상수항(1)을 결합하여 디자인 행렬 A를 생성.
# [문법] .T: 행렬의 전치(Transpose)를 수행하여 (n, 2) 형태로 변환.
A = np.vstack([x, np.ones(len(x))]).T
print(A)

# 본래 데이터를 직선으로 표현하기 위해 선형대수학 이용
import numpy.linalg as lin

# y^ = wx + b 의 w(기울기), b(절편)값 구하기
# [문법] lin.lstsq(a, b): 선형 최소제곱 문제를 해결함. 반환값의 첫 번째 요소[0]가 해(기울기와 절편)임.
weight, bias = lin.lstsq(A, y, rcond=None)[0]   # 최소제곱법 연산(내부적으로 편미분 사용)
print(weight, ' ', bias)
# 0.96   -0.9899999999999998
print('\n')

# 회귀식 y^ = 0.96 * x + -0.9899999
# [개념] 결정된 가중치(weight)와 편향(bias)을 사용하여 입력값에 대한 예측값(y_hat)을 산출함.
print(0.96 * 0 + -0.9899999999999998)   # -0.9899999999999998
print(0.96 * 1 + -0.9899999999999998)   # -0.029999999999999805
print(0.96 * 2 + -0.9899999999999998)   # 0.9300000000000002
print(0.96 * 3 + -0.9899999999999998)   # 1.8900000000000001

plt.scatter(x, y, marker='o', label='실제값')
plt.plot(x, weight * x + bias, 'r', label='최적화된 선형직선')  # [개념] 회귀분석을 통해 도출된 최적의 추세선(모델)
plt.grid(True)
plt.show()

# 경험하지 않은 x 값에 대한 Y값은?
x = 1.23456
yhat = weight * x + bias # [개념] 학습된 모델의 파라미터를 사용하여 새로운 데이터에 대한 추론(Inference) 수행
print('예측결과 : ', yhat)  # 예측결과 :  0.19517760000000028

x = 7.654321
yhat = weight * x + bias
print('예측결과 : ', yhat)  # 예측결과 :  6.358148160000001