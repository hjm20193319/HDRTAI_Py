import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 1) 병렬 Q&A 데이터
data = [
    ("안녕",           "안녕하세요"),
    ("이름이 뭐야?",   "저는 챗봇입니다"),
    ("날씨 어때?",     "맑고 화창해요"),
    ("지금 뭐해?",     "파이썬과 씨름 중"),
    ("하하 이제 좀 쉬어",  "네 그럴께요"),
]

# 2) 디코더 입력용 토큰 추가
questions = [q for q, a in data]
answers   = [f"<sos> {a} <eos>" for q, a in data]

# 3) 토크나이즈 함수
def tokenize(texts, num_words=1000):
    tok = Tokenizer(num_words=num_words, filters='')
    tok.fit_on_texts(texts)
    seqs = tok.texts_to_sequences(texts)
    return seqs, tok

# 4) 시퀀스 변환 & 패딩
q_seqs, q_tok = tokenize(questions)
a_seqs, a_tok = tokenize(answers)
q_pad = pad_sequences(q_seqs, padding='post')
a_pad = pad_sequences(a_seqs, padding='post')

# 5) decoder 입력/타겟 분리
  # a_pad: 전체 디코더 시퀀스 (예: <sos> 안녕하세요 <eos>)
  # a_pad[:, 1:]: 맨 앞 <sos>는 제거하고, <답변 내용> <eos>만 남기는 부분.
  # 즉, 예측해야 할 정답 시퀀스를 만든다.
  # "a_pad[0]=[1, 2, 3]" <sos> 안녕하세요 <eos>를 "a_pad[0, 1:]=[2, 3]" 안녕하세요 <eos>로.
decoder_input_data  = a_pad[:, :-1]               # <eos> 제거

# 차원을 (3D 텐서)로 맞추기 위한 작업
  # a_pad[:, 1:]의 shape은 (5, N)  # 5는 샘플 수, N은 디코더 시퀀스 길이
  # 하지만 model.compile(..., loss='sparse_categorical_crossentropy')에서 사용하는 
  # sparse_categorical_crossentropy는 타겟이 다음과 같은 3차원이어야 함. (batch_size, sequence_length, 1)
  # 그래서 마지막 차원을 np.newaxis로 추가하여 다음과 같이 바꾼다. [..., np.newaxis]
  # before = a_pad[:, 1:] shape은 (5, 6)  ==> after = a_pad[:, 1:][..., None] shape은 (5, 6, 1)
  # ... (ellipsis)의 의미는 NumPy에서 "앞에 오는 모든 차원은 그대로 두고" 라는 의미다.
  # 즉, [..., np.newaxis]는 기존 앞 차원은 그대로 유지하고, 맨 마지막에 새 축(axis) 하나를 추가하라는 뜻.
  # 동일한 표현 : a_pad[:, 1:][:, :, np.newaxis] (마지막에 차원을 하나 추가해 (batch, time, 1)로 맞춤)
  # 최종 shape	(5, 시퀀스길이, 1) — 각 시점마다 예측할 정답 토큰 인덱스 하나씩
decoder_target_data = a_pad[:,  1:][..., np.newaxis]    # <sos> 제거 + 차원 변환

# 6) 파라미터
enc_vocab   = len(q_tok.word_index) + 1
dec_vocab   = len(a_tok.word_index) + 1
hidden_size = 64

# 7) 학습용 Seq2Seq 모델 구성
# 7.1) 인코더 목적 : 입력 시퀀스(예: 한국어 문장)를 받아서 요약된 의미 벡터인
# state_h (hidden state)와 state_c (cell state)를 얻는 것이다.
# 이 상태 정보는 디코더가 답변을 생성하는 데 필요한 문맥이 된다.
enc_inputs   = Input(shape=(None,), name='enc_inputs')
# 단어 인덱스를 의미 벡터로 변환하는 임베딩 레이어.
enc_emb_layer= tf.keras.layers.Embedding(enc_vocab, hidden_size, name='enc_emb')
# 입력된 단어 인덱스 시퀀스를 임베딩 벡터 시퀀스로 변환
enc_emb = enc_emb_layer(enc_inputs)
# return_state=True: 최종 시점의 hidden state (state_h)와 cell state (state_c)를 반환
encoder_lstm = LSTM(hidden_size, return_state=True, name='encoder_lstm')
# encoder_emb을 LSTM에 입력
_, state_h, state_c = encoder_lstm(enc_emb)

encoder_states = [state_h, state_c]   # 디코더에 넘겨줄 상태 정보를 리스트로 묶음

