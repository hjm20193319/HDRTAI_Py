# RNN 으로 스펨 메일 분류 모델 (이항 분류)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils import class_weight

data = pd.read_csv('spam.csv', encoding='latin1')
data = data[['v1', 'v2']]
# print(data[:3])
data['v1'] = data['v1'].replace(['ham', 'spam'], [0, 1])
# print(data[:3])

data.drop_duplicates(subset=['v2'], inplace=True)

x_data = data['v2']
y_data = data['v1']

tokenizer = Tokenizer()
tokenizer.fit_on_texts(x_data)
sequences = tokenizer.texts_to_sequences(x_data)

word_index = tokenizer.word_index
vocabsize = len(word_index) + 1
print('vocab size : ', vocabsize)   # vocab size :  8921

# 패딩
max_len = max(len(i) for i in sequences)
data_pad = pad_sequences(sequences, maxlen=max_len)

# train/test split
n_train = int(len(data_pad) * 0.8)
x_train, x_test = data_pad[:n_train], data_pad[n_train:]
y_train, y_test = np.array(y_data[:n_train]), np.array(y_data[n_train:])

# 데이터 불균형 보정 작업
weights = class_weight.compute_class_weight(
    class_weight='balanced',   # 자동으로 클래스 비율에 따라 가중치 계산
    classes=np.unique(y_train),  # 고유 클래스 목록 : [0, 1]
    y=y_train   # 실제 훈련 라벨
)


class_weight = {0:weights[0], 1:weights[1]}
print('클래스 가중치 : ', class_weight)
# 클래스 가중치 :  {0: np.float64(0.5744651292025562), 1: np.float64(3.857276119402985)}


# model
model = Sequential()
model.add(Embedding(vocabsize, 32))
model.add(SimpleRNN(32))    # activation='tanh'
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
print(model.summary())

early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
history = model.fit(x_train, y_train, epochs=300, batch_size=64, validation_split=0.2, class_weight=class_weight, callbacks=early_stop)


# 성능 시각화
loss, acc = model.evaluate(x_test, y_test)
print('테스트 정확도 : ', acc)

plt.figure(figsize=(10,4))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Train val loss')
plt.title('Loss over epochs')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['acc'], label='Train acc')
plt.plot(history.history['val_acc'], label='Train val acc')
plt.title('Acc over epochs')
plt.xlabel('epoch')
plt.ylabel('acc')
plt.legend()

plt.tight_layout()
plt.show()


# 예측
new_mail = [
    "Go until jurong point, crazy.. Available only in bugis n great world la e buffet... Cine there got amore wat...",
    "Nah I don't think he goes to usf, he lives around here though",
    "FreeMsg Hey there darling it's been 3 week's now and no word back! I'd like some fun you up for it still? Tb ok! XxX std chgs to send, 1.50 to rcv",
    "Please be at work by 10:00 tomorrow. Have a good rest"
]

new_emcoded = tokenizer.texts_to_sequences(new_mail)
new_padded = pad_sequences(new_emcoded, maxlen=max_len)
predicted = model.predict(new_padded)
print(predicted)
print('\n')

for i, m in enumerate(new_mail):
    prob = predicted[i][0]
    label = 'spam' if prob > 0.5 else 'ham'
    print(f'[{label.upper()}] ({prob:.4f}) - \"{m}\"')