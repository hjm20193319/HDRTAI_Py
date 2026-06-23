# 비계층적 군집 분석 Non Hierachical Clustering
# : 주어진 데이터를 k개의 군집으로 나눔
# 원하는 군집의 수 k 는 사전에 지정
# [K-means Clustering 알고리즘]
# : 군집의 중심이 되는 k개의 seed 점들을 선택
# | seed와 거리가 가까운 개체들을 그룹화 하는 방법

# 1. k개의 중심점 임의 배치
# 2. 모든 자료와 k개의 중심점과의 거리를 계산하여 가장 가까운 중심점의 군집으로 할당
# 3. 군집의 중심을 구함( 평균 )
# 4. 정지 규칙에 이를 때까지 단계 반복
#     - 군집의 변화가 없을 때
#     - 중심점의 이동이 임계값 이하일 때
#     - 왜곡값이 줄어들었다가 다시 늘어나는 지점(distortion : 각 클러스터의 거리제곱의 총합)

# 실습 1 ) - make_blobs 사용
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import koreanize_matplotlib

# [문법] make_blobs(n_samples, n_features, centers, ...): 가상의 클러스터 데이터를 생성하는 함수
x, _ = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, shuffle=True, random_state=0)
# n_samples: 생성할 총 데이터 개수
# n_features: 데이터의 특성(차원) 수
# centers: 생성할 군집(클러스터)의 개수
# cluster_std: 클러스터 내 데이터의 표준편차 (값이 작을수록 뭉쳐 있음)
print(x[:3], ' ', x.shape)  # (150, 2)
print('\n')

# 시각화 - 산포도
plt.scatter(x[:, 0], x[:, 1], c='blue', marker='o', s=50)
plt.grid(True)
plt.tight_layout()
plt.show()

# KMeans 모델 작성
# cluster 의 중심을 선택하는 방법
init_centroid = 'random'    # 'random': 초기 중심점을 데이터 중에서 무작위로 선택 (수렴 속도가 느릴 수 있음)
init_centroid = 'k-means++' # 'k-means++': 초기 중심점들이 서로 멀리 떨어지도록 선택하는 알고리즘 (기본값, 더 효율적이고 안정적인 결과 제공)

kmodel = KMeans(n_clusters=3, init=init_centroid, n_init=10, max_iter=300, random_state=0)
# [문법] KMeans(n_clusters, init, n_init, ...): K-평균 군집화 모델 객체를 생성
# n_clusters: 형성할 군집의 개수 (k). 사전에 결정해야 함.
# n_init: 초기 중심점 시도 횟수 (가장 좋은 결과 선택)
# max_iter: 한 번의 실행에서 수행할 최대 반복 횟수
pred = kmodel.fit_predict(x)    # 클러스터링으로 구분한 결과 얻기
print(pred) # 0, 1, 2 로 나눠짐
print('\n')

# 각 그룹별 보기
# print(x[pred==0])
# print(x[pred==1])
# print(x[pred==2])

print('중심정 : \n', kmodel.cluster_centers_)
#  [[-1.5947298   2.92236966]
#  [ 2.06521743  0.96137409]
#  [ 0.9329651   4.35420712]]
print('\n')

# 시각화
plt.scatter(x[pred==0, 0], x[pred==0, 1], c='red', marker='o', s=50, label='cluster 1')
plt.scatter(x[pred==1, 0], x[pred==1, 1], c='blue', marker='o', s=50, label='cluster 2')
plt.scatter(x[pred==2, 0], x[pred==2, 1], c='green', marker='o', s=50, label='cluster 3')
# 각 군집 중심점 표시
plt.scatter(kmodel.cluster_centers_[:, 0], kmodel.cluster_centers_[:, 1], s=250, marker='*', c='black', label='centroids')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# KMeans의 k 값은? elbow or silhouette 기법을 이용해 k값 얻기
# 1. elbow 기법
def elbow(x):
    sse = []
    for i in range(1, 11):
        km = KMeans(n_clusters=i, init=init_centroid, random_state=0)
        km.fit(x)
        sse.append(km.inertia_) # [문법] inertia_: 각 샘플과 가장 가까운 군집 중심 간의 거리 제곱 합(SSE)
    plt.plot(range(1, 11), sse, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('SSE')
    plt.title('Elbow Method')
    plt.tight_layout()
    plt.show()

elbow(x)

# 2. silhouette 기법

# 실루엣(silhouette) 기법
# 클러스터링의 품질을 정량적으로 계산해 주는 방법이다.
# 클러스터의 개수가 최적화되어 있으면 실루엣 계수의 값은 1에 가까운 값이 된다.
# 실루엣 기법은 k-means 클러스터링 기법 이외에 다른 클러스터링에도 적용이 가능하다

import numpy as np
from sklearn.metrics import silhouette_samples

# 데이터 X와 X를 임의의 클러스터 개수로 계산한 k-means 결과인 y_km을 인자로 받아 각 클러스터에 속하는 데이터의 실루엣 계수값을 수평 막대 그래프로 그려주는 함수를 작성함.
# y_km의 고유값을 멤버로 하는 numpy 배열을 cluster_labels에 저장. y_km의 고유값 개수는 클러스터의 개수와 동일함.

def plotSilhouette(x, pred):
    cluster_labels = np.unique(pred) # [문법] np.unique: 배열 내 중복되지 않는 고유한 값들을 정렬하여 반환
    n_clusters = cluster_labels.shape[0]   # 클러스터 개수를 n_clusters에 저장
    sil_val = silhouette_samples(x, pred, metric='euclidean')  # [문법] silhouette_samples: 모든 개별 데이터의 실루엣 계수를 계산
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []

    for i, c in enumerate(cluster_labels):
        # 각 클러스터에 속하는 데이터들에 대한 실루엣 값을 수평 막대 그래프로 그려주기
        c_sil_value = sil_val[pred == c]
        c_sil_value.sort()
        y_ax_upper += len(c_sil_value)

        plt.barh(range(y_ax_lower, y_ax_upper), c_sil_value, height=1.0, edgecolor='none')
        yticks.append((y_ax_lower + y_ax_upper) / 2)
        y_ax_lower += len(c_sil_value)

    sil_avg = np.mean(sil_val)         # 평균 저장

    plt.axvline(sil_avg, color='red', linestyle='--')  # 계산된 실루엣 계수의 평균값을 빨간 점선으로 표시
    plt.yticks(yticks, cluster_labels + 1)
    plt.ylabel('클러스터')
    plt.xlabel('실루엣 개수')
    plt.title('Silhouette Analysis')
    plt.show() 

# 그래프를 보면 클러스터 1~3 에 속하는 데이터들의 실루엣 계수가 0으로 된 값이 아무것도 없으며, 실루엣 계수의 평균이 0.7 보다 크므로 잘 분류된 결과라 볼 수 있다.
X, y = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, shuffle=True, random_state=0)
km = KMeans(n_clusters=3, random_state=0) 
y_km = km.fit_predict(X)

plotSilhouette(X, y_km)