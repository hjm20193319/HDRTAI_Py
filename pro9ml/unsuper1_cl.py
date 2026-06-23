# 군집 분석 Clustering
# : 데이터 간의 유사도를 정의하고 그 유사도에 가까운 것부터 순서대로
# | 합쳐가는 방법으로, 거리나 상관계수 등을 이용
# | 이는 비슷한 특성을 가진 개체를 그룹으로 만들고, 군집 분리 후 t-test, ANOVA 분석 등을 통해
# | 그룹 간 평균의 차이를 확인할 수도 있음
# | 군집 분석은 데이터만 주고 Label은 제공하지 않는 비지도 학습

# 클러스터링 기법 중 계층적 클러스터링 연습
# 응집형 : 군집의 크기를 점점 늘리기 -> 상향식
# 분리형 : 군집의 크기를 점점 줄이기 -> 하향식

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(123)
var = ['x','y']
labels = ['점0','점1','점2','점3','점4']

x = np.random.random_sample([5,2])*10
df = pd.DataFrame(x, columns=var, index=labels)
print(df)
print('\n')

# 시각화
plt.scatter(df.x, df.y, c='blue', marker='o', s=50)
for i, txt in enumerate(labels):
    plt.annotate(txt, (df.x[i], df.y[i]))
plt.grid(True)
plt.tight_layout()
plt.show()

# 각 점 간의 거리 계산
from scipy.spatial.distance import pdist, squareform
dist_vec = pdist(df, metric='euclidean')    # metric='euclidean' 유클리드 거리 계산 방식
print(dist_vec)
print('\n')
# pdist의 결과를 사각형 형식으로 보기
row_dist = pd.DataFrame(squareform(dist_vec), columns=labels, index=labels)
print(row_dist)
#        점0        점1       점2       점3       점4
# 점0  0.000000  5.393133  1.388848  4.896710  2.401826
# 점1  5.393133  0.000000  5.090279  7.656440  2.998344
# 점2  1.388848  5.090279  0.000000  3.698301  2.405416
# 점3  4.896710  7.656440  3.698301  0.000000  5.792346
# 점4  2.401826  2.998344  2.405416  5.792346  0.000000
print('\n')

from scipy.cluster.hierarchy import linkage, dendrogram
# linkage : 응집형, 계층적 클러스터링
row_clusters = linkage(dist_vec, method='ward')
df2 = pd.DataFrame(row_clusters, columns=['클러스터id1', '클러스터id2', '거리', '멤버수'])
print(df2)
#    클러스터id1  클러스터id2     거리     멤버수
# 0      0.0       2.0         1.388848    2.0
# 1      4.0       5.0         2.657109    3.0
# 2      1.0       6.0         5.454004    4.0
# 3      3.0       7.0         6.647102    5.0
print('\n')

# 클러스터의 계층 구조를 계통도 dendrogram 로 출력
row_dend = dendrogram(row_clusters, labels=labels)
plt.ylabel('유클리드 거리')
plt.tight_layout()
plt.show()