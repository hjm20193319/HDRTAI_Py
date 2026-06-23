# 지도학습(KNN)과 비지도학습(KMeans)의 비교 분석 - Iris 데이터셋 활용
# 지도학습은 정답(Label)이 있는 데이터를 학습하여 분류/회귀를 수행하고,
# 비지도학습은 정답 없이 데이터의 유사성(거리 등)만을 기준으로 그룹화(Clustering)를 수행함.

from sklearn.datasets import load_iris
iris_data = load_iris()

from sklearn.model_selection import train_test_split
# [문법] train_test_split(x, y, test_size, random_state): 데이터를 학습용과 검증용으로 분리함
x_train, x_test, y_train, y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.25, random_state=42)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape) # (112, 4) (38, 4) (112,) (38,) 
print('\n')

##############################################
# 지도학습 KNN(K 최근접 이웃 알고리즘)
##############################################
from sklearn.neighbors import KNeighborsClassifier
# [문법] KNeighborsClassifier(n_neighbors, weights, metric): KNN 분류 모델 생성
# n_neighbors: 참조할 이웃의 수 (K)
# weights='distance': 거리에 반비례하여 가중치 부여
# metric='euclidean': 유클리드 거리 측정 방식 사용
knnModel = KNeighborsClassifier(n_neighbors=3, weights='distance', metric='euclidean') 
knnModel.fit(x_train, y_train)

# 예측 및 성능 확인(acc)
from sklearn.metrics import accuracy_score
# [문법] predict(X): 학습된 모델을 사용하여 새로운 데이터의 라벨을 예측
pred_label = knnModel.predict(x_test)
print('예측값 : ', pred_label[:10])
print('실제값 : ', y_test[:10])
# 예측값 :  [1 0 2 1 1 0 1 2 1 1]
# 실제값 :  [1 0 2 1 1 0 1 2 1 1]
print('\n')
# [문법] accuracy_score(y_true, y_pred): 실제값과 예측값을 비교하여 정확도를 계산
print('분류 정확도 : ', accuracy_score(y_test, pred_label)) # 분류 정확도 : 1.0
print('\n')

# 새로운 값 군집 분류
import numpy as np
new_input = np.array([[6.1, 2.8, 4.7, 1.2]]) # [추천] 새로운 데이터를 입력할 때는 학습 시 사용한 특성(Feature)의 순서와 개수를 맞춰야 함
clu_pred = knnModel.predict(new_input)
print(f'KNN 새로운 값은 라벨 {clu_pred[0]}에 속합니다.')
print('\n')

# 새로운 데이터는 몇번째 자료와 거리를 확인했을까?
# [문법] kneighbors(X): 입력 데이터와 가장 가까운 이웃들의 거리와 인덱스를 반환
dist, index = knnModel.kneighbors(new_input)
print(dist, index)
# [[0.2236068  0.3    0.43588989]] [[71 82 31]]
# K = 3 이므로 3개의 자료가 분류에 참여
# 새로운 자료와의 거리
# ==> 1번째 라벨 자료 2개가 포함되어 있어서 1번째로 분류
print('\n')

#################################################
# 비지도학습 KMeans(K 평균 비계층 군집 알고리즘)
#################################################
from sklearn.cluster import KMeans
# [문법] KMeans(n_clusters, init, ...): K-평균 군집화 모델 생성. n_clusters는 나눌 군집의 수
kmeansModel = KMeans(n_clusters=3, init='k-means++', random_state=0)
# [추천] KMeans는 거리 기반 알고리즘이므로 데이터의 스케일이 다를 경우 StandardScaler 등을 통한 스케일링이 권장됨
kmeansModel.fit(x_train)    # 비지도학습이므로 label(y_train)이 주어지지 않음
# [문법] labels_: 학습 데이터에 대해 할당된 군집 번호(0, 1, 2...)를 반환
print(kmeansModel.labels_)  
print('\n')

# 군집별 자료 보기
# [문법] 불리언 인덱싱을 통해 특정 군집(0, 1, 2)에 속한 실제 라벨(y_train)의 분포를 확인
print('0 cluster : ', y_train[kmeansModel.labels_==0])  # 0 번째 군집은 라벨 2
print('1 cluster : ', y_train[kmeansModel.labels_==1])  # 1 번째 군집은 라벨 0
print('2 cluster : ', y_train[kmeansModel.labels_==2])  # 2 번째 군집은 라벨 1
print('\n')

# 새로운 값 군집 분류
new_input = np.array([[6.1, 2.8, 4.7, 1.2]])
# [문법] predict(X): 새로운 데이터가 어느 군집 중심(Centroid)과 가장 가까운지 예측
clu_pred = kmeansModel.predict(new_input)
print(f'KMeans 새로운 값은 {clu_pred[0]} 번째 군집에 속합니다.')
print('\n')

# 군집 모델 성능 파악
# [추천] 군집 모델의 성능은 ARI, NMI, 실루엣 계수 등을 사용하여 정량적으로 평가할 수 있음
pred_cluster = kmeansModel.predict(x_test)
print('예측값 : ', pred_cluster[:10])
print('\n')

# 평가 데이터를 적용해 예측한 군집을
# 각 iris의 종류를 의미하는 라벨값으로 다시 바꿔주어야 실제 라벨과 비교해 성능 측정 가능
np_arr = np.array(pred_cluster)
print('변환 전 np_arr : ', np_arr)
print('\n')
np_arr[np_arr==0], np_arr[np_arr==1], np_arr[np_arr==2] = 3, 4, 5   # 값 중복 방지를 위한 임시 저장용 번호 부여
np_arr[np_arr==3] = 2   # 군집 3을 2(virginica)로 변경
np_arr[np_arr==4] = 0   # 군집 4를 0(setosa)로 변경
np_arr[np_arr==5] = 1   # 군집 5를 1(versicolor)로 변경
print('변환 후 np_arr : ', np_arr)
print('\n')

predict_label = np_arr.tolist()
print('예측값 : ', predict_label[:10])
print(f'군집 test acc : {np.mean(predict_label == y_test)}') # 실제 라벨과 매핑 후 정확도 계산
# 군집 test acc : 0.9473684210526315

