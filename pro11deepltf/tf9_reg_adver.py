# 다중 선형 회귀 : Tv, radio, Newspaper 광고비가 Sales에 미치는 영향 분석

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv')
del data['no']
print(data.head(2))

fdata = data[['tv', 'radio', 'newspaper']]
ldata = data['sales']
print(fdata.head(2))
print(ldata.head(2))
print('\n')

# feature 간 단위의 차이가 클 경우 정규화/표준화 작업이 모델 성능에 도움
from sklearn.preprocessing import StandardScaler, MinMaxScaler, minmax_scale

# 정규화 (Normalization) : 데이터의 범위를 0과 1 사이로 조정하는 방법
scaler = MinMaxScaler(feature_range=(0, 1))
fedata = scaler.fit_transform(fdata)
print(fedata[:3])
fedata = minmax_scale(fdata, feature_range=(0, 1), axis=0, copy=True)   
# axis=0 : 열 단위로 정규화, copy=True : 원본 데이터는 유지하면서 정규화된 데이터를 반환
print(fedata[:3])
print('\n')

# train/test 데이터 분할
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(fedata, ldata, test_size=0.3, random_state=123, shuffle=True)
# stratify는 분류에서 클래스 비율을 유지하기 위해 사용하지만, 회귀에서는 사용할 수 없음
print(x_train[:2], x_train.shape)   # (140, 3)
print(x_test[:2], x_test.shape)     # (60, 3)
print('\n')

# 전처리가 모두 끝난 경우 모델 설계 및 실행
model = Sequential()
model.add(Input(shape=(3,)))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='linear'))    # activation 생략 가능
print(model.summary())
#  Total params: 209 (836.00 B)
#  Trainable params: 209 (836.00 B)
#  Non-trainable params: 0 (0.00 B)

model.compile(loss='mse', optimizer='adam', metrics=['mse'])
tf.keras.utils.plot_model(
    model, 
    to_file='model.png', 
    show_shapes=True, 
    show_layer_names=True,
    show_layer_activations=True,
    show_dtype=True
)

####################################################################
# Tensorboard : 모델 학습 과정에서의 다양한 지표와 그래프를 시각적으로 확인할 수 있는 도구
# pip install tensorboard 설치 필요
from tensorflow.keras.callbacks import TensorBoard
import datetime
import os

# TensorBoard 로그 디렉토리 설정
log_dir = os.path.join('logs', 'fit', datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
tb = TensorBoard(
    log_dir=log_dir,    # 로그를 저장할 디렉토리 경로
    histogram_freq=1,  # 히스토그램을 기록할 빈도 (에포크마다 기록)
    write_graph=True,  # 모델 그래프를 기록할지 여부
    write_images=True,  # 모델 가중치의 이미지를 기록할지 여부
    update_freq='epoch'  # 로그 업데이트 빈도 (에포크마다 업데이트)
)
# 위에서 만든 내용을 fit() 함수의 callbacks 매개변수에 전달하여 TensorBoard 로그를 기록할 수 있음
# 결과는 브라우저로 확인
# 터미널 프롬포트에서 → tensorboard --logdir=logs/fit
# 브라우저에서 → http://localhost:6006/ (TensorBoard 대시보드에 접속하여 모델 학습 과정에서의 지표와 그래프를 시각적으로 확인할 수 있음)
####################################################################
# pip install pydot, graphviz 설치 필요
# : keras 모델의 구조를 시각적으로 표현하는 도구로, 모델의 레이어와 각 레이어의 출력 형태를 그래프로 나타냄

history = model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=2, validation_split=0.2, callbacks=[tb])
# validation_split=0.2 : 훈련 데이터의 20%를 검증 데이터로 사용하여 모델의 성능을 평가하는 데 활용

ev_loss = model.evaluate(x_test, y_test, verbose=0)
print('eval loss : ', ev_loss)

# history 값 확인
print('history : ', history.history)
print('history val_loss : ', history.history['val_loss'])   # validation 이 있는 경우
print('history val_mse : ', history.history['val_mse'])
print('history loss : ', history.history['loss'])
print('history mse : ', history.history['mse'])
print('\n')

# loss 시각화
import matplotlib.pyplot as plt
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.show()

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(y_test, model.predict(x_test)))
print('\n')

# 예측
pred = model.predict(x_test)
print('예측값 : ', pred[:5].flatten())
print('실제값 : ', y_test[:5].values)
print('\n')

# Functional API로 모델 설계
from tensorflow.keras.models import Model

# 입력층 정의
inputs = Input(shape=(3,), name='input_layer')

# 은닉층 정의
x = Dense(16, activation='relu', name='hidden_layer1')(inputs)
x = Dense(8, activation='relu', name='hidden_layer2')(x)

# 출력층 정의
outputs = Dense(1, activation='linear', name='output_layer')(x)

# 모델 생성(입력과 출력 연결)
func_model = Model(inputs=inputs, outputs=outputs)
print(func_model.summary())

func_model.compile(loss='mse', optimizer='adam', metrics=['mse'])
history_func = func_model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=2, validation_split=0.2)
print('학습 완료')

ev_loss_func = func_model.evaluate(x_test, y_test, verbose=0)
print('eval loss : ', ev_loss_func)
print('설명력 : ', r2_score(y_test, func_model.predict(x_test)))


