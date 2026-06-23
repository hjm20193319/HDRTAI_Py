# RNN 으로 글자 단위 학습 후 영문 생성
import os, sys, random, json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Dense, LSTM, Dropout, Input

#######################################################################################
tf.random.set_seed(42)
np.random.seed(42)
random.seed(42)

filename = 'rnn6text.txt'
with open(filename, encoding='utf-8') as f:
    et = f.read().lower()   # 소문자

print(et[:300] if len(et) > 300 else et)

# 문자 단위 어휘집 생성
chars = sorted(list(set(et)))
print(chars)
print()
char_to_int = {c:i for i, c in enumerate(chars)}
print(char_to_int)
print()
int_to_char = {i:c for i, c in enumerate(chars)}
print(int_to_char)
print()

n_chars = len(et)
n_vocab = len(chars)
print('문자 수 : ', n_chars)
print('어휘 수 : ', n_vocab)
print('\n')

#######################################################################################
# 시퀀스 구성
seq_length = 10     # 입력 window 길이 (이전 10글자로 다음 글자 한개를 예측)
dataX, dataY = [], []

for i in range(0, n_chars - seq_length, 1):
    seq_in = et[i:i + seq_length]
    seq_out = et[i + seq_length]
    dataX.append([char_to_int[ch] for ch in seq_in])
    dataY.append(char_to_int[seq_out])

# print(dataX)
# print(dataY)

N = len(dataX)  # 전체 학습 샘플의 개수
print('전체 학습 샘플의 개수 : ', N)    # 10
print('\n')
if N == 0:
    raise ValueError('데이터가 적어 학습 시퀀스 생성 불가')

# x/y One-Hot 처리
x = to_categorical(dataX, num_classes=n_vocab)
y = to_categorical(dataY, num_classes=n_vocab)
print(x.shape)  # (10, 10, 12)
print('\n')

# model 정의
model = Sequential([
    Input(shape=(seq_length, n_vocab)),
    LSTM(128, return_sequences=True),
    Dropout(0.2),
    LSTM(128),
    Dropout(0.2),
    Dense(n_vocab, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

chkpoint_path = 'data_stru/rnn6model.keras'
os.makedirs(os.path.dirname(chkpoint_path), exist_ok=True)
chkpoint = ModelCheckpoint(chkpoint_path, monitor='loss', save_best_only=True, mode='min', verbose=0)
early = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
batch_size = min(8, max(1, N // 2))
history = model.fit(x, y, epochs=500, batch_size=batch_size, callbacks=[chkpoint, early])

#######################################################################################
# 학습 곡선 시각화
fig, loss_ax = plt.subplots()
acc_ax = loss_ax.twinx()

loss_ax.plot(history.history['loss'], label='train loss')
loss_ax.set_xlabel('Epoch')
loss_ax.set_ylabel('Loss')
loss_ax.legend(loc='upper left')

acc_ax.plot(history.history['accuracy'], label='train accuracy')
acc_ax.set_ylabel('Accuracy')
acc_ax.legend(loc='lower left')

plt.tight_layout()
plt.show()


#######################################################################################
# 샘플링 함수
# 모델이 예측한 확률분포에서 temperature와 top_k 를 적용해 다른 글자의 인덱스를 무작위로 선택
# 모델이 예측한 확률을 그대로 쓰지 않고 조금 더 무작위성을 준다

'''
# argpartition(대상 배열, 기준 인덱스) : 부분 정렬 함수(전체 정렬이 아니라, 상위 k 개의 인덱스 반환)
k = 3
arr = np.array([7,2,9,4,1])
idx = np.argpartition(-arr, k)[:k]
print(idx)
'''
def sample_with_temperatureFunc(probs, temperature=0.8, top_k=5):
    p = np.asarray(probs).astype('float64')

    # 상위 k개 확률만 남기기
    if top_k is not None and top_k > 0 and top_k < len(p):
        idx = np.argpartition(p, -top_k)[-top_k:]
        mask = np.zeros_like(p)     # p 동일 크기 배열
        mask[idx] = p[idx]      # 선택된 k개 위치만 원래 확률 유지
        p = mask    # 확률 벡터를 '상위 k개만 남긴' 형태로 갱신 → 낮은 후보는 제외

    p = np.log(p + 1e-9) / max(temperature, 1e-8)   # temperature 조절
    p = np.exp(p)
    p = p / p.sum() # 확률 재정규화. 확률의 총합이 1이 되도록 조정
    return np.random.choice(len(p), p=p)    # 확률 p에 따라 인덱스 하나를 무작위로 선택해, 선택된 인덱스를 정수로 반환

# 문장 생성
start = np.random.randint(0, N - 1)
pattern = list(dataX[start])    # 시작 시퀀스
# print(pattern)
seed_text = ''.join([int_to_char[i] for i in pattern])
print(seed_text)

steps = 500 # 생성할 문자수
temperature = 0.8
top_k = 5

generated = []  # 생성 결과 저장 리스트

for _ in range(steps):
    x = to_categorical([pattern], num_classes=n_vocab)
    probs = model.predict(x, verbose=0)[0]  # 다음 문자 확률 예측
    idx = sample_with_temperatureFunc(probs, temperature, top_k)
    ch = int_to_char[idx]
    generated.append(ch)
    pattern.append(idx)     # 입력 시퀀스 갱신(슬라이딩 윈도우)
    pattern = pattern[1:]   # 시퀀스 슬라이딩(맨 앞글자 제거)

gen_text = ''.join(generated)
print(gen_text)
print('\n')