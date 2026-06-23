# [K-means Clustering]
# : 비계층적 군집 분석의 대표적인 알고리즘으로, 데이터를 k개의 군집으로 나누며 각 데이터와 군집 중심점 간의 거리를 최소화하는 방식
# | Iris 데이터셋을 활용한 군집 분석, 정량 평가, cluster 별 평균 비교(ANOVA) 수행
# | 보고서 작성 시 활용하기 좋은 분석 절차 포함

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score, normalized_mutual_info_score, silhouette_score
# [문법] adjusted_mutual_info_score: AMI - 군집 결과와 실제 라벨 간의 상호 정보량을 조정하여 비교
# [문법] normalized_mutual_info_score: NMI - 정보량 기반 유사도(두 라벨링이 얼마나 같은 정보를 공유하는가)
# [문법] silhouette_score: 실루엣 계수 - 군집 자체의 품질 평가(군집 내 응집도와 군집 간 분리도를 측정)
from sklearn.decomposition import PCA   # [문법] PCA: 주성분 분석을 통해 고차원 데이터를 저차원(예: 4차원 -> 2차원)으로 압축

# 데이터 로드
iris = load_iris()
x = iris.data
y = iris.target
feature_names = iris.feature_names

df = pd.DataFrame(x, columns=feature_names)
print('데이터 구조 : ', df.shape)
print('\n')

# Scaling
# [문법] StandardScaler(): 각 특성의 평균을 0, 표준편차를 1로 변환하여 데이터의 스케일을 맞춤 (거리 기반 알고리즘인 KMeans에서 필수 권장)
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
print('스케일링 결과(2개) : \n', x_scaled[:2])
print('\n')

# PCA
# [문법] PCA(n_components): 유지할 주성분의 개수를 지정. 여기서는 시각화를 위해 2차원으로 설정
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)
# [문법] explained_variance_ratio_: 각 주성분이 전체 분산의 몇 %를 설명하는지 반환
print('PCA 설명 분산 비율 : ', pca.explained_variance_ratio_)
print('\n')

# KMeans 모델
k = 3
# [문법] KMeans(n_clusters, init, n_init, ...): K-평균 군집화 모델 객체 생성
# n_clusters: 형성할 군집의 개수 (k)
# init='k-means++': 초기 중심점을 효율적으로 배치하여 수렴 속도 향상
# n_init: 초기 중심점 시도 횟수 (가장 좋은 결과 선택)
kmeans = KMeans(n_clusters=k, random_state=42, init='k-means++', n_init=10)
# [문법] fit_predict: 모델을 학습시키고 각 데이터 포인트가 속한 클러스터 인덱스를 반환
clusters = kmeans.fit_predict(x_scaled) # [추천] PCA 데이터(x_pca)보다 원본 스케일링 데이터(x_scaled)로 학습하는 것이 정보 손실이 적음
df['cluster'] = clusters
# [문법] cluster_centers_: 학습된 모델에서 계산된 각 군집의 중심점 좌표를 반환
print('클러스터 중심 값(스케일링 기준) : \n', kmeans.cluster_centers_)
print('\n')

plt.figure(figsize=(6,5))
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=clusters, palette='Set1')
plt.title('Iris data with KMeans clustering')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.tight_layout()
plt.show()

# [문법] pd.crosstab(index, columns): 실제 라벨과 군집 결과 간의 빈도수를 표 형태로 나타내어 일치 여부 확인
# 실제 라벨과 군집 비교(교차표)
ct = pd.crosstab(y, clusters)
print(ct)
print('\n')
# col_0   0   1   2     -> 열 : 군집 번호(KMeans 결과)
# row_0            
# 0       0  50   0     > setosa
# 1      39   0  11     > versicolor - 섞임
# 2      14   0  36     > verginica  - 섞임
# 행 : 실제 라벨(iris)

# 정량 평가
# [문법] adjusted_rand_score: ARI - 무작위 할당을 보정한 군집 유사도 지표 (0.7 이상이면 매우 우수)
ari = adjusted_rand_score(y, clusters)
ari_mi = adjusted_mutual_info_score(y, clusters)
nmi = normalized_mutual_info_score(y, clusters)
# [문법] silhouette_score: 전체 데이터의 평균 실루엣 계수 계산 (1에 가까울수록 군집화가 잘 됨)
sil_score = silhouette_score(x_scaled, clusters)

print(f'ARI : {ari:.4f}') # [추천] 군집 평가 시 ARI와 AMI를 함께 확인하는 것이 일반적임
print(f'AMI : {ari_mi:.4f}')
print(f'NMI : {nmi:.4f}') 
print(f'Silhouette Score : {sil_score:.4f}')
print('\n')
# 실루엣 계수는 1에 근사할수록 좋음 0 또는 음수면 잘못된 군집
# 좋은 군집이란 군집 내 요소끼리는 가깝고(응집도), 다른 군집 간에는 거리가 멀다(분리도).

