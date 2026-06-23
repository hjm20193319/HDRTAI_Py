# [개념] RandomForestRegressor (랜덤 포레스트 회귀)
# [개념] 여러 개의 결정 트리(Decision Tree)를 생성하고, 각 트리의 예측값을 평균내어 최종 결과를 도출하는 앙상블(Bagging) 학습 기법입니다.
# [개념] RandomForest는 분류(Classifier)와 회귀(Regressor) 모두 적용 가능하며, 사이킷런(scikit-learn)의 대부분 알고리즘이 이와 같은 유연성을 가집니다.

# [추천] 회귀 모델 평가 시 MSE 외에도 MAE(Mean Absolute Error)를 함께 확인하여 오차의 실제 규모를 파악하는 것이 좋습니다.
# [추천] 트리 기반 모델은 특성 스케일링(Scaling)에 민감하지 않으나, 이상치(Outlier)가 많은 경우 데이터 정제 후 학습시키는 것을 권장합니다.

import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 데이터
housing = fetch_california_housing(as_frame=True) # [문법] fetch_california_housing: 사이킷런에서 제공하는 캘리포니아 주택 가격 데이터셋 로드.
print(housing.DESCR) # [문법] DESCR: 데이터셋에 대한 상세 설명(변수 정보, 샘플 수 등) 출력.
# :Number of Instances: 20640
# :Attribute Information:
#     - MedInc        median income in block group
#     - HouseAge      median house age in block group
#     - AveRooms      average number of rooms per household
#     - AveBedrms     average number of bedrooms per household
#     - Population    block group population
#     - AveOccup      average number of household members
#     - Latitude      block group latitude
#     - Longitude     block group longitude
print('\n')

print(housing.data[:2])
print(housing.target[:2])
print('\n')
print(housing.feature_names[:2])
print('\n')
df = housing.frame # [문법] frame: Bunch 객체에서 독립변수와 종속변수가 합쳐진 pandas DataFrame 추출.
print(df.head())
print('\n')

x = df.drop('MedHouseVal', axis=1) # [문법] drop(): 종속변수 'MedHouseVal'을 제외하여 독립변수(Feature) 생성.
y = df['MedHouseVal'] # [개념] 종속변수(Target): 주택 가격의 중앙값 (연속형 수치).

# 데이터 분리
# [문법] train_test_split: 데이터를 학습용(70%)과 테스트용(30%)으로 분리함.
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3, random_state=42) 
print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)

# 모델
# [문법] RandomForestRegressor: n_estimators(결정트리 개수)를 200으로 설정하여 회귀 모델 생성.
rfmodel = RandomForestRegressor(n_estimators=200, random_state=42) 
rfmodel.fit(train_x, train_y) # [문법] fit(): 학습 데이터를 사용하여 모델 학습 수행.

# 예측
# [문법] predict(): 테스트 데이터에 대한 주택 가격 예측.
pred = rfmodel.predict(test_x) 
print(f'MSE : {mean_squared_error(test_y, pred):.3f}') # [문법] mean_squared_error: 평균 제곱 오차(낮을수록 우수).
print(f'R2 : {r2_score(test_y, pred):.3f}') # [문법] r2_score: 결정 계수(1에 가까울수록 모델의 설명력이 높음).
# MSE : 0.254
# R2 : 0.807
print('\n')

# [문법] feature_importances_: 각 특성이 예측에 기여한 정도(불순도 감소량)를 수치로 표현.
importances = rfmodel.feature_importances_ 
indices = np.argsort(importances)[::-1] # [문법] argsort(): 중요도가 높은 순서대로 인덱스 정렬.

# 시각화
plt.figure(figsize=(10, 5))
plt.bar(range(x.shape[1]), importances[indices], align='center')
plt.xticks(range(x.shape[1]), x.columns[indices])
plt.xlabel('변수')
plt.ylabel('중요도')
plt.title('변수 중요도')
plt.tight_layout()
plt.show()
print('\n')

# 중요 변수 순위 정보 저장
ranking = pd.DataFrame({
    '변수': x.columns[indices],
    '중요도': importances[indices]
})
print(ranking)
print('\n')

# 파라미터 튜닝
# [개념] RandomizedSearchCV: GridSearchCV와 달리 사용자가 지정한 범위 내에서 임의의 조합을 샘플링하여 탐색함.
# [개념] 모든 조합을 시도하지 않으므로 속도가 빠르며, 연속적인 값의 범위 탐색에 유리함(단, 최적 조합을 놓칠 가능성 있음).

param_dist = {
    'n_estimators': [200, 400, 800], # [개념] 생성할 결정 트리의 개수.
    'max_depth': [None, 10, 20, 30], # [개념] 트리의 최대 깊이 제한.
    'min_samples_leaf': [1, 2, 4],  # [개념] 리프 노드가 되기 위해 필요한 최소 샘플 수.
    'min_samples_split': [2, 5, 10],  # [개념] 노드를 분할하기 위한 최소 샘플 수.
    'max_features': [None, 'sqrt', 'log2', 1.0, 0.8, 0.6]   # [개념] 분할 시 고려할 최대 특성(Feature) 수.
}

# [문법] RandomizedSearchCV: 교차 검증을 통해 랜덤하게 하이퍼파라미터 조합을 탐색함.
from sklearn.model_selection import RandomizedSearchCV
search = RandomizedSearchCV( 
    RandomForestRegressor(random_state=42),
    param_distributions=param_dist,
    n_iter=20,  # [개념] 탐색 횟수: 20개의 랜덤한 파라미터 조합을 시도함.
    cv=3,       # [개념] 3-Fold 교차 검증 수행.
    scoring='r2', # [개념] 평가 지표로 결정 계수(R2) 사용.
    verbose=1,  # [문법] verbose: 실행 과정 로그 출력 레벨 설정.
    n_jobs=-1,  # [문법] n_jobs=-1: 가용한 모든 CPU 코어를 사용하여 병렬 처리.
    random_state=42
)
search.fit(train_x, train_y)    # [문법] fit(): 전처리 및 최적 파라미터 탐색 학습 수행.

print('best params : ', search.best_params_) # [문법] best_params_: 탐색된 최적의 파라미터 조합 출력.
best = search.best_estimator_ # [문법] best_estimator_: 최적의 파라미터로 학습이 완료된 모델 객체 반환.
print('best score : ', search.best_score_) # [문법] best_score_: 최적 파라미터에서의 평균 검증 점수.
print('\n')

pred = best.predict(test_x) # [문법] 최적 모델을 사용한 테스트 데이터 예측.
print(f'Best MSE : {mean_squared_error(test_y, pred):.3f}')
print(f'Final R2 : {r2_score(test_y, pred):.3f}')