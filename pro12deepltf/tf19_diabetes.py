# 이항 분류(sigmoid)는 다항 분류(softmax)로 처리 가능

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split


datas = np.loadtxt('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/diabetes.csv', delimiter=',')
print(datas.shape) # (759, 9)
print('\n')
print(datas[:1])
print('\n')
print(set(datas[:, -1]))


x_train, x_test, y_train, y_test = train_test_split(datas[:, 0:8], datas[:, -1], test_size=0.3, random_state=123, shuffle=True)
print(x_train.shape)
print(x_test.shape)
print('\n')


# 이항분류(sigmoid)
model = Sequential()
model.add(Input(shape=(8, )))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())
print('\n')

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.fit(
    x_train, y_train,
    epochs=100,
    batch_size=32,
    verbose=0
)
print('학습 완료')
print('\n')

scores = model.evaluate(x_test, y_test, verbose=0)
print('Sigmoid 모델 평가 결과 : ', scores)
print('\n')



# 다항분류(softmax)
from tensorflow.keras.utils import to_categorical

y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)


model = Sequential()
model.add(Input(shape=(8, )))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(2, activation='softmax'))
print(model.summary())
print('\n')

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.fit(
    x_train, y_train,
    epochs=100,
    batch_size=32,
    verbose=0
)
print('학습 완료')
print('\n')

scores = model.evaluate(x_test, y_test, verbose=0)
print('Softmax 모델 평가 결과 : ', scores)
print('\n')