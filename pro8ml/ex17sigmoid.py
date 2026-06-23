# Sigmoid function 적용 연습
# [개념] 로지스틱 회귀에서 선형 결합 wx + b는 로짓(Logit) 값을 의미함.
# [개념] 로짓 수식: log(p / (1 - p)) = wx + b
# [개념] Z = wx + b를 시그모이드 함수에 대입하면 0~1 사이의 확률값(p)을 얻게 됨.

# 시그모이드 함수 수식으로 반환된 값 확인
from cProfile import label
from calendar import c
import math
from turtle import color

# [문법] math.exp(x): e(자연상수)의 x거듭제곱을 계산함.
def sigmoidFunc(num):
    return 1 / (1 + math.exp(-num))

# [개념] 입력값이 클수록 1에 수렴하고, 작을수록 0에 수렴함.
print(sigmoidFunc(3))   # 0.9525741268224334 (약 95% 확률)
print(sigmoidFunc(1))   # 0.7310585786300049 (약 73% 확률)
print(sigmoidFunc(0))   # 0.5
print(sigmoidFunc(-1))  # 0.2689414213699951
print(sigmoidFunc(-5))  # 0.0066928509242848554
print(sigmoidFunc(-10)) # 4.5397868702434395e-05
print('\n')

print('-----------------')
# 로짓 변환된(가정) 값으로 시그모이드 함수 통과 후, 그 결과를 시각화
from matplotlib.lines import lineStyles
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
# [추천] 시각화의 가독성을 높이기 위해 plt.style.use('ggplot') 사용을 권장함.

# [문법] np.linspace(start, stop, num): 지정된 범위 내에서 균일한 간격의 숫자들을 생성함.
x = np.linspace(-10, 10, 50)    # 입력 자료 : 연속형 독립변수
print(x)
print('\n')

# 선형 결합(이미 logit 된 값으로 가정)
w = 1.5
b = -2
z = w * x + b # [개념] 결정 경계(Decision Boundary)를 형성하는 선형 방정식

# [문법] np.exp(): 배열 연산을 지원하는 지수 함수. 시그모이드 함수를 벡터화하여 계산함.
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

p = sigmoid(z)      # [개념] 0.0 ~ 1.0 사이의 확률값 얻음
print('p : \n', p)
# 이후에 if 문으로 0.5를 기준으로 분류하면 됨(이항 분류)
print('\n')

# 일부값 보기
print('x[:3] : ', np.round(x[:3], 2))
print('z[:3] : ', np.round(z[:3], 2))
print('p[:3] : ', p[:3])
# x[:3] :  [-10.         -9.59            -9.18]    # data
# z[:3] :  [-17.          -16.39          -15.78]   # logit
# p[:3] :  [4.1399e-08   7.6369e-08    1.408e-07]   # sigmoid
print('\n')
# [추천] 분류 임계값(Threshold)을 0.5가 아닌 비즈니스 목적에 따라 조정하여 정밀도나 재현율을 최적화할 수 있음.

# 시각화
plt.figure(figsize=(8, 5))
plt.plot(x, p, label='sigmoid(z)', color='blue', linewidth=2) # [문법] 시그모이드 곡선(S-curve) 출력
plt.axhline(0.5, color='red', linestyle='--') # [문법] 확률 0.5 지점에 기준선 표시
plt.title('z = wx + b --> sigmoid ==> 확률')
plt.xlabel('x(입력값)')
plt.ylabel('p(확률값)')
plt.legend()
plt.grid(True)
plt.show()