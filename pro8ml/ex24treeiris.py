# Decision Tree 분류 모델
# [개념] 다항 분류(Multinomial Classification): 종속변수의 범주가 3개 이상인 경우 사용함.
# [개념] Decision Tree: 데이터의 균일도(Gini, Entropy)를 기준으로 규칙 기반의 트리를 생성하여 분류함.
# [추천] max_depth를 조절하여 모델의 복잡도를 제어하고 과적합(Overfitting)을 방지해야 함.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler    # 표준화
from sklearn.datasets import load_iris

iris = load_iris()
print(iris.keys()) # [문법] 데이터셋의 구성 요소(data, target, target_names 등) 확인
print(iris.target) # [개념] 종속변수(Label): 0(Setosa), 1(Versicolor), 2(Virginica)
print(iris.data[:3]) # [문법] 독립변수(Feature) 상위 3개 행 확인
print('\n')
# [문법] np.corrcoef(): 피어슨 상관계수를 계산하여 변수 간 선형 관계의 강도를 확인.
print(np.corrcoef(iris.data[:,2], iris.data[:,3])[0,1])  # 0.96286543
print('\n')

# [개념] 꽃잎의 길이(petal length)와 너비(petal width) 두 개의 특징만 추출하여 학습에 사용.
x = iris.data[:, [2, 3]]
y = iris.target
print(x.shape, ' ', y.shape)
# (150, 2)   (150,)
print('\n')
# [문법] set(map(int, y)): 중복을 제거하여 고유한 클래스 종류를 확인.
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
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(criterion='gini', max_depth=5, random_state=0) # [문법] DecisionTreeClassifier: 의사결정나무 분류 모델 생성.
model.fit(x_train, y_train) # [문법] fit(): 학습 데이터를 사용하여 모델의 파라미터(Weight, Bias)를 최적화함.

# 분류 예측
# [문법] predict(): 학습된 모델을 사용하여 테스트 데이터의 클래스(0, 1, 2)를 예측함.
y_pred = model.predict(x_test)
print('예측값 : ', y_pred)
print('실제값 : ', y_test)
print('\n')

# [문법] (y_test != y_pred).sum(): 실제값과 예측값이 일치하지 않는 샘플의 개수를 합산함.
print(f'총 개수 : {len(y_test)}, 오류수 : {(y_test != y_pred).sum()}')
# test data 총 개수 : 45, 오류수 : 1
print('\n')

# 분류 정확도 확인 1
# [문법] accuracy_score(y_true, y_pred): 전체 샘플 중 맞게 예측한 비율을 계산함.
print(f'분류 정확도 는 {accuracy_score(y_test, y_pred)}')
# 분류 정확도 는 0.9777777777777777
print('\n')

# 분류 정확도 확인 2
# [문법] pd.crosstab(): 혼동 행렬(Confusion Matrix)을 데이터프레임 형태로 생성하여 상세 분류 현황 파악.
con_mat = pd.crosstab(y_test, y_pred, rownames=['예측치'], colnames=['관측치'], margins=True)
print(con_mat)
mat_accuracy = (con_mat[0][0] + con_mat[1][1] + con_mat[2][2]) / len(y_test)
print(f'분류 정확도 는 {mat_accuracy}')
# 분류 정확도 는 0.977777777
print('\n')

# 분류 정확도 확인 3
# [문법] model.score(): 내부적으로 predict를 수행한 후 정확도(Accuracy)를 반환함.
print('test score : ', model.score(x_test, y_test))
print('train score : ', model.score(x_train, y_train))
# [개념] test score 와 train score의 차이가 크다면 과적합(Overfitting)을 의심해야 함.
# [추천] classification_report를 사용하여 클래스별 정밀도, 재현율, F1-score를 확인하는 것을 권장함.
print('\n')

################################################################
# 학습 후 검증이 된 모델을 저장 후 읽기
import joblib   # pickle보다 빠르고 대용량 지원
joblib.dump(model, 'treemodel.pkl')     # sav, model, ...
del model
read_model = joblib.load('treemodel.pkl')

# 이 후에는 read_model 사용

# 새로운 값으로 예측하기
new_data = np.array([[5.5, 2.2], [0.6, 0.3], [1.1, 0.5]])
# [주의!] 만약 표준화 된 자료로 모델을 생성했다면, new_data도 표준화 해야 함
# sc.fit(new_data)
# new_data = sc.transform(new_data)

print(read_model.predict_proba(new_data))
print('\n')
# 각 클래스별 확률값 중 가장 높은 확률을 가진 인덱스를 반환함
new_pred = read_model.predict(new_data)
print('예측결과 : ', new_pred)

# 시각화
# iris dataset 분류 연습용 시각화 코드
import matplotlib.pyplot as plt

import koreanize_matplotlib
from matplotlib.colors import ListedColormap

def plot_decision_regionFunc(X, y, classifier, test_idx=None, resolution=0.02, title=''):
    markers = ('s', 'x', 'o', '^', 'v')      # 마커 표시 모양 5개 정의
    colors = ('r', 'b', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    #print('cmap : ', cmap.colors[0], cmap.colors[1], cmap.colors[2])

    # decision surface 그리기
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    xx, yy = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))

    # xx, yy를 1차원 배열로 만든 후 예측값을 계산하여 Z에 저장
    Z = classifier.predict(np.array([xx.ravel(), yy.ravel()]).T)
    Z = Z.reshape(xx.shape)   # Z를 reshape()을 이용해 원래 배열 모양으로 복원한다.

    # X를 xx, yy가 축인 그래프 상에 cmap을 이용해 등고선을 그림
    plt.contourf(xx, yy, Z, alpha=0.5, cmap=cmap)   
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    X_test = X[test_idx, :]
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], color=cmap(idx), marker=markers[idx], label=cl)

    if test_idx:
        X_test = X[test_idx, :]
        plt.scatter(X_test[:, 0], X_test[:, 1], c=[], linewidth=1, marker='o', s=80, label='testset')

    plt.xlabel('꽃잎 길이')
    plt.ylabel('꽃잎 너비')
    plt.legend(loc=2)
    plt.title(title)
    plt.show()

x_combined_std = np.vstack((x_train, x_test))
y_combined = np.hstack((y_train, y_test))
plot_decision_regionFunc(X=x_combined_std, y=y_combined, classifier=read_model, test_idx=range(105, 150), title='scikit-learn제공') 
