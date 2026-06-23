# 단어(공백으로 구분) 단위 자연어 생성 - 소설 '토지' 데이터 사용
import tensorflow as tf
import numpy as np
import re
print('\n')

path_to_file = tf.keras.utils.get_file(
    'toji.txt',
    'https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/rnn_test_toji.txt'
)

with open(path_to_file, encoding='utf-8', errors='ignore') as obj:
    raw_text = obj.read()

# print(raw_text[:100])
# 제 1 편 어둠의 발소리
# 1897년의 한가위.
# 까치들이 울타리 안 감나무에 와서 아침 인사를 하기도 전에, 무색 옷에 댕기꼬리를 늘인 
# 아이들은 송편을 입에 물고 마을길을 쏘다니며
# print('문자 수 : ', len(raw_text))
# 문자 수 :  677125


#######################################################################################
# 정제 후 corpus 만들기
def clean_str(text:str) -> str:
    text = re.sub(r"[^가-힣0-9() \n]", " ", text)
    #                  허용문자     나머지는 공백 처리,  대상은 text
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()     # 좌우 공백 제거

# print('abc가나다  _^&$12하하')
# print(clean_str('abc가나다  _^&$12하하'))

cleaned = clean_str(raw_text)
# print(cleaned[:100])
# 제 1 편 어둠의 발소리
# 1897년의 한가위 까치들이 울타리 안 감나무에 와서 아침 인사를 하기도 전에 무색 옷...
corpus = cleaned.replace('\n', ' [NL] ')    # NL : New Line , 줄바꿈을 토큰으로 처리하기 위해 특수 문자 사용
# print(corpus[:100])     # 줄바꿈도 문자로 처리 → 학습에 참여시키기 위해서
# 제 1 편 어둠의 발소리 [NL] 1897년의 한가위 까치들이 울타리 안 감나무...

# 토큰 처리 : 문자열 → 단어 분리 → 단어 사전 → 정수 번호로 변환
vectorizer = tf.keras.layers.TextVectorization(
    standardize = None,
    split = 'whitespace',
    output_mode = 'int',
    output_sequence_length = None,
    vocabulary = None
)

# 단어 사전 생성
vectorizer.adapt(tf.data.Dataset.from_tensor_slices([corpus]))

vocab = vectorizer.get_vocabulary()
# print(vocab[:10])
# ['', '[UNK]', np.str_('[NL]'), np.str_('그'), np.str_('안'), np.str_('있었다'), np.str_('다'), 
# np.str_('한'), np.str_('것'), np.str_('이')]
PAD, UNK = 0, 1
vocab_size = len(vocab)
print(f'어휘 수 : {vocab_size} (PAD={PAD}, UNK={UNK})')
# 어휘 수 : 51358 (PAD=0, UNK=1)
print('샘플 어휘 : ', vocab[:20])
print('\n')

token_ids = vectorizer(tf.constant([corpus]).numpy())[0]
print('토큰 수 : ', len(token_ids))
print(token_ids)
# 토큰 수 :  164150
# tf.Tensor([   51 51341  2059 ...    49  1590   275], shape=(164150,), dtype=int64)
print(vocab[51], ' ', vocab[51341], ' ', vocab[2059]) # 맵핑이 되어 있다
print('\n')

# 지나치게 데이터가 작은 경우 대비용
if len(token_ids) <= 50:
    raise ValueError('토큰 수가 너무 적어 작업 안함')

# 학습용 시퀀스
SEQ_LEN = 25    # 입력 길이 (과거 25개의 토큰을 보고 다음 토큰 예측)
BATCH = 64      # 배치 크기
BUFFER = 5000   # 셔플 버퍼

# tf.data.Dataset은 탠서플로우에서 고성능 데이터 입력 파이프라인을 구축하기 위한 핵심 API
# 메모리 내 데이터를 슬라이싱하여 데이터셋을 생성
# .map(), .batch(), .shuffle() 등으로 전처리한 뒤 반복 순회하여 사용

ds = tf.data.Dataset.from_tensor_slices(token_ids)  # 배열이나 리스트를 한 개씩 잘라서 Dataset으로 만듦
ds = ds.window(SEQ_LEN + 1, shift=1, drop_remainder=True)   # 한 칸씩 우측으로 밀기
ds = ds.flat_map(lambda w:w.batch(SEQ_LEN + 1))     # 각 윈도우를 텐서로 수집
# Dataset 안의 각 원소를 다시 Dataset으로 바꾼 뒤 하나로 펼치기

# 하나의 토큰 묶음(chunk)을 입력(x), 정답(y), 가중치(w)로 나누는 함수
def split_xyFunc(chunk):    # chunk : SEG_LEN + 1
    x = chunk[:-1]  # 입력 (마지막 값 제외)
    y = chunk[-1]    # 정답 (마지막 값) - 각 시점의 다음 토큰 예측
    w = tf.cast(tf.not_equal(y, PAD), tf.float32)   # 정답이 실제 토큰이면 1, 정답이 PAD면 0
    return x, y, w

# 파이프라인 구축
ds = (ds.map(split_xyFunc, num_parallel_calls=tf.data.AUTOTUNE).cache().shuffle(BUFFER).batch(BATCH, drop_remainder=True).prefetch(tf.data.AUTOTUNE))
# 학습 데이터 준비 병렬화

windows = len(token_ids) - SEQ_LEN  # 윈도우 크기
steps_per_epoch = max(1, windows // BATCH)  # 0 방지
print('stepa_per_epoch : ', steps_per_epoch)


# 모델
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(SEQ_LEN, )),
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=128),
    tf.keras.layers.LSTM(256, return_sequences=True),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(vocab_size)     # activation='softmax'
])
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)   # loss를 직접 계산
model.compile(optimizer='adam', loss=loss_fn, metrics=[tf.keras.metrics.SparseCategoricalAccuracy])
model.summary()


# 모델이 예측한 점수인 logits를 확률로 바꾼 뒤, 그 확률에 따라 다음 토큰 하나를 추출하는 함수
def sample_from_logits():
    pass

# 토큰 id를 사람이 읽을 수 있는 문자로 변환 함수
def ids_to_text(ids):
    pass

# 사용자가 넣은 시작 문장을 바탕으로 학습된 모델이 뒤에 이어질 문장으로 자동 생성하는 함수
def generateFunc():
    pass

# 일정 주기로 샘플 출력 - 학습 진행 상태 확인용 클래스
class SamplerCallback(tf.keras.callbacks.Callback):
    def on_each_end(self, epoch, logs=None):    # 매 epoch이 끝날 때 마다 자동 호출
        pass

EPOCHS = 2      # 사실 많이 줘야 함
history = model.fit(ds, epochs=EPOCHS, steps_per_epoch=steps_per_epoch, callbacks=[SamplerCallback()], verbose=2)
print('final loss : ', float(history.history['loss'][-1]))
print('final accuracy : ', float(history.history['sparse_categorical_accuracy'][-1]))
print('\n')

# 최종 테스트
seed = '아이들은 송편을 입에 무고 마을길을 쏘다니며'
out = generateFunc(seed, max_new_tokens=200, temperature=0.8, top_k=40)
print('최종 결과 : \n')
print(seed, out)