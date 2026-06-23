# 학습된 대영모델(백본)인 MobileNet v2를 전이학습하여 cifar10 dataset 분류하기

# 전이학습 Transfer Learning
# 이미 학습된 모델을 일부 재학습하여 내가 가진 새 데이터에 활용하기


#######################################################################################
import tensorflow as tf

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()


# 전처리
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.



NUM_CLASSES = 10
# one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, NUM_CLASSES)
y_test = tf.keras.utils.to_categorical(y_test, NUM_CLASSES)

print('train data : ', x_train.shape)
print('test data : ', x_test.shape)


#######################################################################################
# 전이학습 : 기존 모델(백본)의 가중치는 모두 동결(freeze) → 분류기만 학습에 참여
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128, 128, 3),      # 입력 크기 96, 128, 160, 192, 224 등을 지원
    include_top=False,      # MobileNet V2의 분류기 부분을 뺌, 컨볼루션 레이어만 남김
    weights='imagenet'      # 사전 학습 된 가중치 호출(120만장 이미지, 1000개의 클래스)
) 

base_model.trainable = False    # 가중치 동결 → MobileNet V2는 학습에 참여하지 않도록 동결
print(base_model.summary())
#  Total params: 2,257,984 (8.61 MB)
#  Trainable params: 0 (0.00 B)
#  Non-trainable params: 2,257,984 (8.61 MB)


#######################################################################################
# 새로운 모델 생성 - MobileNet V2 모델 이용
inputs = tf.keras.Input(shape=(32, 32, 3))
x = tf.keras.layers.Resizing(128, 128)(inputs)      # cifar10 이미지를 MobileNet V2에 맞게 리사이징
x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)     # MaxPooling2D 보다 더 급격하게 feature 의 크기를 줄임
outputs = tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')(x)   # 새 분류기로 정의

model_tl = tf.keras.Model(inputs, outputs, name='model_tl')
print(model_tl.summary())



#######################################################################################
model_tl.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model_tl.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2, verbose=2)



#######################################################################################
loss, acc = model_tl.evaluate(x_test, y_test, verbose=0)

print(f'loss : {loss:.4f}, acc : {acc:.4f}')


#######################################################################################
# 성능 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], 'b-', label='train_loss')
plt.plot(history.history['val_loss'], 'r--', label='val_loss')
plt.legend()
plt.xlabel('epoch')
plt.ylabel('loss')

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], 'b-', label='train_acc')
plt.plot(history.history['val_accuracy'], 'r--', label='val_acc')
plt.legend()
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.tight_layout()
plt.show()



#######################################################################################
# 미세 조정 Fine Tunning - 전이 학습 이후 성능 향상을 위해 백본의 일부 층을 학습에 참여시킴
base_model.trainable = True     # 모델 전체 학습에 참여 가능

for layer in base_model.layers[:-10]:   # 마지막 10개층만 해제하고, 나머지는 다시 동결
    layer.trainable = False

model_tl.compile(
    optimizer=tf.keras.optimizers.Adam(0.000001),    # 학습률을 매우 낮춤 → 미세조정이기 때문에
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model_tl.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2, verbose=2)

loss, acc = model_tl.evaluate(x_test, y_test, verbose=0)
print(f'loss : {loss:.4f}, acc : {acc:.4f}')