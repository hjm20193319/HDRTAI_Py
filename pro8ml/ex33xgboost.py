# [개념] XGBoost (eXtreme Gradient Boosting): 트리 기반의 앙상블 학습 알고리즘으로, 병렬 처리와 규제(Regularization)를 통해 속도와 성능을 모두 잡은 모델입니다.
# [개념] Santander Customer Satisfaction: 고객의 금융 데이터를 바탕으로 만족(0)과 불만족(1)을 예측하는 이진 분류 문제.
# [추천] 클래스 불균형이 심한 데이터셋이므로 Accuracy보다는 ROC-AUC 점수를 주요 평가지표로 활용하는 것이 적절합니다.
# [추천] 피처가 매우 많으므로(371개) PCA를 통한 차원 축소나 Feature Selection을 고려해볼 수 있습니다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from xgboost import XGBClassifier # [문법] XGBoost의 분류 모델 클래스
from sklearn.metrics import accuracy_score, roc_auc_score # [문법] 성능 평가 지표 함수
from sklearn.model_selection import GridSearchCV, train_test_split # [문법] 하이퍼파라미터 튜닝 및 데이터 분리 도구
from xgboost import plot_importance # [문법] 피처 중요도를 시각화하는 함수
from sklearn import metrics
# pd.set_option('display.max_columns', None)

# 데이터
df = pd.read_csv('train_san.csv', encoding='latin-1') # [문법] pd.read_csv: CSV 파일을 데이터프레임으로 로드.
# print(df.head(2))
print(df.shape)
# (76020, 371)
print(df.info()) # [문법] 데이터프레임의 요약 정보(결측치, 데이터 타입 등) 확인
print('\n')
# dtypes: float64(111), int64(260)

# 전체 데이터에서 만족과 불만족의 비율
print(df['TARGET'].value_counts()) # [문법] value_counts: 타겟 레이블의 클래스별 빈도수 확인
# 0    73012
# 1     3008
unsatisfied_cnt = df[df['TARGET'] == 1].TARGET.count()
total_cnt = df.TARGET.count()
print('\n')
print(f'불만족 비율은 : {unsatisfied_cnt / total_cnt}')
# 불만족 비율은 : 0.039
print('\n')

print(df.describe())    # [문법] describe: 기술 통계량(평균, 표준편차, 사분위수 등) 확인
# var3 : 이상치 확인
df['var3'].replace(-999999, 2, inplace=True) # [개념] 이상치 처리: 특정 비정상 값을 최빈값 등으로 대체
df.drop('ID', axis=1, inplace=True)     # [개념] ID 제거: 예측에 불필요한 식별자 컬럼 삭제
print(df.describe())
print('\n')

# feature / label 분리
x_features = df.iloc[:, :-1]
y_label = df.iloc[:, -1]
print(x_features.shape, y_label.shape)  # (76020, 369)
print('\n')

# train / test split
# [문법] train_test_split: 데이터를 학습용(80%)과 테스트용(20%)으로 분리.
x_train, x_test, y_train, y_test = train_test_split(x_features, y_label, test_size=0.2, random_state=0)
train_cnt = y_train.count()
test_cnt = y_test.count()
print(x_train.shape, x_test.shape)  # (60816, 369) (15204, 369)
print('\n')
print('학습 데이터 레이블 값 분포 비율')
print(y_train.value_counts() / train_cnt)
print('\n')
print('검증(테스트) 데이터 레이블 값 분포 비율')
print(y_test.value_counts() / test_cnt)
print('\n')

