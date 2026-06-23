# [개념] 앙상블 학습(Ensemble Learning)
# [개념] 여러 개의 분류기를 생성하고 그 예측을 결합함으로써 보다 정확한 예측 결과를 얻는 기법.
# [개념] 강력한 하나의 모델보다는 약한 모델 여러 개를 조합하여 일반화 성능을 높이고 과적합을 방지함.
# [추천] 데이터의 특성에 따라 Voting, Bagging, Boosting 중 적절한 기법을 선택하는 것이 중요함.

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
# [문법] VotingClassifier: 서로 다른 알고리즘을 가진 분류기들을 결합하는 앙상블 모델.
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score
from collections import Counter
import numpy as np

#################################################
# Data
cancer = load_breast_cancer() # [문법] 유방암 진단 데이터셋 로드
print(cancer.keys())
print('\n')
x, y = cancer.data, cancer.target
print(x[:2])
print(y[:2])
print('\n')
print('diagnosis(y) : ', np.unique(y))  # [문법] unique(): 종속변수의 고유값 확인 [0(악성) 1(양성)]
print('\n')

# 0과 1의 비율
counter = Counter(y)
total = sum(counter.values())
for cls, cnt in counter.items():
    print(f'class {cls} : {cnt}개 ({cnt/total*100:.2f}%)')
# class 0 : 212개 (37.26%)
# class 1 : 357개 (62.74%)
print('\n')

# [문법] stratify=y: 타겟 값의 비율을 유지하며 데이터를 분할하여 학습/테스트 데이터의 편향을 방지함.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12, stratify=y) 
# stratify = y : train, test 비율 유지
y_li = y.tolist()
ytr_li = y_train.tolist()
yts_li = y_test.tolist()
print('전체 분포 : ', Counter(y_li))
print('train 분포 : ', Counter(ytr_li))
print('test 분포 : ', Counter(yts_li))
# 전체 분포 :  Counter({1: 357, 0: 212})
# train 분포 :  Counter({1: 285, 0: 170})
# test 분포 :  Counter({1: 72, 0: 42})
print('\n')

##################################
# 개별 모델
# [문법] make_pipeline: 데이터 전처리(StandardScaler)와 모델 학습 과정을 하나의 객체로 묶어 관리함.
logi = make_pipeline(StandardScaler(), LogisticRegression(max_iter=100, solver='lbfgs', random_state=12))

knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))

# [개념] DecisionTree는 스케일링의 영향을 거의 받지 않으므로 파이프라인 없이 단독 사용 가능.
tree = DecisionTreeClassifier(criterion='gini', max_depth=5, random_state=12)
####################################
###########중요#####################
####################################
# 앙상블 모델
# [개념] voting='soft': 각 분류기의 예측 확률을 평균내어 확률이 가장 높은 클래스를 선택 (일반적으로 hard보다 성능 우수).
# [개념] voting='hard': 다수결 원칙으로 가장 많이 예측된 클래스를 선택.
voting = VotingClassifier(estimators=[('LR', logi), ('KNN', knn), ('DT', tree)], voting='soft')
####################################
####################################
####################################
# 개별 모델 성능 확인
named_models = [('LR', logi), ('KNN', knn), ('DT', tree)]
for name, clf in named_models:
    clf.fit(x_train, y_train) # [문법] fit(): 개별 모델 학습
    pred = clf.predict(x_test) # [문법] predict(): 개별 모델 예측
    print(f'{name} 정확도 : {accuracy_score(y_test, pred):.4f}')
# LR 정확도 : 0.9912
# KNN 정확도 : 0.9737
# DT 정확도 : 0.8772
print('\n')

####################################
# Voting 성능 평가
voting.fit(x_train, y_train) # [문법] fit(): 앙상블 모델 학습
vpred = voting.predict(x_test) # [문법] predict(): 앙상블 모델 예측
print(f'Voting 분류기 정확도 : {accuracy_score(y_test, vpred):.4f}')
# Voting 정확도 : 0.9649
print('\n')

# 선택 : 교차 검증으로 안정성 확인
# [문법] StratifiedKFold: 불균형한 레이블 분포를 가진 데이터에 대해 비율을 유지하며 교차 검증 수행.
cvfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)
cv_score = cross_val_score(voting, x, y, cv=cvfold, scoring='accuracy') # [문법] 교차 검증 수행
print(f'Voting 5겹 cv 정확도 평균 : {np.mean(cv_score):.4f}')
print(f'표준편차 : +- {cv_score.std():.4f}')
# Voting 5겹 cv 정확도 평균 : 0.9701
# 표준편차 : +- 0.0181
print('\n')

# 모델 성능 지표
from sklearn.metrics import confusion_matrix, classification_report,roc_auc_score
# 보팅 모델 상세 평가
# [문법] classification_report: 정밀도(Precision), 재현율(Recall), F1-score를 종합적으로 출력.
print(classification_report(y_test, vpred)) 
print('confusion matrix : \n', confusion_matrix(y_test, vpred)) # [문법] 혼동 행렬 출력
# [문법] roc_auc_score: 모델의 이진 분류 성능을 나타내는 지표로 1에 가까울수록 우수함.
print('roc_auc_score : ', roc_auc_score(y_test, voting.predict_proba(x_test)[:, 1])) 