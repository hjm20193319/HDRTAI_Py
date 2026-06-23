# jamotools(한글 자소단위로 분리 및 결합 라이브러리) 설치
# !pip install jamotools

# 자모 분리 테스트
import jamotools
import tensorflow as tf
import numpy as np
import sys
from tensorflow.keras.preprocessing.sequence import pad_sequences

path_to_file = tf.keras.utils.get_file('toji.txt', 'https://raw.githubusercontent.com/pykwon/etc/master/rnn_test_toji.txt')

# open(path_to_file, 'rb'): rb는 "read binary", 즉 바이트 단위로 읽기를 의미.
# 이걸 쓰면 텍스트가 아닌 **바이너리 데이터(bytes)**로 파일을 읽어온다.
# .read(): : 전체 파일을 한 번에 읽어와서 bytes 객체로 반환.
# .decode(encoding='utf-8'): bytes를 UTF-8로 **디코딩하여 문자열(str)**로 변환함.
# 왜 이렇게 쓰는가? UTF-8 텍스트 파일을 읽을 때 인코딩 문제 없이 안전하게 처리할 수 있기 때문.
train_text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
s = train_text[:100]
print('s:', s)   # 제 1 편 어두문의 발소리 1897년의 한가위 ...

# 한글 텍스트를 자모 단위로 분리. 숫자,기호, 영어, 한자 등에는 영향 X
s_split = jamotools.split_syllables(s)   # 100글자의 한글이 자모(초성, 중성, 종성) 단위로 분리됨
print('s_split:', s_split)   # ㅈㅔ 1 ㅍㅕㄴ ㄹㅗ㉡ㄱㄹㅠ ㅂㅏㄹㅅㅐㄹㅓ...

# 자모 결합 테스트
s2 = jamotools.join_jamos(s_split)
print('s2:', s2)    # 결합된 결과 ==> 제 1 편 어두문의 발소리...
print(s == s2)    # True    분리 전후의 문장이 비교 결과 같음

# 자모 토큰화 : 텍스트를 자모 단위로 나누다. 지연 시간 필요.
train_text_X = jamotools.split_syllables(train_text)
# 자모 문자열 전체에서 중복 없이 고유한 문자 집합(set)을 뽑고, 정렬.
# 이걸 통해 모델이 사용하는 자모 사전(vocabulary)을 정의한다.
vocab = sorted(set(train_text_X))

# 자모 기반 언어 모델을 만들 때, 예외 처리를 위한 특수 토큰을 추가하는 작업
# UNK는 UNKnown 약자로  \u출현 빈도가 낮은 단어들을 모두 대체한다.
# 모델이 학습 중 본 적 없는 문자를 만났을 때, 대체용으로 사용하는 예외 처리용 토큰이다.
# 예: 모델이 '㉡', '★', '𐤀' 같은 이상하거나 드문 기호를 만나면 → 'UNK'로 처리.
vocab.append('UNK')   # 사전에 정의되지 않은 기호가 있을 수 있으므로 'UNK'도 사전에 넣음
print ('{} unique characters'.format(len(vocab)))  # 179 unique characters

# vocab list를 숫자로 매핑하고, 반대도 실행.
char2idx = {u:i for i, u in enumerate(vocab)}  # 'ㄱ' → 2, 'ㅏ' → 10 등으로 문자 → 정수 변환

# 각 자모를 char2idx로 숫자로 변환해서 넘파이 배열로 만든다.
# 이 배열이 바로 모델 입력으로 쓰이는 시퀀스 데이터다.
text_as_int = np.array([char2idx[c] for c in train_text_X])
print(text_as_int)
# 텍스트 안에 존재하지 않는 토큰을 나타내는 'UNK' 사용
print('index of UNK: {}'.format(char2idx['UNK']))   # 'UNK'가 vocab 리스트의 178번에 있음

# 토큰 데이터 확인
print(train_text_X[:20])   # ㅈㅔ 1 ㅍㅕㄴ ㄹㅗ㉡ㄱ ㄹㅠ ㅂ
print(text_as_int[:20])    # [69 81  2 13  2 74 82 49  2 68 80 52 89  ...

# 학습 데이터세트 생성
# 모델에 입력할 문자열의 길이(sequence length)를 지정한다.
# 즉, 모델은 80개의 자모 문자를 입력으로 받고, 그 다음 문자를 예측하게 된다.
seq_length = 80

# text_as_int는 전체 학습 텍스트를 정수 배열로 변환한 결과이다.
# 이걸 80개씩 잘라서 학습에 사용하므로, 전체 데이터를 몇 개의 시퀀스로 만들 수 있는지를 계산.
# 예: 전체 글자 수가 80,000개라면 → examples_per_epoch = 80,000 // 80 = 1,000
examples_per_epoch = len(text_as_int) // seq_length
# tf.data.Dataset으로 정수 배열(text_as_int)을 하나씩 나누어 스트림처럼 처리할 수 있게 작성
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

idx2char = np.array(vocab)   # 숫자 인덱스를 다시 문자로 변환하기 위한 배열. idx2char[5] → 'ㄱ'

