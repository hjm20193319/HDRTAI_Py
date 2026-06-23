# 이원분산분석 : 요인 복수 - 각 요인의 레벨(그룹)도 복수
# [개념] 이원분산분석(Two-way ANOVA): 두 개의 독립변수(요인)가 하나의 종속변수(평균)에 미치는 영향을 동시에 분석하는 기법.

# 두 개의 요인에 대한 집단(독립변수) 각각이 종속변수(평균)에 영향을 주는지 검정
# [개념] 주효과(Main Effect): 다른 독립변수의 변화와 상관없이, 하나의 독립변수가 종속변수에 미치는 직접적인 영향.
# [개념] 상호작용효과(Interaction Effect): 한 독립변수가 종속변수에 미치는 영향이 다른 독립변수의 수준(Level)에 따라 달라지는 현상.

# < 실습 1 >
# : 태아 수와 관측자 수가 태아의 머리 둘레 평균에 영향을 주는가?

# 주효과 가설
# 귀무가설 : 태아 수와 태아의 머리 둘레 평균은 차이가 없다.
# 대립가설 : 태아 수와 태아의 머리 둘레 평균은 차이가 있다.
# 귀무가설 : 관측자 수와 태아의 머리 둘레 평균은 차이가 없다.
# 대립가설 : 관측자 수와 태아의 머리 둘레 평균은 차이가 있다.

# 교호작용 가설
# 귀무가설 : 교호작용이 없다. 태아 수와 관측자 수는 관련이 없다.
# 대립가설 : 교호작용이 있다. 태아 수와 관측자 수는 관련이 있다.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
# [문법] statsmodels: 통계 모델 추정 및 검정을 위한 라이브러리. ols는 최소제곱법 회귀 모델 생성에 사용됨.
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# 데이터 수집
# [문법] pd.read_csv: 외부 URL의 텍스트 데이터를 읽어와 데이터프레임 생성
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3_2.txt')
print(data.head())
print(data.shape)   # (36, 3)
# [문법] .unique(): 컬럼 내 중복되지 않는 고유값들을 반환하여 요인의 레벨 구성을 확인
print(data['태아수'].unique())   # [1 2 3]
print(data['관측자수'].unique())    # [1 2 3 4]
print('\n')

# 시각화
# data.boxplot(by='태아수', column='머리둘레')
# plt.show()

# data.boxplot(by='관측자수', column='머리둘레')
# plt.show()
# [추천] : sns.pointplot(x='태아수', y='머리둘레', hue='관측자수', data=data)를 사용하면 상호작용 효과를 시각적으로 더 쉽게 파악할 수 있습니다.

# 선형모델
# [문법] ols('종속변수 ~ 독립변수1 + 독립변수2', data).fit(): C()는 해당 변수가 범주형임을 명시함.
linreg = ols('머리둘레 ~ C(태아수) + C(관측자수)', data=data).fit()     # 교호작용이 없는
# [문법] 'A:B' 또는 'A*B' 표기법: 두 변수 간의 상호작용 항을 모델에 포함시킴.
linreg2 = ols('머리둘레 ~ C(태아수) + C(관측자수) + C(태아수):C(관측자수)', data=data).fit()    # 교호작용이 있는
linreg3 = ols('머리둘레 ~ C(태아수) * C(관측자수)', data=data).fit()    # 교호작용이 있는
# [문법] anova_lm(model, typ=2): 적합된 모델을 바탕으로 분산분석표를 생성함. typ=2는 불균형 설계에 권장되는 방식.
result = anova_lm(linreg3, typ=2)
print(result)
#                          sum_sq        df            F          PR(>F)
# C(태아수)              324.008889      2.0     2113.101449   1.051039e-27   
# C(관측자수)             1.198611       3.0      5.211353     6.497055e-03
# C(태아수):C(관측자수)    0.562222      6.0      1.222222     3.295509e-01

# 판정
# 태아수 pvalue < 0.05 귀무 기각 :  태아 수와 태아의 머리둘레 평균은 차이가 있다.
# 관측자수 pvalue < 0.05 귀무 기각 : 관측자수와 태아의 머리둘레 평균은 차이가 있다.
# 상호작용 pvalue > 0.05 귀무 채택: 태아수와 관측자 수는 관련이 없다.

# 해석 : 태아수와 관측자 수는 각각 종속변수에 유의한 영향을 미친다.
#        그러나 태아수와 관측자 수 간의 상호작용 효과는 유의하지 않다.
#        주효과는 있음, 상호작용은 없음

print('-------------------------------------------')
print('\n')

# < 실습 2 >
# : poison과 treat가 독 퍼짐 시간의 평균에 영향을 주는가?

