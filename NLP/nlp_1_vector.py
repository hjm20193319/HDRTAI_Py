# 자연어 처리는 숫자화, 벡터화해야 한다
# '안녕 반가워' : [0,1,0,1,1,0], [0.12, -0.30, 0.56, 0.23] 처럼 변경해서 작업을 해줘야 함
# [처리의 흐름]
# 문장 → 단어 분리 → 숫자화 → 모델 또는 분석-> 결과 예측
# [방법]
# One-Hot, Word2Vec, CountVectorizer, TfidfVectorizer, BERT, ....



print('<One Hot Encoding>')
# 문자를 0과 1로 바꾸는 방법
datas = ['python', 'lan', 'program', 'computer', 'say']
sorted_datas = sorted(datas)
print('정렬된 결과 : ', sorted_datas)
print('\n')
# 인덱싱, 라벨링
manual_labels=list(range(len(sorted_datas)))
print('인덱싱 : ', manual_labels)
print('\n')


# numpy.eye() 사용
print('<numpy.eye()>')
import numpy as np
onehot_manual = np.eye(len(manual_labels))
print(onehot_manual)
print('\n')


# sklenrn.LabelEncoder 사용
# 정렬을 하고 인코딩을 해줌
print('<sklearn.LabelEncoder>')
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
encoded_labels = encoder.fit_transform(datas)   # 정렬 안된 데이터
print('정렬된 고유 클래스 목록 : ', encoder.classes_)
print('라벨 인코딩된 결과 : ', encoded_labels)
print('\n')
print('디코딩 결과 : ', encoder.inverse_transform(encoded_labels))
#  [3 1 2 0 4] ⇨  ['python' 'lan' 'program' 'computer' 'say']
print('\n')


# sklearn.OneHotEncoder 사용
print('<sklearn.OneHotEncoder>')
from sklearn.preprocessing import OneHotEncoder
sorted_datas_2d = np.array(sorted_datas).reshape(-1, 1)
onehot_encoder = OneHotEncoder(sparse_output=False)     # ndarray 반환
onehot_encoded = onehot_encoder.fit_transform(sorted_datas_2d)
print('One-Hot 인코딩 결과 : \n', onehot_encoded)
print('\n')
# 복원
decodeed_label = onehot_encoder.inverse_transform(onehot_encoded).ravel()
print('복원(디코딩) 결과 : ', decodeed_label)
print('\n')


# pandas.dataFrame 사용
print('<pandas.DataFrame>')
import pandas as pd
df = pd.DataFrame({'datas':sorted_datas})
onehot_df = pd.get_dummies(df, dtype=int)
print(onehot_df)
print(onehot_df.values)
print('\n')



#######################################################################################
# 밀집 벡터
# ↪ 0이 아닌 숫자로 채워진 벡터
# Word2Vec : 주어진 문맥을 바탕으로 특정 단어를 예측하여 벡터로 변환
# ↪ 코사인 유사도로 단어 간 의미 파악
# pip install gensim

from gensim.models import Word2Vec      # 어떤 단어가 어떤 단어들과 자주 등장하는지를 보고 의미를 학습
sentences = [['king', 'queen', 'man', 'woman'], ['apple', 'banana', 'fruit']]
model = Word2Vec(sentences=sentences, vector_size=10, window=2, min_count=1, sg=1)
# 벡터 사이즈를 직접 지정 가능, 문맥 윈도우 크기 - 좌우 몇개를 문맥으로 참고할건지, 단어 빈도수 1 이상이면 작업에 참여, sg-모델 학습 방법 결정
# sg=1 : Skip-Gram - 중심 단어를 이용해 주변 단어를 예측
# sg=0 : CBOW (Continuous Bag Of Words) - 주변 단어를 이용해 중심 단어를 예측
print(model.wv)
print(model.wv['king'])     # 10차원 벡터(임베딩 벡터)가 만들어짐 - 의미를 가지고 있음
print()
print(model.wv.similarity('king', 'queen'))     # 유사도(두 단어간 코사인) 계산 결과 → -0.04264535
# 유사도 : -1 ~ 1 (1에 근사하면 의미가 비슷, 0은 관련 없음, -1은 반대 의미)
print()
print(model.wv.most_similar('apple'))
print('\n')


sentences2 = [['python', 'lan', 'program', 'computer', 'say']]
model2 = Word2Vec(sentences=sentences2, vector_size=50, window=2, min_count=1, sg=1, alpha=0.025)
print('인덱스 사전 : ', model2.wv.key_to_index)
print('keys : ', model2.wv.key_to_index.keys())
print('values : ', model2.wv.key_to_index.values())
print()

vocabs = model2.wv.key_to_index.keys()
wordvec_list = [model2.wv[voca] for voca in vocabs]
# print(wordvec_list[0])
print()

# for word in vocabs:
#     print(word, model2.wv[word])

print(model2.wv.similarity(w1='python', w2='lan'))  # -0.20600513
print()

# 'python'과 가장 유사한 단어 2개 얻기
print(model2.wv.most_similar('python', topn=2)) # [('program', 0.16563551127910614), ('computer', 0.12486253678798676)]
print()
print(np.degrees(np.arccos(0.1656355)))   # 80.4658454
print('\n')


#######################################################################################
# 시각화
import matplotlib.pyplot as plt

def plotFunc(vocabs, x, y):
    plt.figure(figsize=(6, 5))
    plt.scatter(x, y)
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(x[i], y[i]))



# 주성분 분석으로 차원 축소 PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
xytrans = pca.fit_transform(wordvec_list)
print(xytrans)  # 2차원으로 축소, 원래 의미는 유지
print()

xs = xytrans[:, 0]
ys = xytrans[:, 1]
plotFunc(vocabs, xs, ys)
# plt.show()



#######################################################################################
# 유사도 순으로 정렬하여 텍스트로 가까운 정도 표현
target = 'python'
sim = {w:model2.wv.similarity(w1=target, w2=w) for w in vocabs if w != target}
sorted_sim = sorted(sim.items(), key=lambda x:x[1], reverse=True)
print(f'{target} 기준 단어별 코사인 유사도\n')
for word, s in sorted_sim:
    bar = '▮' * int((s + 1) * 10)
    print(f'{word:<10}|{bar:20} ({s:.3f})')