# 7.2) 디코더: 인코더에서 전달받은 상태로 <sos>부터 시작해 하나씩 단어를 생성해가는 구조
dec_inputs = Input(shape=(None,), name='dec_inputs')
dec_emb_layer = tf.keras.layers.Embedding(dec_vocab, hidden_size, name='dec_emb')
dec_emb = dec_emb_layer(dec_inputs)
decoder_lstm = LSTM(hidden_size, return_sequences=True, return_state=True, name='decoder_lstm')
dec_outputs, _, _ = decoder_lstm(dec_emb, initial_state=encoder_states)
dec_dense = Dense(dec_vocab, activation='softmax', name='decoder_dense')

# 위에서 나온 decoder_outputs를 Dense layer에 통과시켜 각 시점마다 단어 예측 결과를 얻음
dec_outputs = dec_dense(dec_outputs)

# 모델 컴파일/학습 : 모델을 학습시키는 최종 단계
train_model = Model([enc_inputs, dec_inputs], dec_outputs)
train_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
train_model.fit([q_pad, decoder_input_data], decoder_target_data,
                batch_size=2, epochs=200, verbose=0)
print("학습 완료")

# 8) 인퍼런스용 모델 분리
# 8.1) Encoder 모델
encoder_model = Model(enc_inputs, encoder_states)

# 8.2) Decoder 모델
# -- 상태 입력 레이어 (상태 입력 정의)
state_input_h = Input(shape=(hidden_size,), name='state_h_in')
state_input_c = Input(shape=(hidden_size,), name='state_c_in')

# -- 토큰 입력
dec_input_single = Input(shape=(1,), name='dec_input_single')

# -- 레이어 재사용
dec_emb2    = dec_emb_layer(dec_input_single)

# LSTM 실행 (상태를 외부에서 입력)
dec_outputs2, h2, c2 = decoder_lstm(dec_emb2, initial_state=[state_input_h, state_input_c])
dec_outputs2 = dec_dense(dec_outputs2)  # 단어 확률 → 단어 인덱스

decoder_model = Model(    # 디코더 모델 정의
    [dec_input_single, state_input_h, state_input_c],
    [dec_outputs2, h2, c2]
)

# 9) 답변 생성 함수 : 학습된 인코더–디코더(Seq2Seq) 모델을 이용해, 사용자의 질문(question)을 받아 
#                     대응하는 답변을 한 토큰씩 생성해 내는 인퍼런스(inference) 루틴
def reply(question):
    # 인코더로부터 초기 상태 획득
    # q_tok (질문용 토크나이저)를 사용해 입력 문장을 인덱스 시퀀스로 변환
    seq = q_tok.texts_to_sequences([question])
    seq = pad_sequences(seq, maxlen=q_pad.shape[1], padding='post')
    states = encoder_model.predict(seq, verbose=0)   # 인코더 상태 획득
    # 패딩된 시퀀스를 인코더 모델에 넣어 마지막 시점의 은닉 상태(state_h)와 셀 상태(state_c)를 가져옴
    # 반환된 states는 리스트 형태로 [state_h, state_c]

    # 디코더 시작 토큰 (디코더 초기화)
    # 디코더의 시작 토큰(<sos>) 인덱스로 구성된 1×1 배열을 준비
    target_seq = np.array( [ [ a_tok.word_index['<sos>'] ] ] )
    decoded = [ ]   # 생성된 단어를 모아둘 decoded 리스트 초기화

    # 토큰 반복 생성 - 최대 20번 반복하며 한 스텝씩 단어를 생성 
    for _ in range(20):
        # decoder_model에 현재 입력 토큰(target_seq)과 이전 상태(states)를 넣어 
        # 다음 단어 예측 확률(output_tokens)과 새로운 상태(h, c) 획득
        output_tokens, h, c = decoder_model.predict([target_seq] + states, verbose=0)

        # 확률이 가장 높은 토큰 인덱스(sampled_idx) 선택
        sampled_idx = np.argmax(output_tokens[0, -1, :])

        # a_tok.index_word로 인덱스를 실제 단어(sampled_word)로 매핑
        sampled_word = a_tok.index_word.get(sampled_idx, '')

        if sampled_word == '<eos>' or not sampled_word:  # 종료 조건 판단 및 출력 누적
            # '<eos>' 토큰을 만나거나, 매핑되지 않는(빈 문자열) 경우 루프 탈출
            break
        decoded.append(sampled_word)  # 계속: 생성된 단어를 decoded 리스트에 추가

        # 다음 스텝을 위해 target_seq를 방금 생성한 토큰(sampled_idx)으로 교체
        target_seq = np.array( [ [ sampled_idx ] ] )
        states = [ h, c ]   # 디코더 상태를 새로 받은 [h, c]로 업데이트

    return ' '.join(decoded)  # 리스트에 쌓인 단어들을 공백으로 결합해 하나의 문장으로 반환

# 10) 테스트
print("\n챗봇 테스트:")
# 저장해 둔 questions 목록의 각 질문에 대해 reply(q)를 실행
# 원문 질문과 함께, 생성된 답변을 “질문 ➜ 답변” 형태로 출력
for q in questions:
    print(f"{ q } ➜ { reply(q) }")
