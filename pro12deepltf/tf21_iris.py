# iris dataset으로 꽃 종류 분류기 (ROC curve 까지 표현)
# Layer 수에 따른 모델 성능 비교

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout

iris = load_iris()
print(iris.keys())
print('\n')


x = iris.data
y = iris.target
print(x[:2])
print(y[:2])
print('\n')

names = iris.target_names
print(names)
print('\n')

feature_names = iris.feature_names
print(feature_names)
print('\n')


# label One-Hot 처리
onehot = OneHotEncoder(categories='auto')
y = onehot.fit_transform(y.reshape(-1, 1)).toarray()
print(y[:2])
print('\n')


# feature 표준화
scaler = StandardScaler()
x_scale = scaler.fit_transform(x)



# train/test split
x_train, x_test, y_train, y_test = train_test_split(x_scale, y, test_size=0.3, random_state=42)


n_features = x_train.shape[1]
n_classes = y_train.shape[1]
print(n_features)
print(n_classes)
print('\n')



# Layer의 개수가 다른 모델 여러 개 생성 함수
def create_custom_model(input_dim, output_dim, out_nodes, n, model_name='model '):
    # print(input_dim, output_dim, out_nodes, n, model_name)
    def create_model():
        model = Sequential(name = model_name)
        model.add(Input(shape=(input_dim, )))
        for _ in range(n):
            model.add(Dense(out_nodes, activation='relu'))

        model.add(Dense(output_dim, activation='softmax'))
        
        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        return model
    return create_model     # 클로저 → 주소만 넘김



models = [create_custom_model(n_features, n_classes, 10, n, 'model_{}'.format(n)) for n in range(1, 4)]


# 구조 확인
for create_model in models:
    print()
    create_model().summary()



# 모델 생성
history_dict = {}

for create_model in models:
    model = create_model()
    print('모델명 : ', model.name)
    histories = model.fit(
        x_train, y_train,
        validation_split=0.3,
        epochs=50,
        batch_size=4,
        verbose=0
    )
    score = model.evaluate(x_test, y_test, verbose=0)
    print(f'loss : {score[0]:.4f}, acc : {score[1]:.4f}')
    history_dict[model.name] = [histories, model]


print(history_dict)



# 시각화
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8,8))

for model_name in history_dict:
    # print('h_d : ', history_dict[model_name][0].history['accuracy'])
    val_acc = history_dict[model_name][0].history['val_accuracy']
    val_loss = history_dict[model_name][0].history['val_loss']
    ax1.plot(val_acc, label=model_name)
    ax2.plot(val_loss, label=model_name)
    ax1.set_ylabel('Accuracy')
    ax2.set_ylabel('Loss')
    ax2.set_xlabel('Epochs')
    ax1.set_title('Validation Accuracy')
    ax2.set_title('Validation Loss')
    ax1.legend()
    ax2.legend()
    plt.tight_layout()
plt.show()



# ROC Curve - 분류기에 대한 성능 평가 기법
from sklearn.metrics import roc_curve, auc

plt.figure()
plt.plot([0, 1], [0, 1], 'k--')     # 기준선

for model_name in history_dict:
    model = history_dict[model_name][1]
    y_pred = model.predict(x_test)
    fpr, tpr, thresholds = roc_curve(y_test.ravel(), y_pred.ravel())
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f})')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()