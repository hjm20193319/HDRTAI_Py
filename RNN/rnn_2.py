# LSTM 으로 다음 숫자 예측
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, GRU, Input

x = np.array([[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7],[6,7,8],[7,8,9],[8,9,10]])
y = np.array([4,5,6,7,8,9,10,11])

x = x.reshape((8, 3, 1))     # 입력 형태 (samples, time_steps, features)


# 모델 정의
model = Sequential()
model.add(Input(shape=(3,1)))   # 시계열(time_steps) 3개, features=1 → 각 time_step 마다 갖는 개수
model.add(LSTM(32, activation='tanh'))
# model.add(LSTM(10, activation='tanh', return_sequences=True))   # → many to many / LSTM → 표준
# model.add(GRU(10, activation='tanh', return_sequences=True))   # → many to many
#            ↪ 계산량 적고 속도는 빠름, parameter 수가 줄어듦
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='linear'))
model.summary()



#######################################################################################
model.compile(loss='mse', optimizer='adam')

from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='loss', patience=3, mode='auto')
model.fit(x, y, epochs=1000, batch_size=1, verbose=2, callbacks=[es])



#######################################################################################
print('예측값 : ', model.predict(x).ravel())
print('실제값 : ', y.ravel())

# 새로운 값으로 예측
x_input = np.array([25, 35, 45])
x_input = x_input.reshape((1, 3, 1))

new_pred = model.predict(x_input)
print('new_pred : ', new_pred.ravel())