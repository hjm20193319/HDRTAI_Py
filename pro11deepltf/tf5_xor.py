import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam

# 1) 데이터 수집 및 가공
x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])      # XOR 게이트

model = Sequential()
model.add(Input(shape=(2, )))   # 입력층 input layer
# model.add(Dense(units=1))
# model.add(Activation('sigmoid'))
model.add(Dense(units=5, activation='relu'))     # 은닉층 hidden layer
model.add(Dense(units=5, activation='relu'))     # 은닉층 hidden layer
model.add(Dense(units=1, activation='sigmoid'))     # 출력층 output layer
print(model.summary())  # 설계된 모델의 Layer, Parameter 수 확인
# (입력 2 + 편향 1) * 노드 5 = 15
# (입력 5 + 편향 1) * 노드 5 = 30
# (입력 5 + 편향 1) * 출력 1 = 6
# 총 Parameter = 51

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

history = model.fit(x, y, batch_size=1, epochs=100, verbose=1)
loss_metrics = model.evaluate(x, y)
print('loss_metrics : ', loss_metrics)
print('history : \n', history.history)
# history.history → 학습 도중에 발생된 정확도와 손실을 보여준다

pred = (model.predict(x) > 0.5).astype("int32")
print('예측값 : \n', pred.ravel())

# 시각화
import matplotlib.pyplot as plt
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['accuracy'], label='accuracy')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

