import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 데이터 수집
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv', index_col=0)
print(data.head())
print(data.shape)   # (200, 4)
print('\n')

r = data.corr()
print(r)
#                  tv     radio  newspaper     sales
# tv         1.000000  0.054809   0.056648  0.782224
# radio      0.054809  1.000000   0.354104  0.576223
# newspaper  0.056648  0.354104   1.000000  0.228299
# sales      0.782224  0.576223   0.228299  1.000000
print('\n')

# sales 상관관계
rs = r['sales'].sort_values(ascending=False)
print(rs)
# sales        1.000000
# tv           0.782224
# radio        0.576223
# newspaper    0.228299

# 시각화
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.show()