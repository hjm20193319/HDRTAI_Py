# 전통적 방법의 선형회귀(기계학습 중 지도학습) 
# [개념] 독립변수(IQ)와 종속변수(점수) 사이의 선형적 인과관계를 분석하여 모델을 생성함.

# 방법 4 ) : scipy.stats.linregress() 사용, model 생성 X
# [개념] scipy.stats.linregress는 간단한 선형 회귀 분석을 수행하며 기울기, 절편, p-value 등을 반환함.

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
# IQ 에 따른 시험 점수 예측

# 데이터
score_iq = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/score_iq.csv')
print(score_iq.head())
print(score_iq.info())

x = score_iq['iq']
y = score_iq['score']
print('iq : \n', x[:3])
print('score : \n', y[:3])
print('\n')

# 상관계수 
# [개념] 두 변수 간의 선형적 관계의 강도를 나타냄 (0.88은 매우 강한 양의 상관관계).
print('상관계수 : ', np.corrcoef(x, y)[0, 1])   # 상관계수 :  0.8822203446134701
print(score_iq[['iq', 'score']].corr())
#             iq    score
# iq     1.00000  0.88222 
# score  0.88222  1.00000
print('\n')

# 시각화 - 상관계수
# plt.scatter(x, y)
# plt.grid(True)
# plt.title('상관계수')
# plt.show()

# 단순 선형회귀분석
# [문법] stats.linregress(x, y): 기울기(slope), 절편(intercept), 상관계수(rvalue), p-value, 표준오차를 반환함.
model = stats.linregress(x, y)
print(model.slope)  # 기울기 0.6514309527270075
print(model.intercept)  # 절편 -2.8564471221974657
print(model.pvalue) # p value 2.8476895206683644e-50    -> [개념] 유의수준 0.05보다 매우 작으므로 인과관계가 유의함.
print('\n')

# 시각화
plt.scatter(x, y)
# [추천] plt.style.use('ggplot') # 그래프의 시각적 품질을 높이기 위해 스타일 설정 권장
plt.grid(True)
plt.plot(x, model.intercept + model.slope * x, c='r')
plt.title('추세선 확인')
plt.xlabel('iq')
plt.ylabel('score')
plt.show()

# predict() 메소드를 지원하지 않음 
# [개념] stats.linregress는 sklearn이나 statsmodels와 달리 별도의 예측 함수를 제공하지 않아 수식을 직접 계산하거나 polyval을 사용함.
# 정수 예측 : np.polyval() 
# [문법] np.polyval([기울기, 절편], x): 다항식의 계수를 이용하여 입력값에 대한 결과값을 계산함.
print(np.polyval([model.slope, model.intercept], np.array(score_iq['iq'])))
print('\n')

newdf = pd.DataFrame({'iq':[55,66,77,88,150]}) 
print('특정값 정수예측 : \n', np.polyval([model.slope, model.intercept], newdf))
# 특정값 정수예측 :
#  [[32.97225528]
#  [40.13799576]
#  [47.30373624]
#  [54.46947672]
#  [94.85819579]]
print('\n')