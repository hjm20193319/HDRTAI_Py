import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sympy import plot
from sklearn.preprocessing import LabelEncoder
import numpy as np

# 데이터

data = pd.read_csv('mushrooms.csv')
print(data.head())
print(data.info())
print('\n')

pd.set_option('display.max_columns', None)
x = data.iloc[:, 1:]
y = data.iloc[:, 0]
print(x.head())
print(y.head())
print('\n')

x = pd.get_dummies(x)
print(x.head())
print('\n')

y = LabelEncoder().fit_transform(y)
print(y[:5])
print('\n')

# 모델

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

from xgboost import plot_importance
from xgboost import XGBClassifier

xgb_clf = XGBClassifier(n_estimators=5, random_state=0, early_stopping_rounds=3, eval_metric='auc')
xgb_clf.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)])
plot_importance(xgb_clf)
plt.tight_layout()
plt.show()
print('\n')

x = x[['gill-size_b', 'bruises_f', 'spore-print-color_r', 'stalk-surface-below-ring_y', 'stalk-root_r', 'stalk-root_c', 'odor_n', 'odor_l', 'odor_a', 'spore-print-color_u']]
print(x.head())

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)


# 모델 학습
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(x_train, y_train)

# 예측
from sklearn.metrics import accuracy_score, confusion_matrix
pred = model.predict(x_test)
print('예측값 : ', pred[:10])
print('실제값 : ', y_test[:10])
print('\n')
print('정확도 : ', accuracy_score(y_test, pred))
print('\n')
print('혼동 행렬 : \n', confusion_matrix(y_test, pred))
print('\n')

# 교차 검증
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x, y, cv=5)
print('교차 검증 결과에서 각 fold의 정확도 : ', scores)
print('교차 검증 평균 : ', scores.mean())
print('\n')

# feature 중요도 분석
mean_0 = model.theta_[0]
mean_1 = model.theta_[1]

importance = np.abs(mean_1 - mean_0)

feat_impo = pd.DataFrame({
    'feature' : x.columns,
    'importance' : importance
}).sort_values(by='importance', ascending=False)
print('feature 중요도 : \n', feat_impo)
print('\n')

feat_impo = feat_impo.sort_values(by='importance', ascending=True)
plt.figure()
plt.barh(feat_impo['feature'], feat_impo['importance'])
plt.title('feature 중요도(평균 차이)')
plt.tight_layout()
plt.show()
print('\n')