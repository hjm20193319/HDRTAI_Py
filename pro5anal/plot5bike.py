# 자전거 공유 시스템 분석용
#  : kaggle 사이트의 Bike Sharing in Washington D.C. Dataset를 편의상 조금 변경한 dataset을 사용함

# columns : 
#  'datetime', 
#  'season'(사계절:1,2,3,4), 
#  'holiday'(공휴일(1)과 평일(0)), 
#  'workingday'(근무일(1)과 비근무일(0)), 
#  'weather'(4종류:Clear(1), Mist(2), Snow or Rain(3), Heavy Rain(4)), 
#  'temp'(섭씨온도), 'atemp'(체감온도), 
#  'humidity'(습도), 'windspeed'(풍속), 
#  'casual'(비회원 대여량), 'registered'(회원 대여량), 
#  'count'(총대여량)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import koreanize_matplotlib

# plt.style.use(): 그래프의 전체적인 디자인 테마(배경색, 격자 스타일 등)를 설정함
plt.style.use('ggplot')     # ggplot style 사용 

#================================
# EDA : 탐색적 분석 / 데이터 로드, 확인
# parse_dates: 특정 컬럼을 문자열이 아닌 datetime64 객체로 변환하여 읽어옴 (날짜 연산 가능)
train = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv', parse_dates=['datetime'])   # object타입이 아니고 dates 타입으로 파싱 지정

# pd.set_option: 데이터프레임 출력 시 생략되는 부분을 방지하기 위해 최대 행/열 표시 제한을 해제
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print(train.info())
print()
print(train.head())
print()
print(train.describe())
print()
print(train.dtypes)     # dtypes: datetime64[ns](1), float64(3), int64(8)
print()
print(train.shape)      # (10886, 12) - (행의 개수, 열의 개수) 반환
print()
print(train.columns)        
# ['datetime', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered', 'count']
print()
print(train.head(3))
print()
print(train.temp.describe())    # 온도 확인(중요한 데이터라고 판단)
print()
# isnull().sum(): 각 컬럼별 결측치(NaN)의 개수를 합산하여 출력
print(train.isnull().sum())

###################################################
# 연/월/일/시분초 별도의 칼럼 추가 생성(기존 칼럼 뒤에 추가)
# .dt 연산자: datetime 시리즈에서 연, 월, 일 등 속성 정보를 추출하는 접근자
train['year'] = train['datetime'].dt.year       # dt 연산자 활용
train['month'] = train['datetime'].dt.month
train['day'] = train['datetime'].dt.day
train['hour'] = train['datetime'].dt.hour
train['minute'] = train['datetime'].dt.minute
train['second'] = train['datetime'].dt.second

print(train.head(1))
print(train.columns)

#####################################################
# 대여량 시각화

# barplot
# plt.subplots(): 여러 개의 그래프를 그리기 위한 Figure(도화지)와 Axes(축) 객체를 생성
figure, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4)
figure.set_size_inches(15, 5)

# sns.barplot: 카테고리별 평균값과 신뢰구간(오차 막대)을 시각화
sns.barplot(data=train, x='year', y='count', ax=ax1)
sns.barplot(data=train, x='month', y='count', ax=ax2)
sns.barplot(data=train, x='day', y='count', ax=ax3)
sns.barplot(data=train, x='hour', y='count', ax=ax4)

# .set(): 축의 라벨, 제목 등 여러 속성을 한 번에 설정하는 메소드
ax1.set(ylabel='대여수', title='연도별 대여수', xlabel='연도')
ax2.set(ylabel='대여수', title='월별 대여수', xlabel='월')
ax3.set(ylabel='대여수', title='일별 대여수', xlabel='일')
ax4.set(ylabel='대여수', title='시간별 대여수', xlabel='시간')

plt.show()

# boxplot
# 박스 플롯: 데이터의 사분위수(Q1, Q2, Q3)와 이상치를 한눈에 파악하기 위한 그래프
fig, exes = plt.subplots(nrows=2, ncols=2)
fig.set_size_inches(12, 10)

# orient='v': 박스 플롯의 방향을 수직(vertical)으로 설정
sns.boxplot(data=train, y='count', ax=exes[0][0], orient='v')
sns.boxplot(data=train, y='count', x='season', ax=exes[0][1], orient='v')
sns.boxplot(data=train, y='count', x='hour', ax=exes[1][0], orient='v')
sns.boxplot(data=train, y='count', x='workingday', ax=exes[1][1], orient='v')

exes[0][0].set(ylabel='대여수', title='대여량')
exes[0][1].set(ylabel='대여수', title='계절별 대여량', xlabel='계절')
exes[1][0].set(ylabel='대여수', title='시간별 대여량', xlabel='시간')
exes[1][1].set(ylabel='대여수', title='근무일에 따른 대여량', xlabel='근무일')

plt.show()

# 산점도 : regplot (온도, 습도, 풍속)
# sns.regplot: 산점도(Scatter plot) 위에 선형 회귀선(Regression line)을 함께 그려 변수 간 상관관계를 보여줌
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)
fig.set_size_inches(12, 5)

sns.regplot(data=train, x='temp', y='count', ax=ax1)
sns.regplot(data=train, x='humidity', y='count', ax=ax2)
sns.regplot(data=train, x='windspeed', y='count', ax=ax3)
plt.show()