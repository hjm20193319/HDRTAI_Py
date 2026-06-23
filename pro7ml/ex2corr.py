# 공분산 / 상관계수
# [개념] 공분산은 두 변수의 변화 방향을, 상관계수는 방향과 강도를 나타냄 (-1 ~ 1 사이 값)
# [개념] 상관계수는 공분산을 각 변수의 표준편차의 곱으로 나누어 표준화한 값임.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 수집
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv')
print(data.head())
print(data.shape)   # (264, 3)
print('\n')

# 표준편차
# [문법] np.std(): 표준편차 계산. ddof=0이 기본값(모표준편차), ddof=1 설정 시 표본표준편차.
print('친밀도 표준편차:', np.std(data.친밀도))  # 0.96850
print('적절성 표준편차:', np.std(data.적절성))  # 0.8580277
print('만족도 표준편차:', np.std(data.만족도))  # 0.82717
print('\n')

# 시각화
# [추천] plt.style.use('ggplot') # 그래프 스타일을 지정하여 가시성을 높일 수 있음
# plt.hist([np.std(data.친밀도), np.std(data.적절성), np.std(data.만족도)])
# plt.show()

# 공분산
# [문법] np.cov(x, y): 공분산 행렬 반환. [0, 1] 위치의 값이 두 변수 간의 공분산.
print('친밀도-적절성 공분산:\n', np.cov(data.친밀도, data.적절성)) # 0.41642
print('친밀도-만족도 공분산:\n', np.cov(data.친밀도, data.만족도)) # 0.3756
print('적절성-만족도 공분산:\n', np.cov(data.적절성, data.만족도)) # 0.5463
print('\n')
print(data.cov())   # [문법] DataFrame.cov(): 데이터프레임 내 모든 수치형 변수 간의 공분산 행렬 반환
#           친밀도       적절성       만족도
# 친밀도 |  0.941569   0.416422      0.375663
# 적절성 |  0.416422   0.739011      0.546333
# 만족도 |  0.375663   0.546333      0.686816
print('\n')

# 상관계수
# [문법] np.corrcoef(x, y): 피어슨 상관계수 행렬 반환.
print('친밀도-적절성 상관계수:\n', np.corrcoef(data.친밀도, data.적절성))    # 0.49920861
print('친밀도-만족도 상관계수:\n', np.corrcoef(data.친밀도, data.만족도))    # 0.46714498
print('적절성-만족도 상관계수:\n', np.corrcoef(data.적절성, data.만족도))    # 0.7668527
print('\n')
print(data.corr())  # [문법] DataFrame.corr(): 데이터프레임 내 모든 수치형 변수 간의 상관계수 행렬 반환
# print(data.corr(method='pearson')) : 연속형 변수 -> 정규성을 따름
# print(data.corr(method='spearman'))  : 범주형 변수(서열) -> 정규성을 따르지 않음 (비모수 검정)
# print(data.corr(method='kendall'))  : spearman과 비슷
#           친밀도       적절성       만족도
# 친밀도 | 1.000000     0.499209     0.467145
# 적절성 | 0.499209     1.000000     0.766853
# 만족도 | 0.467145     0.766853     1.000000
print('\n')

# 만족도에 따른 다른 특성 사이의 상관관계
co_re = data.corr()
# [문법] sort_values(): 특정 열을 기준으로 데이터를 정렬함.
print(co_re['만족도'].sort_values(ascending=False))
# 만족도    1.000000
# 적절성    0.766853
# 친밀도    0.467145
print('\n')

# 시각화
# [문법] kind='scatter': 산점도 그래프를 그림. 두 변수 간의 관계를 시각적으로 파악하기 용이함.
data.plot(kind='scatter', x='적절성', y='만족도')   # 양의 상관관계(우상향) 그래프 확인
plt.show()

from pandas.plotting import scatter_matrix
attr = ['친밀도', '적절성', '만족도']
# [문법] scatter_matrix(): 여러 변수 간의 산점도와 히스토그램을 한꺼번에 그려주는 행렬 그래프.
scatter_matrix(data[attr], figsize=(12, 8)) 
plt.show()

import seaborn as sns
# [문법] sns.heatmap(): 상관계수 행렬을 색상으로 시각화. annot=True는 수치 표시.
sns.heatmap(data[attr].corr(), annot=True, cmap='coolwarm') # [추천] cmap='coolwarm'으로 양/음의 상관관계 색상 구분
plt.show()

# heatmap에 텍스트 표시 추가사항 적용해 보기
corr = data.corr()
# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool)) # [문법] np.triu: 상삼각 행렬 생성 (중복 정보 제거용 마스크)
# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
fig, ax = plt.subplots()     # Set up the matplotlib figure

sns.heatmap(corr, mask=mask, vmin=-vmax, vmax=vmax, square=True, linecolor="lightgray", linewidths=1, ax=ax)

for i in range(len(corr)):
    ax.text(i + 0.5, len(corr) - (i + 0.5), corr.columns[i], ha="center", va="center", rotation=45)
    for j in range(i + 1, len(corr)):
        s = "{:.3f}".format(corr.values[i, j])
        ax.text(j + 0.5, len(corr) - (i + 0.5), s, ha="center", va="center")
ax.axis("off")
plt.show()