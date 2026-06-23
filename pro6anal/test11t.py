# 어느 음식점의 매출 데이터와 기상청이 제공한 날씨 데이터를 활용하여
# 강수 여부에 따른 매출액의 평균에 차이가 있는지 검정
# 두 집단 : 강수량이 있을 때, 맑을 때
# [개념] 독립 표본 t-검정: 서로 다른 두 집단(비 오는 날 vs 맑은 날)의 매출액 평균이 통계적으로 유의미하게 차이가 나는지 검정함.

# 가설 수립
# 귀무 가설 : 어느 음식점의 매출 데이터는 강수 여부에 따라 매출액 평균에 차이가 없다.
# 대립 가설 : 어느 음식점의 매출 데이터는 강수 여부에 따라 매출액 평균에 차이가 있다.
# [개념] 귀무가설(H0): 차이가 없다, 효과가 없다 / 대립가설(H1): 차이가 있다, 효과가 있다.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

# 매출 데이터 읽기
# [문법] pd.read_csv: CSV 파일을 읽어 데이터프레임 생성. dtype 옵션으로 특정 컬럼의 타입을 지정 가능
sales_data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tsales.csv', dtype={'YMD':'object'}) # int -> object
print(sales_data.head())
#         YMD     AMT  CNT
# 0  20190514       0    1
# 1  20190519   18000    1
# 2  20190521   50000    4
# 3  20190522  125000    7
# 4  20190523  222500   13
# [문법] .info(): 데이터프레임의 행/열 개수, 결측치 여부, 데이터 타입을 요약해서 보여줌
print(sales_data.info())     # int type
# 328 * 3 행렬
print('\n')

# 날씨 데이터 읽기
wt_data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tweather.csv')
print(wt_data.head())
#    stnId          tm  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  2018-06-01   23.8   17.5   30.2    0.0    4.3    1.9    0.0
# 1    108  2018-06-02   23.4   17.6   30.1    0.0    4.5    2.0    0.0
# 2    108  2018-06-03   24.0   16.9   30.8    0.0    4.2    1.6    0.0
# 3    108  2018-06-04   22.6   18.9   27.5    0.0    4.4    1.9    0.0
# 4    108  2018-06-05   23.7   17.7   29.2    0.0    4.0    1.7    0.0
print(wt_data.info())    # object type
# 702 * 9 행렬
print('\n')

# 두 데이터의 날짜 형식 맞추기
# sales : YMD = 20190514
# wt : tm = 2018-06-01
# [문법] .map(lambda): 시리즈의 각 요소에 함수를 적용하여 데이터를 변환함 (날짜의 '-' 제거)
wt_data.tm = wt_data.tm.map(lambda x:x.replace('-', ''))
print(wt_data.head())
print('\n')

# 두 데이터를 병합
# [문법] pd.merge: 공통된 키(날짜)를 기준으로 두 데이터프레임을 합침. how='left'는 왼쪽 데이터 기준 유지
frame = sales_data.merge(wt_data, how='left', left_on='YMD', right_on='tm')
print(frame.head())
print('데이터 가짓수 : ', len(frame))   # 328
print('\n')

# [문법] .iloc: 정수 인덱스를 사용하여 특정 행과 열을 슬라이싱함
data = frame.iloc[:,[0,1,7,8]]      # YMD     AMT  maxTa  sumRn
print(data.head())
print('결측치 확인 : ', data.isnull().sum())
print('\n')

# 독립 표본 t-검정
# print(data['sumRn'] > 0)    # 강수량이 조금이라도 있으면 True

# 칼럼추가 : 강수량 있으면 1, 없으면 0
# 방법 1)
# data['rain_yn'] = (data.loc[:,('sumRn')] > 0).astype(int)
# 방법 2)
# [개념] 불리언 값에 숫자를 곱하면 True는 1, False는 0으로 변환됨
# print(True * 1, ' ', False * 1)
data['rain_yn'] = (data.loc[:,('sumRn')] > 0) * 1
print(data.head())
print('\n')
#         YMD     AMT  maxTa  sumRn  rain_yn
# 0  20190514       0   26.9    0.0        0
# 1  20190519   18000   21.6   22.0        1
# 2  20190521   50000   23.8    0.0        0

# 시각화 - box plot
# [문법] np.array: 데이터프레임의 특정 컬럼들을 넘파이 배열로 변환
sp = np.array(data.iloc[:, [1, 4]])     # AMT, rain_yn
print(sp)

tg1 = sp[sp[:,1] == 0, 0]       # 비 안올 때 매출액
tg2 = sp[sp[:,1] == 1, 0]       # 비 올 때 매출액
print(tg1[:3])  # [     0  50000 125000]
print(tg2[:3])  # [ 18000 274000 318000]
print('\n')

print('tg1(맑은날) 매출액 평균 : ', np.mean(tg1))
print('tg2(비온날) 매출액 평균 : ', np.mean(tg2))
# tg1(맑은날) 매출액 평균 :  761040.2542372881
# tg2(비온날) 매출액 평균 :  757331.5217391305
# 이 둘의 차이가 통계적으로 유의미한 차이인지 검정
# [추천] : sns.kdeplot을 사용하여 두 집단의 매출 분포 곡선을 겹쳐 그리면 평균 차이를 더 직관적으로 볼 수 있습니다.
plt.boxplot([tg1, tg2], meanline=True, showmeans=True, notch=True)
plt.xlabel('강수 여부')
plt.ylabel('매출액')
plt.show()

# 선행 조건 1 : 정규성 검정
# [개념] 샤피로-윌크 검정: 데이터가 정규분포를 따르는지 확인 (H0: 정규분포를 따른다)
print(len(tg1), ' ', len(tg2))  # 236   92  -> 비 안온 날이 더 많음
print(stats.shapiro(tg1).pvalue)    # 0.0560
print(stats.shapiro(tg2).pvalue)    # 0.882
# 두 그룹 모두 0.05 보다 크므로 정규성을 만족한다
# [판정] p-value > 0.05 이므로 귀무가설을 채택하여 정규성 가정을 충족함

# 선행 조건 2 : 등분산성 검정
# [개념] 레빈 검정(Levene's test): 두 집단의 분산이 동일한지 확인 (H0: 분산이 같다)
print(stats.levene(tg1, tg2).pvalue)    # 0.7123
# 0.05보다 크므로 등분산을 만족한다
# [판정] p-value > 0.05 이므로 귀무가설을 채택하여 등분산성 가정을 충족함

# 독립 표본 t-검정 진행
# [문법] stats.ttest_ind(a, b, equal_var=True): 독립 표본 t-검정 수행. equal_var=True는 등분산성을 만족할 때 사용
print(stats.ttest_ind(tg1, tg2, equal_var=True))
# statistic=0.101098, pvalue=0.9195, df=326
# [개념] 자유도(df): (n1 + n2) - 2 = (236 + 92) - 2 = 326

# 판정
# 정규성, 등분산성을 만족
# p-value = 0.9195 > alpha 0.05 이므로, 귀무가설 채택(수집한 데이터는 우연히 발생한 데이터다)
# 결론 : 어느 음식점의 매출 데이터는 강수 여부에 따라 매출액 평균에 차이가 없다
# [추천] : 만약 등분산성을 만족하지 못했다면 equal_var=False 옵션을 주어 Welch's t-test를 수행해야 합니다.