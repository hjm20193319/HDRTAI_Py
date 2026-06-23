# Perceptron : sklearn이 제공하는 단층신경망(뉴런, 노드) 구조의 알고리즘입니다.
# 가장 단순한 형태의 신경망으로, 입력값에 가중치를 곱하고 편향을 더한 뒤 활성화 함수를 통해 출력값을 결정합니다.
# 이항분류 가능하며, 선형 분리가 가능한 문제에 주로 사용됩니다.
# [추천] 선형 분리가 불가능한 XOR 문제 등에는 MLPClassifier나 SVC(kernel='rbf') 사용을 권장합니다.
# [추천] 데이터의 스케일에 민감하므로 특성 간 단위 차이가 크다면 StandardScaler를 통한 표준화 전처리를 권장합니다.


# 실습 1 ) 논리 회로 분류
import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

feature = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# [문법] np.array(): 리스트 데이터를 넘파이 배열 형태로 변환하여 독립변수(Feature) 생성.

# and 연산 레이블
# label = np.array([0, 0, 0, 1])
# or 연산 레이블
# label = np.array([0, 1, 1, 1])
# xor 연산 레이블
label = np.array([0, 1, 1, 0])

# xor 해결 못함(단층 퍼셉트론은 선형 분리만 가능하기 때문)
ml = Perceptron(max_iter=10)     # [문법] Perceptron: max_iter(최대 학습 횟수, Epoch)를 설정하여 모델 생성.
ml.fit(feature, label) # [문법] fit(): 학습 데이터를 사용하여 최적의 가중치(W)와 편향(b)을 학습함.
pred = ml.predict(feature) # [문법] predict(): 학습된 모델을 바탕으로 입력 데이터의 클래스를 예측함.
print('예측값 : ', pred)
print('실제값 : ', label)
print('분류 정확도 : ', accuracy_score(label, pred)) # [문법] accuracy_score: 실제값과 예측값을 비교하여 정확도 계산.
print('\n')
# Perceptron은 딥러닝의 경사하강법과는 달리, 틀린 샘플에 대해서만 가중치를 조정하는 Heaviside step function 기반 알고리즘입니다.
# 작동 원리: 예측 -> 맞았는지 확인 -> 틀리면 weight(가중치)를 갱신, 맞으면 통과하는 과정을 max_iter 만큼 반복합니다.
# [추천] 확률 기반의 예측값이 필요하다면 predict_proba를 지원하는 SGDClassifier나 LogisticRegression 사용을 권장합니다.

# 실습 2 ) 일반 자료 분류
x = np.array([
    [2, 3],
    [3, 3],
    [1, 1],
    [5, 2],
    [6, 1]
])

y = np.array([1, 1, 1, -1, -1])

model = Perceptron(max_iter=100, eta0=0.1, random_state=42) # [문법] eta0: 학습률(Learning Rate)을 설정하여 가중치 갱신 강도 조절.
model.fit(x, y) # [문법] fit: 독립변수 x와 종속변수 y를 매핑하여 학습 수행.
pred = model.predict(x) # [문법] predict: 학습된 가중치를 적용하여 클래스(-1 또는 1) 예측.
print('예측값 : ', pred)
print('실제값 : ', y)
print('분류 정확도 : ', accuracy_score(y, pred))
print('\n')

# 모델 파라미터 확인
print('가중치(W) : ', model.coef_) # [문법] coef_: 각 특성(Feature)에 할당된 가중치 행렬을 반환.
print('절편(b) : ', model.intercept_) # [문법] intercept_: 모델의 편향(Bias) 또는 절편 값을 반환.
print('\n')

# 결정 경계(W1*x1 + W2*x2 + b) 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.scatter(x[:, 0], x[:, 1], c=y, cmap='bwr') # [문법] scatter: 산점도를 그리고 클래스(y)에 따라 색상을 구분.
w = model.coef_[0] # 학습된 가중치 추출
b = model.intercept_[0] # 학습된 절편 추출
x_vals = np.linspace(0, 7, 100)
y_vals = - (w[0] * x_vals + b) / w[1] # 결정 경계 방정식(w1x1 + w2x2 + b = 0)을 x2에 대해 정리
plt.plot(x_vals, y_vals, 'k') # [문법] plot: 계산된 결정 경계를 선 그래프로 시각화.
plt.title('sklearn Perceptron Decision Boundary')
plt.xlabel('X1')
plt.ylabel('X2')
plt.tight_layout()
plt.show()