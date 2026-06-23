# 쓰레기 재활용 분류기 모델 + 전이 학습 + 미세 조정
# dataset → Google Drive 에 저장

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import confusion_matrix, classification_report

DATASET_PATH = '/content/drive/MyDrive/data/garbage classification'

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

# train / validation split
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset='training',
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset='validation',
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

print(len(train_ds.file_paths)) # 2022
print('\n')
print(len(val_ds.file_paths))   # 505

class_names = train_ds.class_names
print(class_names)
# ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']




#######################################################################################
# 원래 validation dataset을 다시 validation + test dataset으로 나누기
# ⇨ train / validation / test 3개로 나누기 ⇨ 8 : 1 : 1 
val_batchs = tf.data.experimental.cardinality(val_ds)   # cardinality : batch 개수 세기(batch 기준)
test_ds = val_ds.take(val_batchs // 2)
val_ds = val_ds.skip(val_batchs // 2)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)

# 데이터 증강
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip('horizontal'),    # 좌우 반전
    layers.RandomRotation(0.1),         # -10% ~ +10% 범위 내에서 무작위 회전
    layers.RandomZoom(0.1),             # -10% ~ +10% 범위 내에서 무작위 확대/축소
    layers.RandomContrast(0.1)          # -10% ~ +10% 범위 내에서 무작위 대비 조절
])

base_model = MobileNetV2(
    input_shape = (224, 224, 3),
    include_top = False,
    weights = 'imagenet'
)

base_model.trainable = False

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    data_augmentation,          # 개수를 늘린 것이 아니라 학습 시 이미지가 입력될 때 랜덤하게 변형이 됨
    layers.Rescaling(1. / 127.5, offset=-1),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(units=128, activation='relu'),
    layers.Dropout(0.3),    
    layers.Dense(units=len(class_names), activation='softmax')
])

print(model.summary())



#######################################################################################
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    EarlyStopping(
        patience=5,
        restore_best_weights=True,
    ),
    ReduceLROnPlateau(
        factor=0.3,
        patience=2,
        verbose=1
    )
    # 학습율이 고정되면 경우에 따라 학습이 발산 또는 너무 작아져 학습이 느려질 수 있다 ⇨ ReduceLROnPlateau 처리
]

history_baseline = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    callbacks=callbacks
)

baseline_loss, baseline_acc = model.evaluate(test_ds)
print(f'loss : {baseline_loss:.4f}, acc : {baseline_acc:.4f}')




#######################################################################################
# Fine Tunning
base_model.trainable = True     # backbone unfreeze

for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss = 'sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_ft = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=100,
    callbacks=callbacks
)

ft_loss, ft_acc = model.evaluate(test_ds)
print(f'After Fine_Tunning → loss : {ft_loss:.4f}, acc : {ft_acc:.4f}')

model.save('garbage_classify.keras')



#######################################################################################
# 시각화
acc = (history_baseline.history['accuracy'] + history_ft.history['accuracy'])
val_acc = (history_baseline.history['val_accuracy'] + history_ft.history['val_accuracy'])

loss = (history_baseline.history['loss'] + history_ft.history['loss'])
val_loss = (history_baseline.history['val_loss'] + history_ft.history['val_loss'])

epochs_range = range(len(acc))
plt.figure(figsize=(14, 5))

# acc
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='train_acc')
plt.plot(epochs_range, val_acc, label='val_acc')
plt.legend('lower right')
plt.title('Accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')

# loss
plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='train_loss')
plt.plot(epochs_range, val_loss, label='val_loss')
plt.legend('upper right')
plt.title('Loss')
plt.xlabel('epoch')
plt.ylabel('loss')

plt.tight_layout()
plt.show()



#######################################################################################
# 예측
y_true = []
y_pred = []

for image, labels in test_ds:
    predictions = model.predict(image)
    y_true.extend(labels.numpy())
    y_pred.extend(np.argmax(predictions, axis=1))

cm = confusion_matrix(y_true, y_pred)
# print(cm)

plt.figure(figsize=(4, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predict')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

print(classification_report(y_true, y_pred, target_names=class_names))



#######################################################################################
#######################################################################################
# 새로운 이미지를 분류 예측 - 여기부터는 새로운 파일이라 가정
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model('garbage_classify.keras')

class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

def predict_garbageFunc(imag_path):
    img = image.load_img(imag_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)   # (1, 224, 224, 3)

    predictions = model.predict(img_array)
    pred_index = np.argmax(predictions)
    pred_class = class_names[pred_index]
    confidence = np.max(predictions)

    print('예측결과 : ', pred_class)
    print('신뢰도 : ', round(confidence * 100, 2), '%')
    return pred_class, confidence

predict_garbageFunc('myimage.jpg')