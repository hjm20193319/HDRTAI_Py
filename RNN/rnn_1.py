# RNN
# 순서가 있는 데이터를 다룬다
# 이전 값들의 흐름을 기억하면서 다음 값을 예측한다

# 노이즈가 있는 사인파 데이터를 이용해, RNN 예측 모델 작성

import numpy as np
import matplotlib.pyplot as plt

xdata = np.linspace(-2 * np.pi, 2 * np.pi)      # x축 데이터 생성
# print(xdata)    # 50개 만들어짐(default 값)

sindata = np.sin(xdata) + 0.1 * np.random.randn(len(xdata))     # 난수로 노이즈 추가
# print('sindata : \n', sindata)

# 시각화
# plt.plot(xdata, sindata)
# plt.show()


#######################################################################################
n_rnn = 10
n_sample = len(xdata) - n_rnn   # 학습 샘플 개수
x = np.zeros((n_sample, n_rnn)) # 입력 시퀀스를 저장할 배열
t = np.zeros((n_sample, n_rnn))     # 예측 대상 시퀀스를 저장할 배열 (한 칸 뒤로 밀린 값을 정답 t로 생성)

for i in range(0, n_sample):
    x[i] = sindata[i : i + n_rnn]
    t[i] = sindata[i + 1 : i + n_rnn + 1]
# print('x : \n', x[:3])
# print('t : \n', t[:3])

x = x.reshape(n_sample, n_rnn, 1)     # RNN은 입력을 (샘플수, 시계열수, 입력층 뉴런)
print(x.shape)      # (40, 10, 1)
t = t.reshape(n_sample, n_rnn, 1)
print(t.shape)      # (40, 10, 1)
# ------데이터 준비 완료-----



#######################################################################################
# SimpleRNN 구축
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense

n_in = 1        # 입력층 뉴런 수
n_mid = 20      # 은닉층 뉴런 수
n_out = 1       # 출력층 뉴런 수

model = Sequential()
model.add(SimpleRNN(n_mid, input_shape=(n_rnn, n_in), return_sequences=True))   # activation='tanh'
# return_sequences = True : RNN이 마지막 시점의 결과만 내보내는 것이 아니라, 각 시점마다 결과를 출력
#               ↪ 출력이 many가 됨 (many to many)
model.add(Dense(n_out,activation='linear'))
print(model.summary())
model.compile(loss='mean_squared_error', optimizer='sgd')



#######################################################################################
history = model.fit(x, t, epochs=20, batch_size=8, validation_split=0.1)

loss = history.history['loss']
val_loss = history.history['val_loss']
plt.plot(np.arange(len(loss)), loss, label='loss')
plt.plot(np.arange(len(val_loss)), val_loss, label='val_loss')
plt.legend()
plt.tight_layout()
plt.show()



#######################################################################################
# 에측
pred = x[0].reshape(-1)     # 1차원 벡터화
print('pred : ', pred)

# 총 n_sample 횟수만큼 반복하며 예측값을 이어 붙이기
for i in range(0, n_sample):
    yhat = model.predict(pred[-n_rnn:].reshape(1, n_rnn, 1))     # 뒤 10개를 
    pred = np.append(pred, yhat[0][n_rnn - 1][0])   # 출력의 최후 결과 추가

plt.plot(np.arange(len(sindata)), sindata, label='Train Data')
plt.plot(np.arange(len(pred)), pred, label='Prediction')
plt.legend()
plt.tight_layout()
plt.show()



#######################################################################################
# 예측값과 실제값 비교
predicted = pred[n_rnn:]
actual = sindata[n_rnn:]

for i in range(10):
    print(f'{i:02d} - 예측:{predicted[i]:.4f}, 실제:{actual[i]:.4f}')

# MSE
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(actual, predicted)
print('MSE : ', mse)
# RMSE
rmse = np.sqrt(mse)
print('RMSE : ', rmse)