# 모델
# [문법] XGBClassifier: n_estimators(반복 횟수), early_stopping_rounds(조기 종료 조건) 설정.
xgb_clf = XGBClassifier(n_estimators=5, random_state=0, early_stopping_rounds=3, eval_metric='auc') # 시간 관계상 500ro -> 5개로 설정
# [문법] fit: 학습 수행. eval_set을 통해 매 단계마다 검증 데이터에 대한 성능(AUC)을 모니터링함.
xgb_clf.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)]) 
# [개념] early_stopping_rounds=n : 학습이 어느정도 완료되면(같은 값이 n회 반복되면) 조기 종료 시킴, 학습 시간 단축
# [문법] roc_auc_score: 이진 분류의 성능 지표인 ROC-AUC 점수 계산.
xgb_roc_score = roc_auc_score(y_test, xgb_clf.predict_proba(x_test)[:, 1])
print(f'ROC AUC 값 : {xgb_roc_score:.5f}')
# ROC AUC 값 : 0.83431
print('\n')

# 예측
pred = xgb_clf.predict(x_test)
print('예측값 : ', pred[:5])
print('실제값 : ', np.array(y_test[:5]))
print('맞춘 개수 : ', (pred == y_test).sum())
print('오류수 : ', (pred != y_test).sum())
print('전체 대비 맞춘 비율 : ', sum(y_test == pred) / len(y_test))
print('\n')
print('분류 정확도 : ', metrics.accuracy_score(y_test, pred)) # [문법] accuracy_score: 전체 중 정답을 맞춘 비율
# 분류 정확도 :  0.9583

xgb_clf = XGBClassifier(n_estimators=5)

# 최적의 파라미터 구하기
# [개념] GridSearchCV: 하이퍼파라미터 조합을 교차 검증을 통해 탐색하여 최적의 설정을 찾음.
params = {
    'max_depth':[5, 7], # [개념] 트리 깊이: 과적합 제어를 위해 사용
    'min_child_weight':[1, 3],  # [개념] 관측치에 대한 가중치 합의 최소: 값이 클수록 보수적인 모델 생성
    'colsample_bytree':[0.5, 0.75]  # [개념] feature 비율: 각 트리 생성 시 무작위로 선택할 피처의 비율
}
gridcv = GridSearchCV(xgb_clf, param_grid=params)
gridcv.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)])
print('GridSearchCV 최적 파라미터 : ', gridcv.best_params_) # [문법] best_params_: 최적의 조합 출력
print('GridSearchCV 최고 예측 정확도 : {0:.5f}'.format(gridcv.best_score_)) # [문법] best_score_: 최고 검증 점수
xgb_roc_score = roc_auc_score(y_test, gridcv.predict_proba(x_test)[:, 1], average='macro')
print(f'xgb_roc_score : {xgb_roc_score:.5f}')
# GridSearchCV 최적 파라미터 :  {'colsample_bytree': 0.5, 'max_depth': 5, 'min_child_weight': 3}
# GridSearchCV 최고 예측 정확도 : 0.96100
# xgb_roc_score : 0.82045
print('\n')

# 최적의 파라미터로 모델 생성
xgb_clf2 = XGBClassifier(n_estimators=5, random_state=12, max_depth=5, min_child_weight=3, colsample_bytree=0.5)
xgb_clf2.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)])
xgb_roc_score2 = roc_auc_score(y_test, xgb_clf2.predict_proba(x_test)[:, 1])
print(f'ROC AUC2 값 : {xgb_roc_score2:.5f}')
# ROC AUC : 0.83445
print('\n')

# 예측
pred2 = xgb_clf2.predict(x_test)
print('예측값 : ', pred2[:5])
print('실제값 : ', np.array(y_test[:5]))
print('맞춘 개수 : ', (pred2 == y_test).sum())
print('오류수 : ', (pred2 != y_test).sum())
print('분류 정확도 : ', metrics.accuracy_score(y_test, pred2))
# 예측값 :  [0 0 0 0 0]
# 실제값 :  [0 0 0 0 0]
# 맞춘 개수 :  14571
# 오류수 :  633
# 분류 정확도 :  0.95836
print('\n')

# 중요 feature 시각화
# [문법] plot_importance: 모델 학습 시 사용된 피처들의 중요도(F-score)를 차트로 시각화.
fig, ax = plt.subplots(figsize=(10, 8))
plot_importance(xgb_clf2, ax=ax, max_num_features=20, height=0.5, color='orange')
plt.show()
print('\n')