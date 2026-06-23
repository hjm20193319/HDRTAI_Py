# [개념] 과적합(Overfitting) 방지 목적
# [개념] train-test split : 학습 데이터에만 익숙해지는 것을 방지하여 일반화 성능 향상
# [개념] K-Fold : 데이터를 K개로 나누어 교차 검증함으로써 모델 평가의 안정성 확보
# [개념] GridSearchCV : 교차 검증을 기반으로 하이퍼 파라미터 튜닝을 자동화하여 최적의 모델 탐색

# iris dataset 사용

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
# import test  # [오류] 존재하지 않는 모듈이므로 주석 처리 또는 삭제 필요

iris = load_iris()
print(iris.keys()) 

train_data = iris.data
train_label = iris.target
print(train_data[:3])
print(train_label[:3])
print('\n')

# 분류 모델 작성
dt_clf = DecisionTreeClassifier() # [문법] DecisionTreeClassifier: 의사결정나무 분류 모델 생성
dt_clf.fit(train_data, train_label)     # [문법] fit(): 모든 데이터를 학습에 참여 (지도 학습)

pred = dt_clf.predict(train_data)       # [문법] predict(): 학습 데이터로 검증(예측)
print('예측값 : ', pred)
print('실제값 : ', train_label)
print('분류 정확도 : ', accuracy_score(train_label, pred))
# 분류 정확도 :  1.0   ==>> 과적합 의심
print('\n')

###############################################
# 과적합 방지 목적의 처리 1
# train-test split
from sklearn.model_selection import train_test_split # [문법] 데이터를 학습용과 테스트용으로 분리하는 함수
x_train, x_test, y_train, y_test = train_test_split(train_data, iris.target, test_size=0.3, random_state=121)
dt_clf = DecisionTreeClassifier()
dt_clf.fit(x_train, y_train)    # [문법] train data로 학습

pred2 = dt_clf.predict(x_test)  # [문법] test data로 검증(예측)
print('예측값 : ', pred2)
print('실제값 : ', y_test)
print('분류 정확도 : ', accuracy_score(y_test, pred2))
# 분류 정확도 :  0.9555555555555556     ==> 효과 : 과적합 여부

###################################################
# 과적합 방지 목적의 처리 2
# 교차검증 Cross Validation
# [개념] train data를 분할해(k개 만큼) 학습과 평가를 병행하는 방법 : K-Fold가 가장 일반적
from sklearn.model_selection import KFold # [문법] K-Fold 교차 검증을 위한 클래스
import numpy as np

features = iris.data
label = iris.target
dt_clf2 = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=12)
kfold = KFold(n_splits=5) # [문법] n_splits=5: 데이터를 5개의 폴드로 나눔
cv_accuracy = []
print('붓꽃 데이터 세트 크기 : ', features.shape[0])
# 붓꽃 데이터 세트 크기 :  150

# KFold 학습 시 전체 150 행 -> 학습 데이터(4/5, 120개), 검증 데이터(1/5, 50개)로 분할 되어 학습함

n_iter = 0
# [문법] KFold 객체의 split()을 호출하면 Fold 별 학습용, 검증용 test의 행 인덱스를 array로 반환
for train_index, test_index in kfold.split(features):
    # print('n_iter(반복수) : ', n_iter)
    # print('train_index : ', train_index)
    # print('test_index : ', test_index)
    # print('\n')
    x_train, x_test = features[train_index], features[test_index]
    y_train, y_test = label[train_index], label[test_index]
    # 학습 및 예측
    dt_clf2.fit(x_train, y_train)   # [문법] train으로 학습
    pred3 = dt_clf2.predict(x_test)  # [문법] test로 검증
    n_iter += 1
    # 반복할 때 마다 정확도 출력
    accuracy = np.round(accuracy_score(y_test, pred3), 4) # [문법] accuracy_score: 정확도 계산
    train_size = x_train.shape[0]
    test_size = x_test.shape[0]
    print(f'반복수 : {n_iter}, 교차검증 정확도 : {accuracy}, 학습데이터 크기 : {train_size}, 검증데이터 크기 : {test_size}')
    print(f'검증 세트 인덱스 : {test_index}')
    print('\n')
    cv_accuracy.append(accuracy)

print('cv_accuracy : ', np.array(cv_accuracy).astype(float))
print('평균 검증 정확도 : ', np.mean(cv_accuracy))
print('\n')

# [개념] StratifiedKFold - 불균형한 분포도를 가진 레이블 데이터 집합을 처리하기 위한 KFold 방식
# 예 ) 대출 사기 데이터의 경우, 대부분은 정상/사기 레이블은 극히 일부임
# [추천] 분류 문제에서는 레이블의 비율을 유지하는 StratifiedKFold 사용을 권장함.
# from sklearn.model_selection import StratifiedKFold 

###################################################
# 과적합 방지 목적의 처리 2-1 : 교차 검증 단순화
# [문법] cross_val_score 를 이용해, 교차 검증을 간단히 처리 가능
from sklearn.model_selection import cross_val_score     # [개념] 내부적으로 StratifiedKFold(분류) 또는 KFold(회귀) 처리함
data = iris.data
label = iris.target # [개념] 종속변수(Label)
scores = cross_val_score(dt_clf2, data, label, scoring='accuracy', cv=5)
print('교차 검증별 정확도 : ', np.round(scores, 3))
print('평균 검증 정확도 : ', np.round(np.mean(scores), 3))
print('\n')

####################################################
# 과적합 방지 목적의 처리 3
# [개념] GridSearchCV - 과적합 방지 간접 방법
# [개념] 교차 검증과 최적의 하이퍼 파라미터 찾기(내부적으로 KFold를 사용해, 과적합을 줄임)
from sklearn.model_selection import GridSearchCV # [문법] 하이퍼 파라미터 튜닝을 위한 클래스
# 연습용으로 일부 파라미터만 사용 : max_depth, min_samples_split
# [개념] min_samples_split: 노드 분할을 위한 최소한의 샘플 수로 과적합 제어

parameters = {'max_depth': [1, 2, 3], 'min_samples_split': [2, 3]} # [문법] 테스트할 파라미터 딕셔너리 정의

grid_dtree = GridSearchCV(estimator=dt_clf2, param_grid=parameters, cv=3, refit=True) # [문법] refit=True: 최적 파라미터로 재학습
grid_dtree.fit(x_train, y_train)    # [개념] 내부적으로 복수 개의 모형을 생성하고, 실행시켜서 최적의 파라미터를 찾아줌
# best_score_, best_params_, best_estimator_, grid_score_....

import pandas as pd
scores_df = pd.DataFrame(grid_dtree.cv_results_) # [문법] cv_results_: 파라미터별 상세 결과 확인
print(scores_df)
print('\n')
print('GridSearchCV 최적 파라미터 : ', grid_dtree.best_params_) # [문법] 최적의 파라미터 조합 출력
print('GridSearchCV 최고 정확도 : ', grid_dtree.best_score_) # [문법] 최고 교차 검증 정확도 출력
print('\n')

#####################################################
# 최적의 모델
bestmodel = grid_dtree.best_estimator_ # [문법] 최적의 파라미터로 학습된 모델 객체 반환
print(bestmodel)
print('\n')

best_pred = bestmodel.predict(x_test) # [문법] 최적 모델로 예측 수행
print('예측 결과 : ', best_pred)
print('정확도 : ', accuracy_score(y_test, best_pred))
print('\n')