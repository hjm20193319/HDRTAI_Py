# 단순선형회귀 - iris dataset
# 상관관계가 약한 경우와 강한 경우로 회귀분석모델을 생성 후 비교
# [개념] 독립변수와 종속변수 간의 상관계수가 높을수록 회귀 모델의 설명력(R-squared)이 높아지는 경향이 있음.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf

# [문법] sns.load_dataset('iris'): seaborn에서 제공하는 붓꽃 데이터셋을 DataFrame으로 로드함.
iris = sns.load_dataset('iris')
print(iris.head()) # [문법] 데이터의 상위 5개 행 확인
print(iris.info()) # [문법] 데이터 타입 및 결측치 존재 여부 확인
print('\n')
print(iris.iloc[:,0:4].corr()) # [문법] 수치형 변수들 간의 피어슨 상관계수 행렬 계산
#               sepal_length  sepal_width  petal_length  petal_width
# sepal_length      1.000000    -0.117570      0.871754     0.817941
# sepal_width      -0.117570     1.000000     -0.428440    -0.366126
# petal_length      0.871754    -0.428440      1.000000     0.962865
# petal_width       0.817941    -0.366126      0.962865     1.000000
print('\n')
# [추천] sns.pairplot(iris, hue='species')를 사용하면 변수 간 관계를 한눈에 시각화할 수 있음.

###########################################################################
# 연습 1 : 상관관계가 약한 변수를 사용 -0.117570
# [문법] smf.ols(formula='y ~ x', data=df).fit(): 최소제곱법을 이용한 선형 회귀 모델 생성 및 학습
result1 = smf.ols(formula='sepal_length ~ sepal_width', data=iris).fit()
print(result1.summary()) # [개념] 모델의 통계적 유의성(F-통계량), 설명력(R-squared), 계수(coef) 등을 포함한 요약 보고서 출력
print('\n')
print('R-squared : ', result1.rsquared) # 0.0138 [개념] 모델의 설명력이 매우 낮음 (약 1.3%)
print('p-value : \n', result1.pvalues.iloc[1])  # 0.15 > 0.05 : [개념] 유의수준 0.05보다 크므로 독립변수가 종속변수에 미치는 영향이 유의하지 않음.
print('\n')

# 시각화
plt.scatter(iris['sepal_width'], iris['sepal_length'])
plt.grid(True)
plt.xlabel('sepal_width') # [문법] x축 이름 설정
plt.ylabel('sepal_length')
plt.plot(iris['sepal_width'], result1.predict(), c='r')
plt.show()

print('---------------------------------------------------------')

##############################################################################
# 연습 2 : 상관관계가 강한 변수를 사용  0.871754
result2 = smf.ols(formula='sepal_length ~ petal_length', data=iris).fit()
print(result2.summary())
print('R-squared : ', result2.rsquared) # 0.7599 [개념] 모델이 데이터의 변동을 약 76% 설명함.
print('p-value : \n', result2.pvalues.iloc[1])  # 1.0386674194497976e-47 < 0.05 : [개념] 통계적으로 매우 유의한 모델임.
print('\n')

# 시각화
plt.scatter(iris['petal_length'], iris['sepal_length'])
plt.grid(True)
plt.xlabel('petal_length')
plt.ylabel('sepal_length')
plt.plot(iris['petal_length'], result2.predict(), c='r') # [문법] predict(): 학습 데이터에 대한 예측값(y_hat)을 반환하여 회귀선 시각화
plt.show()

# 새로운 값으로 예측
print('실제값 : ', iris.sepal_length[:10].values)
print('예측값 : ', result2.predict()[:10]) # [개념] 실제값과 예측값의 차이를 잔차(Residual)라고 함.
# 실제값 :  [5.1,       4.9,       4.7,        4.6,         5,          5.4,         4.6,           5,            4.4,       4.9]
# 예측값 :  [4.8790946  4.8790946  4.83820238  4.91998683   4.8790946   5.00177129   4.8790946      4.91998683    4.8790946  4.91998683]
print('\n')

# 새로운 값으로 예측 : 꽃잎의 길이로 꽃받침의 길이를 예측하는 것
# [문법] predict(pd.DataFrame): 새로운 독립변수 데이터를 DataFrame 형태로 전달하여 예측 수행
new_data = pd.DataFrame({'petal_length':[1.1, 0.5, 6.0]})
y_pred = result2.predict(new_data)
print('예측값 : \n', y_pred.values)
# 예측값 : [4.75641792 4.51106455 6.76013708]
print('\n')
print('-----------------------------------------------------')
# [추천] result2.params를 통해 회귀계수(기울기, 절편)를 직접 확인하여 회귀식을 도출할 수 있음.

#######################################################################
# 연습 3 : 독립변수를 복수로 사용 - 다중 선형 회귀
# [개념] 다중 선형 회귀는 여러 개의 독립변수를 사용하여 종속변수의 변화를 설명함.
# result3 = smf.ols(formula='sepal_length ~ petal_length + petal_width', data=iris).fit()
column_select = "+".join(iris.columns.difference(['sepal_length','sepal_width','species'])) # [문법] 특정 컬럼을 제외한 나머지 컬럼명들을 '+'로 연결함.
print(column_select)
result3 = smf.ols(formula='sepal_length ~ ' + column_select, data=iris).fit()
print(result3.summary())
# Prob (F-statistic):           4.00e-47 < 0.05 : [개념] 모델 전체가 통계적으로 유의함.
# Adj. R-squared:                  0.763 [개념] 수정된 결정계수. 변수의 개수가 늘어남에 따른 과적합을 보정한 지표.
print('\n')