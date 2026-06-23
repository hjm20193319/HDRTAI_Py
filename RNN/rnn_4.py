# RNN 을 이용한 텍스트 생성
# 문맥을 반영해 다음 단어를 예측하여 텍스트 생성 (다항 분류)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential

text = """
현대차그룹은 현대차·기아의 자동차 생산 현장에 아틀라스를 2만5천대 이상 도입하겠다고 밝혔다. 다만 구체적인 도입 시기와 투입 공장은 공개하지 않았다.
현대차그룹은 2028년까지 연간 3만대 규모의 로봇 생산 시스템을 구축할 계획인데 그중 83％에 해당하는 규모다.
아틀라스 양산 초기에는 생산 비용과 판매 단가가 높을 수밖에 없는 만큼 현대차·기아의 구매력을 거름 삼아 규모의 경제를 달성하겠다는 구상으로 풀이된다.
증권업계에 따르면 아틀라스의 생산 초기 원가는 대당 13만∼14만달러(약 2억원) 수준이지만 5만대 생산 시 원가는 3만달러(4천300만원)로 하락하는 것으로 분석됐다.
최근 송호성 기아 사장은 다른 기업설명회에서 "첫 1∼2년은 미국 공장에 대량 배치해 데이터를 축적하고 안전성을 확보할 것"이라며 "특정 공정에서 아틀라스 활용이 입증되면 완성차의 공장 레이아웃이 글로벌하게 유사하기 때문에 다른 공장으로도 손쉽게 확장할 수 있다"고 말했다.
아울러 현대차그룹은 미국 현지에 휴머노이드 액추에이터 생산시설(연 생산능력 35만개 이상)을 구축하고 2028년부터 가동할 계획이다.
2028년부터 단계적으로 아틀라스를 산업 현장에 투입할 예정인 가운데 핵심 부품인 액추에이터의 내재화 계획이 구체화한 것이다.
액추에이터는 로봇의 관절 역할을 하는 구동 장치로서 휴머노이드 전체 제조 비용의 60％를 차지하는 핵심 부품이다.
아틀라스 액추에이터 공급을 맡는 현대모비스가 생산시설 운영도 담당할 것으로 예상된다. 다만 새 공장을 지을지, 기존의 부품 라인을 활용할지는 공개되지 않았다.
현대모비스는 향후 휴머노이드 센서, 제어기, 핸드 그리퍼(로봇 손) 등 다른 부품 시장으로 진출할 계획도 갖고 있다.
한편, 현대차그룹이 미국 현지에서 로보틱스 전략을 주제로 별도 기업설명회를 개최하면서 보스턴다이내믹스 상장 준비 작업이 본격화한 것 아니냐는 분석도 조심스럽게 제기된다.
이번 행사에는 현대차·기아, 현대모비스, 현대글로비스, 현대오토에버, 보스턴다이내믹스 등 6개 그룹사가 총출동했고 장재훈 현대차그룹 부회장을 비롯해 김흥수 글로벌전략조직(GSO) 담당 부사장. 아만다 맥마스터 보스턴다이내믹스 임시 최고경영자(CEO) 등이 참석했다.
보스턴다이내믹스의 기업 가치는 2021년 현대차그룹이 인수할 당시 11억달러(약 1조2천482억원)에서 현재는 최소 수십 배 수준으로 뛰어올랐다고 업계는 평가하고 있다.
다만 송 사장은 최근 기업설명회에서 "내부적으로는 아직 기업공개(IPO) 시점이나 외부 자금 조달 추진 여부도 결정하지 않았다"면서 "예상 상장 시점을 구체적으로 언급하기엔 다소 이른 시점"이라고 말했다.
"""

# tok = Tokenizer(char_level=True)    # 글자 단위
# tok = Tokenizer(char_level=False)   # 단어 단위, 기본 값
tok = Tokenizer()
tok.fit_on_texts([text])
print(tok.word_index)
encoded = tok.texts_to_sequences([text])[0]
print(encoded)
print('\n')

vacab_size = len(tok.word_index) + 1    # 실제 단어 집합 + 1 을 함
# Tokenizer 정수 인덱싱은 1부터 시작하기 때문에 인덱스를 맞춰주기 위해서

# 훈련 데이터 작성
sequences = list()
for line in text.split('\n'):   # 문장 토큰화
    enco = tok.texts_to_sequences([line])[0]     # 줄 단위로 인코딩
    # print(enco)
    # 바로 다음 단어를 label로 사용하기 위해 리스트에 담기
    for i in range(1, len(enco)):
        sequ = enco[:i+1]
        # print(sequ)
        sequences.append(sequ)
print('학습에 참여할 Sample 수 : ', len(sequences)) # 11개

print(max(len(i) for i in sequences))
print('\n')

# 전체 각각의 벡터 길이를 통일
max_len = max(len(i) for i in sequences)
psequences = pad_sequences(sequences, maxlen=max_len, padding='pre')
print(psequences)
print('\n')

# 각 벡터의 마지막 요소를 label로 사용하기 위해 분리
x = psequences[:, :-1]  # feature
y = psequences[:, -1]   # label
print(x)
print(y)
# [ 3  1  4  5  1  7  1  9 10  1 11]    → 11 종류
print('\n')

# 다항 분류이기 때문에 label을 One-Hot 처리 해줘야 함
y = to_categorical(y, num_classes=vacab_size)
print(y[:2])
print('\n')



#######################################################################################
# 모델 정의
model = Sequential()
model.add(Embedding(vacab_size, 32, input_length=max_len-1))
model.add(LSTM(32, activation='tanh'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(vacab_size, activation='softmax'))      # 확률로 출력

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x, y, epochs=200, verbose=2)
print(model.summary())
print(model.evaluate(x, y))



#######################################################################################
# 문자열 생성 함수
def sequence_gen_text(model, t, current_word, n):
    init_word = current_word
    sentence = ''

    for _ in range(n):
        encoded = t.texts_to_sequences([current_word])[0]
        encoded = pad_sequences([encoded], maxlen=max_len-1, padding='pre')
        result = np.argmax(model.predict(encoded, verbose=0), axis=-1)

        # 예측 단어 찾기
        for word, index in t.word_index.items():
            # print(word, index)
            if index == result:
                break

        current_word = current_word + ' ' + word
        sentence = sentence + ' ' + word
    sentence = init_word + sentence
    return sentence

print(sequence_gen_text(model, tok, '생산', 20))
print('\n')
print(sequence_gen_text(model, tok, '시스템', 20))
print('\n')
print(sequence_gen_text(model, tok, '현대차', 20))
print('\n')