# 스팸 메일 분류기 - spam 자료를 파일에서 읽기
# MultinomialNB: 단어의 출현 빈도와 같은 이산적인 특징 데이터를 분류하는 데 적합한 알고리즘.
# 베이즈 정리를 기반으로 하며, 모든 특성이 독립적이라는 가정하에 클래스 확률을 계산함.

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 로드
# [문법] pd.read_csv: 온라인상의 CSV 파일을 데이터프레임으로 로드.
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/fa236a226b6cf7ff7f61850d14f087ade1c437be/testdata_utf8/mydata.csv')
print(df.head())
print(df.info()) # [문법] 데이터프레임의 요약 정보(결측치, 데이터 타입 등) 확인.
print('\n')

# label 분리
# [문법] str.strip().str.lower(): 레이블 데이터의 앞뒤 공백을 제거하고 소문자로 통일하여 전처리.
df['label']=df['label'].str.strip().str.lower()     
texts = df['text'].tolist() # [문법] tolist: 시리즈 데이터를 리스트 형태로 변환.
label = df['label'].tolist() 
print(texts[:3])
print(label[:3])
print('\n')

# test train 분리
# [문법] train_test_split: 데이터를 학습용(75%)과 테스트용(25%)으로 분리. stratify=label로 클래스 비율 유지.
x_train, x_test, y_train, y_test = train_test_split(texts, label, test_size=0.25, random_state=42, stratify=label)

# 단어 등장 횟수 기반 벡터
# [문법] CountVectorizer: 텍스트를 단어 빈도수 기반의 수치 벡터(BoW)로 변환하는 클래스.
vectorizer = CountVectorizer() 
x_train_vec = vectorizer.fit_transform(x_train) # [문법] fit_transform: 학습 데이터로 단어 사전을 만들고 벡터화 수행.
x_test_vec = vectorizer.transform(x_test)   # test는 transform만 해줘야 함 -> 숫자 변환만 (학습 시 생성된 사전 기준)

# 모델
# [문법] MultinomialNB: 텍스트 분류에 최적화된 다항 분포 나이브 베이즈 모델 생성.
model = MultinomialNB() 
model.fit(x_train_vec, y_train) # [문법] fit: 벡터화된 텍스트와 레이블을 사용하여 모델 학습.

# 예측
# [문법] predict: 테스트 데이터를 입력하여 스팸 여부(spam/ham)를 예측.
y_pred = model.predict(x_test_vec) 
print('예측값 : ', y_pred[:10])
print('실제값 : ', y_test[:10])
print('\n')
print('분류 정확도 : ', accuracy_score(y_test, y_pred)) # [문법] accuracy_score: 전체 중 맞춘 비율 계산.
print('\n')

# Confusion Matrix 시각화
from sklearn.metrics import ConfusionMatrixDisplay

print('혼동 행렬 : \n', confusion_matrix(y_test, y_pred)) # [문법] confusion_matrix: 상세 분류 현황(TP, FP, FN, TN) 확인.
print('\n')

# [문법] ConfusionMatrixDisplay: 혼동 행렬을 시각적으로 표현하는 클래스.
disp = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred), display_labels=model.classes_) 
disp.plot(cmap=plt.cm.Blues) # [문법] plot: 파란색 계열의 색상 지도를 사용하여 차트 출력.
plt.tight_layout
plt.title('Confusion Matrix')
plt.show()
print('\n')

# 사용자 입력 메일 내용 분류
while True:
    userInput = input('이메일 내용 입력(종료는 q) : ')
    if userInput.lower() == 'q':
        break
    x_new = vectorizer.transform([userInput])
    # [문법] predict_proba: 각 클래스(ham, spam)에 속할 확률을 반환.
    prob = model.predict_proba(x_new)[0] 
    # [문법] model.classes_.tolist().index('spam'): 'spam' 클래스의 인덱스 번호를 찾아 해당 확률 추출.
    spam_prob = prob[model.classes_.tolist().index('spam')] 

    # [추천] 한국어 텍스트의 경우 KoNLPy(Okt, Mecab 등) 형태소 분석기를 사용하여 토큰화한 후 벡터화하는 것이 정확도 향상에 유리함.
    result = '스팸' if spam_prob > 0.7 else '정상'
    print(f'스팸 확률은 {spam_prob:.2f} -> {result}')