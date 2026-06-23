# 비계층적 군집 분석 (Non-Hierarchical Clustering)
# : 데이터를 k개의 군집으로 나누며, 각 데이터와 군집 중심점 간의 거리를 최소화하는 방식
# [K-means Clustering 알고리즘]
# 1. k개의 중심점(Centroid) 임의 배치
# 2. 모든 자료와 k개의 중심점과의 거리를 계산하여 가장 가까운 중심점의 군집으로 할당
# 3. 군집의 중심을 구함(평균)
# 4. 군집의 변화가 없거나 중심점 이동이 임계값 이하일 때까지 반복

# 학생 10명의 시험 점수 사용

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import KMeans
import pandas as pd

students = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']
# [문법] reshape(-1, 1): 1차원 배열을 행의 개수는 자동으로 계산하고 열은 1개인 2차원 배열로 변환
scores = np.array([76,95,65,85,60,92,55,88,83,72]).reshape(-1,1)
print('점수 : ', scores)
print('\n')

# K = 3 -> 이미 알고 있는 데이터이므로(원래는 엘보우(Elbow)나 실루엣(Silhouette) 기법으로 최적의 k를 찾아야 함)
# [문법] KMeans(n_clusters, init, ...): K-평균 군집화 모델 객체 생성. init='k-means++'는 초기 중심점을 효율적으로 배치함
kmeans = KMeans(n_clusters=3, random_state=0, init='k-means++')
km_clusters = kmeans.fit_predict(scores) # [문법] fit_predict: 모델을 학습시키고 각 데이터 포인트가 속한 클러스터 인덱스를 반환
print('학생 자료 군집 결과')
for stu, cluster in zip(students, km_clusters):
    print(f'{stu} : {cluster}')
print('\n')

df = pd.DataFrame({
    '학생': students,
    '점수': scores.flatten(),
    '군집': km_clusters
})
print(df)
print('\n')

# 군집별 평균 점수
# [문법] groupby('군집')['점수'].mean(): 특정 열을 기준으로 그룹화하여 해당 그룹의 평균값을 계산
grouped = df.groupby('군집')['점수'].mean()
print(grouped)
print('\n')

# 시각화 - 학생별 군집 색으로 구분해, 산점도 출력
x_position = np.arange(len(students))
# [문법] ravel(): 다차원 배열을 1차원 배열로 평평하게(flatten) 펼쳐주는 함수
y_scores = scores.ravel()
colors = {0:'red', 1:'blue', 2:'green'}
plt.figure(figsize=(10,7))
for i, (x, y, cluster) in enumerate(zip(x_position, y_scores, km_clusters)):
    plt.scatter(x, y, c=colors[cluster], label=f'Cluster {cluster}')
    plt.annotate(students[i], (x, y+1.5), fontsize=12, ha='center')
# 중심점
# [문법] cluster_centers_: 학습된 모델에서 계산된 각 군집의 중심점 좌표를 반환
centers = kmeans.cluster_centers_
for center in centers:
    plt.scatter(len(students)//2, center[0], marker='X', c='black', s=200)

plt.xticks(x_position, students)
plt.xlabel('Students')
plt.ylabel('Students score')
plt.title('Score Cluster')
plt.legend()
plt.grid(True)
plt.tight_layout()
# [추천] plt.show() 대신 plt.savefig('kmeans_result.png')를 사용하여 시각화 결과를 이미지 파일로 저장 가능
plt.show()