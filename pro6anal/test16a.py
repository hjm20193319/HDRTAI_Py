# 어느 음식점의 매출 데이터와 기상청이 제공한 날씨 데이터를 활용하여
# 최고온도 여부에 따른 매출액의 평균에 차이가 있는지 검정
# 세 집단 : 추움, 보통, 더움

# 가설 수립
# [개념] 귀무가설(H0): 차이가 없다, 효과가 없다 / 대립가설(H1): 차이가 있다, 효과가 있다.
# 귀무 가설 : 어느 음식점의 매출 데이터는 최고기온에 따라 매출액 평균에 차이가 없다.
# 대립 가설 : 어느 음식점의 매출 데이터는 최고기온에 따라 매출액 평균에 차이가 있다.

import numpy as np
import pandas as pd
# [문법] scipy.stats: 통계 분석을 위한 다양한 함수(검정, 분포 등)를 제공하는 라이브러리
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

# [문법] .describe(): 수치형 데이터의 주요 기술 통계량(개수, 평균, 표준편차, 사분위수 등) 요약
print(data.maxTa.describe())
# [문법] plt.boxplot: 데이터의 분포와 이상치(Outlier)를 시각화함
plt.boxplot(data.maxTa)
plt.show()
print('\n')

# [문법] pd.cut: 연속형 변수를 특정 구간(bins)으로 나누어 범주형 변수로 변환함
# 온도를 세 그룹으로 분리 ( 연속형 -> 범주형 )
print(data.isnull().sum())
print('\n')
data['ta_gubun'] = pd.cut(data.maxTa, bins=[-5, 8, 24, 37], labels=[0, 1, 2])
print(data.head(), ' ', data['ta_gubun'].unique())
#         YMD     AMT  maxTa  sumRn ta_gubun
# 0  20190514       0   26.9    0.0        2
# 1  20190519   18000   21.6   22.0        1
# 2  20190521   50000   23.8    0.0        1
# 3  20190522  125000   26.5    0.0        2
# 4  20190523  222500   29.2    0.0        2   [2, 1, 0]
# Categories (3, int64): [0 < 1 < 2]
print('\n')

# [문법] 불리언 인덱싱: 특정 조건을 만족하는 행의 데이터만 추출하여 넘파이 배열로 변환
# 선행조건 검증 위한 변수 선언
x1 = np.array(data[data.ta_gubun == 0].AMT)     # 추움 그룹 매출액
x2 = np.array(data[data.ta_gubun == 1].AMT)     # 보통 그룹 매출액
x3 = np.array(data[data.ta_gubun == 2].AMT)     # 더움 그룹 매출액
print(x1[:5])
print(x2[:5])
print(x3[:5])
print('\n')

# 등분산성
# [문법] stats.levene: 세 집단 이상의 분산이 동일한지 확인 (H0: 분산이 같다). 이상치에 강함.
print(stats.levene(x1, x2, x3).pvalue)
# [문법] stats.bartlett: 정규성을 따르는 데이터에 적합한 등분산성 검정
print(stats.bartlett(x1, x2, x3).pvalue)
# 0.039002396565063324
# 0.009677579972661264
# [판정] p-value < 0.05 이므로 귀무가설을 기각하여 등분산성 가정을 충족하지 못함
print('\n') # [추천] : 등분산성이 깨진 경우 일반 ANOVA 대신 Welch's ANOVA를 사용하는 것이 좋습니다.

# 정규성
print(stats.shapiro(x1).pvalue)
print(stats.shapiro(x2).pvalue)
print(stats.shapiro(x3).pvalue)
# 0.2481924204382751
# 0.03882572120522948
# 0.3182989573650957
# [판정] x2 그룹이 p-value < 0.05로 정규성을 만족하지 못함
print('\n')

# 온도별 매출액 평균
spp = data.loc[:, ['AMT', 'ta_gubun']]
# [문법] .groupby().mean(): 특정 컬럼을 기준으로 그룹화하여 평균값을 계산함
print(spp.groupby('ta_gubun').mean())
# 과학적 표기법이 아닌 상태로 보기 위해
print(np.mean(x1))
print(np.mean(x2))
print(np.mean(x3))
# 1032362.3188405797
# 818106.8702290077
# 553710.9375
print('\n')

group1 = x1
group2 = x2
group3 = x3

# plt.boxplot([group1, group2, group3], meanline=True, showmeans=True, notch=True)
# plt.xlabel('온도')
# plt.ylabel('매출액')
# plt.show()
# print('\n')

# [문법] stats.f_oneway(a, b, c): 세 집단 이상의 평균 차이를 검정하는 일원분산분석 수행
print(stats.f_oneway(group1, group2, group3))
# F_onewayResult(statistic=np.float64(99.1908012029983), pvalue=np.float64(2.3607e-34))
# 판정
# [판정] p-value < 0.05 이므로 귀무가설 기각
# 결론 : 어느 음식점의 매출 데이터는 온도에 따라 차이가 있다
print('\n')

# f_oneway() : 정규성 깨지면 stats.kruskal(), 등분산성이 깨지면 welch ANOVA 사용
# [개념] 비모수 검정(Kruskal-Wallis): 정규성 가정이 위배되었을 때 순위합을 이용해 평균 차이를 검정함
print(stats.kruskal(group1, group2, group3))
# KruskalResult(statistic=np.float64(132.7022591443371), pvalue=np.float64(1.5278142583114522e-29))
print('\n')
# pip install pingouin
# [개념] Welch's ANOVA: 등분산성 가정이 위배되었을 때 자유도를 수정하여 검정하는 방식
from pingouin import welch_anova
print(welch_anova(dv='AMT', between='ta_gubun', data=data))
#      Source  ddof1     ddof2           F         p_unc       np2
# 0  ta_gubun      2  189.6514  122.221242  7.907874e-35  0.379038
print('\n')

# [개념] 사후분석(Post Hoc): ANOVA 결과가 유의미할 때(p < 0.05), 구체적으로 어떤 집단들 사이에 차이가 있는지 검정함.
# 사후검정
from statsmodels.stats.multicomp import pairwise_tukeyhsd
# [문법] pairwise_tukeyhsd(endog, groups): Tukey의 HSD(Honestly Significant Difference) 검정 수행
# [개념] reject: True면 두 집단 간 평균 차이가 유의미함, False면 유의미한 차이가 없음.
print(pairwise_tukeyhsd(data.AMT, data.ta_gubun), alpha=0.05)
#        Multiple Comparison of Means - Tukey HSD, FWER=0.05       
# =================================================================
# group1 group2   meandiff   p-adj    lower        upper     reject
# -----------------------------------------------------------------
#      0      1 -214255.4486   0.0  -296755.647 -131755.2503   True
#      0      2 -478651.3813   0.0 -561484.4539 -395818.3088   True
#      1      2 -264395.9327   0.0 -333326.1167 -195465.7488   True
# -----------------------------------------------------------------

# 시각화
# [문법] .plot_simultaneous(): 각 집단의 신뢰구간을 시각화하여 겹치지 않으면 유의미한 차이가 있음을 보여줌
pairwise_tukeyhsd(data.AMT, data.ta_gubun).plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()