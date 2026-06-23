# tf dataset의 cat/dog 이미지 분류 + 전이 학습 + 미세 조정
# 백본 : MobileNet V2

import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds

# tfds.disable_progress_bar()     # 진행률 표시 바 비활성화 옵션
(raw_train, raw_validation, raw_test), metadata = tfds.load(
    'cats_vs_dogs',
    split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],     # 8:1:1
    with_info=True,
    as_supervised=True  # dict type으로 반환(기본-tuple)
)

print(raw_train)



#######################################################################################
total = metadata.splits['train'].num_examples
print('train 전체 수 : ', total)
print('raw_train 전체 수 : ', int(total*0.8))
print('raw_vali 전체수 : ', int(total * 0.1))
print('raw_test 전체수 : ', int(total * 0.1))




#######################################################################################
# label 명 얻기
get_label_name = metadata.features['label'].int2str
print(get_label_name(1))


# 샘플자료 보기
for image, label in raw_train.take(1):
    print('원본 1 개 : ', image.shape, label.numpy())
    plt.figure()
    plt.imshow(image)
    plt.title(get_label_name(label))
    plt.axis('off')
    plt.show()



#######################################################################################
# 전처리 함수 - cat/dog 크기가 다양함 → 크기 고정, 정규화
IMG_SIZE = 160
def format_exampleFunc(image, label):
    image = tf.cast(image, tf.float32)      # uint → float32
    image = (image / 127.5) - 1.0       # [0, 255] → [-1, 1]
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    return image, label


# 원본 dataset을 전처리 된 dataset으로 변경
# AUTOTUNE : 여러 개의 샘플을 병렬로 자동 처리(CPU 코어 수, 리소스 자원 관리 등)
#      ↪ GPU의 유휴 시간을 최소화
train = raw_train.map(format_exampleFunc, num_parallel_calls=tf.data.AUTOTUNE)
validation = raw_validation.map(format_exampleFunc, num_parallel_calls=tf.data.AUTOTUNE)
test = raw_test.map(format_exampleFunc, num_parallel_calls=tf.data.AUTOTUNE)


# 전처리 검증
for img, label in train.take(1):
    print('전처리 샘플 dtype : ', img.dtype)
    print('전처리 샘플 shape : ', img.shape)
    print('min/max : ', float(tf.reduce_min(img)), float(tf.reduce_max(img)))


# batch pipeline 운영
BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 1000

# train 만 shuffle 진행 - validation, test 는 고정 → 1000 개의 샘플을 메모리에 로딩해서 섞음
# prefetch : 모델이 학습하는 동안 다음 학습에 필요한 데이터를 미리 가져와, 전처리
train_batches = (train.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE))
validation_batches = (validation.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE))
test_batches = (test.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE))

# 아래 코드 참고용 : batch 아님
for image_single, label_single in raw_train.take(2):
    print('원본 단일 이미지 shape : ', image_single.numpy().shape)
    print('라벨 : ', label_single.numpy())




#######################################################################################
# base model : 전이 학습 중
IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
base_model = tf.keras.applications.MobileNetV2(
    input_shape = IMG_SHAPE,
    include_top = False,    # 분류기 뺌
    weights = 'imagenet'
)

print(base_model.summary())




#######################################################################################
# 전처리/배치가 된 텐서를 통과시켜 특징 맵 얻기
images_batch, labels_batch = next(iter(train_batches))
feature_batch = base_model(images_batch)

print('입력 배치 shape : ', images_batch.shape)
print('특징맵 배치 shape : ', feature_batch.shape)
# 입력 배치 shape :  (32, 160, 160, 3)
# 특징맵 배치 shape :  (32, 5, 5, 1280)
# 하나의 이미지는 (5, 5, 1280) 짜리 특징 맵이 됨

global_avg = tf.keras.layers.GlobalAveragePooling2D()(feature_batch)
print('GAP 후 shape : ', global_avg.shape)
# GAP 후 shape :  (32, 1280)  : 5 x 5를 평균 내고 채널 축만 남김 (1280차 벡터 하나로 요약)
# 배치 크기는 유지하면서 최종 shape : (32, 1280)을 축만 남기면 이미지 당 한개의 고정길이 벡터를 얻어
# Dense(분류기)네 넣기 쉬워진다




