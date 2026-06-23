# 쇼핑몰 고객 리뷰 데이터 분석 - CountVectorizer / TfidfVectorizer 사용

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CountVectorizer - 단어의 등장 횟수를 벡터로 변환
# TfidfVectorizer - 단어의 중요도를 계산해 벡터로 변환

reviews = [
    "배송이 빠르고 포장이 깔끔해서 만족했습니다",
    "상품 품질은 좋았지만 가격이 조금 비쌌습니다",
    "주문한 색상과 다른 제품이 도착했습니다",
    "고객센터 응답이 늦어서 불편했습니다",
    "교환 처리가 빠르게 진행되어 만족했습니다",
    "앱에서 결제가 자꾸 실패해서 주문을 못 했습니다",
    "재구매하고 싶을 만큼 제품이 마음에 들었습니다",
    "배송이 지연되어 선물 날짜를 맞추지 못했습니다",
    "환불 처리가 너무 오래 걸려서 불만족스러웠습니다",
    "제품 설명과 실제 상품이 달라서 실망했습니다",
    "쿠폰 적용이 되지 않아 결제 금액이 다르게 나왔습니다",
    "포장이 훼손되어 상품 일부가 파손된 상태로 도착했습니다",  
    "고객센터 상담원이 친절하게 문제를 해결해 주었습니다",
    "반품 신청 과정이 복잡해서 이용하기 어려웠습니다",
    "상품 품질이 좋아서 다음에도 다시 구매하고 싶습니다"
]

review_df = pd.DataFrame({
    'review_id':range(1, len(reviews)+1),
    'review_text':reviews
})

#######################################################################################
# CountVectorizer 사용
count_vectorizer = CountVectorizer()
# 리뷰 문장을 학습하고 단어 등장 횟수 벡터로 변환
count_matrix = count_vectorizer.fit_transform(review_df['review_text'])
# print(count_matrix)
count_words = count_vectorizer.get_feature_names_out()
# print(count_words)

count_df = pd.DataFrame(
    count_matrix.toarray(),
    columns=count_words
)

# 원본 리뷰 정보와 단어 등장 횟수를 옆으로 합치기
count_result_df = pd.concat(
    [review_df[["review_id", "review_text"]], count_df],
    axis=1
)
# print(count_result_df)    # 각 리뷰별 단어 등장 횟수 출력



#######################################################################################
# TfidfVectorizer 사용
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(review_df['review_text'])
tfidf_words = tfidf_vectorizer.get_feature_names_out()

tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=tfidf_words
)
# print(tfidf_df.head(3))

# 원본 리뷰정보와 단어 등장 횟수를 옆으로 합치기
tfidf_result_df = pd.concat(
    [review_df[["review_id", "review_text"]], tfidf_df],
    axis=1
)


#######################################################################################
# CountVectorizer 와 TfidfVectorizer 의 차이 확인
target_word = '배송이'      # 비교 기준 단어

if target_word in count_df.columns:
    compare_df = pd.DataFrame({
        "review_id": review_df["review_id"],
        "review_text": review_df["review_text"],
        "CountVectorizer": count_df[target_word],
        "TfidfVectorizer": tfidf_df[target_word].round(3)
    })

    print(f'<{target_word}의 단어 비교>')
    print(compare_df)

else:
    print(f'{target_word} 단어가 단어 목록에 없어요')

print('\n')

#######################################################################################
# 새 리뷰와 기존 리뷰의 유사도 분석
new_review = '배송이 늦고 포장이 파손되어 불편했습니다'

all_reviews = review_df['review_text'].tolist() + [new_review]      # 기존 리뷰 데이터에 새 리뷰 추가
print(all_reviews)
print('\n')

similarity_vectorizer = TfidfVectorizer()   # 유사도 계산에 사용할 객체
similarity_matrix = similarity_vectorizer.fit_transform(all_reviews)
# print(similarity_matrix)

new_review_vector = similarity_matrix[-1]
# print(new_review_vector)

# 새 리뷰와 기존 리뷰들 사이 코사인 유사도 계산
similarities = cosine_similarity(new_review_vector, similarity_matrix[:-1])

similarity_df = pd.DataFrame({
    "review_id": review_df["review_id"],
    "기존리뷰": review_df["review_text"],
    "새리뷰와의 유사도": similarities[0]
})
# print(similarity_df)
similarity_df = similarity_df.sort_values(by="새리뷰와의 유사도", ascending=False)
print(similarity_df)    # 긍정이든 부정이든 일단 관련이 있는 리뷰들 순서대로 출력
print('\n')


