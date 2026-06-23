# 나이브-베이즈 알고리즘을 이용한 분류 - weather.csv 사용
# [개념] GaussianNB: 특성들이 정규 분포를 따른다고 가정하고 베이즈 정리를 적용하여 분류하는 알고리즘.

from hmac import new
import pandas as pd
import numpy as np
from sympy import Max

# [문법] pd.read_csv: CSV 파일을 데이터프레임으로 로드.
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv') 
print(df.head(2))
print(df.info()) # [문법] 데이터프레임의 요약 정보(결측치, 데이터 타입 등) 확인.
print('\n')

# 전처리 작업
# [문법] drop: 분석에 불필요한 'Date' 컬럼을 제거.
df = df.drop('Date', axis=1) 
# 결측치 처리
# [문법] fillna: 결측치를 'Sunshine' 컬럼의 평균값으로 대체.
df = df.fillna(df['Sunshine'].mean()) 
print(df.info())
print('\n')

# 범주형 처리
# [문법] map: 문자열 데이터를 모델 학습이 가능한 수치형(0, 1)으로 변환.
df['RainToday'] = df['RainToday'].map({'Yes':1, 'No':0}) 
df['RainTomorrow'] = df['RainTomorrow'].map({'Yes':1, 'No':0})
print(df.head(2))
print('\n')

# 독립변수, 종속변수 분리
x = df.drop('RainTomorrow', axis=1)     # [개념] feature: 독립변수
y = df['RainTomorrow']      # [개념] label(class): 종속변수
print('\n')

# test/train
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

# 모델 학습 - Naive Bayes
from sklearn.naive_bayes import GaussianNB
# [문법] GaussianNB: 연속형 변수 분류에 적합한 가우시안 나이브 베이즈 모델 생성.
model = GaussianNB() 
model.fit(x_train, y_train) # [문법] fit: 학습 데이터를 사용하여 모델의 파라미터를 최적화함.

# 예측 및 평가
from sklearn.metrics import accuracy_score, confusion_matrix
# [문법] predict: 테스트 데이터를 입력하여 내일 비가 올지 여부를 예측.
pred = model.predict(x_test) 
print('예측값 : ', pred[:10])
print('실제값 : ', y_test[:10].values)
print('\n')
print('정확도 : ', accuracy_score(y_test, pred))    # [문법] accuracy_score: 전체 중 맞춘 비율 계산.
print('\n')
print('혼동 행렬 : \n', confusion_matrix(y_test, pred)) # [문법] confusion_matrix: 상세 분류 현황(TP, FP, FN, TN) 확인.
print('\n')

# 교차 검증
from sklearn.model_selection import cross_val_score
# [문법] cross_val_score: 데이터를 5개(cv=5)의 폴드로 나누어 교차 검증 수행하여 모델의 일반화 성능 확인.
scores = cross_val_score(model, x, y, cv=5) 
print('교차 검증 결과에서 각 fold의 정확도 : ', scores)
print('교차 검증 평균 : ', scores.mean())
print('\n')

# feature 중요도 분석
# feature 가 정규 분포를 따른다는 가정하에 클래스별 평균
# GaussianNB 의 멤버로 theta_ : 각 클래스별 feature 평균을 구함
# [문법] theta_: 각 클래스별 피처의 평균값을 담고 있는 속성.
mean_0 = model.theta_[0]    # [개념] RainTomorrow=0 (비 안오는 날 평균)
mean_1 = model.theta_[1]    # [개념] RainTomorrow=1 (비 오는 날 평균)

# 각 feature가 '비 오는 날 VS 비 안오는 날' 에서 얼마나 차이가 나는가?
# [문법] np.abs: 두 클래스 간 평균 차이의 절대값을 계산하여 중요도로 사용.
importance = np.abs(mean_1 - mean_0) 

feat_impo = pd.DataFrame({
    'feature' : x.columns,
    'importance' : importance
}).sort_values(by='importance', ascending=False)
print('feature 중요도 : \n', feat_impo)
print('\n')

# importance에 대한 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib

# [문법] sort_values: 시각화를 위해 중요도 순으로 정렬.
feat_impo = feat_impo.sort_values(by='importance', ascending=True) 
plt.figure()
plt.barh(feat_impo['feature'], feat_impo['importance']) # [문법] barh: 가로 바 차트로 변수 중요도 시각화.
plt.title('feature 중요도(평균 차이)')
plt.tight_layout()
plt.show()
print('\n')

# 새로운 자료로 예측
# [추천] 새로운 데이터 예측 시에도 학습 데이터와 동일한 전처리(결측치 처리, 인코딩 등)가 적용되어야 함.
newdata = pd.DataFrame([{
    'MinTemp':12.3,
    'MaxTemp':27.0,
    'Rainfall':0.0,
    'Sunshine':10.0,
    'WindSpeed':8.0,
    'Humidity':40,
    'Pressure':1005.0,
    'Cloud':1,
    'Temp':20.0,
    'RainToday':0 
}])
# [문법] predict_proba: 각 클래스(비 안옴, 비 옴)에 속할 확률을 반환함.
newpred = model.predict(newdata) 
print('예측값 : ', '비' if newpred == 1 else '비 안옴')
print('확률은 : ', model.predict_proba(newdata))
print('\n')