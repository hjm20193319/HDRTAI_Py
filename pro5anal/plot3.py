# seaborn 라이브러리 : matplotlib의 기능 보충용 라이브러리
# - Matplotlib을 기반으로 하며, 더 세련된 디자인과 통계용 시각화 기능을 제공함
# - Pandas DataFrame과 연동이 매우 강력하여 데이터 분석 시 필수적으로 사용됨
# - 테마, 통계형 차트(분포, 관계, 회귀 등)에 대한 고수준 인터페이스를 제공함

import matplotlib.pyplot as plt
import seaborn as sns       # 시각화 라이브러리
import numpy as np
import pandas as pd
import koreanize_matplotlib # 한글 폰트 설정을 자동으로 처리해주는 라이브러리

# 타이타닉 데이터를 사용해서 처리하기
# sns.load_dataset(): 온라인 저장소에서 연습용 데이터셋(CSV 형태)을 DataFrame으로 로드함
titanic = sns.load_dataset('titanic') 
print(titanic.head())
print(titanic.info())       # 데이터 구조, 결측치(Non-Null), 데이터 타입 확인
print(titanic.describe())   # 수치형 데이터의 기술 통계량(평균, 표준편차, 사분위수 등) 확인
print()

# sns.displot(): 데이터의 분포(Distribution)를 시각화 (히스토그램 + 밀도 추정선 등)
sns.displot(titanic['age']) 
plt.title('나이 차트')
plt.show()

# sns.boxplot(): 사분위수를 시각화하여 데이터의 분포와 이상치(Outlier)를 파악
# palette: 색상 테마 설정 ('Paired', 'Set1', 'husl' 등)
sns.boxplot(x='class', y='age', data=titanic, palette='Paired')
plt.show()

# sns.barplot(): 카테고리별 평균값(기본값)을 막대로 표시하고, 오차 막대(Error Bar)를 함께 출력
# hue: 특정 컬럼을 기준으로 데이터를 한 번 더 그룹화하여 색상으로 구분
sns.barplot(x='sex', y='survived', hue='class', data=titanic)
plt.show()

# sns.countplot(): 각 카테고리별 데이터의 개수(빈도)를 막대 그래프로 표시
sns.countplot(x='class', hue='who', data=titanic)
plt.show()

# sns.relplot(): 두 변수 간의 관계(Relationship)를 시각화 (기본값 kind='scatter')
sns.relplot(x='who', y='age', data=titanic)
plt.show()
# kind='line': 산점도 대신 선 그래프로 관계를 표현
sns.relplot(x='who', y='age', data=titanic, kind='line')
plt.show()

# pivot_table: 데이터를 재구조화하여 행(index)과 열(columns)의 교차 빈도나 통계량을 계산
# aggfunc='size': 데이터의 개수를 카운트
titanic_pivot = titanic.pivot_table(index='class', columns='sex', aggfunc='size')
print(titanic_pivot)

# sns.heatmap(): 2차원 숫자 데이터를 색상으로 시각화
# cmap: 컬러 맵 설정, annot=True: 셀 안에 실제 수치 표시, fmt='d': 정수 형식(Decimal)으로 출력
sns.heatmap(titanic_pivot, cmap=sns.light_palette('gray'), annot=True, fmt='d')      # 밀도를 색으로 표시 (Heatmap)
plt.show()

#========================================================================
# 박스 플롯 이상치 분석하기
#========================================================================
# 1. 데이터 정의
data = [10, 12, 13, 15, 14, 12, 11, 100] # 100은 다른 값들에 비해 매우 큰 이상치 후보
df = pd.DataFrame({'score': data})

# 2. IQR 기반 이상치 탐지
# IQR(Interquartile Range): 3사분위수(Q3) - 1사분위수(Q1)
Q1 = df['score'].quantile(0.25) # 하위 25% 지점
Q3 = df['score'].quantile(0.75) # 상위 25% 지점
IQR = Q3 - Q1                   # 데이터의 중간 50%가 분포하는 범위

# 이상치 경계값 계산 (Tukey's Fences 방식)
# 보통 IQR의 1.5배를 넘어서는 지점을 이상치로 간주함
lower_bound = Q1 - 1.5 * IQR    # 하한선
upper_bound = Q3 + 1.5 * IQR    # 상한선

# 3. 이상치, 정상치 분리
# 불리언 인덱싱을 사용하여 조건에 맞는 행만 추출
outliers = df[(df['score'] < lower_bound) | (df['score'] > upper_bound)]
filtered_df = df[(df['score'] >= lower_bound) & (df['score'] <= upper_bound)]

# 4. 이상치 출력
print("이상치 값:")
print(outliers)

# 5. 박스플롯 시각화: 제거 전/후 비교
# plt.subplots(행, 열): 여러 개의 그래프를 하나의 Figure에 배치
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 이상치 포함
# ax=axes[0]: 첫 번째 서브플롯 영역에 그림
sns.boxplot(y=df['score'], ax=axes[0], color='salmon') 
axes[0].set_title('이상치 포함 데이터')
axes[0].set_ylabel('Score')
axes[0].grid(True)

# 이상치 제거 후
sns.boxplot(y=filtered_df['score'], ax=axes[1], color='lightblue')
axes[1].set_title('이상치 제거 후')
axes[1].set_ylabel('Score')
axes[1].grid(True)

plt.tight_layout() # 서브플롯 간의 겹침을 방지하기 위해 여백 자동 조정
plt.show()