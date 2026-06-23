# [개념] XGBoost (eXtreme Gradient Boosting) : Boosting 알고리즘을 구현한 분류/예측 모델
# [개념] Boosting은 약한 분류기에 대해 샘플의 일부를 보완해가며 순차적으로 학습해, 강한 분류기를 만듦
# [개념] LightGBM: XGBoost보다 학습 속도가 빠르고 메모리 사용량이 적은 리프 중심(Leaf-wise) 트리 분할 방식 알고리즘.

# [추천] 데이터셋의 크기가 작을 경우 LightGBM은 과적합(Overfitting)에 취약할 수 있으므로 데이터 양에 따라 모델을 선택함.
# [추천] 하이퍼파라미터 튜닝 시 learning_rate, n_estimators, max_depth 등을 GridSearchCV나 RandomizedSearchCV로 최적화하는 것을 권장함.

# breast cancer dataset 사용
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import koreanize_matplotlib
import xgboost as xgb
from lightgbm import LGBMClassifier     # xgboost 보다 성능 우수하지만 자료가 적으면 과적합 발생
import lightgbm as lgb

# 데이터
data = load_breast_cancer() # [문법] load_breast_cancer(): 사이킷런에서 제공하는 유방암 진단 데이터셋 로드.
df = pd.DataFrame(data.data, columns=data.feature_names) # [문법] feature_names: 데이터셋의 독립변수 컬럼명 추출.
df['target'] = data.target # [개념] 종속변수(Target): 0(악성), 1(양성)

x = df.drop('target', axis=1) # [문법] drop(): 종속변수를 제외하여 독립변수(Feature) 데이터 생성.
y = df['target']

print(x[:3])
print(y[:3])
print('\n')

print(x.shape, y.shape)
print('\n')

# 레이블 분포 확인
print({name:(y == i).sum() for i, name in enumerate(data.target_names)})
print('\n')

# [문법] train_test_split: 데이터를 학습용(80%)과 테스트용(20%)으로 분리. stratify=y로 클래스 비율 유지.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12, stratify=y)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
print('\n')

# 모델 1
# [문법] XGBClassifier: XGBoost의 분류 모델 클래스.
xgb_clf = xgb.XGBClassifier(
    booster='gbtree',       # [개념] 'gbtree' : tree기반, 'gblinear' : 선형 모델
    max_depth=6,    # [개념] 개별 결정 tree 최대 깊이 제한(과적합 방지)
    n_estimators=200,      # [개념] 반복 수행할 약한 분류기의 개수
    eval_metric='logloss', # [수정] eval_matric -> eval_metric (오타 수정)
    random_state=42,
)
xgb_clf.fit(x_train, y_train) # [문법] fit(): 학습 데이터를 사용하여 모델 학습 수행.

# 모델 2
# [문법] LGBMClassifier: LightGBM의 분류 모델 클래스.
lgb_clf = LGBMClassifier(
    n_estimators=200,
    random_state=42,
    verbose=-1  # [문법] verbose=-1: 불필요한 학습 과정 로그 숨기기
)
lgb_clf.fit(x_train, y_train) # [문법] fit(): 학습 데이터를 사용하여 모델 학습 수행.

# 예측 및 평가
pred_xgb = xgb_clf.predict(x_test) # [문법] predict(): 테스트 데이터에 대한 클래스 예측.
pred_lgb = lgb_clf.predict(x_test)

print(f'xgboost 정확도 : {accuracy_score(y_test, pred_xgb):.5f}') # [문법] accuracy_score: 전체 중 맞춘 비율 계산.
print(f'lightgbm 정확도 : {accuracy_score(y_test, pred_lgb):.5f}')
print('\n')

# [개념] feature 중요도 : gain(정보 이득) 기준으로 통일하여 모델 간 기여도 비교
booster = xgb_clf.get_booster() # [문법] get_booster(): XGBoost의 내부 부스터 객체 접근.
xgb_gain = pd.Series(booster.get_score(importance_type='gain'))

lgb_gain = pd.Series(lgb_clf.booster_.feature_importance(importance_type='gain'), index=x_train.columns) # [문법] feature_importance: 특성 중요도 수치 반환.

# xgb_gain / xgb_gain.sum() : 각 feature의 기여도를 비율로 만들기
xgb_gain_pct = 100 * xgb_gain / (xgb_gain.sum() if xgb_gain.sum() != 0 else 1)
lgb_gain_pct = 100 * lgb_gain / (lgb_gain.sum() if lgb_gain.sum() != 0 else 1)

# 사용되지 않은 feature는 0으로 채움
xgb_gain_pct = xgb_gain_pct.reindex(x_train.columns).fillna(0)
lgb_gain_pct = lgb_gain_pct.reindex(x_train.columns).fillna(0)

comp_df = pd.DataFrame({
    'xgboost (gain %)': xgb_gain_pct,
    'lightgbm (gain %)': lgb_gain_pct
}).sort_values('xgboost (gain %)', ascending=False)
print(comp_df.head(10))      # [개념] 중요 변수 top 10 출력
print('\n')

# 시각화
topk = 5
top = comp_df.head(topk)[::-1]

fig, axes = plt.subplots(1, 2, figsize=(10, 5)) # [문법] subplots: 여러 개의 그래프를 한 화면에 배치.
xmax = float(np.ceil(top.max().max()))  # 두 모델의 최대값

for ax, col in zip(axes, comp_df.columns):
    ax.barh(top.index, top[col])

    ax.set_title(f'{col.split()[0]} Feature importance')
    ax.set_xlabel('Importance (%)')
    ax.set_xlim(0, xmax)

plt.tight_layout()
plt.show()
print('\n')