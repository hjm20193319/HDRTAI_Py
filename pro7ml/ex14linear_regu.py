# Linear Regression의 기본 알고리즘에 오버피팅 방지 목적의 제약조건을 담은 Ridge, Lasso, ElasticNet 회귀모형이 있다.
# 과적합 모델에 규제를 줄 수 있다
# [개념] 규제(Regularization)는 모델의 복잡도를 줄여 일반화 성능을 높이고 과적합(Overfitting)을 방지하는 기법임.

# L1 규제(Regulation), L2 규제(Regulation) ...

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error

# [문법] load_iris(): 사이킷런에서 제공하는 붓꽃 데이터셋을 로드함.
iris = load_iris() 
print(iris)
print(iris.keys())
# dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename'])

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df["target"] = iris.target
iris_df["target_names"] = iris.target_names[iris.target]
print(iris_df[:3])

# train dataset, test dataset으로 나누기
# [문법] train_test_split: 데이터를 학습용과 검증용으로 분리함. random_state는 결과 재현성을 위해 사용.
from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(iris_df, test_size = 0.3,random_state=12)

# 회귀분석 방법 1 - LinearRegression
from sklearn.linear_model import LinearRegression
print(train_set.iloc[:, [2]])  # petal length (cm), 독립변수
print(train_set.iloc[:, [3]])  # petal width (cm), 종속변수

# 학습은 train dataset 으로 작업 
# [문법] LinearRegression().fit(X, y): 최소제곱법을 사용하여 선형 회귀 모델을 학습시킴.
model_linear = LinearRegression().fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])
print('slope : ', model_linear.coef_)  # 0.42259168 [개념] 회귀 계수(기울기)
print('bias : ', model_linear.intercept_)  # -0.39917733 [개념] 편향(절편)

# [문법] predict(X): 학습된 모델을 사용하여 새로운 데이터에 대한 예측값을 반환함.
# 모델 평가는 test dataset 으로 작업
pred = model_linear.predict(test_set.iloc[:, [2]])
print('예측값 : ', np.round(pred[:5].flatten(),1))
print('실제값 : ', test_set.iloc[:, [3]][:5].values.flatten())

from sklearn.metrics import r2_score
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred)))  # 0.93833

# [추천] sns.regplot을 사용하면 산점도와 회귀선을 더 간편하게 시각화할 수 있음.
plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='red')
plt.plot(np.array(test_set.iloc[:, [2]]), model_linear.predict(test_set.iloc[:, [2]]))
plt.show()

print('\nRidge -----------')
# 회귀분석 방법 - Ridge: alpha값을 조정(가중치 제곱합을 최소화)하여 과대/과소적합을 피한다. 다중공선성 문제 처리에 효과적.
# [개념] L2 규제를 사용하며, 가중치들의 제곱합을 최소화하여 계수의 크기를 제한함.
from sklearn.linear_model import Ridge 
model_ridge = Ridge(alpha=10).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_ridge.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]]))  # 0.91880
print(model_ridge.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))    # 0.94101
pred_ridge = model_ridge.predict(test_set.iloc[:, [2]])
print('ridge predict : ', pred_ridge[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_ridge)))  # 0.9410

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='blue')
plt.plot(np.array(test_set.iloc[:, [2]]), model_ridge.predict(test_set.iloc[:, [2]]))
plt.show()

print('\nLasso -----------')
# 회귀분석 방법 - Lasso: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
# [개념] L1 규제를 사용하며, 가중치 절대값의 합을 최소화함. 중요한 변수만 남기고 나머지는 0으로 만드는 특징이 있음.
from sklearn.linear_model import Lasso 
model_lasso = Lasso(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_lasso.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
print(model_lasso.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
pred_lasso = model_lasso.predict(test_set.iloc[:, [2]])
print('lasso predict : ', pred_lasso[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_lasso)))

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='green')
plt.plot(np.array(test_set.iloc[:, [2]]), model_lasso.predict(test_set.iloc[:, [2]]))
plt.show()

# 회귀분석 방법 4 - Elastic Net 회귀모형 : Ridge + Lasso의 형태로 가중치 절대값의 합(L1)과 제곱합(L2)을 동시에 제약 조건으로 가지는 모형
print('\nElasticNet -----------')
# 회귀분석 방법 - ElasticNet: alpha값을 조정(가중치 절대값의 합을 최소화)하여 과대/과소적합을 피한다.
# [개념] Ridge와 Lasso의 장점을 결합한 모델로, 상관관계가 높은 변수가 많을 때 유리함.
from sklearn.linear_model import ElasticNet 
model_elastic = ElasticNet(alpha=0.1).fit(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])

#점수
print(model_elastic.score(X=train_set.iloc[:, [2]], y=train_set.iloc[:, [3]])) # 0.913863
print(model_elastic.score(X=test_set.iloc[:, [2]], y=test_set.iloc[:, [3]]))   # 0.940663
pred_elastic = model_elastic.predict(test_set.iloc[:, [2]])
print('ElasticNet predict : ', pred_elastic[:5])
print('r2_score(결정계수):{}'.format(r2_score(test_set.iloc[:, [3]], pred_elastic)))

plt.scatter(train_set.iloc[:, [2]], train_set.iloc[:, [3]],  color='cyan')
plt.plot(np.array(test_set.iloc[:, [2]]), model_elastic.predict(test_set.iloc[:, [2]]))
plt.show() 
# [추천] 하이퍼파라미터 alpha 최적화를 위해 GridSearchCV를 활용해 볼 수 있음.