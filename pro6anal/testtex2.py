import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import pymysql
import pickle

print('-----------------------')

# 가설 수립
# 귀무가설 : 남여 혈관 내의 콜레스테롤 양의 차이는 없다.
# 대립가설 : 남여 혈관 내의 콜레스테롤 양의 차이는 있다.

# 데이터 수집
male = np.array([0.9, 2.2, 1.6, 2.8, 4.2, 3.7, 2.6, 2.9, 3.3, 1.2, 3.2, 2.7, 3.8, 4.5, 4, 2.2, 0.8, 0.5, 0.3, 5.3, 5.7, 2.3, 9.8])
female = np.array([1.4, 2.7, 2.1, 1.8, 3.3, 3.2, 1.6, 1.9, 2.3, 2.5, 2.3, 1.4, 2.6, 3.5, 2.1, 6.6, 7.7, 8.8, 6.6, 6.4])

# 15 명 비복원 추출
mdata = np.random.choice(male, 15, replace=False)
print(mdata)
fdata = np.random.choice(female, 15, replace=False)
print(fdata)
print('\n')

# 정규성 검정
print(stats.shapiro(mdata).pvalue)
print(stats.shapiro(fdata).pvalue)
# 0.07067152177995045
# 0.007301370308207732
# mdata가 0.05보다 크므로 정규성을 만족한다고 가정
print('\n')

# 등분산성
print(stats.levene(mdata, fdata).pvalue)
# 0.8991952766266895 > 0.05 이므로 등분산성 만족

# t-test
print(stats.ttest_ind(mdata, fdata, equal_var=True))
# TtestResult(statistic=np.float64(-1.1141416229266439), pvalue=np.float64(0.2746911043180187), df=np.float64(28.0))# 판정
# 0.2746911043180187 > 0.05 이므로, 귀무 가설 채택
# 결론 : 남여 혈관 내의 콜레스테롤 양의 차이는 없다.
print('\n')

print('-----------------------')

# 가설 수립
# 귀무가설 : 총무부와 영업부 직원의 연봉의 평균에 차이가 없다.
# 대립가설 : 총무부와 영업부 직원의 연봉의 평균에 차이가 있다.

# 데이터 수집
with open('mydb.dat', mode = 'rb') as obj:         
    config = pickle.load(obj)

conn = pymysql.connect(**config)         

sql = '''
    select busername, jikwonpay
    from jikwon left outer join buser
    on jikwon.busernum = buser.buserno
    where buser.busername in ('총무부', '영업부')
    order by busername
'''

df = pd.read_sql(sql, conn)
print(df)
print('\n')
conn.close()

data1 = df[df['busername'] == '총무부']['jikwonpay']
data2 = df[df['busername'] == '영업부']['jikwonpay']
print(data1)
print(data2)

print(len(data1))
print(len(data2))
print('\n')


# 정규성 검정
print(stats.shapiro(data1).pvalue)
print(stats.shapiro(data2).pvalue)
# 0.026044936412817302
# 0.025608399511523605
# 0.05 보다 작으므로 정규성 만족X

# 비모수 검정
mann_result = stats.mannwhitneyu(data1, data2)
print(mann_result)
# MannwhitneyuResult(statistic=np.float64(51.0), pvalue=np.float64(0.47213346080125185))
# 판정
# 0.47213346080125185 > 0.05 이므로 귀무 가설 채택
# 결론 : 총무부와 영업부 직원의 연봉의 평균에 차이가 없다.
print('\n')

print('-----------------------')

# 가설 수립
# 귀무 가설 : 시험 성적의 결과를 보았을 때 학업능력의 변화는 없다.
# 대립 가설 : 시험 성적의 결과를 보았을 때 학업능력의 변화가 있다.

# 데이터 수집
mid = np.array([80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80])
final = np.array([90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95])

# 정규성 검정
print(stats.shapiro(mid).pvalue)
print(stats.shapiro(final).pvalue)
# 0.3681471063353156
# 0.19300297267172734
# 0.05 보다 크므로 정규성 만족
print('\n')

# t-test
print(stats.ttest_rel(mid, final))
# TtestResult(statistic=np.float64(-2.6281127723493998), pvalue=np.float64(0.023486192540203194), df=np.int64(11))
# 판정
# 0.023486192540203194 < 0.05 이므로 귀무가설 기각
# 결론 : 시험 성적의 결과를 보았을 때 학업능력의 변화가 있다.
# 시각화
plt.bar(['전', '후'], [np.mean(mid), np.mean(final)])
plt.xlim(0, 1)
plt.xlabel('시험 전후', fontdict={'size':12, 'fontweight':'bold'})
plt.show()
print('\n')

print('-----------------------')