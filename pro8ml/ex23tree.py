# Decision Tree 의사 결정 나무 분류 모델 : 분류 모델
# [개념] 데이터 균일도(Gini, Entropy)에 따른 규칙 기반의 결정 트리.
# [개념] Entropy: 정보 불순도를 측정하는 지표. 0에 가까울수록 데이터가 균일함을 의미함.

# 키, 머리카락 길이 데이터로 남여 구분

from sklearn.tree import DecisionTreeClassifier, plot_tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터
x = [[180, 15], [177, 42], [156, 35], [174, 65], [161, 25], [160, 45], [170, 65], [155, 55]]
y = ['man', 'woman', 'woman', 'man', 'woman', 'man', 'man', 'man']   # [개념] 종속변수(Label): 0, 1로 나누지 않아도 상관 없다(범주형 문자열 지원)

feature_names = ['height', 'hair_length']

# 모델 생성
# [문법] criterion='entropy': 정보 이득(Information Gain)을 최대화하기 위해 엔트로피 불순도 사용.
# [문법] max_depth=3: 트리의 최대 깊이를 제한하여 모델의 복잡도를 조절함.
model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0) 
model.fit(x, y) # [문법] fit(): 독립변수와 종속변수를 전달하여 지도 학습(Supervised Learning) 수행.

# 분류 모델 성능 점수
# [문법] model.score(): 학습된 모델의 정확도(Accuracy)를 반환함.
print('정확도 : ', model.score(x, y)) 
print('예측값 : ', model.predict(x)) # [문법] predict(): 학습된 규칙에 따라 입력 데이터의 클래스를 예측함.
print('실제값 : ', y)
print('\n')
# [추천] 과적합 방지를 위해 train_test_split을 사용하여 학습 데이터와 검증 데이터를 분리하는 것을 권장함.

# 새로운 데이터
new_data = [[177, 78]]
print('새로운 데이터 예측 : ', model.predict(new_data))
print('\n')

# 시각화
plt.figure(figsize=(10, 6))
# [문법] plot_tree: 결정 트리의 분기 규칙과 노드 정보를 시각화함.
# [문법] filled=True: 노드의 클래스 비중에 따라 색상을 채움. rounded=True: 노드 상자를 둥글게 표현.
plot_tree(model, feature_names=feature_names, class_names=model.classes_, filled=True, rounded=True, fontsize=12)
plt.tight_layout()
plt.title('Decision Tree')
plt.show()