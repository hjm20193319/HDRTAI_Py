# 계층적 군집 분석
# : 데이터를 단계적으로 묶어 군집을 형성하는 알고리즘
# | 거리가 가까운 데이터를 계속 묶어가는 방식
# | 군집 수를 미리 정하지 않아도 됨
# | 구조는 Dendrogram으로 확인

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler    # 권장
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

# [문법] load_iris(): 사이킷런에서 제공하는 붓꽃(Iris) 데이터셋을 불러오는 함수
iris = load_iris()
x = iris.data
y = iris.target

df = pd.DataFrame(x, columns=iris.feature_names)
print(df.head())
print('\n')

# Scaling (데이터 스케일링)
# [문법] StandardScaler(): 평균을 0, 표준편차를 1로 변환하여 데이터의 단위를 맞춤
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# 계층적 군집 분석 수행
# [문법] linkage(data, method='ward'): 워드 연결법을 사용하여 군집 간 오차 제곱합을 최소화하며 병합
z = linkage(x_scaled, method='ward')

# Dendrogram (계통도 시각화)
plt.figure(figsize=(12, 6))
dendrogram(z)   # [문법] dendrogram: linkage 함수로 생성된 계층 구조를 시각화
plt.title('Iris data with hierarchy clustering')
plt.xlabel('sample index')
plt.ylabel('distance(ward)')
plt.tight_layout()
plt.show()

# 덴드로그램을 잘라서 최대 3개의 군집 만들기 (Flat Clustering)
# [문법] fcluster(Z, t, criterion): 계층적 군집 결과로부터 특정 기준(t)에 따라 평면적인 군집을 형성
clusters = fcluster(Z=z, t=3, criterion='maxclust')
df['cluster'] = clusters
print(df.head())
print('\n')

# 2개 feature 시각화
plt.figure(figsize=(6, 5))
# [문법] sns.scatterplot: 산점도를 그리는 함수. hue=clusters : 군집 결과에 따라 색을 달리 표시, palette='Set1' : 색상 스타일 지정
sns.scatterplot(x=x_scaled[:, 0], y=x_scaled[:, 1], hue=clusters, palette='Set1')
plt.title('Iris data with hierarchy clustering')
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.tight_layout()
plt.show()  # 꽤 비슷하게 나눠짐 / 군집은 정답 라벨이 없음

print('실제 라벨 : ', y[:10])
print('군집 결과 : ', clusters[:10])
# 실제 라벨 :  [0 0 0 0 0 0 0 0 0 0]
# 군집 결과 :  [1 1 1 1 1 1 1 1 1 1]
print('\n')
# 실제 0이 군집 1로 군집화 됨

# 군집 결과 검증
# 교차표(Contingency Table) : 실제 라벨 VS 군집 결과
# [문법] pd.crosstab(index, columns): 두 요인 간의 빈도수를 표 형태로 나타냄
ct = pd.crosstab(y, clusters)
print(ct)
print('\n')

# 교차표 보조 설명
# 각 실제 클래스가 가장 많이 속한 군집
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idxmax()
    print(f'실제 클래스 {i}가 가장 많이 속한 군집 : {max_cluster}, 개수 : {ct.iloc[i].max()}')
print('\n')

# 정량적 평가 (External Evaluation)
# : 군집 결과가 실제 정답(Ground Truth)과 얼마나 유사한지를 수치로 표현
from sklearn.metrics import adjusted_mutual_info_score, normalized_mutual_info_score

# [문법] adjusted_mutual_info_score: AMI - 두 라벨링 사이의 상호 정보량을 조정하여 계산 (ARI와 유사한 용도)
# ARI(Adjusted Rand Index) 개념: 무작위로 할당된 군집의 점수를 0으로 보정하여 같은 그룹끼리 잘 묶였는지 평가
# 해석 기준
# 0.7 이상 : 매우 잘 된 그룹
# 0.5 ~ 0.7 : 잘 된 그룹
# 0.5 미만 : 문제 있음
print(f'ARI : {adjusted_mutual_info_score(y, clusters):.4f}')

# [문법] normalized_mutual_info_score: NMI - 정보량 기준 얼마나 유사한지 확인(그룹 간 얼마나 같은 정보를 공유하는가)
# 해석 기준
# 1 : 완벽
# 0 : 완전 다름
print(f'NMI : {normalized_mutual_info_score(y, clusters):.4f}')