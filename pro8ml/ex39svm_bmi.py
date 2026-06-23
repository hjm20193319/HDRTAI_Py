# # BMI 측정 관련
# # 공식 : 체중(kg) / 키(m)의 제곱
# # ex) 키:170, 몸무게:68  =>  68 / ((170 / 100)) * ((170 / 100))

###################################################################
# BMI dataset 생성 코드
# import random
# random.seed(12)

# def culc_bmi(h, w):
#     bmi = w / (h / 100) ** 2
#     if bmi < 18.5:
#         return '저체중'
#     elif 18.5 <= bmi < 25:
#         return '정상'
#     else:
#         return '비만'
    
# print(culc_bmi(170, 68))

# fp = open('bmi.csv', mode='w', encoding='utf-8')
# fp.write('height,weight,label\n')   # 제목
# # 무작위 데이터 생성
# cnt = {'저체중':0, '정상':0, '비만':0}

# for i in range(50000):
#     h = random.randint(150, 200)
#     w = random.randint(35, 100)
#     label = culc_bmi(h, w)
#     cnt[label] += 1
#     fp.write('{0},{1},{2}\n'.format(h, w, label))
# fp.close()
# print(cnt)
#####################################################################

# bmi data를 SVM으로 분류

from sklearn import svm, metrics # [문법] svm: SVM 알고리즘 포함, metrics: 성능 평가 지표 포함.
from sklearn.model_selection import train_test_split # [문법] 데이터를 학습용과 테스트용으로 분리.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import koreanize_matplotlib

df = pd.read_csv('bmi.csv') # [문법] pd.read_csv: CSV 파일을 데이터프레임으로 로드.
print(df.head(2))
print(df.shape) # (50000, 3)
print(df.info()) # [문법] 데이터프레임의 요약 정보(결측치, 데이터 타입 등) 확인.
print('\n')

label = df['label'] # [개념] 종속변수(Target): 저체중, 정상, 비만
print(label[:2])

# weight, height 정규화
# [개념] Feature Scaling: SVM은 거리 기반 알고리즘이므로 변수들의 범위를 일정하게 맞추는 과정이 필요함.
w = df['weight'] / 100 # [문법] 몸무게를 100으로 나누어 0~1 사이 범위로 조정.
print(w[:2].values)
h = df['height'] / 200 # [문법] 키를 200으로 나누어 0~1 사이 범위로 조정.
print(h[:2].values)
print('\n')

wh = pd.concat([w, h], axis=1) # [문법] concat: 분리된 몸무게와 키 시리즈를 하나의 데이터프레임으로 결합.
print(wh[:2])
print('\n')

# label은 dummy화 ( 문자형 -> 범주형 )
# [문법] map: 문자열 레이블을 모델 학습이 가능한 수치형(정수)으로 변환.
label = label.map({'저체중':0, '정상':1, '비만':2}) 
print(label[:2])
print('\n')

# train_test_split
# [문법] train_test_split: 전체 데이터를 학습용(70%)과 테스트용(30%)으로 분리.
x_train, x_test, y_train, y_test = train_test_split(wh, label, test_size=0.3, random_state=1)
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)
print('\n')

# 모델
# [문법] SVC: C(오차 허용 규제), kernel='rbf'(방사 기저 함수 커널)를 설정하여 모델 생성.
# [개념] C 값이 작을수록 마진을 넓게 설정하여 과적합(Overfitting) 방지 효과가 커짐.
model = svm.SVC(C=0.01, kernel='rbf')     
model.fit(x_train, y_train) # [문법] fit: 학습 데이터를 사용하여 최적의 결정 경계를 탐색.
print(model)
print('\n')

# 예측
# [문법] predict: 테스트 데이터를 입력하여 BMI 등급을 예측.
pred = model.predict(x_test) 
print('예측값 : ', pred[:10])
print('실제값 : ', np.array(y_test[:10]))
print('맞춘 개수 : ', (pred == y_test).sum())
print('오류수 : ', (pred != y_test).sum())
print('전체 대비 맞춘 비율 : ', sum(y_test == pred) / len(y_test))
print('분류 정확도 : ', metrics.accuracy_score(y_test, pred)) # [문법] accuracy_score: 전체 중 정답 비율 계산.
print('\n')

# 교차 검증 모델
# [문법] cross_val_score: 데이터를 3개(cv=3)의 폴드로 나누어 교차 검증 수행하여 모델의 일반화 성능 확인.
from sklearn.model_selection import cross_val_score 
scores = cross_val_score(model, wh, label, cv=3) 
print('각 3회 교차 검증 정확도 : ', scores)
print('교차 검증 평균 정확도 : ', np.round(scores.mean(), 5))
print('\n')

# 새로운 값 예측
# [주의] 학습 시 사용한 정규화 방식(100, 200으로 나누기)을 새로운 데이터에도 동일하게 적용해야 함.
new_data = pd.DataFrame({'weight':[66, 88], 'height':[188, 160]}) 
new_data['weight'] = new_data['weight'] / 100 
new_data['height'] = new_data['height'] / 200 
new_pred = model.predict(new_data)
print('예측값 : ', new_pred)
print('\n')

# 시각화
df2 = pd.read_csv('bmi.csv', index_col=2)
def scatter_func(lbl, color):
    # [문법] loc: 인덱스(label)를 기준으로 특정 등급의 데이터만 추출.
    b = df2.loc[lbl] 
    plt.scatter(x=b['weight'], y=b['height'], c=color, label=lbl) # [문법] scatter: 산점도 시각화.
    plt.legend()

scatter_func('정상', 'green')
scatter_func('비만', 'red')
scatter_func('저체중', 'yellow')
plt.xlabel('몸무게')
plt.ylabel('키')
plt.tight_layout()
plt.show()
print('\n')