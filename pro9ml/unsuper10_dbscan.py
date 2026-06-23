# DBSCAN(Density-Based Spatial Clustering of Applications with Noise)
# : 밀도 기반 군집 분석으로, 점들이 밀집한 영역을 클러스터로 인식하고 기하학적인 모양의 군집도 잘 찾아내며 이상치(Noise)를 효과적으로 구분함

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# 일반적으로 계층적/비계층적 군집 분석을 선행하고, 마음에 안들면 DBSCAN을 함

np.random.seed(42)

# data 생성
vip = pd.DataFrame({
    '연간 지출액':np.random.normal(700, 40, 80),
    '월 방문 횟수':np.random.normal(20, 2, 80),
    '평균 구매량':np.random.normal(80, 10, 80),
    '그룹':'vip'
})

# 일반 고객
normal = pd.DataFrame({
    '연간 지출액':np.random.normal(300, 100, 150),
    '월 방문 횟수':np.random.normal(10, 4, 150),
    '평균 구매량':np.random.normal(30, 15, 150),
    '그룹':'normal'
})

# 저활동 고객
low = pd.DataFrame({
    '연간 지출액':np.random.normal(100, 30, 70),
    '월 방문 횟수':np.random.normal(3, 1, 70),
    '평균 구매량':np.random.normal(10, 5, 70),
    '그룹':'low'
})

# print(low.head()) 데이터 확인

# 특이 패턴 고객 ( 비선형 패턴 ) - 일정하지 않은 소비 패턴
t = np.linspace(0, 3*np.pi, 60)
curve = pd.DataFrame({
    '연간 지출액':np.random.normal(0, 10, len(t)) + 200 +100*np.cos(t),
    '월 방문 횟수':np.random.normal(0, 1, len(t)) + 10 + 5* np.sin(t),
    '평균 구매량':40 + 10*np.sin(t),
    '그룹':'curve'
})

# 이상 고객 ( 이상치 ) - 너무 많이 사거나, 거의 안사거나
outliers = pd.DataFrame({
    '연간 지출액':[900, 50, 850],
    '월 방문 횟수':[10, 1, 25],
    '평균 구매량':[120, 5, 100],
    '그룹':'outlier'
})

# data 합치기
# [문법] pd.concat([df1, df2, ...], ignore_index=True): 여러 데이터프레임을 하나로 합치며, 기존 인덱스를 무시하고 새로 부여함
df = pd.concat([vip, normal, low, curve, outliers], ignore_index=True) 
print(df.head(2))
print('\n')

# 초기 데이터 시각화
import seaborn as sns
plt.figure(figsize=(6, 5))
# [문법] sns.scatterplot(x, y, hue, palette): 산점도를 그리며 hue 인자에 따라 그룹별로 색상을 다르게 표시함
sns.scatterplot(x=df['연간 지출액'], y=df['월 방문 횟수'], hue=df['그룹'], palette='Set2')
plt.title('초기 데이터 시각화')
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.legend(title='소비자 패턴')
plt.tight_layout()
plt.show()

##########################
# DBSCAN
##########################
# [추천] DBSCAN은 거리 기반 알고리즘이므로 특성 간의 단위 차이를 맞추기 위해 StandardScaler를 사용하는 것이 필수적임
scaler = StandardScaler()
# [문법] fit_transform(X): 데이터의 평균과 표준편차를 계산(fit)함과 동시에 스케일링(transform)을 수행함
x_scaled = scaler.fit_transform(df[['연간 지출액', '월 방문 횟수', '평균 구매량']])

# [문법] DBSCAN(eps, min_samples, metric): 밀도 기반 군집화 모델 생성
# eps: 이웃을 정의하기 위한 최대 거리 (반경)
# min_samples: 핵심 포인트(Core Point)가 되기 위해 eps 반경 내에 있어야 하는 최소 샘플 수
# metric: 거리 측정 방식 (기본값 'euclidean')
dbscan = DBSCAN(eps=0.5, min_samples=5, metric='euclidean')

# [문법] fit_predict(X): 모델을 학습시키고 각 데이터 포인트가 속한 클러스터 인덱스를 반환함 (-1은 노이즈/이상치를 의미)
clusters = dbscan.fit_predict(x_scaled)
df['cluster'] = clusters
print(df.head())
print('\n')

# 군집 결과 시각화
plt.figure(figsize=(6, 5))
sns.scatterplot(x=df['연간 지출액'], y=df['월 방문 횟수'], hue=df['cluster'], palette='Set1')
plt.title('군집 결과 시각화')
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.legend(title='소비자 패턴')
plt.tight_layout()
plt.show()
# 매출에 따라 3개의 군집으로 분류함

# 각 군집 평균
# [문법] groupby('cluster').mean(): 생성된 군집별로 지정된 열들의 평균값을 계산하여 특성을 파악함
print(df.groupby('cluster')[['연간 지출액', '월 방문 횟수', '평균 구매량']].mean())
print('\n')