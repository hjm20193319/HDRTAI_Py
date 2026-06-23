import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pymysql
import pickle

print('-----------------------')

# 귀무가설 : 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 없다.
# 대립가설 : 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 있다.

data = pd.DataFrame({
    'kind':[1, 2, 3, 4, 2, 1, 3, 4, 2, 1, 2, 3, 4, 1, 2, 1, 1, 3, 4, 2],
    'quantity':[64, 72, 68, 77, 56, np.nan, 95, 78, 55, 91, 63, 49, 70, 80, 90, 33, 44, 55, 66, 77]
})
print(data)
print('\n')

oil1 = data[data['kind'] == 1]['quantity']
oil1 = oil1.fillna(np.mean(oil1))
oil2 = data[data['kind'] == 2]['quantity']
oil3 = data[data['kind'] == 3]['quantity']
oil4 = data[data['kind'] == 4]['quantity']
print(oil1)
print(oil2)
print(oil3)
print(oil4)
print('\n')

# 정규성 확인
print(stats.shapiro(oil1).pvalue)
print(stats.shapiro(oil2).pvalue)
print(stats.shapiro(oil3).pvalue)
print(stats.shapiro(oil4).pvalue)
# 0.8830095529017977
# 0.5923924912154501
# 0.48601083943678747
# 0.4162161718602888
# 정규성을 만족한다고 가정
print('\n')

# 등분산성
print(stats.levene(oil1, oil2, oil3, oil4).pvalue)
# 0.3473294159708626 > 0.05 이므로 등분산성 만족
print('\n')

# 일원분산분석
f_stat, p_val = stats.f_oneway(oil1, oil2, oil3, oil4)
print('f_stat : ', f_stat)
print('p_val : ', p_val)
# f_stat :  0.32254711830668814
# p_val :  0.8089979993442262
# 판정
# 0.8089979993442262 > alpha 0.05 이므로 귀무 가설 채택
# 결론 : 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 없다.
print('\n')

# 사후 검증
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(endog=data['quantity'].fillna(np.mean(oil1)), groups=data['kind'])
print(tukResult)
#  Multiple Comparison of Means - Tukey HSD, FWER=0.05 
# =====================================================
# group1 group2 meandiff p-adj   lower    upper  reject
# -----------------------------------------------------
#      1      2   6.4333 0.9115 -21.5731 34.4397  False
#      1      3     4.35  0.978 -26.9621 35.6621  False
#      1      4    10.35 0.7811 -20.9621 41.6621  False
#      2      3  -2.0833 0.9974 -33.3954 29.2288  False
#      2      4   3.9167 0.9837 -27.3954 35.2288  False
#      3      4      6.0 0.9578 -28.3007 40.3007  False
# -----------------------------------------------------

# 시각화
tukResult.plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()

print('-----------------------')

# 가설 수립
# 귀무 가설 : 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 없다.
# 대립 가설 : 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 있다.

# 데이터 수집
with open('mydb.dat', mode = 'rb') as obj:         
    config = pickle.load(obj)

conn = pymysql.connect(**config)

sql = '''
    select busername, jikwonpay
    from jikwon left outer join buser
    on jikwon.busernum = buser.buserno
    order by busername
'''

pay = pd.read_sql(sql, conn)
print(pay)
print('\n')
conn.close()

gr1 = pay[pay['busername'] == '총무부']['jikwonpay']
gr2 = pay[pay['busername'] == '영업부']['jikwonpay']
gr3 = pay[pay['busername'] == '전산부']['jikwonpay']
gr4 = pay[pay['busername'] == '관리부']['jikwonpay']
print(gr1)
print(gr2)
print(gr3)
print(gr4)
print('\n')

# 정규성 검증
print(stats.shapiro(gr1).pvalue)
print(stats.shapiro(gr2).pvalue)
print(stats.shapiro(gr3).pvalue)
print(stats.shapiro(gr4).pvalue)
# 0.026044936412817302
# 0.025608399511523605
# 0.4194072051776978
# 0.9078027897950541
# 정규성을 만족한다고 가정
print('\n')

# 등분산성
print(stats.levene(gr1, gr2, gr3, gr4).pvalue)  
# 0.7980753526275928
# 등분산성 만족
print('\n')

# 일원분산분석
f_stat, p_val = stats.f_oneway(gr1, gr2, gr3, gr4)
print('f_stat : ', f_stat)
print('p_val : ', p_val)
# f_stat :  0.41244077160708414
# p_val :  0.7454421884076983
# 판정
# 0.7454421884076983 > alpha 0.05 이므로 귀무가설 채택
# 결론 : 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 없다.
print('\n')

# 사후 검증
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(endog=pay['jikwonpay'], groups=pay['busername'])
print(tukResult)
#     Multiple Comparison of Means - Tukey HSD, FWER=0.05    
# ===========================================================
# group1 group2  meandiff  p-adj    lower      upper   reject
# -----------------------------------------------------------
#    관리부    영업부 -1354.1667 0.6937 -4736.5568 2028.2234  False
#    관리부    전산부  -933.9286  0.897 -4605.9199 2738.0628  False
#    관리부    총무부  -848.2143 0.9202 -4520.2056 2823.7771  False
#    영업부    전산부   420.2381 0.9756 -2366.0209 3206.4971  False
#    영업부    총무부   505.9524 0.9588 -2280.3066 3292.2114  False
#    전산부    총무부    85.7143 0.9998 -3045.7705  3217.199  False
# -----------------------------------------------------------

# 시각화
tukResult.plot_simultaneous(xlabel='mean', ylabel='group')
plt.show()
print('\n')