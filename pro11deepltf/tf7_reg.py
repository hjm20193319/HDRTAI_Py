# 단순 선형 회귀 모델 작성
import tensorflow as tf
import matplotlib.pyplot as plt
import koreanize_matplotlib
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam
import numpy as np

# feauture와 label 데이터 준비 : 2차원 형태로 입력하기 위함
xdata = np.array([1, 2, 3, 4, 5], dtype='float32').reshape(-1, 1)
ydata = np.array([1.2, 2.0, 3.0, 3.5, 5.5]).reshape(-1, 1)
print('상관 계수 : ', np.corrcoef(xdata.ravel(), ydata.ravel()))    # r = 0.98 : x와 y는 강한 양의 상관 관계가 있음

model = Sequential()
model.add(Input(shape=(1,)))
model.add(Dense(5, activation='relu'))    
model.add(Dense(1, activation='linear'))    
# 선형 회귀 모델이므로 activation은 'linear'로 설정 - 선형 활성화 함수는 입력값을 그대로 출력하는 함수
print(model.summary())

model.compile(loss='mse', optimizer='sgd', metrics=['mse'])    # 손실 함수는 MSE, 최적화 알고리즘은 SGD
# MSE(Mean Squared Error)는 예측값과 실제값의 차이를 제곱하여 평균한 값으로, 회귀 문제에서 자주 사용되는 손실 함수입니다.

model.fit(xdata, ydata, epochs=30, batch_size=1, verbose=1, shuffle=True)    # 모델 학습 - 30번 반복, verbose=1은 학습 과정 출력
print('학습 완료')
loss_eval = model.evaluate(xdata, ydata)
print('loss_eval : ', loss_eval)

pred = model.predict(xdata)
print('예측값 : ', pred.ravel())
print('실제값 : ', ydata.ravel())
print('\n')

# 결정계수 R² , 설명력
from sklearn.metrics import r2_score
print('결정계수 R²(설명력) : ', r2_score(ydata, pred))    
# R²는 모델이 실제 데이터를 얼마나 잘 설명하는지를 나타내는 지표로, 1에 가까울수록 모델이 데이터를 잘 설명한다는 의미입니다.
# 시각화
plt.scatter(xdata, ydata, label='실제값')
plt.plot(xdata, pred, color='red', label='예측값')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('선형 회귀 모델')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')

# 새로운 값으로 예측
new_x = np.array([1.5, 5.7, -3.0]).reshape(-1, 1)
new_pred = model.predict(new_x)
print('새로운 입력값 : ', new_x.ravel())
print('새로운 예측값 : ', new_pred.ravel())
print('\n')