# 주효과 가설
# 귀무가설 : poison 종류와 독 퍼짐 시간의 평균은 차이가 없다.
# 대립가설 : poison 종류와 독 퍼짐 시간의 평균은 차이가 있다.
# 귀무가설 : treat(응급처치) 방법과 독 퍼짐 시간의 평균은 차이가 없다.
# 대립가설 : treat(응급처치) 방법과 독 퍼짐 시간의 평균은 차이가 있다.

# 교호작용 가설
# 귀무가설 : 교호작용이 없다. (poison 종류와 응급처치 방법은 관련이 없다)
# 대립가설 : 교호작용이 있다. (poison 종류와 응급처치 방법은 관련이 있다)

# 데이터 수집
# [문법] index_col=0: 파일의 첫 번째 열을 데이터프레임의 인덱스로 사용함
data2 = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/poison_treat.csv', index_col=0)
print(data2.head())
print(data2.shape)  # (48, 3)
print('\n')

# [문법] .groupby().agg(len): 특정 컬럼으로 그룹화하여 각 그룹의 데이터 개수(표본수)를 확인
print(data2.groupby('poison').agg(len))
print(data2.groupby('treat').agg(len))
print(data2.groupby(['poison', 'treat']).agg(len))  # 요인별 레벨의 표본수는 4로 동일(균형적인 설계)
print('\n')

# 선형 모델
# [문법] 'time ~ C(poison) * C(treat)': poison 주효과, treat 주효과, 그리고 둘 사이의 상호작용 효과를 모두 포함하는 모델
result2 = ols('time ~ C(poison) * C(treat)', data=data2).fit()
# [문법] anova_lm(result2): 분산분석표를 출력하여 각 요인의 유의성(PR(>F))을 확인
print(anova_lm(result2)) 
#                       df    sum_sq   mean_sq          F        PR(>F)
# C(poison)            2.0  1.033013  0.516506  23.221737  3.331440e-07
# C(treat)             3.0  0.921206  0.307069  13.805582  3.777331e-06
# C(poison):C(treat)   6.0  0.250138  0.041690   1.874333  1.122506e-01
print('\n')

# 판정
# poison 종류 : 귀무기각
# treat 방법 : 귀무기각
# 상호작용 : 귀무채택

# 해석 : poison 종류와 treat 방법은 각각 종속변수에 유의한 영향을 미친다. 하지만 상호작용은 없다.

# 사후 분석
# [개념] 사후분석(Post Hoc): ANOVA 결과가 유의미할 때(p < 0.05), 구체적으로 어떤 집단들 사이에 차이가 있는지 검정함.
from statsmodels.stats.multicomp import pairwise_tukeyhsd
# [문법] pairwise_tukeyhsd(endog, groups): Tukey의 HSD(Honestly Significant Difference) 검정 수행
print(pairwise_tukeyhsd(data2.time, data2.poison))
# Multiple Comparison of Means - Tukey HSD, FWER=0.05 
# ====================================================
# group1 group2 meandiff p-adj   lower   upper  reject
# ----------------------------------------------------
#      1      2  -0.0731 0.5882 -0.2525  0.1063  False
#      1      3  -0.3412 0.0001 -0.5206 -0.1619   True
#      2      3  -0.2681 0.0021 -0.4475 -0.0887   True
# ----------------------------------------------------
print('\n')

print(pairwise_tukeyhsd(data2.time, data2.treat))
# Multiple Comparison of Means - Tukey HSD, FWER=0.05 
# ====================================================
# group1 group2 meandiff p-adj   lower   upper  reject
# ----------------------------------------------------
#      A      B   0.3625  0.001  0.1253  0.5997   True
#      A      C   0.0783 0.8143 -0.1589  0.3156  False
#      A      D     0.22 0.0778 -0.0172  0.4572  False
#      B      C  -0.2842 0.0132 -0.5214 -0.0469   True
#      B      D  -0.1425  0.387 -0.3797  0.0947  False
#      C      D   0.1417 0.3922 -0.0956  0.3789  False
# ----------------------------------------------------
print('\n')

# 시각화
# [문법] .plot_simultaneous(): 각 집단의 신뢰구간을 시각화하여 겹치지 않으면 유의미한 차이가 있음을 보여줌
pairwise_tukeyhsd(data2.time, data2.poison).plot_simultaneous(xlabel='mean', ylabel='poison')
plt.show()
pairwise_tukeyhsd(data2.time, data2.treat).plot_simultaneous(xlabel='mean', ylabel='treat')
plt.show()
plt.close()
# [추천] : 상호작용이 유의미하지 않더라도 interaction_plot(data2['poison'], data2['treat'], data2['time'])을 그려보면 두 요인의 관계를 더 명확히 시각화할 수 있습니다.