# [개념] RandomForest 분류 알고리즘
# [개념] 여러 개의 의사 결정 나무(Decision Tree)를 결합하여 하나의 강력한 예측 모델을 만드는 앙상블(Ensemble) 학습 기법의 대표적인 알고리즘입니다. 
# [개념] 마치 숲(Forest)이 많은 나무들로 이루어져 있듯, 수많은 결정 트리가 모여 더 정확하고 안정적인 분류 결과를 도출합니다.

# [개념] 앙상블 기법 중 배깅(Bagging, Bootstrap Aggregation)
# [개념] 복수의 샘플 데이터와 Decision Tree를 학습 시키고 결과를 집계(Voting)함.

# [추천] 우수한 성능을 원한다면 Boosting(XGBoost, LightGBM), 모델의 분산을 줄여 과적합을 방지하고 싶다면 Bagging(RandomForest)을 선택함.
# [추천] 범주형 변수가 많을 경우 One-Hot Encoding이나 Label Encoding 전처리가 필수적임.
# [추천] 하이퍼파라미터 튜닝 시 n_estimators, max_depth, min_samples_split 등을 조정하여 최적의 성능을 탐색함.

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

# [문법] pd.read_csv(): 타이타닉 생존자 데이터를 로드함.
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/titanic_data.csv') 
print(df.head())
print(df.info())
print(df.isnull().any())
print('\n')
df = df.dropna(subset=['Pclass', 'Age', 'Sex']) # [문법] dropna(): 분석에 사용할 주요 변수의 결측치가 있는 행을 제거함.
print(df.shape)
print('\n')

# features
df_x = df[['Pclass', 'Age', 'Sex']]
print(df_x.head())
print('\n')

# 전처리 - Sex열 : Label encoding (문자범주형 -> 정수형)
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder() # [문법] LabelEncoder: 문자열 범주를 수치형 정수로 변환하는 클래스.
df_x.loc[:, 'Sex'] = encoder.fit_transform(df_x['Sex']) # [문법] fit_transform(): 'female', 'male'을 0, 1로 변환.
print(df_x.head())
print('\n')

# label(target)
df_y = df['Survived'] # [개념] 종속변수(Label): 0(사망), 1(생존)
print(df_y.head())
print('\n')

# [문법] train_test_split: 데이터를 학습용(70%)과 테스트용(30%)으로 분리함.
train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, test_size=0.3, random_state=12) 
print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)
# (499, 3) (215, 3) (499,) (215,)
print('\n')

# 모델 생성
# [문법] RandomForestClassifier: n_estimators(결정트리 개수)를 500으로 설정하여 앙상블 모델 생성.
model = RandomForestClassifier(criterion='gini', n_estimators=500, random_state=12) 
model.fit(train_x, train_y) # [문법] fit(): 학습 데이터를 사용하여 모델 학습 수행.

pred = model.predict(test_x) # [문법] predict(): 테스트 데이터에 대한 생존 여부 예측.
print('예측값 : ', pred[:5])
print('실제값 : ', np.array(test_y[:5]))
print('맞춘 개수 : ', (pred == test_y).sum())
print('분류 정확도 : ', accuracy_score(test_y, pred))
print('\n')

# 교차 검증 (KFold) - Overfitting이 있다고 판단될 때 교차 검증 진행
cross_vali = cross_val_score(model, df_x, df_y, cv=5)
print('교차 검증 정확도 : ', cross_vali)
print('교차 검증 평균 정확도 : ', np.round(cross_vali.mean(), 5))
# 교차 검증 정확도 :  [0.76223776 0.82517483 0.82517483 0.83216783 0.83802817]
# 교차 검증 평균 정확도 :  0.8165566827538658
print('\n')

############################################
# 중요 변수 확인하기
# [문법] feature_importances_ : 각 특성이 예측에 기여한 정도(중요도)를 수치로 표현.
# [개념] 값의 합은 1.0이며, 수치가 클수록 해당 변수가 불순도 감소(Gini Impurity 감소)에 더 많이 기여함.
print('특성 (변수) 중요도 : ', model.feature_importances_)

print('\n')

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib

n_features = df_x.shape[1]
plt.barh(range(n_features), model.feature_importances_, align='center') # [문법] barh(): 가로 바 차트로 변수 중요도 시각화.
plt.yticks(np.arange(n_features), df_x.columns)
plt.ylim(-1, n_features)
plt.xlabel('특성 중요도')
plt.ylabel('특성')
plt.show()
print('\n')

############################################
# 전체 변수 대상으로 중요도 확인
# [개념] Name, Ticket, Cabin : 문자형 데이터 -> 바로 사용 불가 => Encoding이 필요함.
# [개념] PassengerID, Name : Survived 와 상관이 없는 변수(분석에 필요 X).
# [개념] 해당 변수들은 제외하고 작업 진행.

df_imsi = df[['Pclass', 'Age', 'Sex', 'Fare', 'SibSp', 'Parch']]
# 전처리 - Sex열 : Label encoding (문자범주형 -> 정수형)
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
df_imsi.loc[:, 'Sex'] = encoder.fit_transform(df_imsi['Sex'])

# 모델학습
train_x, test_x, train_y, test_y = train_test_split(df_imsi, df_y, test_size=0.3, random_state=12)
model.fit(train_x, train_y)

importances = model.feature_importances_
# 컬럼명 + 중요도 표시
feature_df = pd.DataFrame({
    'feature': df_imsi.columns, # [문법] columns: 데이터프레임의 열 이름 추출.
    'importance': importances
}).sort_values(by='importance', ascending=False)
print(feature_df)
#   feature  importance
# 1     Age    0.295631
# 3    Fare    0.270275
# 2     Sex    0.244372
# 0  Pclass    0.094242
# 4   SibSp    0.057279
# 5   Parch    0.038202
print('\n')

# 시각화
import seaborn as sns
plt.figure(figsize=(8, 5))
sns.barplot(x='importance', y='feature', data=feature_df, orient='h') # [문법] sns.barplot(): seaborn을 이용한 중요도 시각화.
plt.xlabel('중요도')
plt.ylabel('변수')
plt.title('변수 중요도')
plt.tight_layout()
plt.show()
print('\n')