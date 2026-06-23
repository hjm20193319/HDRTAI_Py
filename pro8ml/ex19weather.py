# LogisticRegression (로지스틱 회귀)
# [개념] 날씨 데이터를 활용하여 내일 비가 올지 여부(RainTomorrow)를 예측하는 이항 분류 모델임.
# [개념] 독립변수(기온, 습도 등)와 종속변수(비 유무) 간의 관계를 시그모이드 함수를 통해 0~1 사이의 확률로 표현함.

# [추천] 데이터의 스케일 차이가 클 경우 sklearn.preprocessing.StandardScaler를 사용하여 표준화하면 모델의 수렴 속도와 성능 향상에 도움이 됨.
# [추천] 결측치가 존재할 경우 data.dropna() 또는 data.fillna()를 통해 전처리를 선행해야 함.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import statsmodels.formula.api as smf

########################################################
# [문법] pd.read_csv(): 외부 데이터를 데이터프레임 형태로 로드함.
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv')
print(data.head(2), data.shape) # (366, 12)
print('\n')

# [문법] drop(axis=1): 특정 열(컬럼)을 제거함. 'Date'와 'RainToday'는 예측에서 제외.
data2 = data.drop(['Date', 'RainToday'], axis=1)
# [문법] map(): 범주형 문자열 데이터를 수치형(0, 1)으로 변환(Label Encoding 효과).
data2['RainTomorrow'] = data2['RainTomorrow'].map({'Yes':1, 'No':0})
print(data2.head(2), data2.shape)   # (366, 10)
print('\n')

# [문법] unique(): 종속변수의 클래스 종류를 확인 (0: 비 안옴, 1: 비 옴)
print(data2['RainTomorrow'].unique())
print('\n')

# RainTomorrow : 종속변수(범주형, label, class)
# 나머지 열 : 독립변수(feature)
####################################################################
# [개념] 데이터 분리 : 학습용(Train data), 검증용(Test data)
#   ㄴ [개념] 모델의 성능을 객관적으로 파악하기 위함.
#   ㄴ [개념] 모델 학습과 검증에 사용된 자료가 같다면 오버피팅(과적합) 우려 발생.

# [문법] train_test_split: 데이터를 학습용과 테스트용으로 무작위 분리. test_size=0.3은 30%를 검증용으로 사용함을 의미.
train, test = train_test_split(data2, test_size=0.3, random_state=42)   # random_state -> seed number 같은
print(train.shape, test.shape)  # (256, 10) (110, 10)
print(train.head(3))
print(test.head(3))
print('\n')

# [문법] columns.difference(): 특정 컬럼을 제외한 나머지 컬럼명들을 추출함.
col_select = '+'.join(train.columns.difference(['RainTomorrow']))
print(col_select)
# Cloud+Humidity+MaxTemp+MinTemp+Pressure+Rainfall+Sunshine+Temp+WindSpeed
print('\n')

# [문법] formula: '종속변수 ~ 독립변수1 + 독립변수2 + ...' 형태의 문자열 정의
my_formula = 'RainTomorrow ~ ' + col_select

# [문법] smf.glm(): 일반화 선형 모델. family=sm.families.Binomial() 설정 시 로지스틱 회귀와 동일함.
model_glm = smf.glm(formula=my_formula, data=train, family=sm.families.Binomial()).fit()
# [문법] smf.logit(): 로지스틱 회귀 전용 모델 생성 및 학습(.fit()).
model_logit = smf.logit(formula=my_formula, data=train).fit()
print(model_logit.summary()) # [개념] 모델의 통계적 유의성(P>|z|), 설명력(Pseudo R-squ) 등을 확인.
print('\n')
print(model_logit.params) # [문법] 학습된 회귀 계수(Weights) 및 절편(Bias) 출력.
print('\n')

# [문법] np.rint(): 소수점 첫째 자리에서 반올림하여 0 또는 1의 정수값으로 변환함.
print('예측값(glm) : ', np.rint(model_glm.predict(test)[:5].values))
print('예측값(logit) : ', np.rint(model_logit.predict(test)[:5].values))
print('실제값 : ', test['RainTomorrow'][:5].values)
print('\n')

# 분류 정확도
conf_mat = model_logit.pred_table()
print(conf_mat)
# [[197.   9.]
#  [ 21.  26.]]
print('\n')
print('분류 정확도(conf_mat) : ', (conf_mat[0][0] + conf_mat[1][1]) / len(train))
from sklearn.metrics import accuracy_score
print('분류 정확도(glm) : ', accuracy_score(test['RainTomorrow'], np.rint(model_glm.predict(test))))
print('분류 정확도(logit) : ', accuracy_score(test['RainTomorrow'], np.rint(model_logit.predict(test))))
print('\n')