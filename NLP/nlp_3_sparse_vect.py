# 희소 벡터 표현 방식
# 희소 벡터는 대부분의 요c소가 0인 벡터로, 텍스트 데이터에서 단어의 존재 여부를 나타내는 데 사용됩니다.

# CountVectorizer 클래스는 텍스트 데이터를 희소 벡터로 변환하는 데 사용됩니다.
# ↪ 단어 등장 횟수 기반, 정수로 표현
# ↪ 단어가 몇번 나왔는가?

# TfidfVectorizer : 문서에서 자주 나타나는 단어에 가중치르 높게 주되, 모든 문서에서 자주 등장하는 단어에는 낮은 가중치를 주는 방식
# ↪ 단어 등장 횟수 기반, 실수로 표현
# ↪ 그 단어가 문서에서 얼마나 중요한가?

# Word2Vec : 단어를 고차원 공간의 벡터로 표현하는 방법
# ↪ 단어 간의 의미적 유사성을 포착할 수 있음
# ↪ 단어가 어떤 의미적 위치에 있는가?

# CountVectorizer와 TfidfVectorizer는 단어의 존재 여부나 빈도를 기반으로 벡터를 생성하는 반면, Word2Vec은 단어 간의 의미적 관계를 포착하는 벡터를 생성합니다.
# 따라서, CountVectorizer와 TfidfVectorizer는 희소 벡터를 생성하는 반면, Word2Vec은 밀집 벡터를 생성합니다.

#######################################################################################
# CountVectorizer
print('<CountVectorizer>')
print('------------------')

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

content = ['How to format my hard disk', 'Hard disk format format problems']

count_vec = CountVectorizer(analyzer='word', min_df=1)
tran = count_vec.fit_transform(content)
print(tran)
print(count_vec.get_feature_names_out())    
# ['disk' 'format' 'hard' 'how' 'my' 'problems' 'to']
#     0      1        2     3    4      5         6
print(tran.toarray())
# [[1 1 1 1 1 0 1]
#  [1 2 1 0 0 1 0]]


#######################################################################################
# TfidfVectorizer
print('<TfidfVectorizer>')
print('------------------')

tfidf_vec = TfidfVectorizer(analyzer='word', min_df=1)

tran2 = tfidf_vec.fit_transform(content)
print(tran2)
print(tfidf_vec.get_feature_names_out())
print(tran2.toarray())  # 출현 빈도 확률값
# [[0.33471228 0.33471228 0.33471228 0.47042643 0.47042643   0. 0.47042643]
#  [0.35409974 0.70819948 0.35409974     0.    0.    0.49767483        0.   ]]
print('\n')