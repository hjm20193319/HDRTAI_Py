import pandas as pd
import numpy as np

data = pd.read_csv('weekendmeal.csv')
print(data)

data = data[(data['요일']=='토') | (data['요일']=='일')]
print(data)

# logit() 사용
import statsmodels.formula.api as smf

result = smf.logit(formula='외식유무 ~ 소득수준', data=data).fit()

pred = result.predict(data)
print('실제값 : ', data['외식유무'].values)
print('예측값 : ', np.around(pred.values).astype(int))
# 실제값 :  [0 0 0 0 1 1 0 0 1 1 0 1 1 1 1 0 0 1 1 0 0]
# 예측값 :  [1 0 0 0 1 1 0 0 1 1 0 1 1 1 1 0 0 1 0 0 0]
print('\n')

from sklearn.metrics import accuracy_score
print('분류 정확도 : ', accuracy_score(data['외식유무'], np.around(pred.values)))
# 분류 정확도 :  0.9047619047619048
print('\n')

# glm() 사용
import statsmodels.api as sm
result2 = smf.glm(formula='외식유무 ~ 소득수준', data=data, family=sm.families.Binomial()).fit()

glm_pred = result2.predict(data)
print('실제값 : ', data['외식유무'].values)
print('glm 예측값 : ', np.around(glm_pred.values).astype(int))
#     실제값 :  [0 0 0 0 1 1 0 0 1 1 0 1 1 1 1 0 0 1 1 0 0]
# glm 예측값 :  [1 0 0 0 1 1 0 0 1 1 0 1 1 1 1 0 0 1 0 0 0]
print('\n')

print('glm 모델 분류 정확도 : ', accuracy_score(data['외식유무'], np.around(glm_pred.values)))
# glm 모델 분류 정확도 :  0.9047619047619048
print('\n')

# 새로운 값으로 분류 예측
newdata = input('소득수준을 입력하시오(양의 정수) : ')
newdf = pd.DataFrame()
newdf['소득수준'] = [int(newdata)]
print('\n')

new_pred = result.predict(newdf)
if np.around(new_pred.values) == 1:
    print('logit()을 사용한 예측 결과, 외식을 합니다')
else:
    print('logit()을 사용한 예측 결과, 외식을 하지 않습니다')

new_pred2 = result2.predict(newdf)
if np.around(new_pred2.values) == 1:
    print('glm()을 사용한 예측 결과, 외식을 합니다')
else:
    print('glm()을 사용한 예측 결과, 외식을 하지 않습니다')