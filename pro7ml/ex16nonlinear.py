# 비선형 회귀 분석 예제
# 70년대 미국 보스턴 시의 주택가격을 설명한 dataset
'''
회귀분석의 한 예로 scikit-learn 패키지에서 제공하는 주택가격을 예측하는 Dataset을 사용할 수 있다. 
이는 범죄율, 공기 오염도 등의 주거 환경 정보 등을 사용하여 70년대 미국 보스턴 시의 주택가격을 표시하고 있다.

* 데이터 세트 특성 :
    : 인스턴스 수 : 506
    : 속성의 수 : 13 개의 숫자 / 범주 적 예측
    : 중간 값 (속성 14)은 대개 대상입니다
    : 속성 정보 (순서대로) :
CRIM   자치시(town) 별 1인당 범죄율
ZN 25,000   평방피트를 초과하는 거주지역의 비율
INDUS   비소매상업지역이 점유하고 있는 토지의 비율
CHAS   찰스강에 대한 더미변수(강의 경계에 위치한 경우는 1, 아니면 0)
NOX   10ppm 당 농축 일산화질소
RM   주택 1가구당 평균 방의 개수
AGE   1940년 이전에 건축된 소유주택의 비율
DIS   5개의 보스턴 직업센터까지의 접근성 지수
RAD   방사형 도로까지의 접근성 지수
TAX   10,000 달러 당 재산세율
PTRATIO   자치시(town)별 학생/교사 비율
B   1000(Bk-0.63)^2, 여기서 Bk는 자치시별 흑인의 비율을 말함.
LSTAT   모집단의 하위계층의 비율(%)
MEDV   본인 소유의 주택가격(중앙값) (단위: $1,000)

['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT','MEDV']
'''

from cProfile import label
from turtle import color

from cv2 import line
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# [문법] pd.read_csv(sep=r'\s+'): 공백(space)이 하나 이상인 정규표현식을 구분자로 사용하여 데이터 로드
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/housing.data', header=None, sep=r'\s+')
df.columns = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT','MEDV']
# [문법] set_option('display.max_columns', None): 모든 컬럼이 생략 없이 출력되도록 설정
pd.set_option('display.max_columns', None)
print(df.head())
# [문법] corr(): 변수 간 피어슨 상관계수 행렬 계산
print(df.corr()) # LSTAT(하층비율) ~ MEDV(집값) : -0.737663
#             CRIM        ZN     INDUS      CHAS       NOX        RM       AGE         DIS       RAD       TAX   PTRATIO         B     LSTAT      MEDV
# LSTAT    0.455621 -0.412995  0.603800 -0.053929  0.590879 -0.613808  0.602339   -0.496996  0.488676  0.543993  0.374044 -0.366087  1.000000 -0.737663
# MEDV    -0.388305  0.360445 -0.483725  0.175260 -0.427321  0.695360 -0.376955   0.249929 -0.381626 -0.468536 -0.507787  0.333461 -0.737663  1.000000
print('\n')

x = df[['LSTAT']].values
y = df['MEDV'].values
print(x[:3])
print(y[:3])
print('\n')

# 단항을 통한 선형 모델
# [개념] 독립변수와 종속변수 간의 직선적인 관계를 가정하는 기초적인 회귀 모델
model = LinearRegression()
model.fit(x, y)

# 다항 특성
# [문법] PolynomialFeatures(degree=n): 주어진 데이터를 n차 다항식 형태로 변환 (x -> x, x^2, ...)
quad = PolynomialFeatures(degree=2, include_bias=False)
x_quad = quad.fit_transform(x) # [문법] fit_transform: 데이터를 학습하고 2차항이 포함된 행렬로 변환

cubic = PolynomialFeatures(degree=3, include_bias=False)
x_cubic = cubic.fit_transform(x) # [문법] 3차항까지 포함된 행렬로 변환
print(x[:3])
print(x_quad[:3])
print(x_cubic[:3])
# [[4.98]
#  [9.14]
#  [4.03]]
# [[ 4.98   24.8004]
#  [ 9.14   83.5396]
#  [ 4.03   16.2409]]
# [[  4.98      24.8004   123.505992]
#  [  9.14      83.5396   763.551944]
#  [  4.03      16.2409    65.450827]]
print('\n')

# 단순 회귀
# [문법] np.arange(min, max, step): 최소값부터 최대값까지 일정 간격의 배열 생성
x_fit = np.arange(x.min(), x.max(), 1)[:, np.newaxis]
y_lin_fit = model.predict(x_fit)    # 그래프 표시용
print('x_fit : \n', x_fit[:3])
print('y_lin_fit : \n',y_lin_fit[:3])
# [개념] r2_score: 결정계수. 1에 가까울수록 모델의 설명력이 높음을 의미함.
model_r2 = r2_score(y, model.predict(x)) 
print('model_r2 : ', model_r2)
# model_r2 :  0.544146
print('\n')

# 2차 
model.fit(x_quad, y)
y_quad_fit = model.predict(quad.fit_transform(x_fit))
quad_r2 = r2_score(y, model.predict(x_quad))
print('quad_r2 : ', quad_r2)
# quad_r2 :  0.640716897163661
print('\n')

# 3차
model.fit(x_cubic, y)
y_cubic_fit = model.predict(cubic.fit_transform(x_fit))
cubic_r2 = r2_score(y, model.predict(x_cubic))
print('cubic_r2 : ', cubic_r2)
# cubic_r2 :  0.6578476405895719

# 시각화
# [문법] plt.scatter: 실제 데이터의 분포를 산점도로 표현
plt.scatter(x, y, label='초기 데이터', color='lightgray', edgecolors='black')
plt.plot(x_fit, y_lin_fit, linestyle=':', label='선형 회귀(d=1), $R^2$=%.2f'%model_r2, c='b', lw=3)
plt.plot(x_fit, y_quad_fit, linestyle='-', label='2차 다항 회귀(d=2), $R^2$=%.2f'%quad_r2, c='r', lw=3)
plt.plot(x_fit, y_cubic_fit, linestyle='--', label='3차 다항 회귀(d=3), $R^2$=%.2f'%cubic_r2, c='g', lw=3)
plt.legend(loc='upper right') # [문법] 범례 표시
plt.xlabel('하위계층 비율')
plt.ylabel('주택 가격')
plt.show()
# [추천] 차수가 너무 높으면 과적합(Overfitting)이 발생할 수 있으므로 검증 데이터셋을 통한 성능 평가가 권장됨.