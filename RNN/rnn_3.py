# LSTM 으로 분류 모델 작성
# 감성 분류

# 총 10개의 평가 글
docs = [
    '너무 재밌네요', 
    '최고에요', 
    '참 잘 만든 영화에요', 
    '추천하고 싶은 영화입니다',
    '한 번 더 보고 싶네요', 
    '글쎄요', 
    '별로에요', 
    '생각보다 지루하네요', 
    '연기가 어색해요', 
    '재미없어요'
]

import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer

labels = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
token = Tokenizer()
token.fit_on_texts(docs)    # 단어 사전 생성
print(token.word_index)

x = token.texts_to_sequences(docs)   # 토큰화
print('x : ', x)

# 시퀀스 데이터를 딥러닝 모델에 넣기 전에 토큰의 길이를 동일하게 해야 함
from tensorflow.keras.preprocessing.sequence import pad_sequences
padded_x = pad_sequences(x, maxlen=5, padding='pre')    # pre : 앞쪽에 0을 채워서 길이를 맞춰줌 / post : 뒤쪽
print('padded_x : ', padded_x)



#######################################################################################
# 모델 처리
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input, Flatten

word_size = len(token.word_index) + 1   # 가능 토큰 개수 + 1
model = Sequential()
model.add(Input(shape=(5, )))
model.add(Embedding(input_dim=word_size, output_dim=8))     # output_dim=8 : 각 단어를 8차원 실수 벡터로 표현
model.add(LSTM(32, activation='tanh'))
# model.add(Flatten())  # 이미 2D 여서 필요 없음 
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(padded_x, labels, epochs=20, verbose=1)
print('정확도 : ', model.evaluate(padded_x, labels)[1])
print('예측값 : ', np.where(model.predict(padded_x) > 0.5, 1, 0).ravel())