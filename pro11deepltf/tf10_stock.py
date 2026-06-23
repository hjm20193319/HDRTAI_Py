# 주식 데이터로 다중선형회귀모델 작성
# 전날 데이터로 다음날 종가 예측

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.preprocessing import MinMaxScaler

# 배열 자료로 읽기
datas = np.loadtxt('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/stockdaily.csv', delimiter=',', skiprows=1)
print(datas[:2], len(datas))    # 732
print('\n')

# feature
x_data = datas[:, 0:-1]
print(x_data.shape)   # (732, 4)
scaler = MinMaxScaler(feature_range=(0, 1)) # 정규화
x_data = scaler.fit_transform(x_data)
print(x_data[:2])
# 참고
print(scaler.inverse_transform(x_data[:2]))   # 정규화된 데이터를 원래 값으로 되돌리는 방법
print('\n')

# label
y_data = datas[:, -1]   # 종가
print(y_data.shape)   # (732,)
print('\n')

# x_data와 y_data를 한 칸씩 어긋나게 만들어서 다음날 종가 예측
print(x_data[0], y_data[0])
print(x_data[1], y_data[1])
x_data = np.delete(x_data, -1, axis=0)  # 마지막 행 삭제
y_data = np.delete(y_data, 0, axis=0)   # 첫 번째 요소 삭제
print(x_data[0], y_data[0])
print('\n')

##################################################
# train/test split 유무에 따른 모델 성능 비교
##################################################

# train/test 데이터 분할 없이 모델 작성
model = Sequential()
model.add(Input(shape=(4,)))
model.add(Dense(1, activation='linear'))
print(model.summary())

model.compile(loss='mse', optimizer='sgd', metrics=['mse'])
model.fit(x_data, y_data, epochs=200, verbose=0)
print('학습 완료')
print('evaluate result : ', model.evaluate(x_data, y_data, verbose=0))
# evaluate result :  [62.501731872558594, 62.501731872558594]
print('\n')

pred = model.predict(x_data, verbose=0)
from sklearn.metrics import r2_score
print('ttsplit 없이 r2_score : ', r2_score(y_data, pred.ravel()))
# 0.9938377354662761 ⇨ 과적합이 매우 의심스러움
print('\n')

# 시각화
plt.plot(y_data, 'b', label='실제값')
plt.plot(pred, 'r', label='예측값')
plt.legend()
plt.title('train/test split 없이 모델 성능')
plt.show()

# train/test split 후 모델 작성
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=123, shuffle=False)
print(x_train.shape, x_test.shape)
# (511, 4) (220, 4)

# 모델 작성
model2 = Sequential()
model2.add(Input(shape=(4,)))
model2.add(Dense(1, activation='linear'))
model2.compile(loss='mse', optimizer='sgd', metrics=['mse'])

# 모델 학습
model2.fit(x_train, y_train, epochs=200, verbose=0)

# 모델 평가
print('train/test split 후 evaluate result : ', model2.evaluate(x_test, y_test, verbose=0))
# train/test split 후 evaluate result :  [35.131065368652344, 35.131065368652344]

# r2_score 계산
pred2 = model2.predict(x_test, verbose=0)
print('train/test split 후 r2_score : ', r2_score(y_test, pred2.ravel()))
#  0.947038412718437 ⇨ train/test split 없이 모델 작성한 경우보다 낮지만, 
# 과적합이 의심스러운 모델보다는 훨씬 현실적인 성능을 보여줌 → 그래도 여전히 과적합이 의심스러운 수준이긴 함
print('\n')

# 시각화
plt.plot(y_test, 'b', label='실제값')
plt.plot(pred2, 'r', label='예측값')
plt.legend()
plt.title('train/test split 후 모델 성능')
plt.show()
print('\n')

# train/test split + validation_split 후 모델 작성
model3 = Sequential()
model3.add(Input(shape=(4,)))
model3.add(Dense(1, activation='linear'))
model3.compile(loss='mse', optimizer='sgd', metrics=['mse'])

# 모델 학습
model3.fit(x_train, y_train, epochs=200, verbose=0, validation_split=0.2)

# 모델 평가
print('train/test split + validation_split 후 evaluate result : ', model3.evaluate(x_test, y_test, verbose=0))
#  [108.25725555419922, 108.25725555419922]

# r2_score 계산
pred3 = model3.predict(x_test, verbose=0)
print('train/test split + validation_split 후 r2_score : ', r2_score(y_test, pred3.ravel()))
# 0.8367974816731931 ⇨ train/test split + validation_split 후 모델 작성한 경우가 가장 낮은 r2_score를 보여줌
#                                                          → 과적합이 의심스러운 모델보다는 훨씬 현실적인 성능을 보여줌
print('\n')

# 시각화
plt.plot(y_test, 'b', label='실제값')
plt.plot(pred3, 'r', label='예측값')
plt.legend()
plt.title('train/test split + validation_split 후 모델 성능')
plt.show()
print('\n')

# 딥러닝의 이슈 : 최적화와 일반화
