# imdb : Internet Movie Data Base
# imdb dataset으로 이진 분류 - 영화 리뷰(긍정, 부정)
# train-25000 / test-25000

from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D, Dropout, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os



# 자주 등장하는 단어 1만개만 사용
num_words = 10000
(train_data, train_label), (test_data, test_label) = imdb.load_data(num_words=num_words)

print(type(train_data), train_data.shape)   # <class 'numpy.ndarray'> (25000,)
print('\n')
print(type(test_data), test_data.shape)
print('\n')
print(train_data[0], len(train_data[0]))    # 218
print('\n')
# ↪ 전처리가 된 데이터로 각 리뷰(단어)가 숫자화 되어 있다
# ↪ 각 숫자는 고유 단어 색인

print(train_label[0])   # 0:부정 / 1:긍정
print('\n')

# [참고]
# 이 리뷰 데이터 한 개(0번째)를 원래 문장으로 보기
word_index = imdb.get_word_index()
# 각 단어 인덱싱 확인 (50개)
sorted_word_index = sorted(list(word_index.items()), key=lambda x: x[1])
for word, index in sorted_word_index[:50]:
    print(word, index)
print('\n')

reverse_word_index = {
    index + 3:word      # load_data() 에는 0~3번을 특수 토큰으로 쓰기 때문에 +3을 해줘야 함
    for word, index in word_index.items()
}

# IMDB에는 특수 토큰이 있음
reverse_word_index[0] = '<pad>' # 패딩
reverse_word_index[1] = '<sos>' # 문장 시작
reverse_word_index[2] = '<unk>' # 알 수 없는 단어
reverse_word_index[3] = '<unused>'   # 사용 안함

# 0번째 리뷰 문장으로 복원
decode_review = ' '.join(
    [reverse_word_index.get(i, '?') for i in train_data[0]]
    # i에 해당하는 단어가 있으면 그 단어 반환, 단어가 없으면 ? 반환
)
print('0번째 리뷰 문장 : ', decode_review)
print('0번째 라벨 : ', train_label[0])
print('\n')

# 리뷰 길이 확인
review_len = [len(review) for review in train_data]
print('리뷰 길이 평균 : ', np.mean(review_len))
print('리뷰 길이 최대 : ', np.max(review_len))
print('리뷰 길이 최소 : ', np.min(review_len))
print('리뷰 길이 중간 : ', np.median(review_len))
# 리뷰 길이 평균 :  238.71364
# 리뷰 길이 최대 :  2494
# 리뷰 길이 최소 :  11
# 리뷰 길이 중간 :  178.0
print('\n')


plt.figure(figsize=(8,5))
plt.hist(review_len, bins=50)
plt.xlabel('리뷰 길이')
plt.ylabel('빈도')
plt.title('리뷰 길이 분포')
plt.tight_layout()
plt.show()
print('\n')


# padding : 리뷰 문장 길이가 다름 → 모델에 넣기 전에 길이를 맞춤
# 각 리뷰를 최대 200 단어 index로 맞춤
# 길면 앞 부분 자르고, 짧으면 0으로 채움
MAXLEN = 200
x_train = pad_sequences(train_data, maxlen=MAXLEN)
x_test = pad_sequences(test_data, maxlen=MAXLEN)
y_train = np.array(train_label).astype('float32')
y_test = np.array(test_label).astype('float32')

print('x_train : ', x_train.shape)
print('x_test : ', x_test.shape)
print('y_train : ', y_train.shape)
print('y_test : ', y_test.shape)
# x_train :  (25000, 200)
# x_test :  (25000, 200)
# y_train :  (25000,)
# y_test :  (25000,)
print('\n')

print('패딩된 리뷰 1번째 : \n', x_train[1])
#  [   0    0    0    0    0    0    0    0    0    0    0    1  194 1153 ....
print('\n')


# 모델 저장용 폴더 준비
MODEL_DIR = './imdb_model/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

model_path = './imdb_model/imdb_best.keras'

model = Sequential([
    Input(shape=(MAXLEN, )),
    Embedding(
        input_dim=num_words,    # 리뷰 1개가 단어번호 200개로 들어옴
        output_dim=32  # 단어 하나를 32개의 실수로 표현
        # 밀집 벡터화 : 실수 기반의 고정 크기에 실수값으로 채움 → 실수화, 의미를 손상시키지 않음
    ),
    GlobalAveragePooling1D(),   # 200개의 단어 벡터를 평균내서 리뷰 전체를 하나의 32차원 벡터화 → 리뷰 전체의 특징이 됨
    Dense(32, activation='relu'),
    Dropout(0.3),   # 과적합 방지: 모델이 특정 뉴런에 의존하지 못하게 만드는 강제 랜덤화 전략
    Dense(16, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

print(model.summary())
#  Total params: 321,601 (1.23 MB)
print('\n')

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.001),
    metrics=['accuracy']
)

early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
chkpoint = ModelCheckpoint(filepath=model_path, monitor='val_loss', save_best_only=True, mode='auto', verbose=0)

history = model.fit(
    x_train, y_train,
    epochs=50,
    batch_size=512,
    validation_split=0.2,
    callbacks=[early_stop, chkpoint],
    verbose=2
)
print('학습 및 저장 완료')
print('\n')

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 평가 손실 : {loss:.2f}')
print(f'테스트 평가 정확도 : {acc*100:.2f}%')
print('\n')


# loss, acc 시각화
# loss
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='train loss', color='blue')
plt.plot(history.history['val_loss'], label='val loss', color='red')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('학습 과정에서의 Loss 변화')
plt.legend()

# accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='train acc', color='blue')
plt.plot(history.history['val_accuracy'], label='val acc', color='red')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('학습 과정에서의 Accuracy 변화')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')


# 저장된 모델 읽어 분류 예측
best_model = load_model(model_path)
loss, acc = best_model.evaluate(x_test, y_test, verbose=0)
print('best model 평가 손실 : ', loss)
print('best model 평가 정확도 : ', acc)
print('\n')


# 기존 데이터 사용해서 예측
new_data = x_test[:5]
new_label = y_test[:5]

pred_prob = best_model.predict(new_data, verbose=0)
pred = (pred_prob >= 0.5).astype(int).ravel()
print('예측 확률 : ', pred_prob.ravel())
print('예측 결과 : ', pred)
print('실제 결과 : ', new_label)
print('\n')


for i in range(5):
    result = '긍정' if pred[i] == 1 else '부정'
    real = '긍정' if new_label[i] == 1 else '부정'
    print(f'{i+1}번 리뷰 예측 : {result}, 실제 : {real} \n 긍정 확률 : {pred_prob[i][0]*100:.2f}%')