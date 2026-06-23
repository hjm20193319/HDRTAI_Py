# Decision Tree 의사결정 나무 : 분류 모델
# [개념] 데이터 균일도(Gini, Entropy)에 따른 규칙기반의 결정 트리
# [개념] 트리는 데이터를 직각(수직, 수평) 기준으로 나누면서 영역을 만든다
# [추천] 과적합(Overfitting) 방지를 위해 max_depth, min_samples_split 등의 하이퍼파라미터 튜닝이 중요함.

# [문법] make_classification: 분류 분석을 위한 가상 데이터를 생성하는 함수.
# [문법] DecisionTreeClassifier: 사이킷런에서 제공하는 의사결정나무 분류 모델 클래스.
# [문법] plot_tree: 학습된 결정 트리 구조를 시각화하는 함수.
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier, plot_tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터
# [문법] n_informative: 독립 변수 중 종속 변수와 상관관계가 있는 성분의 수.
x, y = make_classification(n_samples=100, n_features=2, n_redundant=0, n_informative=2, random_state=42)

# 모델 생성
# [개념] criterion='gini': 지니 불순도를 사용하여 노드를 분할함. (값이 작을수록 데이터가 균일함)
model = DecisionTreeClassifier(criterion='gini', max_depth=3)   # [문법] 최대 깊이 3 : Root -> child -> terminal
model.fit(x, y)     # [문법] fit(): 입력 데이터, 정답 데이터 다 제공 => Supervised learning(지도 학습)

# 트리구조 시각화
plt.figure(figsize=(10, 6))
# [문법] filled=True: 노드의 클래스 비중에 따라 색상을 채움.
plot_tree(model, feature_names=['x1', 'x2'], class_names=['0', '1'], filled=True)
plt.tight_layout()
plt.show()

# 결정 경계 시각화
# [문법] np.meshgrid: x축, y축 값을 조합해서 좌표 격자를 생성
xx, yy = np.meshgrid(np.linspace(x[:, 0].min(), x[:, 0].max(), 100), np.linspace(x[:, 1].min(), x[:, 1].max(), 100))
# x1, x2 범위를 100개의 구간으로 나눔
# [문법] np.c_: 두 개의 1차원 배열을 칼럼으로 붙여 2차원 배열 생성. 모든 좌표에 대해 예측값 계산.
z = model.predict(np.c_[xx.ravel(), yy.ravel()])
z = z.reshape(xx.shape) # [문법] 예측 결과를 원래 grid 모양으로 변환
print(z)

# 시각화
# [문법] plt.contourf: 등고선을 그리고 영역을 색으로 채워 결정경계를 표현 (contour는 선만 그림)
plt.contourf(xx, yy, z, alpha=0.3)   # 영역을 색으로 채워, 결정경계를 표현
plt.scatter(x[:, 0], x[:, 1], c=y)
plt.title('Decision Boundary')
plt.xlabel('x1')
plt.ylabel('x2')
plt.show()