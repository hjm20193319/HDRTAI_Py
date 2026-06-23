# MLP(Multi-Layer Perceptron) - wine dataset 으로 다항 분리 (3등급)
# 여러 개의 퍼셉트론 뉴런을 층으로 쌓은 다층신경망 구조.
# 다항 분류(Multinomial Classification): 종속변수의 범주가 3개 이상인 경우 사용함.
# 역전파(Backpropagation): 예측 오차를 최소화하기 위해 가중치(W)를 갱신하는 학습 과정.
# MLP는 데이터 스케일에 민감하므로 StandardScaler를 통한 표준화 전처리가 필수적임.
# [추천] 과적합 방지를 위해 hidden_layer_sizes와 alpha(규제) 파라미터를 조정하는 것을 권장함.
# [추천] classification_report를 사용하여 클래스별 정밀도, 재현율, F1-score를 확인하는 것을 권장함.

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


data = load_wine() # [문법] load_wine(): 사이킷런에서 제공하는 와인 성분 데이터셋 로드.
x = data.data
y = data.target
print(x[:3], ' ', x.shape)  # [문법] 독립변수(Feature) 상위 3개 행 및 전체 모양(178, 13) 확인.
print(y[:3], ' ', np.unique(y)) # [문법] np.unique(): 종속변수의 고유한 클래스 종류(0, 1, 2) 확인.
print('\n')

# 분리
# [문법] train_test_split: 데이터를 학습용(80%)과 테스트용(20%)으로 분리. stratify=y로 클래스 비율 유지.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y) 

# 스케일링 (MLP는 가중치 최적화를 위해 표준화 권장)
scaler = StandardScaler() # [문법] StandardScaler: 평균 0, 표준편차 1로 표준화하는 클래스.
x_train_scaled = scaler.fit_transform(x_train) # [문법] fit_transform: 학습 데이터의 통계량을 계산하고 변환 수행.
x_test_scaled = scaler.transform(x_test) # [문법] transform: 학습 시 사용된 기준을 바탕으로 테스트 데이터 변환.

# 모델 생성
# [문법] MLPClassifier: hidden_layer_sizes(은닉층 노드), activation(활성화함수), solver(최적화방식) 설정.
model = MLPClassifier(hidden_layer_sizes=(20, 10), activation='relu', solver='adam', learning_rate_init=0.001, max_iter=150, random_state=42, verbose=1)
# 은닉층 2개 / 노드 개수 / 활성화 함수는 relu / 손실 최소화 함수 adam / 학습율 0.001 / 학습 횟수 / 학습 도중 로그 출력 여부
model.fit(x_train_scaled, y_train) # [문법] fit(): 학습 데이터를 사용하여 가중치와 편향을 최적화함.

# 분류 예측
pred = model.predict(x_test_scaled) # [문법] predict(): 학습된 모델을 사용하여 테스트 데이터의 클래스를 예측함.
print('예측값 : ', pred)
print('실제값 : ', y_test)
print('분류 정확도 : ', accuracy_score(y_test, pred)) # [문법] accuracy_score: 전체 샘플 중 맞게 예측한 비율 계산.
print('\n')
print('분류 리포트 \n', classification_report(y_test, pred)) # [문법] 정밀도, 재현율, F1-score 등을 종합적으로 출력.
print('\n')
print('혼동 행렬 \n', confusion_matrix(y_test, pred)) # [문법] confusion_matrix: 실제 클래스와 예측 클래스의 매칭 관계를 행렬로 표현.
print('\n')

# 혼동 행렬 시각화
cm = confusion_matrix(y_test, pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues') # [문법] sns.heatmap: 혼동 행렬을 색상으로 시각화하여 분류 성능 파악.
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()

# MLP의 손실 곡선 시각화
plt.plot(model.loss_curve_) # [문법] loss_curve_: 학습 과정 중 각 에포크에서의 손실(Loss) 값을 담은 리스트.
plt.xlabel('Epoch(학습 횟수)')
plt.ylabel('Loss(손실)')    # 예측값과 실제값의 차이
plt.title('MLP Training Loss Curve')
plt.tight_layout()
plt.show()

# [참고]
# 미분이 MLP (딥 러닝의 옛 이름)에서 어떻게 쓰이는가?
# 미분으로 오차를 줄여나감
# MLP 구조 : 입력 -> 신경망(뉴런) -> 출력 후 오차를 확인
# 예 ) 입력(x) -> 모델 -> 예측값(y^) - 실제값(y) -> 오차(loss) 발생
#      오차함수(loss function) : L = (y - y^)   →  예측이 틀릴수록 값이 커짐
# why 미분?
#       ↪ 오차를 어떻게 줄일지 즉, 오차가 줄어드는 방향으로 W(가중치)를 갱신

# <전체 학습 과정>
# 1. 모델이 예측
# 2. 오차 계산
# 3. 미분(기울기 계산)
# 4. 가중치 W 를 갱신
# 5. 반복 (1~4) - 역전파(back propergation)