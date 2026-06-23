# 퍼셉트론(Perceptron) 분류 모델
# [개념] 단층 신경망(Single-Layer Perceptron): 가장 단순한 형태의 신경망 구조로, 선형 분리가 가능한 문제에 사용됨.
# [개념] 작동 원리: 입력값에 가중치(Weight)를 곱하고 편향(Bias)을 더한 뒤, 활성화 함수를 통해 출력값을 결정함.
# [개념] 학습 알고리즘: 예측값과 실제값의 차이를 바탕으로 가중치를 반복적으로 갱신함 (틀린 샘플에 대해서만 가중치 조정 - Heaviside step function 기반).

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # 데이터를 학습용과 검증용으로 나누기 위한 모듈
from sklearn.metrics import accuracy_score # 모델의 분류 정확도를 측정하기 위한 함수
from sklearn.preprocessing import StandardScaler    # 표준화
from sklearn.datasets import load_iris

iris = load_iris()
print(iris.keys()) # [문법] 데이터셋의 구성 요소(data, target, target_names 등) 확인
print(iris.target) # [개념] 종속변수(Label): 0(Setosa), 1(Versicolor), 2(Virginica) - 모델이 맞추어야 할 정답
print(iris.data[:3]) # [문법] 독립변수(Feature) 상위 3개 행 확인 - 꽃받침과 꽃잎의 길이/너비 정보
print('\n')
# [문법] np.corrcoef(): 피어슨 상관계수를 계산하여 변수 간 선형 관계의 강도를 확인.
print(np.corrcoef(iris.data[:,2], iris.data[:,3])[0,1])  # 0.96286543 (꽃잎 길이와 너비 사이의 매우 높은 상관관계)
print('\n')

# [개념] 꽃잎의 길이(petal length)와 너비(petal width) 두 개의 특징만 추출하여 학습에 사용.
x = iris.data[:, [2, 3]]
y = iris.target
print(x.shape, ' ', y.shape)
# (150, 2)   (150,)
print('\n')
# [문법] set(map(int, y)): 중복을 제거하여 고유한 클래스 종류를 확인. (0, 1, 2 세 종류 확인)
print(x[:3], y[:3], set(map(int, y)))
print('\n')

# [문법] train_test_split: 데이터를 학습용(70%)과 검증용(30%)으로 분리. random_state는 결과 재현을 위한 시드값.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
# (105, 2) (45, 2) (105,) (45,)
print('\n')
print(x_train[:3], y_train[:3])
print('\n')

######################################
# 분류 모델 생성
# [문법] Perceptron: 사이킷런에서 제공하는 퍼셉트론 분류기. max_iter(학습 횟수), eta0(학습률) 등을 설정.
from sklearn.linear_model import Perceptron
model = Perceptron(max_iter=100, eta0=0.1, random_state=0)

# [문법] fit(): 학습 데이터를 사용하여 최적의 가중치(W)와 절편(b)을 학습함.
model.fit(x_train, y_train) 

# 분류 예측
# [문법] predict(): 학습된 가중치를 바탕으로 새로운 데이터의 클래스(0, 1, 2)를 예측함.
y_pred = model.predict(x_test)
print('예측값 : ', y_pred)
print('실제값 : ', y_test)
print('\n')

# [문법] (y_test != y_pred).sum(): 실제값과 예측값이 일치하지 않는 샘플의 개수를 합산함.
print(f'총 개수 : {len(y_test)}, 오류수 : {(y_test != y_pred).sum()}')
# test data 총 개수 : 45, 오류수 : 2
print('\n')

# 분류 정확도 확인 1
# [문법] accuracy_score(y_true, y_pred): 전체 샘플 중 맞게 예측한 비율을 계산함. (정답수 / 전체수)
print(f'분류 정확도 는 {accuracy_score(y_test, y_pred)}')
# 분류 정확도 는 0.9777777777777777
print('\n')