#######################################################################################
# 모델 정의
# Sequential로 정의
model = tf.keras.layers.Sequential([
    tf.keras.layers.Input(shape=IMG_SHAPE),
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(1, activation='sigmoid')      # base_model + 이진 분류기
])


# Functional로 정의
inputs = tf.keras.Input(shape=IMG_SHAPE)
x = base_model(inputs, training=False)
x =     tf.keras.layers.GlobalAveragePooling2D()(x)
outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)

model = tf.keras.Model(inputs, outputs)
print(model.summary())


base_model.trainable = False    # 특징 추출기(Conv + Pooling) 동결





#######################################################################################
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_batches,
    validation_data = validation_batches,
    epochs=10
)

loss, acc = model.evaluate(test_batches, verbose=0)
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
# Fine Tunning 미세 조정
base_model.trainable = True     # 특징 추출기 동결 해제
fine_tune_at = 100       # MobileNetV2 레이어 150개 중 50개만 학습에 참여

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False
    # 0 ~ 100 는 학습에 참여 못하게 막아줌 → 50개만 학습에 참여

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-6),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Checkpoint, EarlyStopping
os.makedirs('checkpoints', exist_ok=True)
ckpt_path_ft = 'checkpoints/finetune_best.keras'

callbacks_ft = [
    tf.keras.callbacks.ModelCheckpoint(
        ckpt_path_ft,
        monitor='val_accuracy',
        mode='max',
        save_best_only=True,
        verbose=0
    ),
    tf.keras.callbacks.ReduceLROnPlateau(   # val_loss 개선이 멈추면, learning_rate 를 0.5 배 줄임 → 정교해짐
        monitor='val_accuracy',
        factor=0.5,
        patience=3,
        verbose=0
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=0
    )
]





#######################################################################################
EPOCHS_TRANSFER = 10    # 전이 학습에서 이미 10회 학습 함
EPOCHS_FINETUNE = 10    # 미세 조정에서 추가 학습할 epoch 수

history_ft = model.fit(
    train_batches,
    validation_data=validation_batches,
    epochs=EPOCHS_TRANSFER + EPOCHS_FINETUNE,
    initial_epoch=EPOCHS_TRANSFER,   # 전이학습 이후 10번만 파인 튜닝함
    callbacks=callbacks_ft,
    verbose=2
)





#######################################################################################
loss, acc = model.evaluate(test_batches, verbose=0)
print(f'loss : {loss:.4f}, acc : {acc:.4f}')




#######################################################################################
# 시각화를 통한 테스트 성능 비교
def concat_hist(h1, h2):
    keys = h1.history.keys()
    out = []
    for k in keys:
        out[k] = h1.history[k] + h2.history[k]  # 각 key(loss, acc) 에 대해 리스트에 이어 붙임
    return out

hist_all = concat_hist(history, history_ft)
acc = hist_all['accuracy']
val_acc = hist_all['val_accuracy']
loss = hist_all['loss']
val_loss = hist_all['val_loss']

epochs = range(1, len(acc) + 1)
split_epoch = EPOCHS_TRANSFER   # 전이 학습과 미세 조정 경계선 위치

plt.figure(figsize=(12, 5))
# acc
plt.subplot(1, 2, 1)
plt.plot(epochs, acc, marker='o', label='train acc')
plt.plot(epochs, val_acc, marker='s', label='val acc')

for i, v in enumerate(acc):
    plt.text(epochs[i], v, f'{v * 100:.1f}%', ha='center', va='bottom', fontsize=9)

for i, v in enumerate(val_acc):
    plt.text(epochs[i], v, f'{v * 100:.1f}%', ha='center', va='bottom', fontsize=9)

# 전이 → 미세 조정 전환선
plt.axvline(split_epoch, linestyle='--', alpha=0.7, label='fine tunning start')
plt.title('Accuracy(transfer → fine tunning)')
plt.xlabel('epoch')
plt.ylabel('acc')
plt.legend(loc='lower right')

# loss
plt.subplot(1, 2, 1)
plt.plot(epochs, loss, marker='o', label='train loss')
plt.plot(epochs, val_loss, marker='s', label='val loss')

for i, v in enumerate(loss):
    plt.text(epochs[i], v, f'{v:.3f}', ha='center', va='bottom', fontsize=9)

for i, v in enumerate(val_loss):
    plt.text(epochs[i], v, f'{v:.1f}', ha='center', va='bottom', fontsize=9)

plt.title('Loss(transfer → fine tunning)')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()