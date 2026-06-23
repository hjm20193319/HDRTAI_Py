# tf_flowers dataset (5종 꽃 이미지)으로 전이 학습 + 미세 조정 실습

import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, models


(train_ds, val_ds), ds_info = tfds.load(
    'tf_flowers',
    split=['train[:80%]', 'train[80%:]'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True
)


for image, label in train_ds.take(1):
    print(type(image), type(label))

print(ds_info.features['label'].names)
# ['dandelion', 'daisy', 'tulips', 'sunflowers', 'roses']




#######################################################################################
# 전처리
IMG_SIZE = (160, 160)
BATCH_SIZE = 32

def preprocessFunc(image, label):
    image = tf.image.resize(image, IMG_SIZE)
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

train_ds = train_ds.map(preprocessFunc).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.map(preprocessFunc).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)




#######################################################################################
# 백본 base model 불러오기
base_model = tf.keras.applications.MobileNetV2(
    input_shape = IMG_SIZE + (3,),       # (160, 160, 3)
    include_top = False,
    weights = 'imagenet'
)

base_model.trainable = False

model = tf.keras.Sequential([
    base_model,     # 학습에 참여 없이, 특징 추출기(Conv + Pool)의 역할만 함
    layers.GlobalAveragePooling2D(),
    layers.Dense(units=128, activation='relu'),
    layers.Dense(units=ds_info.features['label'].num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print(base_model.summary())
print('\n')
print(model.summary())




#######################################################################################
model.fit(train_ds, validation_data=val_ds, epochs=5)

loss, acc = model.evaluate(val_ds)
print(f'loss : {loss:.4f}, acc : {acc:.4f}')




#######################################################################################
# 다음 단계 - Fine Tunning (base model의 일부 레이어를 학습에 참여)
base_model.trainable = True

fine_tune_at = 100
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-6),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print('미세 조정 시작')

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=5,
)

loss, acc = model.evaluate(val_ds)
print(f'After Fine_Tunnig → loss : {loss:.4f}, acc : {acc:.4f}')




#######################################################################################
# 검증 데이터셋에서 이미지 1개 추출
for image, label in val_ds.take(1):
    sample_image = image
    sample_label = label
    break

pred_probs = model.predict(sample_image)
print(pred_probs)
print('\n')

pred_classes = tf.argmax(pred_probs, axis=1)
print(pred_classes)
print('\n')



#######################################################################################
# 클래스 이름 얻기
class_names = ds_info.features['label'].names
print(class_names)

# 예측값과 실제값 출력
for i in range(len(sample_image)):
    predict_index = int(pred_classes[i])
    actual_index = int(sample_label[i])

    predict_name = class_names[predict_index]
    actual_name = class_names[actual_index]

    print(f'[{i:02}] pred : {predict_index} ({predict_name}) | actual : {actual_index} ({actual_name})')



#######################################################################################
# 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(sample_image[i])

    predict_label = class_names[int(pred_classes[i])]
    actual_label = class_names[int(sample_label[i])]

    color = 'green' if predict_label == actual_label else 'red'

    plt.title(f'pred : {predict_label}\nactual : {actual_label}', color=color, fontsize=10)
    plt.axis('off')

plt.tight_layout()
plt.show()
