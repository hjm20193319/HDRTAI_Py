import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("sh6147782/winequalityred")
files = os.listdir(path)
print(files)

df = pd.read_csv(path + '/winequality-red.csv')
pd.set_option('display.max_columns', None)
print(df.head())
print('\n')

# 변수
df_x = df.drop('quality', axis=1)
df_y = df['quality']

# 학습용 데이터 분리
train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, test_size=0.3, random_state=12)

# 표준화
scaler = StandardScaler()
train_x = scaler.fit_transform(train_x)
test_x = scaler.transform(test_x)

# 모델 생성
model = RandomForestClassifier(criterion='gini', n_estimators=500, random_state=12, max_depth=5)
model.fit(train_x, train_y)

# 예측
pred = model.predict(test_x)
print('예측값 : ', pred[:5])
print('실제값 : ', np.array(test_y[:5]))
print('맞춘 개수 : ', (pred == test_y).sum())
print('오류수 : ', (pred != test_y).sum())
print('전체 대비 맞춘 비율 : ', sum(test_y == pred) / len(test_y))
print('분류 정확도 : ', accuracy_score(test_y, pred))
print('\n')

# Overfitting 여부 판단하기
print('훈련 데이터 분류 정확도 : ', model.score(train_x, train_y))
print('\n')

# 교차 검증
cross_vali = cross_val_score(model, df_x, df_y, cv=5)
print('교차 검증 정확도 : ', cross_vali)
print('교차 검증 평균 정확도 : ', np.round(cross_vali.mean(), 5))
print('\n')

# 중요변수 확인하기
print('특성 (변수) 중요도 : ', model.feature_importances_)
# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib

n_features = df_x.shape[1]
plt.barh(range(n_features), model.feature_importances_, align='center')
plt.yticks(np.arange(n_features), df_x.columns)
plt.ylim(-1, n_features)
plt.xlabel('특성 중요도')
plt.ylabel('특성')
plt.tight_layout()
plt.show()
print('\n')