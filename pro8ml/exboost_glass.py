import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import koreanize_matplotlib
import xgboost as xgb
from lightgbm import LGBMClassifier  
import lightgbm as lgb

# 데이터

data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/glass.csv')
print('--데이터 정보--')
print(data.head(3)) 
print(data.info())
print('\n')

x = data.drop('Type', axis=1) 
y = data['Type']

# 레이블 확인
print(y.unique()) 
# [1 2 3 5 6 7]
print('\n')

# 레이블 인코딩
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder() 
y = encoder.fit_transform(y)

# 데이터 구분
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=12, stratify=y)
print(x_train.shape, x_test.shape)
# (149, 9) (65, 9)
print('\n')

# 모델
xgb_clf = xgb.XGBClassifier(
    booster='gbtree',       
    max_depth=6,            
    n_estimators=200,       
    eval_metric='logloss', 
    random_state=42
)
xgb_clf.fit(x_train, y_train) 

lgb_clf = LGBMClassifier(
    n_estimators=200,
    random_state=42,
    verbose=-1              
)
lgb_clf.fit(x_train, y_train) 

# 예측
pred_xgb = xgb_clf.predict(x_test) 
pred_lgb = lgb_clf.predict(x_test)

print(f'xgboost 정확도 : {accuracy_score(y_test, pred_xgb):.5f}') 
print(f'lightgbm 정확도 : {accuracy_score(y_test, pred_lgb):.5f}')
print('\n')

booster = xgb_clf.get_booster() 
xgb_gain = pd.Series(booster.get_score(importance_type='gain'))

lgb_gain = pd.Series(lgb_clf.booster_.feature_importance(importance_type='gain'), index=x_train.columns) 

# xgb_gain / xgb_gain.sum()
xgb_gain_pct = 100 * xgb_gain / (xgb_gain.sum() if xgb_gain.sum() != 0 else 1)
lgb_gain_pct = 100 * lgb_gain / (lgb_gain.sum() if lgb_gain.sum() != 0 else 1)

# 사용되지 않은 feature는 0으로 채움
xgb_gain_pct = xgb_gain_pct.reindex(x_train.columns).fillna(0)
lgb_gain_pct = lgb_gain_pct.reindex(x_train.columns).fillna(0)

comp_df = pd.DataFrame({
    'xgboost (gain %)': xgb_gain_pct,
    'lightgbm (gain %)': lgb_gain_pct
}).sort_values('xgboost (gain %)', ascending=False) 
print(comp_df.head(10))      
print('\n')

# 시각화
topk = 5
top = comp_df.head(topk)[::-1] 

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
xmax = float(np.ceil(top.max().max()))  # 두 모델의 최대값

for ax, col in zip(axes, comp_df.columns):
    ax.barh(top.index, top[col])

    ax.set_title(f'{col.split()[0]} Feature importance')
    ax.set_xlabel('Importance (%)')
    ax.set_xlim(0, xmax)

plt.tight_layout() 
plt.show()
print('\n')