#######################################################################################
# 리뷰 카테고리 분류
category_texts = [
    "배송 지연 늦음 도착 포장 파손 훼손",
    "결제 실패 쿠폰 적용 금액 오류 주문 앱",
    "교환 환불 반품 처리 오래 복잡 불편",
    "상품 품질 제품 설명 색상 다름 실망",
    "만족 재구매 친절 해결 마음 좋음"
]

category_names = [
    '배송/포장 문제',
    '결제/주문 문제',
    '교환/환불/반품 문제',
    '상품 품질/정보 문제',
    '만족/재구매'
]

# 실제 리뷰와 카테고리 대표 문장을 하나로 합치기
texts_for_category = review_df['review_text'].tolist() + category_texts
# print(texts_for_category)

category_vectorizer = TfidfVectorizer()
category_matrix = category_vectorizer.fit_transform(texts_for_category)
# print(category_matrix)
review_vectors = category_matrix[:len(review_df)]
category_vectors = category_matrix[len(review_df):]

category_similarity = cosine_similarity(review_vectors, category_vectors)
# print(category_similarity)

classification_result = []  # 리뷰별 분류 결과를 저장

for i, review in enumerate(review_df['review_text']):
    # 현재 리뷰와 유사도가 가장 높은 카테고리 번호 찾기
    best_category_index = category_similarity[i].argmax()
    best_score = category_similarity[i][best_category_index]
    classification_result.append({
        'review_id': review_df['review_id'][i],
        'review_text': review,
        '분류결과': category_names[best_category_index],
        '유사도': round(best_score, 3)
    })

classification_df = pd.DataFrame(classification_result)
print('<카테고리별 리뷰 분류 결과>')
print(classification_df)
print('\n')


# 카테고리별 리뷰 개수 집계
print('<카테고리별 리뷰 개수 집계>')
category_count_df = classification_df['분류결과'].value_counts().reset_index()
category_count_df.columns = ['카테고리', '리뷰개수']
print(category_count_df)
print('\n')
# 15개 리뷰를 카테고리별로 나눠졌다


#######################################################################################
# 리뷰별 핵심 키워드 추출
# 하나의 리뷰에서 TF-IDF 점수가 높은 단어 n개를 추출하는 함수
def get_top_keywords(row, feature_names, top_n=3):
    word_score_list = []
    # 단어 목록과 해당 리뷰의 TF-IDF 점수를 묶어서 반복
    for word, score in zip(feature_names, row):
        if score > 0:
            word_score_list.append((word, score))

    word_score_list = sorted(
        word_score_list,
        key=lambda x: x[1],
        reverse=True
    )

    top_keywords = [word for word, score in word_score_list[:top_n]]
    return ', '.join(top_keywords)

keyword_results = []   # 리뷰별 핵심 키워드 결과 저장용
for i in range(tfidf_df.shape[0]):  # tfidf 결과의 행 수 만큼 반복
    keywords = get_top_keywords(
        tfidf_df.iloc[i],   # i 번째 리뷰의 tfidf 점수 행
        tfidf_words,        # tfidf 단어 목록 (컬럼명)
        top_n=3             # 추출할 키워드 개수 (상위 3개)
    )
    # print(keywords)
    keyword_results.append({
        'review_id': review_df.loc[i, "review_id"],
        'review_text': review_df['review_text'][i],
        '핵심키워드': keywords
    })

keyword_df = pd.DataFrame(keyword_results)
print('<리뷰별 핵심 키워드>')
print(keyword_df)
print('\n')


#######################################################################################
# 전체 단어 중 중요도 Top 10 - 어떤 단어가 중요한지?
word_total_scores = tfidf_df.sum(axis=0)    # 열단위 합계, 점수를 모두 합산

top_words_df = pd.DataFrame({
    '단어': word_total_scores.index,
    '중요도': word_total_scores
})
print('<전체 단어 중 중요도 Top 10>')
print(top_words_df.sort_values(by='중요도', ascending=False)['중요도'].head(10))
print('\n')



#######################################################################################
# 최종 보고서
final_report_df = classification_df.merge(
    keyword_df[['review_id', '핵심키워드']],
    on='review_id'
)
print('<최종 보고서>')
print(final_report_df)