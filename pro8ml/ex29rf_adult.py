# [개념] RandomForest 분류 알고리즘 - adult dataset 성인 소득 예측 자료
# [개념] 연봉이 50K(약 5만 $) 이상인지 예측 - 이진 분류(Binomial Classification)
# [개념] Pipeline: 데이터 전처리부터 모델 학습까지의 과정을 하나로 묶어 관리하여 코드의 가독성과 재사용성을 높임.
# [개념] ColumnTransformer: 데이터프레임의 각 컬럼별로 서로 다른 전처리(스케일링, 인코딩 등)를 독립적으로 적용함.

# [추천] 데이터셋의 클래스 불균형이 심할 경우, RandomForestClassifier의 class_weight='balanced' 파라미터를 고려함.
# [추천] 범주형 변수의 카테고리 개수가 너무 많을 경우 OneHotEncoder 대신 TargetEncoder나 LabelEncoder를 검토할 수 있음.

import pandas as pd
import numpy as np
from sklearn import pipeline
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline   # 전처리 + 모델을 하나로 묶어서 실행
from sklearn.compose import ColumnTransformer   # 칼럼별 전처리를 다르게 적용
from sklearn.impute import SimpleImputer    # 결측치 처리 클래스
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score

#############################################################
# 데이터
# [문법] fetch_openml(): OpenML 저장소에서 adult 성인 소득 데이터셋을 로드함.
adult = fetch_openml(name='adult', version=2, as_frame=True) 
print(type(adult))  # <class 'sklearn.utils._bunch.Bunch'>
df = adult.frame    # [문법] frame: Bunch 객체에서 pandas dataframe 형태로 추출.
pd.set_option('display.max_columns', None)
print(df.head())
print(df.shape) # (48842, 15)
print(df.info())
print(df.isnull().sum()) # [문법] isnull().sum(): 각 컬럼별 결측치 개수 확인.
# 결측치 : workclass-2799, occupation-2809, native-country-857
print('\n')

# [개념] target 변환 (인코딩) : class(연봉) '>50k' => 1 , '<=50k' => 0
df['class'] = df['class'].apply(lambda x:1 if '>50K' in x else 0)
print(df.head())
print(set(df['class']))
print(df['class'].unique()) # [문법] unique(): 종속변수의 고유값 확인.
print('\n')

x = df.drop('class', axis=1) # [문법] drop(): 종속변수 'class'를 제외하여 독립변수(Feature) 생성.
y = df['class']
print(x.info())
print('\n')

# [문법] select_dtypes: 데이터 타입에 따라 숫자형(int64, float64)과 범주형(object, category) 칼럼을 분리함.
num_cols = x.select_dtypes(include=['int64', 'float64']).columns    # 숫자형 칼럼 리스트
cat_cols = x.select_dtypes(include=['object','category']).columns  # 범주형 칼럼 리스트

# [개념] 전처리 파이프라인(숫자형): 처리 항목들을 연결해, 연속적으로 실행.
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),      # [문법] SimpleImputer: 숫자형 결측치를 중앙값(median)으로 대체.
    ('scaler', StandardScaler())        # [문법] StandardScaler: 데이터 표준화(평균 0, 분산 1).
])

# [개념] 전처리 파이프라인(범주형)
cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),    # [문법] SimpleImputer: 범주형 결측치를 최빈값(most_frequent)으로 대체.
    ('onehot', OneHotEncoder(handle_unknown='ignore'))      # [문법] OneHotEncoder: 범주형 데이터를 0과 1의 희소 행렬로 변환.
])

# < 참고 > 
# 컬럼별 전처리 결합
# 숫자 : 스케일링
# 문자 : 인코딩
#       => 각각 다르게 처리해야 함
# [문법] ColumnTransformer: 정의된 파이프라인을 특정 컬럼에 매핑하여 결합함.
preprocess = ColumnTransformer([
    ('num', num_pipeline, num_cols),    # 숫자형 칼럼에 num_pipeline 적용
    ('cat', cat_pipeline, cat_cols)     # 범주형 칼럼에 cat_pipeline 적용
])

############################################################################
# 전체 파이프라인 (전처리 + 모델)
# [문법] Pipeline: 전처리 객체(preprocess)와 분류 모델(RandomForestClassifier)을 하나로 통합.
pipe = Pipeline([
    ('prep', preprocess),   # 전처리 단계
    ('model', RandomForestClassifier(random_state=12))  # 모델
])

# [문법] train_test_split: 데이터를 학습용(70%)과 테스트용(30%)으로 분리함.
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3, random_state=12)

# [개념] 하이퍼 파라미터 튜닝 범위 설정: '모델명__파라미터명' 형식으로 지정함.
param_grid = {
    'model__n_estimators': [100, 200],  # 트리 개수
    'model__max_depth': [5, 10, None],  # 트리의 최대 깊이
    'model__class_weight': [None, 'balanced']    # 클래스 불균형 보정 여부
}

# 교차 검증
# [문법] StratifiedKFold: 타겟의 비율을 유지하며 데이터를 5개의 폴드로 나눔.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)
# 데이터가 불균형하기 때문에

# [문법] GridSearchCV: 교차 검증을 통해 최적의 하이퍼파라미터 조합을 탐색함.
grid = GridSearchCV(
    estimator=pipe,   # 전체 파이프라인 사용 
    param_grid=param_grid,  # 탐색할 파라미터
    cv=cv,
    scoring='roc_auc', # [개념] 평가 지표로 ROC-AUC 점수 사용.
    n_jobs=-1   # 모든 CPU 사용
)
grid.fit(train_x, train_y)  # [문법] fit(): 전처리 + 최적의 파라미터 탐색 + 학습 수행.
print('최적의 파라미터 : ', grid.best_params_) # [문법] best_params_: 탐색된 최적의 조합 출력.
print('최적의 점수 : ', grid.best_score_) # [문법] best_score_: 최적 파라미터에서의 평균 검증 점수.
# 최적의 파라미터 :  {'model__class_weight': None, 'model__max_depth': 10, 'model__n_estimators': 200}
# 최적의 점수 :  0.909490412502798
print('\n')

# 예측
pred = grid.predict(test_x) # [문법] predict(): 테스트 데이터에 대한 클래스(0, 1) 예측.
proba = grid.predict_proba(test_x)[:, 1]    # [문법] predict_proba(): 클래스 1(연봉 >50K)에 대한 확률값 추출.

# 평가
print('정확도 : ', accuracy_score(test_y, pred)) # [문법] accuracy_score: 전체 예측 중 맞춘 비율.
print('roc_auc score : ', roc_auc_score(test_y, proba)) # [문법] roc_auc_score: 이진 분류 모델의 성능 지표(1에 가까울수록 우수).
# 정확도 :  0.8630997065447349
# roc_auc score :  0.9155748365810268
print('\n')
print('confusion matrix : \n', confusion_matrix(test_y, pred)) # [문법] confusion_matrix: 혼동 행렬 출력.
print('\n')
print('classification report : \n', classification_report(test_y, pred)) # [문법] classification_report: 정밀도, 재현율, F1-score 종합 출력.
print('\n')