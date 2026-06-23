# [개념] SVM(Support Vector Machine)을 이용한 XOR 연산 처리
# [개념] XOR 문제는 선형 분리가 불가능한 대표적인 문제로, 단순 선형 회귀나 로지스틱 회귀로는 해결이 어렵습니다.
# [개념] SVM은 커널 트릭(Kernel Trick)을 통해 데이터를 고차원으로 매핑하여 비선형 결정 경계를 찾아낼 수 있습니다.

# [추천] 데이터셋이 매우 작을 때는 딥러닝보다 SVM과 같은 머신러닝 알고리즘이 더 효율적이고 과적합 위험이 적습니다.
# [추천] 비선형 데이터의 경우 SVC의 kernel 파라미터를 'rbf'(기본값)로 설정하여 학습시키는 것이 좋습니다.


x_data = [
    [0,0,0],
    [0,1,1],
    [1,0,1],
    [1,1,0]
]

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm, metrics
 
# programmer 방식
# feature 와 label 분리
feature = []
label = []
for row in x_data:
    p = row[0]
    q = row[1]
    r = row[2]
    feature.append([p, q])
    label.append(r)

print(feature)
print(label)
print('\n')

# pandas 사용
# [문법] pd.DataFrame: 리스트 데이터를 판다스 데이터프레임으로 변환.
x_df = pd.DataFrame(x_data) 
# [문법] iloc: 행과 열의 인덱스를 사용하여 독립변수(feature)와 종속변수(label) 추출.
feature = np.array(x_df.iloc[:, 0:2]) 
label = np.array(x_df.iloc[:, 2]) 
print(feature)
print(label)
print('\n')

# 모델
# [개념] LogisticRegression: 선형 결정 경계를 사용하는 분류 모델 (XOR 해결 불가).
lmodel = LogisticRegression()      
lmodel.fit(feature, label) # [문법] fit(): 학습 데이터를 사용하여 모델 학습 수행.

# [개념] svm.SVC: 서포트 벡터 머신 분류기. 기본 커널인 'rbf'를 통해 비선형 분류 가능.
smodel = svm.SVC()                  
smodel.fit(feature, label) # [문법] fit(): 학습 데이터를 사용하여 최적의 결정 경계 탐색.

# 예측
# [문법] predict(): 학습된 모델을 사용하여 입력 데이터에 대한 결과값 예측.
pred1 = lmodel.predict(feature) 
pred2 = smodel.predict(feature) 
print('lmodel 예측값 : ', pred1)
print('smodel 예측값 : ', pred2)
print('\n')

# [문법] metrics.accuracy_score: 실제값과 예측값을 비교하여 정확도(0.0 ~ 1.0) 계산.
acc1 = metrics.accuracy_score(label, pred1) 
acc2 = metrics.accuracy_score(label, pred2) 
print('lmodel 정확도 : ', acc1) # [결과] 선형 모델은 XOR을 완벽히 분류하지 못함 (0.5)
print('smodel 정확도 : ', acc2) # [결과] 비선형 커널을 사용하는 SVM은 XOR 분류 성공 (1.0)
print('\n')
print('\n')