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

data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/pima-indians-diabetes.data.csv')
columns = [
    'Pregnancies',              # 임신 횟수
    'Glucose',                  # 포도당 부하 검사 수치
    'BloodPressure',            # 혈압(mm Hg)
    'SkinThickness',            # 삼두근 뒤쪽의 피하지방 측정값(mm)
    'Insulin',                  # 혈청 인슐린(mu U/ml)
    'BMI',                      # 체질량지수(kg/m^2)
    'DiabetesPedigreeFunction', # 당뇨 내력 가중치 값
    'Age',                      # 나이
    'Outcome'                   # 당뇨 여부 (0 또는 1)
]
data.columns = columns
print(data.head())
print('\n')
print(data.info())
print('\n')


# feature/label 분리
x = data.drop('Outcome', axis=1)
y = data['Outcome']


# train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
print(x_train.shape)
print(x_test.shape)
print('\n')


# Scaling
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


# Sequential API 버전 model
model = Sequential([
    Input(shape=(x_train.shape[1], )),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

print(model.summary())
print('\n')

# 모델 저장
MODEL_DIR = './diabetesmodel/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 모델 저장에 대한 조건 설정
# modelpath = 'model/{epoch:02d}-{val_loss:.3f}.keras'
modelpath = './diabetesmodel/diabetesmodel.keras'
chkpoint = ModelCheckpoint(filepath=modelpath, monitor='val_loss', save_best_only=True, mode='auto')

# 학습 모델
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = model.fit(
    x_train, y_train,
    validation_data=(x_test, y_test),
    epochs=100,
    batch_size=32,
    verbose=2,
    callbacks=[early_stop, chkpoint]
)
print('학습 완료')
print('\n')

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 결과 손실 : {loss:.2f}')
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



# Functional API 버전 model
from tensorflow.keras.models import Model

inputs = Input(shape=(x_train.shape[1], ))
outputs = Dense(16, activation='relu')(inputs)
outputs = Dense(8, activation='relu')(outputs)
outputs = Dense(1, activation='sigmoid')(outputs)
model_func = Model(inputs=inputs, outputs=outputs)
print(model_func.summary())
print('\n')

model_func.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

model_func.fit(
    x_train, y_train,
    validation_data=(x_test, y_test),
    epochs=100,
    batch_size=32,
    verbose=2,
    callbacks=[early_stop, chkpoint]
)
print('학습 완료')
print('\n')

loss, acc = model_func.evaluate(x_test, y_test, verbose=0)
print(f'테스트 결과 손실 : {loss:.2f}')
print(f'테스트 모델의 정확도 : {acc*100:.2f}%')
print('\n')