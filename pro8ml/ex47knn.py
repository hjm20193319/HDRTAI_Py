# 최근접 이웃(K-Nearest Neighbors)
# 새로운 데이터가 주어졌을 때 가장 가까운 K개의 이웃 데이터를 찾아 그들의 다수결로 클래스를 분류하는 알고리즘입니다.
# 별도의 학습 과정 없이 데이터를 저장해두었다가 예측 시점에 거리를 계산하는 게으른 학습(Lazy Learning) 모델입니다.

from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터
# [추천] K-NN은 거리 기반 알고리즘이므로 특성(Feature)들의 스케일이 다를 경우 StandardScaler 등을 이용한 표준화 전처리가 필수적입니다.
train = [
    [5,3,2],
    [1,3,5],
    [4,5,7]
]
label = [0, 1, 1] # 종속변수(Label): 분류하고자 하는 정답 클래스

# [문법] plt.plot: 학습 데이터의 분포를 시각적으로 확인하기 위해 마커('o')를 사용하여 그래프를 생성합니다.
plt.plot(train, 'o') 
plt.xlim([-1, 5])
plt.ylim([0, 8])
plt.show()

# 모델
# [문법] KNeighborsClassifier: n_neighbors(K값)는 이웃의 수를 결정하며, weights='distance'는 가까운 이웃에 더 큰 가중치를 부여합니다.
# [추천] K값이 너무 작으면 과적합(Overfitting), 너무 크면 과소적합(Underfitting)이 발생하므로 교차 검증을 통해 최적의 K를 찾는 것이 좋습니다.
kmodel = KNeighborsClassifier(n_neighbors=3, weights='distance') 

kmodel.fit(train, label) # [문법] fit(): 학습 데이터를 모델에 저장하여 예측을 위한 준비를 수행합니다.

pred = kmodel.predict(train) # [문법] predict(): 학습된 모델을 사용하여 입력 데이터의 클래스를 예측합니다.
print('예측값 : ', pred)
print('\n')
# [문법] model.score(): 학습 데이터에 대한 분류 정확도(Accuracy)를 계산하여 반환합니다.
print(f'test acc : ', {kmodel.score(train, label)}) 
print('\n')

# 새로운 데이터 예측
new_data = [[1,2,9], [6,2,1]] 
new_pred = kmodel.predict(new_data) # [문법] 새로운 샘플에 대해 가장 가까운 이웃을 찾아 클래스를 결정합니다.
print('예측값 : ', new_pred)
print('\n')