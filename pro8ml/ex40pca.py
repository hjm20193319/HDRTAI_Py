# PCA 주성분분석
# [개념] PCA(Principal Component Analysis): 선형 대수 관점에서, 입력 데이터의 공분산 행렬을 고유값 분해하고 
# [개념] 구한 고유벡터에 입력 데이터를 선형 변환하는 것이다.
# [개념] 이 고유벡터가 PCA의 주 성분 벡터로서 입력 데이터의 분산이 큰 방향을 나타낸다.
# [개념] 입력 데이터의 성질을 최대한 유지한 상태로 고차원을 저차원 데이터로 변환하는 기법.

# [개념] iris data로 차원 축소 실습
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.metrics import accuracy_score

# [추천] PCA 수행 전 데이터의 스케일이 다르면 결과가 왜곡될 수 있으므로 StandardScaler를 통한 표준화 전처리를 권장함.

# 데이터
iris = load_iris() # [문법] load_iris(): 사이킷런에서 제공하는 붓꽃 데이터셋 로드.
n = 10
x = iris.data[:n, :2]   # [개념] sepal length, width 열만 선택 (시각화 용도)
print('차원 축소 전 x : \n', x, x.shape, type(x))
print(x.T)

# [문법] 시각화 1 - 각 샘플의 두 특성 값을 선으로 연결해, 패턴 분석
plt.plot(x.T, 'o:')
plt.xticks(range(2), ['꽃받침 길이', '꽃받침 너비'])
plt.grid(True)
plt.legend(['표본 {}'.format(i + 1) for i in range(n)])
plt.title('iris 크기 특성(원본 데이터)')
plt.xlabel('특성 종류')
plt.ylabel('특성 크기')
plt.xlim(-0.5, 2)
plt.ylim(2.5, 6)
plt.tight_layout()
plt.show()
print('\n')

# [문법] 시각화 2 - 산점도, 데이터 분포 확인
df = pd.DataFrame(x, columns=['꽃받침 길이', '꽃받침 너비']) # [문법] pd.DataFrame: 행렬 데이터를 데이터프레임으로 변환.
print(df.head())

ax = sns.scatterplot(x='꽃받침 길이', y='꽃받침 너비', data=df, marker='s', s=100, color='red') # [문법] sns.scatterplot: 산점도 시각화.
# sns.scatterplot(x=df[0], y=df[1], marker='s', s=100, color='red')
plt.title('iris 크기 특성(원본 데이터)')
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃받침 너비')
plt.axis('equal')
plt.grid(True)
plt.tight_layout()
# 각 점에 대해 text 표시
for i in range(n):
    ax.text(x[i, 0] - 0.05, x[i, 1] + 0.03, '표본 {}'.format(i + 1), fontsize=8)
plt.show()
print('\n')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 위 두개의 그래프 결과 두 변수는 공통적인 특징이 있으므로
# 차원 축소의 근거가 있다고 판단
# => PCA를 진행 : 선형 변환을 통해 차원 축소
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# PCA(주성분 분석) 수행 단계 및 논리적 절차
# 1. 데이터의 상관관계 파악: 입력 데이터의 변수 간 상관성을 분석하기 위해 공분산 행렬(Covariance Matrix)을 생성합니다.
# 2. 주성분 후보 추출: 공분산 행렬을 고유값 분해하여, 데이터의 분산 방향을 나타내는 '고유벡터'와 그 크기(정보량)를 나타내는 '고유값'을 계산합니다.
# 3. 정보 중요도에 따른 선택: 고유값이 큰 순서대로(데이터의 변동성을 가장 잘 설명하는 순서) 상위 k개의 고유벡터를 주성분으로 선택합니다.
# 4. 저차원 투영: 선택된 고유벡터를 기저로 삼아 기존 데이터를 선형 변환함으로써, 정보 손실을 최소화하며 차원이 축소된 새로운 공간으로 데이터를 투영합니다.

# sklearn의 PCA클래스 사용하면 순서대로 진행

pca1 = PCA(n_components=1)  # [문법] n_components: 변환할 차원(주성분 개수) 설정.
x_low = pca1.fit_transform(x)   # [문법] fit_transform: 특징 행렬을 낮은 차원의 근사행렬로 변환.
print('x_low : \n', x_low)
print('x_low.shape : ', x_low.shape)    # x_low.shape :  (10, 1)  =>> 차원이 (10, 2)에서 축소 됨
print('\n')
# 주성분 값 원복하기
x2 = pca1.inverse_transform(x_low) # [문법] inverse_transform: 축소된 데이터를 다시 원래 차원으로 복원(정보 손실 발생).
print('원복 후 x2 : \n', x2)    # [개념] 주성분 분석은 원본 데이터를 100% 설명하지 않음.
print('x2.shape : ', x2.shape)
print('\n')

