# 작업 결과를 간단하게 웹으로 출력하기
# [문법] Python Streamlit 라이브러리 사용: 데이터 스크립트를 웹 앱으로 변환해주는 프레임워크
# pip install streamlit

from sklearn.feature_extraction.text import CountVectorizer # [문법] 텍스트 데이터를 단어 횟수 벡터로 변환하는 클래스
from sklearn.naive_bayes import MultinomialNB # [문법] 다항 분포 나이브 베이즈 모델 클래스
import pandas as pd

# [추천] 한국어 텍스트의 경우 KoNLPy(Okt, Mecab 등) 형태소 분석기를 사용하여 토큰화한 후 벡터화하는 것이 정확도 향상에 유리함.
# [추천] 대용량 데이터 처리 시에는 CountVectorizer 대신 TF-IDF(TfidfVectorizer)를 사용하는 것이 단어의 중요도를 더 잘 반영할 수 있음.

# 학습용 데이터 (말뭉치)
texts = [
    '광고성 메일을 확인하세요', 
    '회의 일정 변경 공지', 
    '무료 쿠폰을 지금 사용하세요',
    '중요한 계약 내용을 확인해주세요', 
    '지금 할인 중입니다',
    '오늘 업무 일정 다시 확인해 주세요', 
    '지금 바로 확인하세요', 
    '사내 공지입니다'
]

labels = ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham'] # 종속변수(Label): 스팸(spam)과 정상(ham)

# 단어 등장 횟수 기반 벡터
vect = CountVectorizer() # [문법] CountVectorizer: 단어의 빈도수 정보 추출(순서X), BoW(Bag of Words) 생성
x = vect.fit_transform(texts) # [문법] fit_transform: 말뭉치에서 단어 사전을 만들고 문장을 수치 벡터로 변환

# 모델
model = MultinomialNB() # [문법] MultinomialNB: 텍스트 분류에 최적화된 나이브 베이즈 객체 생성
model.fit(x, labels) # [문법] fit: 벡터화된 텍스트와 레이블을 사용하여 모델 학습 수행

# Streamlit UI
import streamlit as st # [문법] streamlit: 웹 대시보드 구성을 위한 라이브러리

st.title('스팸 메일 분류기(나이브 베이즈)') # [문법] title: 웹 페이지의 메인 제목 출력
user_input = st.text_input('이메일 내용을 입력하세요') # [문법] text_input: 사용자로부터 문자열 입력을 받는 위젯

if user_input:
    # [주의] 새로운 데이터 예측 시에는 반드시 학습 시 사용한 Vectorizer의 transform()만 사용해야 함 (fit 금지)
    x_new = vect.transform([user_input]) # [문법] transform: 기존 단어 사전을 기준으로 새로운 문장을 벡터화
    pred = model.predict(x_new)[0] # [문법] predict: 새로운 데이터의 클래스(spam/ham) 결정
    prob = model.predict_proba(x_new)[0] # [문법] predict_proba: 각 클래스에 속할 확률값을 반환 (합계는 1.0)
    spam_prob = prob[model.classes_.tolist().index('spam')] # [문법] model.classes_: 모델이 학습한 클래스 목록에서 'spam' 인덱스 추출
    ham_prob = prob[model.classes_.tolist().index('ham')] # 베이즈 정리에 의해 계산된 정상 메일 사후 확률

    st.write(f'예측 결과 : {pred}') # [문법] write: 텍스트나 데이터프레임 등을 웹에 출력
    st.progress(spam_prob if pred == 'spam' else ham_prob) # [문법] progress: 진행 바(0.0~1.0) 시각화
    st.write(f'스팸 확률 : {spam_prob:.2%}') # 소수점 확률을 퍼센트 형식으로 출력
    st.write(f'정상 확률 : {ham_prob:.2%}')
    print('\n')
    # [추천] 예측 결과에 따라 st.success()나 st.error()를 사용하여 시각적 피드백을 다르게 주는 것이 사용자 경험에 좋음.