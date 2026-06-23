import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from scipy.stats import wilcoxon

# 귀무가설 : 새 백열전구의 수명은 300시간이다
# 대립가설 : 새 백열전구의 수명은 300시간이 아니다

data = pd.DataFrame({
    'life':[305, 280, 296, 313, 287, 240, 259, 266, 318, 280, 325, 295, 315, 278]
})
print(data)
print(data.describe())
print('수집한 데이터 수 : ', len(data))

# 정규성 검사
print(stats.shapiro(data['life'])) # pvalue=np.float64(0.8208613446833366)
# alpha 0.05 < pvalue=0.82 이므로 정규성을 따른다

# ttest
result = stats.ttest_1samp(data['life'], popmean=300)
print('result : ', result)  # pvalue=np.float64(0.143606254517609)
# alpha 0.05 < pvalue=np.float64(0.143606254517609) 이므로 귀무가설 채택
# 결론 : 새 백열전구의 수명은 300시간이다, 한국 연구소의 발표 결과는 옳다

# 시각화
stats.probplot(data['life'], plot=plt)
plt.title('백열전구 수명 분포')
plt.show()

print('-----------------------------------')

# 귀무가설 : A회사 생산 노트북 평균 사용 시간은 5.2 시간이다.
# 대립가설 : A회사 생산 노트북 평균 사용 시간은 5.2 시간이 아니다.

data2 = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/one_sample.csv')
print(data2)
print(data2.time.dtype)
print('수집한 데이터 수 : ', len(data2))

pd.set_option('display.max_rows', None)
data2['time'] = data2['time'].replace("     ", np.nan)
data2 = data2.dropna().astype('float')
print(data2)
print('수집한 데이터 수 : ', len(data2))

# 데이터가 109개 이므로 정규성을 따름

# ttest
result2 = stats.ttest_1samp(data2['time'], popmean=5.2)
print('result2 : ', result2) 
# pvalue=np.float64(0.0001416669139019709)
# alpha 0.05 > pvalue=0.0001416 이므로 귀무가설 기각
# 결론 : A회사 생산 노트북 평균 사용 시간은 5.2 시간이 아니다

# 시각화
stats.probplot(data2['time'], plot=plt)
plt.title('노트북 사용 시간 분포')
plt.show()

print('-----------------------------------')

# 귀무가설 : 전국 평균 미용 요금은 15000원이다.
# 대립가설 : 전국 평균 미용 요금은 15000원이 아니다.

data3 = pd.read_excel('ttestsample.xlsx').T
print(data3)
print('수집한 데이터 수 : ', len(data3))
data3 = data3.dropna()
data3 = data3.drop(['번호', '품목']).astype('float')
print(data3)
print('수집한 데이터 수 : ', len(data3))

# 데이터 수는 16개 이므로 정규성 검정 실시
print(stats.shapiro(data3))
# pvalue=np.float64(0.08795706717610463)
# alpha 0.05 < pvalue=0.088 이므로 정규성을 따른다

# ttest
result3 = stats.ttest_1samp(data3.iloc[:,0], popmean=15000)
print('result3 : ', result3)
# pvalue=np.float64(3.2057661925789937e-06)
# alpha 0.05 > pvalue=0.000 이므로 귀무가설 기각
# 결론 : 전국 평균 미용 요금은 15000원이 아니다

# 시각화
stats.probplot(data3.iloc[:,0], plot=plt)
plt.title('미용 요금 분포')
plt.show()