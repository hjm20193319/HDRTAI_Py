# 시퀀스 투 시퀀스

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# 병렬 문장 데이터
# : 한국어 질문과 영어 답변의 쌍으로 이루어진 리스트

# Seq2Seq 모델이 "입력 시퀀스" → "출력 시퀀스" 형태로 학습할 수 있게 해준다

data = [
    ("안녕", "hi"),
    ("잘 지내?", "How are you?"),
    ("고마워", "thank you"),
    ("좋은 아침", "good morning"),
    ("사랑해", "I love you"),
    ("잘 자", "good night"),
]


# 토크나이저 함수
# 가장 빈도가 높은 100개 단어만 사용하고 나머지는 OOV(Out Of Vacabulary) 처리
def tokenizerFunc(sentences, num_words = 100):
    tok = Tokenizer(num_words = num_words, filters='')  # filters='' → 공백 기준으로 토큰 나눔
    tok.fit_on_texts(sentences)     # 단어 사전 (단어 → 정수 인코딩)
    seqs = tok.texts_to_sequences(sentences)    # [[2], [1,3] ... ]
    return seqs, tok


# 입출력 문장 분리
input_texts = [kor for kor, eng in data]
target_texts = ['<sos> ' + eng + ' <eos>' for kor, eng in data]     # 문장의 시작과 끝을 표시
print('input texts : ', input_texts)
print('target texts : ', target_texts)
print('\n')


# 토크나이징

# 인코더용
encoder_seqs, enc_tok = tokenizerFunc(input_texts)
print(encoder_seqs)     # [[2], [1, 3], [4], [5, 6], [7], [1, 8]]
print(enc_tok)
print(enc_tok.word_index)   # {'잘': 1, '안녕': 2, '지내?': 3, '고마워': 4, '좋은': 5, '아침': 6, '사랑해': 7, '자': 8}
print(enc_tok.index_word)   # {1: '잘', 2: '안녕', 3: '지내?', 4: '고마워', 5: '좋은', 6: '아침', 7: '사랑해', 8: '자'}
print('\n')


# 디코더용
decoder_seqs, dec_tok = tokenizerFunc(target_texts)
print(decoder_seqs)     # [[1, 3, 2], [1, 5, 6, 7, 2], [1, 3, 2], [1, 8, 4, 2], [1, 9, 10, 4, 2], [1, 11, 12, 2]]
print(dec_tok)
print(dec_tok.word_index)   # {'<sos>': 1, '<eos>': 2, 'hi': 3, 'you': 4, 'how': 5, 'are': 6, 'you?': 7, 'thank': 8, 'i': 9, 'love': 10, 'good': 11, 'night': 12}
print(dec_tok.index_word)   # {1: '<sos>', 2: '<eos>', 3: 'hi', 4: 'you', 5: 'how', 6: 'are', 7: 'you?', 8: 'thank', 9: 'i', 10: 'love', 11: 'good', 12: 'night'}


# Padding : 길이를 동일 길이로 맞추기
encoder_input_data = pad_sequences(encoder_seqs, padding='post')
decoder_sequences = pad_sequences(decoder_seqs, padding='post')
print(encoder_input_data)
# [[2 0]
#  [1 3]
#  [4 0]
#  [5 6]
#  [7 0]
#  [1 8]]
print(decoder_sequences)
# [[ 1  3  2  0  0]
#  [ 1  5  6  7  2]
#  [ 1  3  2  0  0]
#  [ 1  8  4  2  0]
#  [ 1  9 10  4  2]
#  [ 1 11 12  2  0]]
print('\n')


# decoder 입력 / 타겟 분리
# 마지막 토큰 <eos> 또는 padding 된 0 을 제거한 입력 시퀀스
decoder_input_data = decoder_sequences[:, :-1]

# 첫 번째 토큰 <sos>를 제거한 출력 시퀀스
decoder_target_data = decoder_sequences[:, 1:]

print('decoder_input_data : \n', decoder_input_data)
print('decoder_target_data : \n', decoder_target_data)
print('\n')


print('차원 확대 전 : ', decoder_target_data.shape)     #  (6, 4)
# sparse_categorical_crossentropy를 사용할 경우 출력 shape은 (batch, timestaeps, 1) 이어야 함
decoder_target_data = decoder_target_data[..., np.newaxis]
print('차원 확대 후 : ', decoder_target_data.shape)     #  (6, 4, 1)


# Seq2Seq 모델의 임베딩 및 LSTM 구조를 설정하는 파라미터 정의
enc_vocab = len(enc_tok.word_index) + 1     # 인코더 레이어의 input_dim 으로 사용
dec_vocab = len(dec_tok.word_index) + 1     # 디코더 레이어의 output_dim 으로 사용
hidden_size = 64    # LSTM의 은닉 상태 벡터 차원 수


