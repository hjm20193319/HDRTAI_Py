# LogisticRegression (Linear)
# [개념] 로지스틱 회귀: 선형 결합을 로그오즈(logit())로 해석하고, 이를 시그모이드 함수를 통해 확률로 변환함.
# [개념] 이항분류(다항도 가능)를 목적으로 하며, 독립 변수는 연속형, 종속 변수는 범주형임.
# [개념] LogisticRegression은 인공신경망(ANN)의 뉴런(Perceptron)에서 활성화 함수를 사용하는 구조의 기초가 됨.

# mtcars dataset 사용
# [추천] 분석 전 sns.boxplot(x='am', y='mpg', data=mtcars)을 통해 범주별 독립변수의 분포 차이를 시각화하면 도움이 됨.

import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# [문법] sm.datasets.get_rdataset('mtcars').data: R의 기본 데이터셋인 mtcars를 로드함.
mtcars = sm.datasets.get_rdataset('mtcars')
mtcars = mtcars.data
print(mtcars.head()) # [문법] 데이터프레임 상위 5개 행 출력
print(mtcars.info()) # [문법] 데이터 타입 및 결측치 여부 확인
print('\n')

# 연비와 마력수에 따른 변속기 분류(수동, 자동)
# [문법] loc[:, [columns]]: 특정 컬럼들만 추출하여 새로운 데이터프레임 생성
mtcar = mtcars.loc[:,['mpg', 'hp', 'am']]
print(mtcar.head(5))
print(mtcar['am'].unique())     # [개념] 1 - 수동(Manual), 0 - 자동(Automatic)
print('\n')

###################################################################################
# 모델 작성 방법 1 - logit()
# [개념] statsmodels의 logit은 최대우도추정법(MLE)을 사용하여 로지스틱 회귀 계수를 추정함.
import statsmodels.formula.api as smf
formula = 'am ~ hp + mpg'       # '연속형 ~ 범주형 + ...'
result = smf.logit(formula=formula, data=mtcar).fit()
print(result.summary())
#                            Logit Regression Results
# ==============================================================================
# Dep. Variable:                     am   No. Observations:                   32
# Model:                          Logit   Df Residuals:                       29
# Method:                           MLE   Df Model:                            2
# Date:                Tue, 07 Apr 2026   Pseudo R-squ.:                  0.5551
# Time:                        15:44:45   Log-Likelihood:                -9.6163
# converged:                       True   LL-Null:                       -21.615
# Covariance Type:            nonrobust   LLR p-value:                 6.153e-06
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    -33.6052     15.077     -2.229      0.026     -63.156      -4.055
# hp             0.0550      0.027      2.045      0.041       0.002       0.108
# mpg            1.2596      0.567      2.220      0.026       0.147       2.372
# ==============================================================================
print('\n')
# [개념] Pseudo R-squ: 로지스틱 회귀에서의 설명력 지표. 1에 가까울수록 모델의 적합도가 높음.

# print('예측값 : \n', result.predict()[:5])
# [문법] predict(): 학습된 모델을 통해 사건이 발생할(am=1) 확률값을 반환함.
pred = result.predict(mtcar[:10])
print('예측값 : \n', pred.values)   # 0.25004729 0.25004729 0.55803435 0.35559974...
print('원하는 형태의 예측값 : ', np.around(pred.values).astype(int)) # [문법] 0.5를 기준으로 반올림하여 이진 분류 수행
print('실제값 : ', mtcar['am'][:10].values)
# 원하는 형태의 예측값 :  [0 0 1 0 0 0 0 1 1 0]
#       실제값        :  [1 1 1 0 0 0 0 0 0 0]
print('\n')

# 수치에 대한 집계표 확인 - Confusion Matrix 혼동행렬
# [문법] pred_table(): 학습 데이터에 대한 혼동 행렬(Confusion Matrix)을 생성함.
conf_tab = result.pred_table() 
print(conf_tab)
# [[16.  3.]
#  [ 3. 10.]]

# 현재 모델의 분류 정확도 확인 1 - Confusion Matrix 이용
print('분류 정확도1-1 : ', (conf_tab[0,0] + conf_tab[1,1]) / np.sum(conf_tab))
print('분류 정확도1-2 : ', (conf_tab[0][0] + conf_tab[1][1]) / len(mtcar))

# 현재 모델의 분류 정확도 확인 2 - module로 확인 
# [문법] accuracy_score(y_true, y_pred): 실제값과 예측값을 비교하여 정확도를 계산함.
from sklearn.metrics import accuracy_score
pred2 = result.predict(mtcar)
print('분류 정확도2 : ', accuracy_score(mtcar['am'], np.around(pred2)))
print('\n')
# [추천] classification_report를 사용하면 정밀도(Precision), 재현율(Recall), F1-score를 한눈에 확인할 수 있음.

print('-------------------------------')

#######################################################################################################
# 모델 작성 방법 2 - glm() 일반화된 선형 모델       - pred_table()을 지원하지 않음
# [개념] GLM(Generalized Linear Model)은 종속변수의 분포에 따라 연결 함수(Link function)를 설정하여 회귀 분석을 수행함.
result2 = smf.glm(formula=formula, data=mtcar, family=sm.families.Binomial()).fit()
# [문법] family=sm.families.Binomial(): 이항 분포를 따르는 종속변수를 위해 로짓 연결 함수를 사용하도록 설정함.
# [개념] Gaussian: 정규분포(기본값), Poisson: 포아송 분포 등 다양한 분포 지원
print(result2.summary())
#                  Generalized Linear Model Regression Results
# ==============================================================================
# Dep. Variable:                     am   No. Observations:                   32
# Model:                            GLM   Df Residuals:                       29
# Model Family:                Binomial   Df Model:                            2
# Link Function:                  Logit   Scale:                          1.0000
# Method:                          IRLS   Log-Likelihood:                -9.6163
# Date:                Tue, 07 Apr 2026   Deviance:                       19.233
# Time:                        16:16:01   Pearson chi2:                     16.1
# No. Iterations:                     7   Pseudo R-squ. (CS):             0.5276
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept    -33.6052     15.077     -2.229      0.026     -63.155      -4.055
# hp             0.0550      0.027      2.045      0.041       0.002       0.108
# mpg            1.2596      0.567      2.220      0.026       0.147       2.372
# ==============================================================================
print('\n')

glm_pred = result2.predict(mtcar[:10])
print('glm 예측값 : ', np.around(glm_pred.values).astype(int))
print('실제값 : ', mtcar['am'][:10].values)
# glm 예측값 :  [0 0 1 0 0 0 0 1 1 0]
#     실제값 :  [1 1 1 0 0 0 0 0 0 0]
print('\n')

glm_pred2 = result2.predict(mtcar)
print('glm 모델 분류 정확도 : ', accuracy_score(mtcar['am'], np.around(glm_pred2)))
# glm 모델 분류 정확도 :  0.8125
print('\n')

# [개념] logit()은 로지스틱 회귀 전용 함수이며, glm()은 다양한 확률 분포를 처리할 수 있는 포괄적인 모델임.

#####################################################################################################
# 새로운 값으로 분류

newdf = pd.DataFrame()
newdf['mpg'] = [10, 30, 120, 200]
newdf['hp'] = [100, 1100, 80, 130]
print(newdf)
print('\n')

new_pred = result2.predict(newdf)
print('예측 결과 : ', np.around(new_pred.values))
print('예측 결과 : ', np.rint(new_pred.values))