# 분류 정확도 확인 3
# [문법] model.score(): 내부적으로 predict를 수행한 후 정확도(Accuracy)를 반환함. (편의 기능)
print('test score : ', model.score(x_test, y_test))
print('train score : ', model.score(x_train, y_train))
# [개념] test score 와 train score의 차이가 크다면 과적합(Overfitting)을 의심해야 함.
# [추천] classification_report를 사용하여 클래스별 정밀도, 재현율, F1-score를 확인하는 것을 권장함.
print('\n')

################################################################
# 학습 후 검증이 된 모델을 저장 후 읽기
import joblib
joblib.dump(model, 'perceptron_model.pkl')     # 학습된 모델 객체를 파일로 저장 (확장자는 pkl, model 등 사용 가능)
del model
read_model = joblib.load('perceptron_model.pkl') # 저장된 모델 파일을 읽어와 객체로 복원

# 이 후에는 read_model 사용

# 새로운 값으로 예측하기
new_data = np.array([[5.5, 2.2], [0.6, 0.3], [1.1, 0.5]])
# [주의!] 만약 표준화 된 자료로 모델을 생성했다면, new_data도 표준화 해야 함
# sc.fit(new_data)
# new_data = sc.transform(new_data)

# [주의] Perceptron은 기본적으로 확률(predict_proba)을 제공하지 않음 (필요 시 SGDClassifier 사용 권장)
# print(read_model.predict_proba(new_data))
print('\n')
# 각 클래스별 확률값 중 가장 높은 확률을 가진 인덱스를 반환함 (0, 1, 2 중 하나)
new_pred = read_model.predict(new_data)
print('예측결과 : ', new_pred)

# 시각화
# iris dataset 분류 연습용 시각화 코드
import matplotlib.pyplot as plt

############################################
# 모델 파라미터 확인
# [개념] coef_: 각 클래스별 피처에 할당된 가중치(Weight) 행렬.
print('가중치(coef_) : \n', read_model.coef_)
print('절편(intercept_) : \n', read_model.intercept_)
############################################

import koreanize_matplotlib
from matplotlib.colors import ListedColormap

def plot_decision_regionFunc(X, y, classifier, test_idx=None, resolution=0.02, title=''):
    markers = ('s', 'x', 'o', '^', 'v')      # 마커 표시 모양 5개 정의
    colors = ('r', 'b', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    #print('cmap : ', cmap.colors[0], cmap.colors[1], cmap.colors[2])

    # decision surface 그리기: 모델이 분류하는 영역을 시각적으로 표현하기 위한 격자 생성
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))

    # xx, yy를 1차원 배열로 만든 후(ravel) 예측값을 계산하여 Z에 저장
    Z = classifier.predict(np.array([xx.ravel(), yy.ravel()]).T)
    Z = Z.reshape(xx.shape)   # Z를 reshape()을 이용해 원래 배열 모양으로 복원한다.

    # X를 xx, yy가 축인 그래프 상에 cmap을 이용해 등고선을 그림
    plt.contourf(xx, yy, Z, alpha=0.5, cmap=cmap)   
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    X_test = X[test_idx, :]
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], color=cmap(idx), marker=markers[idx], label=cl)

    # 테스트 데이터셋을 별도의 마커로 표시
    if test_idx:
        X_test = X[test_idx, :]
        plt.scatter(X_test[:, 0], X_test[:, 1], c=[], linewidth=1, marker='o', s=80, label='testset')

    plt.xlabel('꽃잎 길이') # x축 레이블 설정
    plt.ylabel('꽃잎 너비') # y축 레이블 설정
    plt.legend(loc=2) # 범례 표시 (좌측 상단)
    plt.title(title)
    plt.show()

x_combined_std = np.vstack((x_train, x_test))
y_combined = np.hstack((y_train, y_test))
plot_decision_regionFunc(X=x_combined_std, y=y_combined, classifier=read_model, test_idx=range(105, 150), title='scikit-learn제공') 
