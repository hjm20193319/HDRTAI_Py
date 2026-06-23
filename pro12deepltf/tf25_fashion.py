# Fashion-MNIST 데이터셋

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import tensorflow as tf
import sys
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation, Dropout, Flatten



#######################################################################################
fashion_mnist = tf.keras.datasets.fashion_mnist.load_data()
(x_train, y_train), (x_test, y_test) = fashion_mnist
print(x_train.shape, y_train.shape) # (60000, 28, 28) (60000,)
print(x_test.shape, y_test.shape)   # (10000, 28, 28) (10000,)
print('\n')

class_names = [
    'T-shirt/top',
    'Trouser',
    'Pullover',
    'Dress',
    'Coat',
    'Sandal',
    'Shirt',
    'Sneaker',
    'Bag',
    'Ankle boot'
]
print(class_names)
print('\n')
print(set(map(int, y_test)))
print('\n')


#######################################################################################
# 시각화
plt.imshow(x_train[0], cmap='gray')
plt.show()

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(x_train[i], cmap='gray')
    plt.xlabel(class_names[y_train[i]])
plt.tight_layout()
plt.show()



#######################################################################################
# 정규화
print(x_train[0])
print('\n')
x_train = x_train / 255.0
x_test = x_test / 255.0
print(x_train[0])
print('\n')



#######################################################################################
# model
model = Sequential([
    Input(shape=(28, 28)),  # resize 안해서..
    Flatten(),              # 1차원으로 바꿔줌
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(10, activation='softmax')
])

print(model.summary())
print('\n')

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.fit(
    x_train, y_train,
    validation_split=0.2,
    epochs=10,
    batch_size=128,
    verbose=1
)
print('학습 완료')
print('\n')

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 결과 손실 : {test_loss:.2f}')
print(f'테스트 모델의 정확도 : {test_acc*100:.2f}%')
print('\n')

pred = model.predict(x_test)
print('pred : ', pred)
print('예측값 : ', np.argmax(pred[0]))
print('실제값 : ', y_test[0])
print('\n')


#######################################################################################
# 각 이미지 출력용 함수(예측 이미지와 실제 label 비교)
def plot_image(i, pred, y_true, x_img):
    pred_arr = pred[i]
    true_label = y_true[i]
    img = x_img[i]
    pred_label = np.argmax(pred_arr)
    pred_percent = 100 * np.max(pred_arr)
    color = 'blue' if pred_label == true_label else 'red'
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(img, cmap='gray')
    plt.xlabel(f'예측 : {class_names[pred_label]} ({pred_percent:.0f}%)\n' f'실제 : {class_names[true_label]}', color=color)
    


# 각 이미지에 라벨 등의 정보 표시 - 막대 그래프
def plot_values_arr(i, pred, y_true):
    pred_arr = pred[i]
    true_label = y_true[i]
    pred_label = np.argmax(pred_arr)

    plt.xticks(range(10), class_names, rotation=45, ha='right')
    plt.yticks([])
    plt.ylim([0, 1])
    bars = plt.bar(range(10), pred_arr, color='#777777')
    bars[pred_label].set_color('red')   # 예측값
    bars[true_label].set_color('blue')  # 실제값


def show_one_prediction(i, pred, y_true, x_img):
    plt.figure(figsize=(7,3))
    plt.subplot(1, 2, 1)
    plot_image(i, pred, y_true, x_img)
    plt.subplot(1, 2, 2)
    plot_values_arr(i, pred, y_true)
    plt.tight_layout()
    plt.show()



show_one_prediction(1, pred, y_test, x_test)    # 1개 이미지

# 여러 이미 보기 3x3 출력
def show_prediction_grid(start, pred, y_true, x_img, rows=3, cols=3):
    plt.figure(figsize=(10, 10))
    for n in range(rows*cols):
        i = start + n
        plt.subplot(rows, cols, n+1)
        true_label = y_true[i]
        pred_label = np.argmax(pred[i])
        img = x_img[i]
        pred_percent = 100 * np.max(pred[i])
        color = 'blue' if pred_label == true_label else 'red'
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(img, cmap='gray')
        plt.xlabel(f'예측 : {class_names[pred_label]} ({pred_percent:.0f}%)\n' f'실제 : {class_names[true_label]}', color=color)
    plt.tight_layout()
    plt.show()        
            
# 0 번부터 9개 보기
show_prediction_grid(0, pred, y_test, x_test)

# 15 번부터 9개 보기
show_prediction_grid(15, pred, y_test, x_test)


i = 0
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image