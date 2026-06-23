# 모델 생성 방법 3가지 수행
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np

# 공부 시간에 따른 성적 데이터 예측
xdat = np.array([1, 2, 3, 4, 5], dtype='float32').reshape(-1, 1)
ydat = np.array([15, 32,39, 55, 60], dtype='float32').reshape(-1, 1)

# 모델 생성 방법 1 - Sequential API
model = Sequential()
model.add(Input(shape=(1,)))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='linear'))
print(model.summary())
opti = optimizers.SGD(learning_rate=0.001)

model.compile(loss='mse', optimizer=opti, metrics=['mse'])
history = model.fit(xdat, ydat, epochs=100, batch_size=1, verbose=0, shuffle=True)
print('학습 완료')
loss_metrics = model.evaluate(xdat, ydat)
print('loss_metrics : ', loss_metrics)

ypred = model.predict(xdat, verbose=0)
print('예측값 : ', ypred.ravel())
print('실제값 : ', ydat.ravel())
# 예측값 :  [16.803114 27.403105 38.00309  48.60308  59.20307 ]
# 실제값 :  [15. 32. 39. 55. 60.]
print('\n')

from sklearn.metrics import r2_score
r2 = r2_score(ydat.ravel(), ypred.ravel())
print('결정계수 R² : ', r2)
# 0.9490932822227478
print('\n')

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.scatter(xdat, ydat, label='실제값')
plt.plot(xdat, ypred, color='red', label='예측값')
plt.xlabel('공부 시간')
plt.ylabel('성적')
plt.title('단순 선형 회귀 모델')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')

# mse(Mean Squared Error) 변화량 시각화
plt.plot(history.history['mse'])
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.title('학습 과정에서의 MSE 변화')
plt.show()
print('\n')

# 모델 생성 방법 2 - Functional API
# 유연한 구조 : 입력 자료로 여러 층을 공유하거나 다양한 종류의 입출력 모델 생성 가능
# 다중 입력값 모델, 다중 출력값 모델, 층을 공유하는 모델 등 다양한 모델 생성 가능(데이터 흐름이 비순차적인 경우에도 효과적)
from tensorflow.keras.models import Model

inputs = Input(shape=(1,))
output1 = Dense(4, activation='relu')(inputs)   # 입력층과 첫 번째 은닉층 연결(이전층을 인자로 전달)
outputs = Dense(1, activation='linear')(output1)  # 첫 번째 은닉층과 출력층 연결

model2 = Model(inputs=inputs, outputs=outputs)

opti2 = optimizers.SGD(learning_rate=0.001)
model2.compile(loss='mse', optimizer=opti2, metrics=['mse'])
history2 = model2.fit(xdat, ydat, epochs=100, batch_size=1, verbose=0, shuffle=True)
print('학습 완료')
loss_metrics2 = model2.evaluate(xdat, ydat)
print('loss_metrics2 : ', loss_metrics2)

ypred2 = model2.predict(xdat, verbose=0)
print('예측값 : ', ypred2.ravel())
print('실제값 : ', ydat.ravel())
print('설명력 : ', r2_score(ydat.ravel(), ypred2.ravel()))
print('\n')

# 모델 생성 방법 3 - Subclassing API : 직접 모델 클래스 정의하여 모델 생성
# 모델을 상속 받아 직접 모델 생성
class MyModel(keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.dense1 = Dense(4, activation='relu')
        self.dense2 = Dense(1, activation='linear')

    # x : input 매개변수
    def call(self, x):      # Input 클래스를 사용하지 않고 call 메서드에서 직접 모델의 연산 정의
        x = self.dense1(x)
        return self.dense2(x)

model3 = MyModel()
opti3 = optimizers.SGD(learning_rate=0.001)
model3.compile(loss='mse', optimizer=opti3, metrics=['mse'])
history3 = model3.fit(xdat, ydat, epochs=100, batch_size=1, verbose=0, shuffle=True)
print('학습 완료')
loss_metrics3 = model3.evaluate(xdat, ydat)
print('loss_metrics3 : ', loss_metrics3)

ypred3 = model3.predict(xdat, verbose=0)
print('예측값 : ', ypred3.ravel())
print('실제값 : ', ydat.ravel())
print('설명력 : ', r2_score(ydat.ravel(), ypred3.ravel()))
print('\n')

# 모델 생성 방법 3-1 : Custom Layer 층 사용
from tensorflow.keras.layers import Layer

class MyLayer(Layer):
    def __init__(self, units=1, **kwargs):
        super(MyLayer, self).__init__(**kwargs)
        self.units = units
        self.dense1 = Dense(units, activation='relu')
        self.dense2 = Dense(1, activation='linear')

    def build(self, input_shape):   # 내부적으로 call() 호출
        print(f'build : input_shape = {input_shape}')
        self.w = self.add_weight(shape=(input_shape[-1], self.units), initializer='random_normal', trainable=True)
        self.b = self.add_weight(shape=(self.units,), initializer='zeros', trainable=True)

    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b   # 선형 변환 수행 y = wx + b
    
class MLP(Model):
    def __init__(self, **kwargs):
        super(MLP, self).__init__(**kwargs)
        self.layer1 = MyLayer(2)
        self.layer2 = MyLayer(1)

    def call(self, inputs):
        net = self.layer1(inputs)
        net = tf.nn.relu(net)    # 활성화 함수 적용
        return self.layer2(net)
    
model4 = MLP()
opti4 = optimizers.SGD(learning_rate=0.001)
model4.compile(loss='mse', optimizer=opti4, metrics=['mse'])
history4 = model4.fit(xdat, ydat, epochs=100, batch_size=1, verbose=0, shuffle=True)
print('학습 완료')
loss_metrics4 = model4.evaluate(xdat, ydat)
print('loss_metrics4 : ', loss_metrics4)

ypred4 = model4.predict(xdat, verbose=0)
print('예측값 : ', ypred4.ravel())
print('실제값 : ', ydat.ravel())
print('설명력 : ', r2_score(ydat.ravel(), ypred4.ravel()))
print('\n')
    