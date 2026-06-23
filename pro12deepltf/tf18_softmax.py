# 다항 분류는 출력층에 softmax를 사용

#############################################################################################################
# 참고 : softmax 함수 보기
#           ↪ 입력 받은 실수 벡터를 0~1 사이의 확률값으로 정규화 → 모든 출력의 합이 1이 되도록 하는 함수 
import numpy as np

def softmaxFunc(a):
    c = np.max(a)
    exp_a = np.exp(a-c)
    sum_exp_a = np.sum(exp_a)
    return exp_a / sum_exp_a

data = np.array([0.3, 2.8, 4.0])
print(softmaxFunc(data))
# [0.01864635 0.22715905 0.7541946 ]    ⇨ 제일 큰 값을 택하면 됨
print('\n')
##############################################################################################################


# 다항 분류 모델 - 출력은 softmax로 인해 복수개의 확률값으로 출력
#                  이 떄 가장 큰 인덱스를 분류 결과로 취함
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical   # OneHot 지원
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib


np.random.seed(1)
np.set_printoptions(suppress=True ,precision=3)


xdata = np.random.random((1000, 12))        # feature : 시험 점수
ydata = np.random.randint(5, size=(1000, 1))       # label : 다섯 과목
print(xdata[:2])
print('\n')
print(ydata[:2])
print('\n')

# softmax에서는 label을 반드시 One-Hot 처리한 값을 model에 넣어줘야 함(희소 벡터)
ydata = to_categorical(ydata, num_classes=5)
print(ydata[:2])
print('\n')


# model
model = Sequential()
model.add(Input(shape=(12, )))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(5, activation='softmax'))
print(model.summary())

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history = model.fit(
    xdata, ydata,   # One-Hot 처리된 ydata
    epochs=2000,
    batch_size=32,
    verbose=2,
    shuffle=True
)
print('학습 완료')
print('\n')

model_eval = model.evaluate(xdata, ydata, verbose=0)
print('모델 평가 결과 : ', model_eval)
print('\n')


# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(history.history['loss'], label='train loss', color='blue')
ax1.set_xlabel('Epochs')
ax1.set_ylabel('Loss')
ax1.set_title('학습 과정에서의 Loss 변화')
ax1.legend()

ax2.plot(history.history['accuracy'], label='train acc', color='blue')
ax2.set_xlabel('Epochs')
ax2.set_ylabel('Accuracy')
ax2.set_title('학습 과정에서의 Accuracy 변화')
ax2.legend()
plt.tight_layout()
plt.show()
print('\n')



# 기존값으로 분류 예측
print('예측값 : ', model.predict(xdata[:5]))
print('예측값 : ', np.argmax(model.predict(xdata[:5]), axis=1))
print('실제값 : ', ydata[:5])
print('실제값 : ', [int(i) for i in np.argmax(ydata[:5], axis=1)])
print('\n')


# 새로운 값으로 예측
x_new = np.random.random([1, 12])
new_pred = model.predict(x_new)
print('분류 결과 : ', new_pred)
print('분류 결과 합 : ', np.sum(new_pred))
print('분류 결과 : ', np.argmax(new_pred))
print('\n')

# 예측 결과를 과목명으로 출력
classes = np.array(['국어', '영어', '수학', '과학', '체육'])
print('예측값 : ', classes[np.argmax(new_pred)])
print('\n')