# 주성분 분석값을 기반으로 시각화
# PCA 방향벡터
pc1 = pca1.components_[0]   # [문법] components_: 계산된 주성분 벡터(고유벡터) 반환.
mean = x.mean(axis=0) # [문법] mean(axis=0): 데이터 평균(중심점) 계산.

df = pd.DataFrame(x, columns=['꽃받침 길이', '꽃받침 너비'])
ax = sns.scatterplot(x='꽃받침 길이', y='꽃받침 너비', data=df, marker='s', s=100, color='blue') # [문법] 산점도 시각화.
for i in range(n):
    ax.text(x[i, 0] - 0.05, x[i, 1] + 0.03, '표본 {}'.format(i + 1), fontsize=8)

# PCA 축 (화살표)
plt.quiver(
    mean[0], mean[1],  # 시작점(평균)
    pc1[0], pc1[1],    # 방향
    scale=3, color='r', width=0.01
)
plt.xlabel('꽃받침 길이')
plt.ylabel('꽃받침 너비')
plt.title('iris 특성 + 제 1 주성분')
plt.axis('equal')
plt.grid(True)
plt.tight_layout()
plt.show()
print('\n')

###################################################################################### 
# [개념] 원본 열 4개를 차원축소하여 2개의 열로 변환 후 SVM 분류 모델을 작성

x = iris.data
print(x[0, :])  # [5.1 3.5 1.4 0.2]
print('\n')

pca2 = PCA(n_components=2) # [문법] 4차원 데이터를 2차원으로 축소 설정.
x_low2 = pca2.fit_transform(x) # [문법] 학습 및 변환 수행.
print('x_low2 : \n', x_low2[0, :])  #  [-2.68412563  0.31939725]
print('x_low2.shape : ', x_low2.shape)  # x_low2.shape :  (150, 2)  =>> 4열->2열
print('\n')

# 변동성 비율 확인
print(pca2.explained_variance_ratio_)   # [문법] explained_variance_ratio_: 각 주성분이 설명하는 분산의 비율. 제1주성분(92%), 제2주성분(5%)
print('\n')

# [문법] 원복
x4 = pca2.inverse_transform(x_low2)
print('최초 자료 : ', x[0]) 
print('차원 축소 : ', x_low2[0])
print('차원 복귀 : ', x4[0, :])
# 최초 자료 :  [5.1 3.5 1.4 0.2]
# 차원 축소 :  [-2.68412563  0.31939725]
# 차원 복귀 :  [5.08303897 3.51741393 1.40321372 0.21353169]
print('\n')

iris1 = pd.DataFrame(x, columns=['sepal length', 'sepal width', 'petal length', 'petal width'])
print(iris1.head()) # [문법] 원본 데이터프레임 확인.
print('\n')

iris2 = pd.DataFrame(x_low2, columns=['var1', 'var2'])
print(iris2.head()) # [문법] PCA 변환 데이터프레임 확인.
print('\n')

from sklearn import svm, metrics
feature1 = iris1.values
print(feature1[:3])
label = iris.target
print(label[:3])
print('\n')

feature2 = iris2.values
print(feature2[:3])
print('\n')

# [개념] 원본 데이터로 SVM 분류 모델 작성
model1 = svm.SVC(C=0.1, random_state=0).fit(feature1, label) # [문법] SVC: SVM 분류 모델 생성 및 학습.
pred1 = model1.predict(feature1) # [문법] predict: 클래스 예측.
print('model1 accuracy : ', accuracy_score(label, pred1))   # [문법] accuracy_score: 정확도 계산. model1 accuracy :  0.94
print('\n')

# [개념] PCA 데이터로 SVM 분류 모델 작성
model2 = svm.SVC(C=0.1, random_state=0).fit(feature2, label) # [문법] 차원 축소된 데이터로 학습.
pred2 = model2.predict(feature2) # [문법] 예측 수행.
print('model2 accuracy : ', accuracy_score(label, pred2))   # [문법] 정확도 계산. model2 accuracy :  0.94667
print('\n')