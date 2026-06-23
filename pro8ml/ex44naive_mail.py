# 나이브 베이즈(Naive Bayes)를 이용한 텍스트 분류
# MultinomialNB: 단어의 출현 빈도와 같은 이산적인 특징 데이터를 분류하는 데 적합한 알고리즘.
# 베이즈 정리를 기반으로 하며, 모든 특성이 독립적이라는 가정하에 클래스 확률을 계산함.

from sklearn.feature_extraction.text import CountVectorizer # [문법] 텍스트 데이터를 단어 횟수 벡터로 변환하는 클래스
from sklearn.naive_bayes import MultinomialNB # [문법] 다항 분포 나이브 베이즈 모델 클래스
import pandas as pd
from sklearn.metrics import accuracy_score # [문법] 모델의 분류 정확도를 측정하는 함수

# [추천] 한국어 텍스트의 경우 KoNLPy(Okt, Mecab 등) 형태소 분석기를 사용하여 토큰화한 후 벡터화하는 것이 정확도 향상에 유리함.

# 학습용 데이터 (말뭉치)
texts = [
    '무료 쿠폰 지금 무료 클릭',
    '한번만 클릭하면 무료',
    '오늘 회의는 2시야',
    '지금 할인 행사 진행 중',
    '회의 자료는 메일로 보내주세요',
    '지금 바로 쿠폰 확인'
]

label = ['spam', 'spam', 'ham', 'spam', 'ham', 'spam'] # 종속변수(Label): 스팸(spam)과 정상(ham)

# 단어 등장 횟수 기반 벡터
vect = CountVectorizer()    # [문법] CountVectorizer: 단어의 빈도수 정보 추출(순서X), BoW(Bag of Words) 생성
x = vect.fit_transform(texts) # [문법] fit_transform: 말뭉치에서 단어 사전을 만들고 문장을 수치 벡터로 변환
print(x)    # CSR(Compressed Sparse Row) 형식: (문서번호, 단어번호) 등장횟수
print(x.toarray()) # [문법] 희소 행렬을 밀집 행렬(배열) 형태로 변환하여 확인
print(vect.get_feature_names_out()) # [문법] 추출된 단어 사전의 특징 이름(단어들) 목록 반환
print('\n')
print(vect.vocabulary_) # [문법] 각 단어와 매핑된 인덱스 번호를 딕셔너리 형태로 확인

# 모델
model = MultinomialNB() # [문법] MultinomialNB: 텍스트 분류에 최적화된 나이브 베이즈 객체 생성
model.fit(x, label) # [문법] fit: 벡터화된 텍스트와 레이블을 사용하여 모델 학습 수행

# 예측
pred = model.predict(x) # [문법] predict: 학습된 데이터를 다시 입력하여 예측 결과 확인
print('정확도 : ', accuracy_score(label, pred)) # [문법] accuracy_score: 실제값과 예측값을 비교하여 정확도 계산
print('\n')

# 새로운 메일로 예측
test_text = ['무료 쿠폰 발급', '간부 회의는 언제 시작하나요?']
# [주의] 새로운 데이터 예측 시에는 반드시 학습 시 사용한 Vectorizer의 transform()만 사용해야 함 (fit 금지)
x_test = vect.transform(test_text) # [문법] transform: 기존 단어 사전을 기준으로 새로운 문장을 벡터화
print(x_test.toarray()) # 학습 데이터에 없던 단어(예: '발급', '언제')는 벡터화 과정에서 무시됨
print('\n')

# 예측 + 확률 출력
pred = model.predict(x_test) # [문법] predict: 새로운 데이터의 클래스(spam/ham) 결정
print('예측값 : ', pred)
print('\n')
# [문법] predict_proba: 각 클래스에 속할 확률값을 반환 (합계는 1.0)
print('확률 : \n', model.predict_proba(x_test)) 
print('\n')

prob = model.predict_proba(x_test) # 베이즈 정리에 의해 계산된 사후 확률
class_names = model.classes_ # [문법] 모델이 학습한 클래스 이름 목록 (['ham', 'spam'])

for text, pred, prob in zip(test_text, pred, prob):
    # [문법] zip을 사용하여 텍스트, 예측결과, 확률을 매칭하여 출력
    prob_str = ', '.join([f'{cls}:{p:.4f}' for cls, p in zip(class_names, prob)])
    print(f"'{text}' -> 예측:{pred}, 확률:{prob_str}")