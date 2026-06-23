# 최근접 이웃(K - Nearest Neighbors) - breast_cancer dataset
# [개념] K-NN: 새로운 데이터가 주어졌을 때 가장 가까운 K개의 이웃 데이터를 찾아 그들의 다수결로 클래스를 분류하는 알고리즘.
# [개념] 유방암 데이터셋(breast_cancer): 30개의 특성(반지름, 질감 등)을 바탕으로 종속변수(0: 악성, 1: 양성)를 분류함.
# [추천] K-NN은 거리 기반 알고리즘이므로 특성(Feature)들의 스케일이 다를 경우 StandardScaler 등을 이용한 표준화 전처리가 필수적입니다.

from typing import final

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler    

# 데이터
# [문법] load_breast_cancer(): 사이킷런에서 제공하는 유방암 진단 데이터셋 로드.
data = load_breast_cancer() 
x = data.data   # [개념] feature: 독립변수 (30개의 수치형 데이터)
y = data.target # [개념] label: 종속변수 (0: Malignant 악성, 1: Benign 양성)
print(x[:2], x.shape) # [문법] x.shape: 데이터의 행과 열 크기 확인 (569, 30)
print(y[:2], np.unique(y)) # [문법] np.unique(): 종속변수의 고유한 클래스 종류 확인
print('\n')

# [문법] train_test_split: 데이터를 학습용(80%)과 테스트용(20%)으로 분리. stratify=y로 클래스 비율 유지.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y) 

# [개념] 스케일링 필요 (∵ 거리기반 모델이므로 변수 간 단위 크기가 거리에 영향을 미침)
scaler = StandardScaler() # [문법] StandardScaler: 평균 0, 표준편차 1로 표준화하는 클래스.
x_train_scaled = scaler.fit_transform(x_train) # [문법] fit_transform: 학습 데이터의 통계량을 계산하고 변환 수행.
x_test_scaled = scaler.transform(x_test) # [문법] transform: 학습 시 사용된 기준을 바탕으로 테스트 데이터 변환.

# [개념] K-NN은 K값이 중요: K 값 변화에 따른 정확도 비교로 최적의 K 값 얻기
# [개념] K 값이 너무 작으면 과적합(Overfitting), 너무 크면 과소적합(Underfitting) 발생 위험.
train_acc = []
test_acc = []
k_range = range(3, 11) # [문법] range(3, 11): K값을 3부터 10까지 변화시키며 테스트.
for k in k_range:
    model = KNeighborsClassifier(n_neighbors=k) # [문법] n_neighbors: 탐색할 이웃의 개수 설정.
    model.fit(x_train_scaled, y_train) # [문법] fit(): 학습 데이터를 모델에 저장.
    # 예측
    y_train_pred = model.predict(x_train_scaled) # [문법] predict(): 학습 데이터에 대한 예측 수행.
    y_test_pred = model.predict(x_test_scaled)
    # 정확도
    train_acc.append(accuracy_score(y_train, y_train_pred)) # [문법] accuracy_score: 실제값과 예측값의 일치 비율 계산.
    test_acc.append(accuracy_score(y_test, y_test_pred))

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.figure() # [문법] plt.plot: K값 변화에 따른 학습/테스트 정확도 추이를 선 그래프로 시각화.
plt.plot(k_range, train_acc, marker='s', label='train')
plt.plot(k_range, test_acc, marker='o', label='test')
plt.xlabel('K value')
plt.ylabel('Accuracy')
plt.legend()
plt.title('K-NN Accuracy comparison')
plt.tight_layout()
plt.grid()
plt.show()

# 최적 k 값 찾기
# [문법] np.argmax(): 배열 내에서 최대값을 가진 요소의 인덱스를 반환.
best_k = k_range[np.argmax(test_acc)] 
print('최적의 K 값 : ', best_k) # 그래프에서 test acc의 값이 제일 높은 지점
# [개념] 하지만 train과 test간의 차이가 크면 과적합의 위험이 있다.
# [개념] 값이 크면서 급격한 기울기가 없고, train~test 간의 차이가 가장 작은 K값을 선정 → 9
print('\n')
worst_k = k_range[np.argmin(test_acc)] # [문법] np.argmin(): 최소값을 가진 인덱스 반환.
print('최악의 K 값 : ', worst_k) #
print('\n')

# 최종 모델
best_k = 9
final_model = KNeighborsClassifier(n_neighbors=best_k)
final_model.fit(x_train_scaled, y_train) # [문법] 선정된 최적의 K값으로 최종 모델 학습.

# 예측
y_pred = final_model.predict(x_test_scaled)
print('예측값 : ', y_pred[:10])
print('실제값 : ', y_test[:10])
print('\n')
print('분류 정확도 : ', accuracy_score(y_test, y_pred)) # [문법] 전체 샘플 중 맞게 예측한 비율.
print('\n')
# [문법] classification_report: 클래스별 정밀도(Precision), 재현율(Recall), F1-score를 종합적으로 출력.
print('분류 리포트 \n', classification_report(y_test, y_pred)) 
print('\n')
# [문법] confusion_matrix: 실제 클래스와 예측 클래스의 매칭 관계를 행렬로 표현(TP, FP, FN, TN).
print('혼동 행렬 \n', confusion_matrix(y_test, y_pred)) 
print('\n')
##############################################################################
# 새로운 자료로 예측
# 1. 새로운 가상 데이터 생성 (30개의 특성)
# [개념] 실제 데이터의 평균과 표준편차를 참고하여 임의의 데이터를 만듭니다.

# [문법] np.mean(axis=0): 각 특성별 평균값 계산. reshape(1, -1)로 2차원 배열 형태 변환.
new_data_malignant = np.mean(x[y == 0], axis=0).reshape(1, -1) # 악성(0) 평균 데이터
new_data_benign = np.mean(x[y == 1], axis=0).reshape(1, -1)    # 양성(1) 평균 데이터

# 두 데이터를 합칩니다.
new_samples = np.vstack([new_data_malignant, new_data_benign])

# 스케일링
new_samples_scaled = scaler.transform(new_samples)

# 예측
new_pred = final_model.predict(new_samples_scaled)
print('새로운 데이터 예측값 : ', new_pred)
print('\n')
# [문법] predict_proba: 주변 이웃들의 비율을 바탕으로 각 클래스(0, 1)에 속할 확률을 반환함.
proba = final_model.predict_proba(new_samples_scaled)
print('새로운 데이터 예측 확률 : \n', proba)
print('\n')

# 시각화
# [추천] seaborn의 heatmap을 사용하여 혼동 행렬을 시각화하면 분류 성능을 더 직관적으로 파악할 수 있습니다.