# k=3을 사용했는데 과연 3이 합리적인지 확인 : 엘보우
inertia_list = []
# [문법] inertia_: 각 샘플과 가장 가까운 군집 중심 간의 거리 제곱 합(SSE). 값이 작을수록 군집 내 응집도가 높음
# 엘보우 기법: k값을 늘려가며 inertia 변화를 관찰하여 기울기가 급격히 완만해지는 지점(Elbow)을 최적의 k로 판단
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, init='k-means++', n_init=10)
    kmeans.fit(x_scaled)
    inertia_list.append(kmeans.inertia_)
plt.figure(figsize=(6, 4))
plt.plot(k_range, inertia_list, marker='o', linestyle='--')
plt.title('엘보우 기법')
plt.xlabel('클러스터 수(k)')
plt.ylabel('inertia_list')
plt.grid(True)
plt.tight_layout()
plt.show()      # K가 3인 경우가 가장 적당(3에서 기울기가 완만해짐)

# 실제 VS 군집 비교 시각화 
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=y, palette='Set1')
plt.title('실제 라벨')
plt.subplot(1, 2, 2)
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=clusters, palette='Set1')
plt.title('군집 결과')
plt.tight_layout()
plt.show()

# 클러스터별 평균 분석
# [문법] groupby('cluster').mean(): 생성된 군집별로 각 특성(Feature)의 평균값을 계산
cluster_mean = df.groupby('cluster').mean()
print('클러스터별 평균 : \n', cluster_mean)
print('\n')

# 군집 3개 : 군집 간 평균차이 검정(ANOVA)
# [문법] f_oneway: 세 개 이상의 집단 간 평균 차이가 유의미한지 검정하는 일원분산분석 함수
from scipy.stats import f_oneway

for col in feature_names:       # 각 군집별 데이터 분리
    group0 = df[df['cluster'] == 0][col] # [문법] 불리언 인덱싱을 사용하여 특정 클러스터에 해당하는 데이터만 추출
    group1 = df[df['cluster'] == 1][col]
    group2 = df[df['cluster'] == 2][col]
    # ANOVA 수행
    f_statistic, p_value = f_oneway(group0, group1, group2)
    print(f'{col} : f-statistic = {f_statistic:.4f}, p-value = {p_value:.4f}')

    # 해석
    if p_value >= 0.05:
        print('군집 간 평균의 차이가 통계적으로 유의미하지 않음')
    else:
        print('군집 간 평균의 차이가 통계적으로 유의미하다')

# KMeans가 꽃받침, 꽃잎 길이/너비를 제대로 군집분석 했음을 알 수 있다

# 사후 검정
# [문법] pairwise_tukeyhsd: ANOVA 결과 유의미한 차이가 있을 때, 구체적으로 어떤 군집 쌍 간에 차이가 있는지 검정
from statsmodels.stats.multicomp import pairwise_tukeyhsd
# petal length로 작업
feature = 'petal length (cm)'
tukey = pairwise_tukeyhsd(
    # [문법] endog: 분석할 데이터, groups: 그룹 라벨, alpha: 유의수준
    endog=df[feature],
    groups=df['cluster'],
    alpha=0.05
)
print('tukeyhsd 결과(petal length) : \n', tukey.summary())
print('\n')
# tukeyhsd 결과(petal length) : 
# Multiple Comparison of Means - Tukey HSD, FWER=0.05
# ===================================================
# group1 group2 meandiff p-adj  lower   upper  reject
# ---------------------------------------------------
#      0      1  -2.9078   0.0 -3.1405 -2.6751   True
#      0      2   1.1408   0.0  0.9043  1.3773   True
#      1      2   4.0486   0.0  3.8088  4.2884   True
# ---------------------------------------------------

# 사후 검정 시각화
# [문법] plot_simultaneous(): 각 그룹의 신뢰구간을 시각화하여 겹치지 않으면 유의미한 차이가 있다고 판단
tukey.plot_simultaneous(figsize=(6, 4))
plt.title(f'tukeyhsd 시각화 - {feature}')
plt.xlabel('평균 차이')
plt.tight_layout()
plt.show()
# 겹치는 부분이 없으므로 평균의 차이가 있음을 확인
print('\n')

# 군집별 boxplot
# [문법] sns.boxplot: 군집별 데이터의 분포(중앙값, 사분위수, 이상치 등)를 시각적으로 비교
for col in feature_names:
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='cluster', y=col, data=df, palette='Set1')
    plt.title(f'{col} - boxplot')
    plt.tight_layout()
    plt.show()

# 클러스터 평균 분석 마지막 열에 Type 추가
cluster_mean['label'] = ['Type A', 'Type B', 'Type C']
print(cluster_mean)