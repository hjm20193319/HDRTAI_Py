# 동물의 타입 분류 Zoo Animal Classification dataset from kaggle

#  animal_name: Unique for each instance
# hair Boolean
# feathers Boolean
# eggs Boolean
# milk Boolean
# airborne Boolean
# aquatic Boolean
# predator Boolean
# toothed Boolean
# backbone Boolean
# breathes Boolean
# venomous Boolean
# fins Boolean
# legs Numeric (set of values: {0,2,4,5,6,8})
# tail Boolean
# domestic Boolean
# catsize Boolean
# class_type Numeric (integer values in range [1,7])



import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import numpy as np






datas = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/zoo.csv')
print(datas.head(3))
print('\n')
print(datas.info())
print('\n')



x_data = datas.iloc[:, :-1].astype('float32').values
y_data = datas.iloc[:, -1].astype('int32').values
print(x_data[0], x_data.shape)
print(y_data[0], sorted(set(map(int, y_data))))
print('\n')


np.random.seed(42)
tf.keras.utils.set_random_seed(42)



x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42, stratify=y_data)


nb_classes = len(set(y_data))

model = Sequential([
    Input(shape=(x_data.shape[1], )),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(nb_classes, activation='softmax')
])

print(model.summary())
print('\n')



# Label One-Hot 처리 안한 경우
model.compile(
    loss='sparse_categorical_crossentropy',     # 내부적으로 One-Hot 처리함, 정수형 label
    optimizer='adam',
    metrics=['accuracy']
)

history = model.fit(
    x_train, y_train,
    validation_split=0.2,
    epochs=50,
    batch_size=32,
    verbose=2
)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 결과 손실 : {loss:.2f}')
print(f'테스트 모델의 정확도 : {acc*100:.2f}%')
print('\n')


# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib

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
print('\n')


# 혼동 행렬 출력
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

y_pred = np.argmax(model.predict(x_test), axis=1)
print('classification report : \n', classification_report(y_test, y_pred))
print('\n')

cm = confusion_matrix(y_test, y_pred)
print(cm)
print('\n')

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
print('\n')

