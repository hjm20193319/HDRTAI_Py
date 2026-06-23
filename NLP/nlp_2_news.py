# 뉴스 정보를 읽어 텍스트 파일로 저장 후 유사도 확인
# 형태소 분석, Word2Vec, 유사도 분석 ...

# pip install konlpy
import pandas as pd
from konlpy.tag import Okt

okt = Okt()

with open('news.txt', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

# print(lines)

word_freq = {}  # 명사만 추출해 기억
for line in lines:
    nouns = [word for word, tag in okt.pos(line) if tag == 'Noun' and len(word) > 1]
    # print(nouns)
    for noun in nouns:
        word_freq[noun] = word_freq.get(noun, 0) + 1
# print(word_freq)


# 단어 건수별 내림차순 정렬해 DataFrame에 저장
sortData = sorted(word_freq.items(), key=lambda dul:(-dul[1], dul[0]))
# print(sortData)
df = pd.DataFrame(sortData, columns=['단어', '빈도수'])
print(df)   # [218 rows x 2 columns]
#        단어  빈도수
# 0      후보   25
# 1      재판   10
# 2      혐의   10
# 3      선거    8
# 4      위반    8
# ..    ...  ...
# 213    허위    1
# 214    헌법    1
# 215    현재    1
# 216    형량    1
# 217  형사재판  1

# df → csv 파일로 저장
df.to_csv('nlp2word.csv', index=False, encoding='utf-8-sig')
df = pd.read_csv('nlp2word.csv')
print(df.head())



#######################################################################################
# 유사도 확인
# 원본 파일에서 명사, 동사 추출

with open('nlp2word_freq.txt', 'w', encoding='utf-8') as fi:
    for line in lines:
        tokens = okt.pos(line, stem=True)   # stem=True 원형으로 출력
        words = [word for word, tag in tokens if tag in ['Noun', 'Verb'] and len(word) > 1]   # 명사와 동사
        if words:
            fi.write(' '.join(words) + '\n')


from gensim.models import word2vec

# LineSentence : 텍스트를 한줄씩 읽어 단어 리스트로 변환 txt 파일 처리할 때 많이 사용
sentences = word2vec.LineSentence('nlp2word_freq.txt')
# print(sentences)

model = word2vec.Word2Vec(sentences=sentences, vector_size=100, window=10, min_count=1, sg=1)
print(model)    # Word2Vec<vocab=245, vector_size=100, alpha=0.025>

# 학습된 모델 저장
model.save('nlp2model.model')

# 저장된 모델 읽기
model = word2vec.Word2Vec.load('nlp2model.model')
print(model.wv.index_to_key[:5])
print('혐의' in model.wv.key_to_index)
print()

print('혐의와 유사한 단어 출력')
print(model.wv.most_similar('혐의'))
print('\n')

# 두 단어의 벡터를 더한 결과에 가장 가까운 단어
print(model.wv.most_similar(positive=['혐의', '재판']))
print('\n')



#######################################################################################
# 시각화 - 유사도 기반 단어간 관계
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.decomposition import PCA
import platform     # 환경정보 확인용

target_word = '재판'

similar_words = model.wv.most_similar(target_word, topn=10)
print(similar_words)
print('\n')

# 단어 리스트 작성(유사도 숫자 빼고)
words = [target_word] + [word for word, _ in similar_words]
print(words)    # ['재판', '하다', '당선', '돼다', '출석', '확정'....]
print('\n')

# 단어 벡터 추출
word_vectors = [model.wv[word] for word in words]
# print(word_vectors[0])
print('\n')

# 차원 축소
pca = PCA(n_components=2)
points = pca.fit_transform(word_vectors)
print(points[0])
print('\n')

# 시각화
plt.figure(figsize=(15, 15))
for i, word in enumerate(words):
    x, y = points[i]
    plt.scatter(x, y, color='blue' if i == 0 else 'black')
    plt.text(x, y, word, fontsize=10, color='red' if i == 0 else 'black')

plt.title(f'Word2Vec 유사 단어 시각화 (기준단어:{target_word})')
plt.grid(True)
plt.show()



#######################################################################################
# 단어들을 의미적으로 군집화
from sklearn.cluster import KMeans

filtered_words = [word for word in words if word in model.wv.key_to_index]
print(filtered_words)
print('\n')
vectors = [model.wv[word] for word in filtered_words]

# KMenas 클러스터링
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit_predict(vectors)

# PCA 차원 축소
pca = PCA(n_components=2)
reduced_vectors = pca.fit_transform(vectors)
centers = pca.transform(kmeans.cluster_centers_)

colors = ['red', 'green', 'blue','orange', 'purple']

plt.figure(figsize=(15, 15))

for i, word in enumerate(filtered_words):
    x, y = reduced_vectors[i]
    plt.scatter(x, y, color=colors[kmeans.labels_[i] % len(colors)], label=f'Cluster {kmeans.labels_[i]}', edgecolor='black')
    plt.text(x, y, word, fontsize=10)

# 클러스터 중심점 표시
for i, center in enumerate(centers):
    plt.scatter(center[0], center[1], color=colors[i], marker='x', s=200, linewidths=3)

plt.title('Word2Vec 단어 군집화 시각화')
plt.grid(True)
plt.legend(title='클러스터', loc='upper right')
plt.tight_layout()
plt.show()


# 군집별 단어 리스트 출력
from collections import defaultdict

cluster_dict = defaultdict(list)
for word, label in zip(filtered_words, kmeans.labels_):
    cluster_dict[label].append(word)

print("클러스터별 단어 리스트:")
for cluster_id, words in cluster_dict.items():
    print(f"Cluster {cluster_id}: {', '.join(words)}")


# 계층적 군집 분석 - 덴드로그램
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
vectors = np.array([model.wv[word] for word in filtered_words])

linkege_matrix = linkage(vectors, method='ward')

plt.figure(figsize=(12, 6))
dendrogram(linkege_matrix, labels=filtered_words, leaf_rotation=90)
plt.title('Word2Vec 단어 계층적 군집 분석')
plt.xlabel('단어')
plt.ylabel('유클리드 거리')
plt.tight_layout()
plt.show()