# 연속된 시퀀스를 묶어 모델 학습에 적합한 형태로 만드는 작업
# 자모 인덱스를 seq_length + 1개씩 묶어서 하나의 시퀀스로 만든다.
# 이유는 앞의 seq_length는 입력, 마지막 1개는 정답(타겟)이다.
# drop_remainder=True: 나누다 남는 조각은 버림. (학습 일관성을 위해)
char_dataset = char_dataset.batch(seq_length+1, drop_remainder=True)

# char_dataset에 저장된 데이터를 직접 확인해보기 위한 테스트
for item in char_dataset.take(1):   # 하나의 배치(길이 81짜리 배열)만 가져옴
    print(idx2char[item.numpy()])   # ['ㅈ' 'ㅔ' ' ' '1' ' ' 'ㅍ' 'ㅕ' 'ㄴ' ...
    print(item.numpy())            # [69 81  2 13  2 74 82 49  2 68 80 52 89  ...

# "입력 시퀀스 → 다음 글자 예측" 형태를 만들기 위해 작성
# chunk: 길이 81짜리 자모 인덱스 시퀀스 (char_dataset의 요소)
def split_input_target2(chunk):
    return [chunk[:-1], chunk[-1]]
    # chunk[:-1]: 앞 80개 → 입력 시퀀스,   chunk[-1]: 마지막 1개 → 예측할 대상 문자

# 최종 전처리 데이터셋을 완성하는 단계
# char_dataset: seq_length + 1 = 81개씩 잘라놓은 자모 인덱스 시퀀스 Dataset.
#   예: [69, 81, 2, 13, ..., 77]
# split_input_target2(chunk):  이 시퀀스를 (입력, 정답) 쌍으로 변환한다.
#   입력: 앞 80개 (chunk[:-1]),  정답: 마지막 1개 (chunk[-1])
# map(...): Dataset의 각 요소에 split_input_target2 함수를 적용한다.
train_dataset = char_dataset.map(split_input_target2)

# train_dataset이 정상적으로 (입력, 정답) 쌍으로 구성을 확인하기 위한 디버깅 테스트
for x,y in train_dataset.take(1):
    print(idx2char[x.numpy()])   # ['ㅈ' 'ㅔ' ' ' '1' ' ' 'ㅍ' 'ㅕ' 'ㄴ'...
    print(x.numpy())             # [69 81  2 13  2 74 82 49  2 ...
    print(idx2char[y.numpy()])  # ㅅ
    print(y.numpy())  # 66

BATCH_SIZE = 64    # 한 번의 학습에서 모델이 처리할 데이터 샘플 수
# 즉, train_dataset에서 한 배치(batch)는 (입력 80개, 정답 1개)짜리 데이터가 64개 묶여 있다.
# RNN 계열 모델은 큰 배치 사이즈보다 작거나 중간 크기가 일반적으로 잘 작동한다.

# 1 에포크(epoch)**에서 처리할 미니 배치(batch)의 수를 정한다.
# examples_per_epoch는 시퀀스 수 (80글자씩 자른 시퀀스 수)
# 따라서 steps_per_epoch는 총 시퀀스 개수 ÷ 배치 크기
# 총 시퀀스 개수 ÷ 배치 크기     예: 총 64000개의 시퀀스가 있다면 → 64000 // 64 = 1000
steps_per_epoch = examples_per_epoch // BATCH_SIZE

# 섞기(shuffle)할 때 사용할 버퍼 크기.. 이 값은 클수록 데이터를 더 잘 섞지만, 메모리를 더 사용한다.
# tf.data.Dataset.shuffle(BUFFER_SIZE) 시 사용된다.
BUFFER_SIZE = 5000

# 학습용 데이터셋을 구성: 데이터를 무작위로 섞고 64개씩 묶어 학습에 적합하게 준비
train_dataset = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

# 자소 단위 생성 모델 정의
total_chars = len(vocab)     # 전체 자모 문자 수 (고유한 자모 개수 + 'UNK')

