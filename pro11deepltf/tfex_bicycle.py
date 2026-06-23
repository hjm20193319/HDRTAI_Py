import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import matplotlib.pyplot as plt
import koreanize_matplotlib

data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv')
print(data.head(2))
print('\n')

pd.set_option('display.max_columns', None)   # 모든 열을 출력하도록 설정

# datetime 칼럼 타입 변환
data['datetime'] = pd.to_datetime(data['datetime'])
print(data.head(2))
print('\n')

# datetime 칼럼에서 연, 월, 일, 시간 추출하여 새로운 칼럼으로 추가
data['year'] = data['datetime'].dt.year
data['month'] = data['datetime'].dt.month
data['day'] = data['datetime'].dt.day
data['hour'] = data['datetime'].dt.hour

# 상관관계 분석
print(data.corr())
#             datetime    season   holiday  workingday   weather      temp     atemp  humidity  windspeed    casual  registered     count
# datetime    1.000000  0.480021  0.010988   -0.003658 -0.005048  0.180986  0.181823  0.032856  -0.086888  0.172728    0.314879  0.310187
# season      0.480021  1.000000  0.029368   -0.008126  0.008879  0.258689  0.264744  0.190610  -0.147121  0.096758    0.164011  0.163439
# holiday     0.010988  0.029368  1.000000   -0.250491 -0.007074  0.000295 -0.005215  0.001929   0.008409  0.043799   -0.020956 -0.005393
# workingday -0.003658 -0.008126 -0.250491    1.000000  0.033772  0.029966  0.024660 -0.010880   0.013373 -0.319111    0.119460  0.011594
# weather    -0.005048  0.008879 -0.007074    0.033772  1.000000 -0.055035 -0.055376  0.406244   0.007261 -0.135918   -0.109340 -0.128655
# temp        0.180986  0.258689  0.000295    0.029966 -0.055035  1.000000  0.984948 -0.064949  -0.017852  0.467097    0.318571  0.394454
# atemp       0.181823  0.264744 -0.005215    0.024660 -0.055376  0.984948  1.000000 -0.043536  -0.057473  0.462067    0.314635  0.389784
# humidity    0.032856  0.190610  0.001929   -0.010880  0.406244 -0.064949 -0.043536  1.000000  -0.318607 -0.348187   -0.265458 -0.317371
# windspeed  -0.086888 -0.147121  0.008409    0.013373  0.007261 -0.017852 -0.057473 -0.318607   1.000000  0.092276    0.091052  0.101369
# casual      0.172728  0.096758  0.043799   -0.319111 -0.135918  0.467097  0.462067 -0.348187   0.092276  1.000000    0.497250  0.690414
# registered  0.314879  0.164011 -0.020956    0.119460 -0.109340  0.318571  0.314635 -0.265458   0.091052  0.497250    1.000000  0.970948
# count       0.310187  0.163439 -0.005393    0.011594 -0.128655  0.394454  0.389784 -0.317371   0.101369  0.690414    0.970948  1.000000
print('\n')
# 낮은 상관관계: holiday, workingday, weather, windspeed, year, month, day

# feature와 label 분리
# 낮은 상관관계 제외하고 feature로 사용할 칼럼 선택
feature_cols = ['season', 'temp', 'atemp', 'humidity', 'hour']
x_data = data[feature_cols]
y_data = data['count']

# 정규화
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
x_data = scaler.fit_transform(x_data)

# 모델 작성
model = Sequential()
model.add(Input(shape=(5,)))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mse'])
print(model.summary())

# 모델 학습
history = model.fit(x_data, y_data, epochs=100, verbose=0, validation_split=0.2)
print('학습 완료')
print('evaluate result : ', model.evaluate(x_data, y_data, verbose=0))
print('\n')

pred = model.predict(x_data, verbose=0)
print('예측값 : ', pred[:5].flatten())
print('실제값 : ', y_data[:5].values)
print('\n')

# 설명력
from sklearn.metrics import r2_score
print('설명력 : ', r2_score(y_data, pred.ravel()))
print('\n')

# loss 시각화
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('model loss')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')