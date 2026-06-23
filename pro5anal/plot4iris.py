# iris dataset : 150 행, 3종류(Setosa, Versicolor, Virginica), 4개의 특성(꽃받침/꽃잎의 길이/너비)
# 붓꽃의 품종을 분류하기 위해 사용되는 머신러닝/통계 분야의 대표적인 기초 데이터셋
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline : 매직 명령어(Magic Command). Jupyter Notebook 환경에서 그래프를 별도 창 없이 셀 바로 아래에 출력하도록 설정

#======================
# 데이터 확인
# pd.read_csv(): 외부 CSV 데이터를 읽어와 DataFrame 객체로 생성
iris_data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/iris.csv')

print(iris_data.info())      # 데이터프레임의 구조, 컬럼명, 데이터 타입(Dtype), 결측치 존재 여부 확인
print(iris_data.head(3))     # 상위 3개의 행 출력
print(iris_data.tail(3))     # 하위 3개의 행 출력
print(iris_data.describe())  # 수치형 데이터의 기술 통계량(평균, 표준편차, 사분위수 등) 요약

#======================
# 산점도
# plt.scatter(x, y): 두 변수 간의 관계를 점으로 표시하는 산점도(Scatter Plot) 생성
plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'])
plt.xlabel('Sepal_Length')   # x축 라벨 설정
plt.ylabel('Petal.Length')   # y축 라벨 설정
plt.title('iris data')       # 그래프 제목 설정
plt.show()                   # 현재까지 생성된 그래프 객체를 화면에 출력

print('------------------')
# .unique(): 특정 컬럼에 존재하는 고유한 값(중복 제거)들을 배열 형태로 반환
print(iris_data['Species'].unique())    # 3종류 : ['setosa' 'versicolor' 'virginica']
# print(set(iris_data['Species']))      # 파이썬 기본 set 자료형을 이용해 중복을 제거하는 방법

cols = []       # 꽃의 종류(범주형)에 따라 다른 색상(수치형)을 부여하기 위한 리스트 생성
for s in iris_data['Species']:
    # 각 품종 문자열을 숫자(1, 2, 3)로 매핑하여 색상 코드로 활용
    if s == 'setosa': choice=1
    elif s == 'versicolor': choice=2
    elif s == 'virginica': choice=3
    cols.append(choice)     # 변환된 숫자를 리스트에 추가

#======================
# 색 입혀서 다시 그려보기
# c=cols: 각 점의 색상을 지정. 수치 리스트를 전달하면 matplotlib의 기본 컬러맵에 따라 색이 배정됨
plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'], c=cols)
plt.xlabel('Sepal_Length')
plt.ylabel('Petal.Length')
plt.title('iris data')
plt.show()

#======================
# pandas 의 시각화 기능
# scatter_matrix: 데이터프레임 내의 모든 수치형 변수 쌍에 대한 산점도를 행렬 형태로 그려줌 (상관관계 파악 용이)
from pandas.plotting import scatter_matrix
# .loc[행_슬라이싱, 열_슬라이싱]: 라벨 기반 인덱싱. 특성(Feature) 데이터만 따로 추출
iris_col = iris_data.loc[:, 'Sepal.Length':'Petal.Width']      
# diagonal='kde': 대각선 방향(자기 자신과의 관계)에 히스토그램 대신 커널 밀도 추정(Kernel Density Estimation) 곡선을 그림
scatter_matrix(iris_col, diagonal='kde', c=cols)    
plt.show()

#=====================
# seaborn 을 사용해서 표시
import seaborn as sns
# sns.pairplot(): scatter_matrix보다 세련된 디자인의 산점도 행렬 제공
# hue='Species': 지정한 컬럼의 값을 기준으로 데이터의 색상을 자동으로 구분하고 범례(Legend)를 생성
sns.pairplot(iris_data, hue='Species', height=2)
plt.show()