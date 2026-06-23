# 와인의 등급과 맛, 산도 등을 측정해, 레드/화이트 와인 분류기 작성

import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os

wdf = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/wine.csv', header=None)
print(wdf.head())
print('\n')
print(wdf.info())
print('\n')
print(wdf.iloc[:, 12].unique())
print('\n')
print(len(wdf[wdf.iloc[:, 12]==0])) # 4898
print(len(wdf[wdf.iloc[:, 12]==1])) # 1599
print('\n')


# array로 변환
dataset = wdf.values
x = dataset[:, 0:12]
y = dataset[:, -1]
print(x[:2])
print(y[:2])
print('\n')


# train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=12, stratify=y, shuffle=True)
print(x_train.shape)
print(x_test.shape)
print('\n')

# 모델
model = Sequential()
model.add(Input(shape=(12, )))
model.add(Dense(24, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())
print('\n')

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

# fit() 전에 훈련되지 않은 모델의 정확도
loss, acc = model.evaluate(x_train, y_train, verbose=0)
print(f'훈련되지 않은 모델의 정확도 : {acc*100:.2f}%')
print('\n')

# 모델 저장
MODEL_DIR = './winemodel/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 모델 저장에 대한 조건 설정
# modelpath = 'model/{epoch:02d}-{val_loss:.3f}.keras'
modelpath = './winemodel/winemodel.keras'
chkpoint = ModelCheckpoint(filepath=modelpath, monitor='val_loss', save_best_only=True, mode='auto')

# 학습 모델
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = model.fit(x_train, y_train, epochs=1000, validation_split=0.2, batch_size=64, callbacks=[early_stop, chkpoint])

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 모델의 정확도 : {acc*100:.2f}%')
print('\n')


# 시각화
epoch_len = np.arange(len(history.epoch))
plt.plot(epoch_len, history.history['loss'], label='train loss', color='blue')
plt.plot(epoch_len, history.history['val_loss'], label='val loss', color='red')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('학습 과정에서의 Loss 변화')
plt.legend()
plt.tight_layout()
plt.show()

plt.plot(epoch_len, history.history['accuracy'], label='train acc', color='blue')
plt.plot(epoch_len, history.history['val_accuracy'], label='val acc', color='red')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('학습 과정에서의 Accuracy 변화')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')


# 저장된 모델로 예측
from tensorflow.keras.models import load_model
mymodel = load_model(modelpath)

new_data = x_test[:5, :]
print(new_data)
print('\n')

new_pred = mymodel.predict(new_data, verbose=0)
print('예측 결과 : ', np.where(new_pred >= 0.5, 1, 0).ravel())
print('\n')