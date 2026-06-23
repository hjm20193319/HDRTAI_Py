# 공분산 / 상관 계수
# [개념] 변수가 하나인 경우에는 분산은 데이터가 평균으로부터 떨어진 거리(퍼짐 정도)와 관련이 있다.
# [개념] 변수가 두 개인 경우에는 공분산(Covariance)을 통해 두 변수 간의 관계 방향을 알 수 있다.

import numpy as np

# 공분산
print(np.cov(np.arange(1, 6), np.arange(2, 7))) # [결과] 양의 공분산: 우상향 (두 변수가 같은 방향으로 변화)
print(np.cov(np.arange(1, 6), (3, 3, 3, 3, 3))) # [결과] 0: 직선(수평선) (한쪽 변수의 변화가 없음)
print(np.cov(np.arange(1, 6), np.arange(6, 1, -1))) # [결과] 음의 공분산: 우하향 (두 변수가 반대 방향으로 변화)
print('\n')

# 우상향 데이터 - 스케일 차이 비교
# [개념] 공분산은 측정 단위(Scale)에 민감하여 값의 크기만으로 상관 정도를 파악하기 어렵다.
print(np.cov(np.arange(10, 60, 10), np.arange(20, 70, 10)))
print(np.cov(np.arange(100, 600, 100), np.arange(200, 700, 100)))
print('\n')

######################################################################
x = [8,3,6,6,9,4,3,9,3,4]
print('x의 평균 : ', np.mean(x)) # [문법] np.mean(): 산술 평균 계산
print('x의 분산 : ', np.var(x))  # [문법] np.var(): 표본 분산(n으로 나눔) 계산. np.cov는 n-1로 나눔에 유의.
y = [6,2,4,6,9,5,1,8,4,5]
print('y의 평균 : ', np.mean(y))
print('y의 분산 : ', np.var(y))
print('\n')

# 시각화
import matplotlib.pyplot as plt
# [추천] plt.style.use('ggplot') # 그래프의 가독성을 높여주는 스타일 적용
# plt.plot(x, y, 'o')
# plt.show()
# 우상향하는 그래프 확인

# x, y 공분산
print('x, y의 공분산 : ', np.cov(x, y))
print('x, y의 공분산 : ', np.cov(x, y)[0, 1])   # 5.222222222222222
# [문법] np.cov()는 공분산 행렬(Covariance Matrix)을 반환함. [0,1] 또는 [1,0]이 두 변수 간의 공분산.

x2 = [80,30,60,60,90,40,30,90,30,40]
y2 = [6,2,4,6,9,5,1,8,4,5]
print('x2, y2의 공분산 : ', np.cov(x2, y2)[0, 1])   # 52.22222222222222
# plt.plot(x2, y2, 'o')
# plt.show()
print('\n')

# 두 데이터의 스케일에 따라 패턴이 일치해도, 공분산의 크기가 달라진다
# => 절대적 크기 판단이 어려움
# ==>> 공분산을 각 변수의 표준편차의 곱으로 나누어 표준화 : (-1 ~ 1) 범위로 만든 것이 상관계수(r)
# 피어슨 상관계수
print('x, y의 상관계수 : ', np.corrcoef(x, y)[0, 1])    # 0.8663686463212855
print('x2, y2의 상관계수 : ', np.corrcoef(x2, y2)[0, 1])    # 0.8663686463212853
print('\n')

# scipy 모듈 사용
from scipy import stats
print('scipy 모듈 사용 : ', stats.pearsonr(x, y)) 
# [개념] stats.pearsonr은 (상관계수, p-value)를 반환함. p-value가 0.05보다 작으면 통계적으로 유의미한 상관관계임.
print('\n')

# [개념] 비선형 데이터인 경우 공분산, 상관계수 의미 없음 (0에 가깝게 나옴)
m = [-3, -2, -1, 0, 1, 2, 3]
n = [9, 4, 1, 0, 1, 4, 9]
print('m, n의 공분산 : ', np.cov(m, n)[0, 1])
print('m, n의 상관계수 : ', np.corrcoef(m, n)[0, 1])
# m, n의 공분산 :  0.0
# m, n의 상관계수 :  0.0
# plt.plot(m, n, 'o')
# plt.show()
# U 자형 그래프 개형 확인
# [추천] 비선형 관계를 파악하려면 산점도를 먼저 확인하거나 스피어먼 상관계수 등을 고려해 볼 수 있음.