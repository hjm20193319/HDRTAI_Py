# 토지 소설을 글자 단위로 학습한 후 소설 쓰기
import numpy as np
import random
import re
import tensorflow as tf

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

path = tf.keras.utils.get_file(
    'rnn_test_toji.txt',
    'https://raw.githubusercontent.com/pykwon/etc/master/rnn_test_toji.txt'
)

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print('글자 수 : ', len(text))              # 전체 글자 수를 출력
print('행 수 : ', len(text.splitlines()))   # 전체 행 수를 출력
print(text[:300])

# 텍스트 전처리
text = re.sub('[^가-힣 .,?!]', '', text)     # 한글, 공백, 기본 구두점만 남긴다
text = re.sub(' +', ' ', text)  # 연속된 공백을 하나의 공백으로 줄인다
text = text.strip()
print('전처리 후 글자 수 : ', len(text))
print('전처리 후 행 수 : ', len(text.splitlines()))

# 고유 문자 정의
chars = sorted(list(set(text)))  # 텍스트에 등장한 고유 문자 목록을 만든다
vocab_size = len(chars)          # 고유 문자 개수를 저장한다
print('사용 가능 문자 수 : ', vocab_size)

# 문자와 인덱스 매핑
char_indices = {char: i for i, char in enumerate(chars)}   # 문자 → 숫자
indices_char = {i: char for i, char in enumerate(chars)}   # 숫자 → 문자

# 학습 데이터 준비
maxlen = 30 # 입력 시퀀스 길이
step = 10   # 시퀀스를 자르는 간격을 정한다
sentences = []    # 입력 시퀀스를 저장할 리스트
next_chars = []   # 정답 글자를 저장할 리스트

for i in range(0, len(text) - maxlen, step): # 텍스트를 일정 간격으로 이동하며 자른다
    sentences.append(text[i:i + maxlen])     # 30글자 입력 문장을 저장
    next_chars.append(text[i + maxlen])      # 그 다음 글자를 정답으로 저장한다

print('시퀀스 개수 : ', len(sentences))

# 정수 인코딩
x = np.zeros((len(sentences), maxlen), dtype=np.int32)  # 입력 문장을 정수 배열로 저장한다
y = np.zeros((len(sentences),), dtype=np.int32)         # 정답 글자를 정수 배열로 저장한다

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):   # 문장 안의 글자를 하나씩 꺼낸다
        x[i, t] = char_indices[char]      # 글자를 숫자 인덱스로 변환해 저장

    y[i] = char_indices[next_chars[i]]    # 정답 글자도 숫자 인덱스로 저장

print('x shape : ', x.shape)
print('y shape : ', y.shape)

# 모델 구성
model = Sequential()
model.add(Input(shape=(maxlen,)))      # 입력은 30개의 정수 인덱스
model.add(Embedding(vocab_size, 64))   # 정수 인덱스를 64차원 벡터로 변환
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(vocab_size, activation='softmax'))

optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001)
model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer)
model.summary()

# 모델 학습
checkpoint = ModelCheckpoint('best_model.keras', monitor='loss', save_best_only=True)
early_stop = EarlyStopping(monitor='loss', patience=3,restore_best_weights=True)

model.fit(x,y,batch_size=128,epochs=10,callbacks=[checkpoint, early_stop])

# 모델 저장
model.save('char_rnn_model.keras')

# 샘플링 함수 정의
def sample(preds, temperature=0.5):
    preds = np.asarray(preds).astype('float64')   # 예측 확률을 실수 배열로 변환
    preds = np.log(preds + 1e-8) / temperature    # temperature로 확률 분포를 조절

    exp_preds = np.exp(preds)             # 지수 함수를 적용
    preds = exp_preds / np.sum(exp_preds) # 전체 합이 1이 되도록 정규화

    probas = np.random.multinomial(1, preds, 1)  # 확률 분포에 따라 하나를 선택
    return np.argmax(probas)    # 선택된 인덱스를 반환


# 시작 문장 준비
start_index = random.randint(0, len(text) - maxlen - 1)  # 무작위 시작 위치를 정한다

seed_text = text[start_index:start_index + maxlen]    # 시작 위치에서 30글자를 가져온다
generated_text = seed_text    # 예측에 사용할 최근 30글자를 저장한다
final_text = seed_text        # 최종 결과를 저장한다

print('시작 문장 : ', seed_text)
print('\n생성 시작...\n')


# 텍스트 생성
for i in range(1000):     # 1000글자를 생성
    sampled = np.zeros((1, maxlen), dtype=np.int32)    # 모델 입력용 정수 배열

    for t, char in enumerate(generated_text): # 최근 30글자를 하나씩 꺼낸다
        sampled[0, t] = char_indices[char]    # 글자를 정수 인덱스로 변환

    preds = model.predict(sampled, verbose=0)[0]  # 다음 글자 확률을 예측
    next_index = sample(preds, temperature=0.5)   # 예측 확률에서 다음 글자를 선택
    next_char = indices_char[next_index]          # 인덱스를 문자로 변환

    generated_text += next_char              # 예측한 글자를 뒤에 붙인다
    generated_text = generated_text[1:]      # 맨 앞 글자를 제거해 길이를 30으로 유지
    final_text += next_char                  # 최종 결과에 예측 글자를 추가
    print(next_char, end='', flush=True)     # 생성된 글자를 바로 출력

print('\n\n생성된 텍스트:\n')
print(final_text)

# 텍스트 저장
with open('generated_text.txt', 'w', encoding='utf-8') as f:
    f.write(final_text) 

print('\n텍스트 저장 완료 → generated_text.txt')