import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd

data = pd.read_csv('tvexer.csv')
print(data.head())
print(data.info())
print('\n')

data = data.replace(np.nan, np.mean(data['지상파']))
# print(data)

data = data[data['운동'] <= 10]
print(data)

# '지상파', '운동' 상관관계 분석
r1 = data['지상파'].corr(data['운동'])
print(r1)
print('\n')
# 0.29342664568626603 강한 상관관계

# '지상파', '종편' 상관관계 분석
r2 = data['지상파'].corr(data['종편'])
print(r2)
print('\n')
# 0.8875299693193012 강한 상관관계

# 시각화 1
plt.scatter(data['지상파'], data['운동'])
plt.grid(True)
plt.title('지상파 시청 시간에 따른 운동 시간')
plt.xlabel('지상파 시청 시간')
plt.ylabel('운동 시간')
plt.show()

# 시각화 2
plt.scatter(data['지상파'], data['종편'])
plt.grid(True)
plt.title('지상파 시청 시간에 따른 종편 시간')
plt.xlabel('지상파 시청 시간')
plt.ylabel('종편 시간')
plt.show()


# 단순 선형회귀분석
#############################################
# linregress() 사용
model = stats.linregress(data['지상파'], data['운동'])
# print('기울기 : ', model.slope)
# print('절편 : ', model.intercept)
# print('p-value : ', model.pvalue)
# 기울기 :  -0.6684550167105406
# 절편 :  4.709676019780582
# p-value :  6.347578533142469e-05
tmodel = stats.linregress(data['지상파'], data['종편'])
print('\n')

# 모델
x = input('지상파 시청 시간을 입력하시오 : ')
print('결과---------------------------------')
newdata = pd.DataFrame({'지상파':[float(x)]})
new_pred = model.slope * float(x) + model.intercept
if new_pred < 0:
    new_pred = 0
    
new_tpred = tmodel.slope * float(x) + tmodel.intercept
if new_tpred < 0:
    new_tpred = 0
print('입력 시간에 따른 운동 시간 예측값은(linregress) : ', new_pred)
print('입력 시간에 따른 종편 시청 시간 예측값은(linregress) : ', new_tpred)
print('\n')


################################################
# ols 사용
import statsmodels.formula.api as smf
model2 = smf.ols(formula='운동 ~ 지상파', data=data)
fit_model2 = model2.fit()
# print(fit_model2.summary())
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                     운동   R-squared:                       0.749
# Model:                            OLS   Adj. R-squared:                  0.728
# Method:                 Least Squares   F-statistic:                     35.84
# Date:                Fri, 03 Apr 2026   Prob (F-statistic):           6.35e-05
# Time:                        12:32:31   Log-Likelihood:                -10.714
# No. Observations:                  14   AIC:                             25.43
# Df Residuals:                      12   BIC:                             26.71
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      4.7097      0.323     14.596      0.000       4.007       5.413
# 지상파           -0.6685      0.112     -5.986      0.000      -0.912      -0.425
# ==============================================================================
# Omnibus:                        0.302   Durbin-Watson:                   2.599
# Prob(Omnibus):                  0.860   Jarque-Bera (JB):                0.017
# Skew:                           0.041   Prob(JB):                        0.991
# Kurtosis:                       2.849   Cond. No.                         6.81
# ==============================================================================

tmodel2 = smf.ols(formula='종편 ~ 지상파', data=data)
fit_tmodel2 = tmodel2.fit()

new_pred2 = float(fit_model2.predict(newdata))
if new_pred2 < 0:
    new_pred2 = 0

new_tpred2 = float(fit_tmodel2.predict(newdata))
if new_tpred2 < 0:
    new_tpred2 = 0

print('입력 시간에 따른 운동 시간 예측값은(ols) : ', new_pred2)
print('입력 시간에 따른 종편 시청 시간 예측값은(ols) : ', new_tpred2)
print('\n')

##################################################
# LinearRegresssion 사용
from sklearn.linear_model import LinearRegression

model3 = LinearRegression()
fit_model3 = model3.fit(data[['지상파']], data['운동'])

tmodel3 = LinearRegression()
fit_tmodel3 = tmodel3.fit(data[['지상파']], data['종편'])

new_pred3 = float(fit_model3.predict(newdata))
if new_pred3 < 0:
    new_pred3 = 0

new_tpred3 = float(fit_tmodel3.predict(newdata))
if new_tpred3 < 0:
    new_tpred3 = 0
    
print('입력 시간에 따른 운동 시간 예측값은(LinearRegression) : ', new_pred3)
print('입력 시간에 따른 종편 시청 시간 예측값은(LinearRegression) : ', new_tpred3)
print('\n')

##########################################
# 전체 시각화 (추세선)

plt.subplot(1, 2, 1)
plt.scatter(data['지상파'], data['운동'])
plt.grid(True)
plt.title('지상파 시청 시간에 따른 운동 시간')
plt.xlabel('지상파 시청 시간')
plt.ylabel('운동 시간')
plt.plot(data['지상파'], model.intercept + model.slope * data['지상파'], c='r')

plt.subplot(1, 2, 2)
plt.scatter(data['지상파'], data['종편'])
plt.grid(True)
plt.title('지상파 시청 시간에 따른 종편 시청 시간')
plt.xlabel('지상파 시청 시간')
plt.ylabel('종편 시간')
plt.plot(data['지상파'], tmodel.intercept + tmodel.slope * data['지상파'], c='r')

plt.tight_layout()
plt.show()