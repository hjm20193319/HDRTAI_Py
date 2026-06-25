# Scaled Dot-Product Attention (Tokenizer + Attention)

import numpy as np
import math
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


#######################################################################################
# Encoding

# 입출력 문장
input_text = "I have a pen"
output_text = "<sos> 나는 펜을 갖고 있다 <eos>"

# 토큰 처리
input_tokenizer = Tokenizer(filters='', lower=False)
output_tokenizer= Tokenizer(filters='', lower=False)

input_tokenizer.fit_on_texts([input_text])
print('input_tokenizer : ', input_tokenizer.word_index)
print('input_tokenizer : ', input_tokenizer.word_counts)
output_tokenizer.fit_on_texts([output_text])
print('output_tokenizer : ', output_tokenizer.word_index)
# input_tokenizer :  {'I': 1, 'have': 2, 'a': 3, 'pen': 4}
# output_tokenizer :  {'<sos>': 1, '나는': 2, '펜을': 3, '갖고': 4, '있다': 5, '<eos>': 6}
print('\n')


# 문장을 숫자 시퀀스화
input_seq = input_tokenizer.texts_to_sequences([input_text])
print('input_seq : ', input_seq)
output_seq = output_tokenizer.texts_to_sequences([output_text])
print('output_seq : ', output_seq)
print('\n')


# 시퀀스 패딩
max_input_len = max(len(s) for s in input_seq)
max_output_len = max(len(s) for s in output_seq)
print(max_input_len, max_output_len)
print()
input_pad = pad_sequences(input_seq, maxlen=max_input_len, padding='post')
output_pad = pad_sequences(output_seq, maxlen=max_output_len, padding='post')
print('\n')


# Q, K, V 구성
n_src = input_pad.shape[1]    # 입력 길이
n_tgt = output_pad.shape[1]   # 출력 길이

K = np.eye(n_src)
V = np.eye(n_src)


#######################################################################################
# Decoder
# 개념이해용 예제이므로 Q를 어디에 집중할지 직접 지정
Q = np.zeros((n_tgt, n_src))

for i in range(n_tgt):
    if i == 0:
        Q[i, 0] = 1.0
    elif i == n_tgt - 1:
        Q[i, -1] = 1.0
    elif i < n_src - 1:
        Q[i, i:i+2] = 0.5
    else:
        Q[i, -1] = 1.0
# print(Q)


def attentionFunc(q, K, V):
    scores = q.dot(K.T) / math.sqrt(K.shape[1])
    exp = np.exp(scores - np.max(scores))
    weights = exp / exp.sum()
    context = (weights[:, None] * V).sum(axis=0)
    return context, weights



#######################################################################################
# Attention 실행 (디코더가 한 스텝씩 생성하는 과정)
print('Attention 결과 : \n')
for i in range(n_tgt):
    context, weights = attentionFunc(Q[i], K, V)
    print(f'[Output 위치 {i}]')
    for src_word, w in zip(input_tokenizer.word_index.keys(), weights):
        print(f'  - {src_word:>5}  -> Attention:{w:.3f}')
    print('  -> Context 벡터 : ', np.round(context, 3), '\n')


# 최종 출력 시퀀스
print('입력 시퀀스 : ', input_pad)
print('출력 시퀀스 : ', output_pad)



#######################################################################################
# 디코더 출력 복원 (불필요한 토큰 제거 : 0, <sos>, <eos>)
reverse_output_index = {v:k for k, v in output_tokenizer.word_index.items()}
print(reverse_output_index)
reconstructed = []

for idx in output_pad[0]:
    if idx == 0:
        continue    # 패딩 무시
    word = reverse_output_index.get(idx, '?')   # 정수 인덱스를 실제 단어로 변환
    if word in ["<sos>", "<eos>"]:
        continue

    reconstructed.append(word)

print('\n')
print('복원 결과 : \n')
print(' '.join(reconstructed))