model = tf.keras.Sequential([
    # Keras가 첫 입력이 들어오는 순간 자동으로 input_length를 감지함.
    # 따라서, 생당해도 문제 없고 오히른 미래 호환성을 위해 제거해야 함.
    # 자모 인덱스 → 100차원의 연속된 벡터(임베딩)로 변환
    # 입력: [69, 81, 2, 13, ..., 55] (숫자 시퀀스),  출력 shape: (batch_size, sequence_length, 100)
    # 정수 인덱스를 dense vector로 바꾸는 역할
    tf.keras.layers.Embedding(total_chars, 100),
    tf.keras.layers.LSTM(units=400),  # 400개의 LSTM 유닛을 가진 순환 신경망 층
    # 과거 시점의 입력들을 기억하면서 다음 문자를 예측하는 데 필요한 문맥을 유지

    # softmax를 통해 각 자모 문자에 대한 다음 글자 확률 분포 생성
    tf.keras.layers.Dense(total_chars, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 모델이 예측한 확률 분포로부터 실제 다음 글자를 뽑는 방식을 제어하는 로직이다.
# 단순한 argmax 예측보다 훨씬 더 창의적이고 다양한 문장을 생성할 수 있게 해준다.
# 글자 인덱스를 "무작위 샘플링" 방식으로 선택
def sample(preds, temperature=0.7):  # 낮을수록 보수적, 높을수록 다양하고 창의적인 출력
    preds = np.asarray(preds).astype('float64')  # 확률 벡터를 float64로 변환 (안정성 확보)
    preds = np.log(preds + 1e-8) / temperature
    # 로그를 취해 확률이 너무 작은 값은 확 줄이고, 높은 값은 부각시킴. 1e-8은 log(0) 방지용
    # temperature 값으로 분포를 부드럽게 또는 날카롭게 조정

    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)   # softmax처럼 다시 확률로 정규화
    probas = np.random.multinomial(1, preds, 1)   # 확률 분포에 따라 샘플 1개 뽑기

    # 예: [0.01, 0.01, ..., 0.90, ..., 0.01] → np.argmax(...)로 인덱스 선택
    return np.argmax(probas)

# 모델 학습 중간에 예측 결과를 실시간으로 출력하는 콜백 함수
# 훈련이 잘 되고 있는지 직접 눈으로 확인할 수 있게 해주며, 특히 텍스트 생성 모델에서는 매우 유용
def testmodel2(epoch, logs):
    if epoch % 5 != 0 and epoch != 49:   # 5에포크 마다 또는 마지막 49에포크에서만 실행됨
        return

    # 원본 텍스트 처음 48자 → 자모 분리하여 시작 시퀀스로 사용
    test_sentence = train_text[:48]
    test_sentence = jamotools.split_syllables(test_sentence)

    next_chars = 300
    for _ in range(next_chars):   # # 300자 예측 반복
        test_text_X = test_sentence[-seq_length:]
        test_text_X = np.array([char2idx[c] if c in char2idx else char2idx['UNK'] for c in test_text_X])
        test_text_X = pad_sequences([test_text_X], maxlen=seq_length, padding='pre', value=char2idx['UNK'])
        # 최근 80자 기준 입력 시퀀스를 만들고, 부족하면 UNK로 패딩

        output_probs = model.predict(test_text_X, verbose=0)[0]
        output_idx = sample(output_probs, temperature=0.7)
        test_sentence += idx2char[output_idx]
        # 모델이 예측한 softmax 확률 → sample()로 다음 글자 선택 → 시퀀스에 추가

        # 실시간으로 자모 글자 하나씩 출력 (개행 없이 붙여서)
        sys.stdout.write(idx2char[output_idx])
        sys.stdout.flush()

    print("\n")  # 300자 다 출력한 후 줄바꿈
    # # 사람이 읽을 수 있도록 음절로 결합된 문장 출력
    print("\n\nGenerated sentence:\n")
    print(jamotools.join_jamos(test_sentence))

# 콜백(callback)을 정의한다.
# on_epoch_end=testmodel2: 에포크가 끝날 때마다 testmodel2() 함수가 실행된다.
# testmodel2()는 5에포크 마다 문장을 예측해서 출력 (자모 + 결합된 한글 문장).
testmodelcb = tf.keras.callbacks.LambdaCallback(on_epoch_end=testmodel2)

history = model.fit(train_dataset.repeat(),   # Dataset을 무한 반복 (에포크 수에 맞춰 끊김)
            epochs=5,
            steps_per_epoch=steps_per_epoch,   # 한 에포크당 처리할 배치 수
            callbacks=[testmodelcb], verbose=2)   # 에포크 끝마다 testmodel2() 실행

model.save('rnnmodel.keras')

# 임의의 문장을 사용한 생성 결과 확인
test_sentence = '최참판댁 사랑은 무인지경처럼 적막하다'
# 초기 입력 문장을 자모 분해해서 모델 입력 형식에 맞춤.
test_sentence = jamotools.split_syllables(test_sentence)

next_chars = 500   # 500자 생성 반복
# 자모 시퀀스를 입력 → softmax 확률 → 샘플링 → 자모 1개 추가
# 자모 단위로 실시간 출력 (줄바꿈 없이 한 글자씩)
for _ in range(next_chars):
    test_text_X = test_sentence[-seq_length:]
    test_text_X = np.array([char2idx.get(c, char2idx['UNK']) for c in test_text_X])
    test_text_X = pad_sequences([test_text_X], maxlen=seq_length, padding='pre', value=char2idx['UNK'])

    output_probs = model.predict(test_text_X, verbose=0)[0]
    output_idx = sample(output_probs, temperature=0.7)
    test_sentence += idx2char[output_idx]

    # 실시간 출력 추가
    sys.stdout.write(idx2char[output_idx])
    sys.stdout.flush()

# 자모 시퀀스를 한글 음절로 조합. 최종 결과는 사람이 읽을 수 있는 문장
generated_text = jamotools.join_jamos(test_sentence)
print("\n\nGenerated sentence:\n")
print(generated_text)

# 시각화
import matplotlib.pyplot as plt
# %matplotlib inline
plt.plot(history.history['loss'], c='r', label='loss')
plt.legend()
plt.show()