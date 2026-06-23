# DBSCAN - Density Based Spatial Clustering of Applications with Noise
# - Multi Dimension의 데이터를 밀도 기반으로 서로 가까운 데이터 포인트를 함께 그룹화하는 알고리즘
# - 밀도가 다양하거나 모양이 불규칙한 클러스터가 있는 데이터, 이상치가 많은 데이터 처리에 유용

import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons

# 샘플 데이터 생성
x, y = make_moons(n_samples=200, noise=0.05, shuffle=True, random_state=0)
print(x[:5], x.shape)
print('\n')

plt.scatter(x[:, 0], x[:, 1], c=y)
plt.grid(True)
plt.tight_layout()  
plt.show()

##########################
# KMeans로 군집 분류
##########################
# [문법] KMeans(n_clusters, ...): K-평균 군집화 모델 객체 생성. n_clusters는 형성할 군집의 개수
km = KMeans(n_clusters=2, random_state=0, init='k-means++')
# [문법] fit_predict(x): 모델을 학습시키고 각 데이터 포인트가 속한 클러스터 인덱스를 반환
km_pred = km.fit_predict(x)
print('km 예측 군집 id : ', km_pred[:10])
print('\n')

# km 결과 시각화
def plotResult(x, pr):
    # [문법] 불리언 인덱싱(pr==0)을 사용하여 특정 군집에 속하는 데이터만 필터링하여 출력
    plt.scatter(x[pr==0, 0], x[pr==0, 1], c='blue', marker='o', s=40, label='cluster1') 
    plt.scatter(x[pr==1, 0], x[pr==1, 1], c='red', marker='s', s=40, label='cluster2')
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s=250, marker='*', c='black', label='centroids')
    plt.legend()
    plt.grid(True)
    plt.title('KMeans Clustering Result')
    plt.tight_layout()
    plt.show()

plotResult(x, km_pred)
# ↪ 분류 결과가 좋지 않다(가운데 부분 데이터를 잘못 분류)
# 설정에 따라 무조건 2개로 분류, 반달을 기준으로 자르기 됨

##########################
# DBSCAN으로 군집 분류
##########################
# [문법] DBSCAN(eps, min_samples, metric): 밀도 기반 군집화 모델 생성
# eps : 샘플 간 최대 거리 (반경)
# min_samples : 핵심 포인트(Core Point)가 되기 위해 eps 반경 내에 있어야 하는 최소 샘플 수
# metric : 거리 측정 방식 (기본값 'euclidean')
db = DBSCAN(eps=0.2, min_samples=5, metric='euclidean')
db_pred = db.fit_predict(x)
print('db 예측 군집 id : ', db_pred[:10])
print('\n')
print('군집 종류 : ', set(db_pred)) # 0, 1 → -1은 노이즈(이상치)를 의미함. 현재는 이상치가 없는 상태
print('\n')

# db 결과 시각화
plotResult(x, db_pred)
# ↪ 분류가 제대로 됨
# 데이터 모양에 따라 군집을 형성

##############################################
# KMeans는 k개에 따라 군집의 개수를 맞추고
# DBSCAN은 밀도에 의해 형태를 맞춘다
##############################################
# [추천] 최적의 eps를 찾기 위해 NearestNeighbors의 kneighbors_graph를 이용한 k-dist 그래프를 그려볼 수 있음