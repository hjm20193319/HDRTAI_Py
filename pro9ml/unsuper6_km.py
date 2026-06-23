# 비계층적 군집 분석 (Non-Hierarchical Clustering)
# : 데이터를 k개의 군집으로 나누며, 각 데이터와 군집 중심점 간의 거리를 최소화하는 방식
# [K-means Clustering 알고리즘]
# 1. k개의 중심점(Centroid) 임의 배치
# 2. 모든 자료와 k개의 중심점과의 거리를 계산하여 가장 가까운 중심점의 군집으로 할당
# 3. 군집의 중심을 구함(평균)
# 4. 군집의 변화가 없거나 중심점 이동이 임계값 이하일 때까지 반복

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import KMeans
# 가상의 고객 데이터 생성
np.random.seed(0)
n_customers = 200   # 고객 200명 대상
annul_spending = np.random.normal(50000, 15000, n_customers)    # 연간 지출액
monthly_visits = np.random.normal(5, 2, n_customers)    # 월 방문 횟수

# 구간 나누기(음수 제거 - clip을 사용해 상,하한선 제한)
# [문법] np.clip(array, min, max): 배열의 요소가 지정된 범위를 벗어날 경우 범위를 제한함. 예시) a = np.array([-3.2, -0.5, 1.7]) -> np.clip(a, 0, 1) -> [0, 0, 1]
annul_spending = np.clip(annul_spending, 0, None)
monthly_visits = np.clip(monthly_visits, 0, None)

data = pd.DataFrame({
    '연간 지출액': annul_spending,
    '월 방문 횟수': monthly_visits
})
# [추천] 데이터의 스케일 차이가 크므로(지출액 vs 방문횟수) StandardScaler를 사용하여 스케일링을 진행하는 것이 권장됨
print(data.head())
print()
print(data.size)
print('\n')

# 시각화 - 산포도
plt.scatter(data['연간 지출액'], data['월 방문 횟수'])
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.title('소비자 분포')
plt.grid(True)
plt.tight_layout()
plt.show()

# KMeans 군집화
# [문법] KMeans(n_clusters, ...): K-평균 군집화 모델 객체 생성. n_clusters는 형성할 군집의 개수
kmeans = KMeans(n_clusters=3, random_state=0)
# [문법] fit_predict(X): 모델을 학습시키고 각 데이터 포인트가 속한 클러스터 인덱스를 반환
clusters = kmeans.fit_predict(data) 

# 군집 결과 시각화
data['cluster'] = clusters
print(data.head())
print('\n')

# [문법] np.unique: 배열 내 중복되지 않는 고유한 값들을 반환
for cluster_id in np.unique(clusters):
    cluster_data = data[data['cluster'] == cluster_id]
    # cluster 별로 데이터 보기
    print(cluster_data)
    plt.scatter(cluster_data['연간 지출액'], cluster_data['월 방문 횟수'], label=f'Cluster {cluster_id}')
# [문법] cluster_centers_: 학습된 모델에서 계산된 각 군집의 중심점 좌표를 반환
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='X', c='black', s=200, label='Centroids')
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.title('소비자 군집 현황')
plt.legend()
plt.grid(True)
plt.tight_layout()
# [추천] 엘보우(Elbow) 기법이나 실루엣(Silhouette) 분석을 통해 최적의 k값을 결정할 수 있음
plt.show()