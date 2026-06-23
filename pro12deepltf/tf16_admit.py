# 데이터를 이용하여 미국 대학원 입학여부를 분류하는 모델을 작성

# label : admit
# feature : gre, gpa, rank

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
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('binary.csv')
print(df.head(3))
print('\n')
print(df.info())
print('\n')


# 전처리
# rank는 숫자이지만 연속형이 아니라, 범주형 데이터 → One Hot 처리
df = pd.get_dummies(df, columns=['rank'], dtype=int)
print(df.head(3))
print('\n')


# feature 와 label 분리
x = df.drop('admit', axis=1)
y = df['admit']
print(x.head(3))
print(y.head(3))
print('\n')


# 🔥 train/test split 먼저 수행
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)
print(x_train.shape)
print(x_test.shape)
print('\n')


# 🔥 scaling은 train 기준으로만 수행
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


# model
model = Sequential([
    Input(shape=(x_train.shape[1], )),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.001),
    metrics=['accuracy']
)

print(model.summary())
print('\n')

history = model.fit(
    x_train, y_train,
    validation_data=(x_test, y_test),
    epochs=100,
    batch_size=32,
    verbose=2
)
print('학습 완료')
print('\n')

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 결과 손실 : {loss:.2f}')
print(f'테스트 모델의 정확도 : {acc*100:.2f}%')
print('\n')

plt.figure(figsize=(12, 6))
# loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='train loss', color='blue')
plt.plot(history.history['val_loss'], label='val loss', color='red')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('학습 과정에서의 Loss 변화')
plt.legend()
# accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='train acc', color='blue')
plt.plot(history.history['val_accuracy'], label='val acc', color='red')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('학습 과정에서의 Accuracy 변화')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')


# 사용자 입력 결과 예측
gre = float(input('GRE 점수 입력 : '))
gpa = float(input('GPA 점수 입력 : '))
rank = float(input('rank 입력(1~4) : '))

rank_encoded = [0, 0, 0, 0]     # 입력된 rank 원핫 처리
rank_encoded[int(rank)-1] = 1

user_input = np.array([[gre, gpa] + rank_encoded])
print('user_input : ', user_input)
print('\n')


user_scaled = scaler.transform(user_input)
new_pred = model.predict(user_scaled, verbose=0)
prob = new_pred[0][0] * 100
print('합격 확률 : ', prob, '%')
print('\n')
if prob >= 0.5:
    print('합격 가능성이 높음')
else:
    print('불합격 가능성이 높음')
print('\n')