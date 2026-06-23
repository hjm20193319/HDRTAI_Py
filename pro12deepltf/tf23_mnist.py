# MNIST
# 60,000개의 훈련 이미지와 10,000개의 손글씨 숫자 테스트 이미지를 포함
# 데이터 세트는 28×28 픽셀 크기의 흑백 이미지로 구성

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import tensorflow as tf
import sys


(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data(path='mnist.npz')
print(x_train.shape, y_train.shape) # (60000, 28, 28) (60000,)
print(x_test.shape, y_test.shape)   # (10000, 28, 28) (10000,)
print('\n')

print(x_train[0])
print(y_train[0])
print('\n')



# 숫자 5 형태를 더 잘 보기 위해
# for i in x_train[0]:
#     for j in i:
#         sys.stdout.write('%s  '%j)
#     sys.stdout.write('\n')
# print('\n')



# # 숫자 시각화
# plt.imshow(x_train[0], cmap='gray')
# plt.show()



# 모델 만들기 선행 작업 - 전처리
x_train = x_train.reshape(60000, 784).astype('float32')     # 3차원 → 2차원
x_test = x_test.reshape(10000, 784).astype('float32')
print(x_train.shape)    # (60000, 784)
print(x_test.shape)     # (10000, 784)
print('\n')

# 정규화 - 필수는 아니지만 모델 성능이 향상 됨
x_train = x_train / 255.0
x_test = x_test / 255.0
print(x_train[0])
print(set(map(int, y_test)))    # 고유한 값 확인
print('\n')

# label One-Hot 처리 - softmax
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
print(y_train[0])   # 5 → [0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]
print('\n')

# validation data 직접 구성
x_val = x_train[50000:60000]    # 10000개는 학습 도중 검증 데이터로 사용
y_val = y_train[50000:60000]
x_train = x_train[:50000]
y_train = y_train[:50000]
print(x_train.shape, x_test.shape)  # (50000, 784) (10000, 784)
print('\n')



# 모델
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation, Dropout, Flatten

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
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),     # 직접 만든 데이터
    epochs=20,
    batch_size=128,
    verbose=2
)
print('학습 완료')
print('\n')

score = model.evaluate(x_test, y_test, batch_size=128, verbose=0)
print(f'loss : {score[0]:.4f}, acc : {score[1]:.4f}')
print('\n')



# 시각화
plt.plot(history.history['loss'], label='train loss', color='blue')
plt.plot(history.history['val_loss'], label='val loss', color='red')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('학습 과정에서의 Loss 변화')
plt.legend()
plt.tight_layout()
plt.show()

plt.plot(history.history['accuracy'], label='train acc', color='blue')
plt.plot(history.history['val_accuracy'], label='val acc', color='red')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('학습 과정에서의 Accuracy 변화')
plt.legend()
plt.tight_layout()
plt.show()




model.save('tf23model.keras')
print('모델 저장 완료')
print('\n')

mymodel = tf.keras.models.load_model('tf23model.keras')
print('모델 로드 완료')
print('\n')

pred = mymodel.predict(x_test[:1])
print('pred : ', pred)
print('예측값 : ', np.argmax(pred, 1)[0])
print('실제값 : ', np.argmax(y_test[0]))
print('\n')