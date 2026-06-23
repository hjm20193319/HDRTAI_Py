import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout


(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data(path='mnist.npz')
print(x_train.shape, y_train.shape) 
print(x_test.shape, y_test.shape)   
print('\n')



x_train = x_train.reshape(60000, 784).astype('float32')     
x_test = x_test.reshape(10000, 784).astype('float32')


# 정규화
x_train = x_train / 255.0
x_test = x_test / 255.0



# validation data
x_val = x_train[50000:60000]   
y_val = y_train[50000:60000]
x_train = x_train[:50000]
y_train = y_train[:50000]


# 모델
model = Sequential()
model.add(Input(shape=(784, )))
# model.add(Dense(64))
# model.add(Activation('relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))
print(model.summary())
print('\n')

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=3,
    batch_size=128,
    verbose=2
)
print('학습 완료')
print('\n')

score = model.evaluate(x_test, y_test, batch_size=128, verbose=0)
print(f'loss : {score[0]:.4f}, acc : {score[1]:.4f}')
print('\n')