# Seq2Seq 모델 정의 - Functional API 사용
# 인코더 : 입력 시퀀스(예 : 한국어 문장)를 받아 요약된 의미 벡터인 state_h(hidden state)와
# state_c(cell state)를 얻는다
# 이 상태 정보는 디코더가 답변을 생성하는데 필요한 문맥이 된다
encoder_inputs = Input(shape=(None, ), name='encoder_input')
enc_emb_layer = tf.keras.layers.Embedding(enc_vocab, hidden_size, name='enc_emb')   # 임베딩 레이어
encoder_emb = enc_emb_layer(encoder_inputs)
encoder_lstm = LSTM(hidden_size, return_state=True, name='encoder_lstm')
# return_state=True → 최종 시점의 hiddden state(state_h) 와 cell state(state_c)를 반환

# _ : 전체출력 시퀀스로 사용
_, state_h, state_c = encoder_lstm(encoder_emb)
encoder_states = [state_h, state_c]     # 디코더에 넘겨줄 상태 정보를 묶음

# 디코더 : 인코더에서 전달 받은 상태로 <sos> 부터 시작해, 하나씩 단어를 생성해가는 구조
decoder_inputs = Input(shape=(None, ), name='decoder_inputs')
dec_emb_layer = tf.keras.layers.Embedding(dec_vocab, hidden_size, name='dec_emb')   # 임베딩 레이어
decoder_emb = dec_emb_layer(decoder_inputs)
decoder_lstm = LSTM(hidden_size, return_sequences=True, return_state=True, name='decoder_lstm')

# _, _ : 마지막 시점 상태 (학습 시점에서는 사용하지 않음)
decoder_outputs, _, _ = decoder_lstm(decoder_emb, initial_state=encoder_states)

# 각 시점의 LSTM 출력을 단어 확률 분포로 변환
decoder_dense = Dense(dec_vocab, activation='softmax', name='decoder_dense')
# 위에서 나온 decoder_outputs를 Dense layer 에 통과시켜 각 시점마다 단어 예측 결과를 얻음
decoder_outputs = decoder_dense(decoder_outputs)


# 모델을 학습 시키는 단계
train_model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
train_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
train_model.fit(
    [encoder_input_data, decoder_input_data],
    decoder_target_data,
    batch_size=2, epochs=300, verbose=2
)
print('학습 완료')



# 학습된 모델을 추론용으로 분리하기

# 인코더 모델 (입력 문장 → 문맥 상태 추출)
# 입력 : encoder_inputs (예 : 안녕 → [1])
# 출력 : encoder_states = [state_h, state_c]
# 목적 : 입력 문장을 인코딩해서 디코더에 넘겨줄 context (문맥 정보)를 생성
encoder_model = Model(encoder_inputs, encoder_states)

# 디코더 모델 (입력 문장 → 문맥 상태 추출)
decoder_state_input_h = Input(shape=(hidden_size,), name='dec_state_h')     # 이전 hidden state
decoder_state_input_c = Input(shape=(hidden_size,), name='dec_state_c')     # 이전 cell state
decoder_state_inputs = [decoder_state_input_h, decoder_state_input_c]

dec_emb2 = dec_emb_layer(decoder_inputs)

decoder_outputs2, state_h2, state_c2 = decoder_lstm(dec_emb2, initial_state=decoder_state_inputs)

# [0.01, 0.03, 0.88] 이라고 할 때 가장 높은 확률을 가진 인덱스를 추출해 번역 단어 생성
decoder_outputs2 = decoder_dense(decoder_outputs2)

decoder_model = Model(
    # 입력 : 현재 단어 인덱스 (decoder_inputs), 이전 상태 (state_h, state_c)
    [decoder_inputs] + decoder_state_inputs,
    # 출력 : 현재 단어의 softmax 확률 분포(decoder_outputs2), 다음 상태(state_h2, state_c2)
    [decoder_outputs2, state_h2, state_c2]
)


# 번역 수행 함수
def translateFunc(sentence):
    seq = enc_tok.texts_to_sequences([sentence])    # 한글 문장을 정수 시퀀스로 변환
    seq = pad_sequences(seq, maxlen=encoder_input_data.shape[1], padding='post')
    states = encoder_model.predict(seq)

    # 번역 시작 : <sos>토큰을 입력으로 넣고 누적 처리
    target_seq = np.array([[dec_tok.word_index['<sos>']]])

    decoded = []
    # 토큰 생성 - 한 단어씩
    while True:
        output_tokens, h, c = decoder_model.predict([target_seq] + states)
        # 가장 확률이 높은 단어 인덱스 선택 → 단어로 변환
        sampled_idx = np.argmax(output_tokens[0, -1, :])
        sampled_word = dec_tok.index_word.get(sampled_idx, '')

        if sampled_word == '<eos>' or len(decoded) > 10:
            break

        decoded.append(sampled_word)

        # 다음 step 준비
        target_seq = np.array([[sampled_idx]])  # 선택 단어를 다음 입력으로 사용하려고 함
        states = [h, c]     # 상태도 갱신해서 이어지는 문맥을 유지

    return ' '.join(decoded)


print('번역 테스트')
for s in input_texts:
    print(f'{s} ⇨ {translateFunc(s)}')