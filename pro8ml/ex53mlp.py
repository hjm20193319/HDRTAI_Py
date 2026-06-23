# MLP(Multi-Layer Perceptron)
# : 여러 개의 퍼셉트론 뉴런을 여러 층으로 쌓은 다층신경망 구조
# 입력층과 출력층 사이에 하나 이상의 은닉층을 가지고 있는 신경망
# 인접한 두 층의 뉴런간에는 완전 연결 => fully connected
# 역전파(Backpropagation) 알고리즘을 통해 가중치를 갱신하며 학습함.

# 실습 1 ) 논리 회로 분류
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# [문법] np.array(): 리스트 데이터를 넘파이 배열로 변환하여 독립변수(Feature) 생성.
feature = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) 
# xor
label = np.array([0, 1, 1, 0])

# max_iter의 추천 횟수 : 500 ~ 1000 
# [문법] MLPClassifier: hidden_layer_sizes(은닉층 노드 수), solver(가중치 최적화 알고리즘), learning_rate_init(초기 학습률) 설정.
# solver='adam' => 가중치 최적화를 위한 손실(cost) 최소화 방식 중 하나.
ml = MLPClassifier(max_iter=500, hidden_layer_sizes=10, solver='adam', learning_rate_init=0.01, verbose=1)  
ml.fit(feature, label) # [문법] fit(): 학습 데이터를 사용하여 가중치(W)와 편향(b)을 최적화함.
pred = ml.predict(feature) # [문법] predict(): 학습된 모델을 바탕으로 입력 데이터의 클래스를 예측함.
print('예측값 : ', pred)
print('실제값 : ', label)
print('분류 정확도 : ', accuracy_score(label, pred)) # [문법] accuracy_score: 실제값과 예측값을 비교하여 정확도 계산.
print('\n')

# 실습 2 ) 일반 자료 분류
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

# [문법] make_moons: 초승달 모양의 비선형 분류용 가상 데이터셋을 생성함.
x, y = make_moons(n_samples=300, noise=0.2, random_state=42) 

# [문법] train_test_split: 데이터를 학습용(80%)과 테스트용(20%)으로 분리함.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42) 

# [문법] activation='relu': 은닉층에서 사용할 활성화 함수로 ReLU(Rectified Linear Unit)를 지정함.
model = MLPClassifier(max_iter=1000, hidden_layer_sizes=(10, 10), solver='adam', random_state=42, activation='relu')
model.fit(x_train, y_train)
pred = model.predict(x_test)
print('예측값 : ', pred)
print('실제값 : ', y_test)
print('분류 정확도 : ', accuracy_score(y_test, pred))
# 분류 정확도 :  0.9666666666666667
print('\n')
# [추천] MLP는 특성 스케일에 민감하므로 학습 전 StandardScaler를 통한 표준화 전처리를 권장함.