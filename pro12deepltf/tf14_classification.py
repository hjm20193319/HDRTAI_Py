# Deep Learning으로 이진 분류 - 전통적인 방식인 Logistic Regression의 확장

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam
import numpy as np
import tensorflow as tf

np.random.seed(42)
tf.keras.utils.set_random_seed(42)


x_data = np.array([[1, 2], [2, 3], [3, 4], [4, 3], [3, 2], [2, 1]], dtype='float32')
y_data = np.array([[0], [0], [0], [1], [1], [1]], dtype='float32')


#####################################################################################3
# 1) Sequential API 버전 → 빠른 구현
#     : 층을 순서대로 쌓는 단순 구조, 분기 구조나 다중 입출력 불가능
# model = Sequential([
#     Input(shape=(2, )),
#     Dense(1, activation='sigmoid')
# ])
model = Sequential()
model.add(Input(shape=(2, )))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())
print('\n')

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

model.fit(x_data, y_data, epochs=20, batch_size=1, verbose=0)
m_eval = model.evaluate(x_data, y_data, verbose=0)
print(f'평가 결과 : 손실 = {m_eval[0]:.4f}, 정확도 = {m_eval[1]:.4f}')
print('\n')
# 손실을 최소화 하기 위해 경사하강법 사용
# Z = W•x + b (행렬곱-내적)
# ⇨ sigmoid(Z)
# ⇨ BCE 계산
# ⇨ 역전파 gradient (ŷ - y)를 최소화
# ⇨ W, b 갱신

# 예측값과 실제값으로 시각화(S 곡선 형태)
import matplotlib.pyplot as plt
import koreanize_matplotlib
# ↪ 2차원 입력(x1, x2)을 가진 모델을 1차원 처럼 만들어, sigmoid(S 곡선)를 보기 위한 준비 작업
x1_range = np.linspace(0, 6, 100)
x2_fixed = 2.5

# 입력 데이터 생성 - 두 배열을 합쳐서 (x1, x2) 쌍 만들기
x_vis = np.column_stack([x1_range, np.full_like(x1_range, x2_fixed)])
# np.full_like(x1_range, x2_fixed) → x1_range와 같은 길이의 배열

y_prob = model.predict(x_vis, verbose=0)
# x1 변화에 따른 출력 확률

x1_real = x_data[:, 0]
y_real = y_data.ravel()

plt.figure(figsize=(8, 6))
plt.plot(x1_range, y_prob, label='Sigmoid curve')
plt.scatter(x1_real, y_real, label='Real data points', color='red')
plt.xlabel('x data')
plt.ylabel('probability')
plt.legend(loc='lower right')
plt.grid(True)
plt.tight_layout()
plt.show()
print('\n')


from sklearn.metrics import accuracy_score
pred = model.predict(x_data, verbose=0)
pred_class = (pred >= 0.5).astype(int)
accuracy = accuracy_score(y_data, pred_class)
print(f'1) 정확도 | {accuracy:.4f}')

# 새로운 값으로 분류 예측
new_data = np.array([[1,2], [10,5]], dtype='float32')
pred = model.predict(new_data, verbose=0)
print('예측 확률 : ', pred.ravel())

print('예측 결과 : ', (pred >= 0.5).astype(int).ravel())
print('예측 결과 : ', [1 if i >=0.5 else 0 for i in pred])
print('예측 결과 : ', np.where(pred >= 0.5, 1, 0).ravel())
print('\n')


###########################################################################
# 2) Functional API - 실무에서 주로 사용
#           : 다중 입출력 가능, 구조가 유연 → 복잡한 모델에 효과적
from tensorflow.keras.models import Model

inputs = Input(shape=(2, ))
outputs = Dense(4, activation='relu')(inputs)
outputs = Dense(1, activation='sigmoid')(outputs)
model_func = Model(inputs=inputs, outputs=outputs)
print(model_func.summary())
print('\n')

model_func.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

model_func.fit(x_data, y_data, epochs=20, batch_size=1, verbose=0)
m_eval = model_func.evaluate(x_data, y_data, verbose=0)
print(f'평가 결과 : 손실 = {m_eval[0]:.4f}, 정확도 = {m_eval[1]:.4f}')
print('\n')



######################################################################33
# 3) Functional API 버전 2 - 다중 입력
#       이전 : [x1, x2] → Dense → Dense → 출력
#       다중 입력 : x1 → Dense
#                               ⇨  concat → Dense → 출력
#                   x2 → Dense
#           ⇨ 입력을 따로 받아서 각각 특징을 뽑아 합치는 방식. 각각 따로 전처리가 가능
from tensorflow.keras.layers import Concatenate

# 입력 분리
input1 = Input(shape=(1, ))
input2 = Input(shape=(1, ))

# 각각 처리
x1 = Dense(2, activation='relu')(input1)
x2 = Dense(4, activation='relu')(input2)

merged = Concatenate()([x1, x2])
output = Dense(1, activation='sigmoid')(merged)
multi_model = Model(inputs=[input1, input2], outputs=output)
print(multi_model.summary())
print('\n')

multi_model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)

# 데이터를 분리해서 입력
x1_data = x_data[:, 0].reshape(-1, 1)
x2_data = x_data[:, 1].reshape(-1, 1)

multi_model.fit([x1_data, x2_data], y_data, epochs=20, batch_size=1, verbose=0)
m_eval = multi_model.evaluate([x1_data, x2_data], y_data, verbose=0)
print(f'평가 결과 : 손실 = {m_eval[0]:.4f}, 정확도 = {m_eval[1]:.4f}')
print('\n')



###############################################################################3
# 4) Model Subclassing 방식 - 완전 자유로운 형태 → 프로그램 능력이 중요
class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.dense1 = Dense(4, activation='relu')
        self.dense2 = Dense(1, activation='sigmoid')

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)

sub_model = MyModel()

sub_model.build(input_shape=(2, ))
print(sub_model.summary())
print('\n')

sub_model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.01),
    metrics=['accuracy']
)
sub_model.fit(x_data, y_data, epochs=20, batch_size=1, verbose=0)
m_eval = sub_model.evaluate(x_data, y_data, verbose=0)
print(f'평가 결과 : 손실 = {m_eval[0]:.4f}, 정확도 = {m_eval[1]:.4f}')
print('\n')