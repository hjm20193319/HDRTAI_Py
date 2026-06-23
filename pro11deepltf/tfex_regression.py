import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/data-8/materials-fa17/refs/heads/master/lec/galton.csv')
print(data.head(2))

ldata = data[data['gender'] == 'male']['childHeight']
print(ldata.head(2))
    # childHeight
fdata = data.loc[ldata.index, 'father']
print(fdata.head(2))

from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from sklearn.model_selection import train_test_split
import numpy as np

fdata = np.array(fdata).reshape(-1, 1)
ldata = np.array(ldata).reshape(-1, 1)

x_train, x_test, y_train, y_test = train_test_split(fdata, ldata, test_size=0.3, random_state=123, shuffle=True)

model = Sequential()
model.add(Input(shape=(1,)))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='linear'))
print(model.summary())

model.compile(loss='mse', optimizer='adam', metrics=['mse'])
history = model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=0, shuffle=True, validation_split=0.2)
print('학습 완료')
loss_metrics = model.evaluate(x_test, y_test)
print('loss_metrics : ', loss_metrics)

ypred = model.predict(x_test, verbose=0)
print('예측값 : ', ypred.ravel())
print('실제값 : ', y_test.ravel())
print('\n')

# train test의 mse 시각화
import matplotlib.pyplot as plt
plt.plot(history.history['mse'], label='train mse')
plt.plot(history.history['val_mse'], label='test mse')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.title('학습 과정에서의 MSE 변화')
plt.show()

# function api 방식
from tensorflow.keras import Model
inputs = Input(shape=(1,))
x = Dense(4, activation='relu')(inputs)
outputs = Dense(1, activation='linear')(x)

model2 = Model(inputs=inputs, outputs=outputs)
print(model2.summary())

model2.compile(loss='mse', optimizer='adam', metrics=['mse'])
history2 = model2.fit(x_train, y_train, epochs=100, batch_size=32, verbose=0, shuffle=True, validation_split=0.2)
print('학습 완료')
loss_metrics2 = model2.evaluate(x_test, y_test)
print('loss_metrics2 : ', loss_metrics2)

ypred2 = model2.predict(x_test, verbose=0)
print('예측값 : ', ypred2.ravel())
print('실제값 : ', y_test.ravel())
print('\n')