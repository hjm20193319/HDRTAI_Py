# [개념] SVM(Support Vector Machine): 데이터들 사이의 거리를 최대화하는 결정 경계(Hyperplane)를 찾아 분류하는 알고리즘.
# [개념] 서포트 벡터(Support Vector): 결정 경계와 가장 가까이 있는 데이터 포인트들로, 경계를 정의하는 핵심 요소임.
# [추천] 데이터의 스케일에 민감하므로 특성 간 단위 차이가 크다면 StandardScaler를 통한 표준화 전처리를 권장함.

from sklearn.datasets import make_blobs
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np

plt.rc('font', family='malgun gothic') # [문법] plt.rc: 그래프 내 한글 깨짐 방지를 위한 폰트 설정.

# 1. 학습용 데이터 생성 및 시각화
# [문법] make_blobs: 가우시안 정규분포를 따르는 가상 데이터를 생성하는 함수.
X, y = make_blobs(n_samples=50, centers=2, cluster_std=0.5, random_state=4) 
y = 2 * y - 1  # [개념] 레이블을 -1과 1로 변환 (SVM의 수학적 최적화 식에서 주로 사용되는 형태)

plt.scatter(X[y == -1, 0], X[y == -1, 1], marker='o', label="-1 클래스")
plt.scatter(X[y == +1, 0], X[y == +1, 1], marker='x', label="+1 클래스")
plt.xlabel("x1")
plt.ylabel("x2")
plt.legend()
plt.title("학습용 데이터")
plt.show()

# 2. SVM 모델 학습 (선형 커널)
# C(tuning parameter) 값을 변경하며 마진의 변화를 관찰해보세요.
# [문법] SVC: SVM 분류 모델. kernel='linear'는 선형 분리를 수행하며, C는 오차에 대한 허용치(규제)를 조절함.
# [개념] C 값이 클수록 하드 마진(오차 허용 적음), 작을수록 소프트 마진(오차 허용 많음, 과적합 방지)에 가까워짐.
model = SVC(kernel='linear', C=1.0).fit(X, y) # [문법] fit(): 학습 데이터를 사용하여 최적의 결정 경계를 찾음.

# 3. 결정 경계(Decision Boundary) 시각화를 위한 그리드 생성
xmin, xmax = X[:, 0].min(), X[:, 0].max()
ymin, ymax = X[:, 1].min(), X[:, 1].max()
xx = np.linspace(xmin, xmax, 10) # [문법] np.linspace: 지정된 범위 내에서 균일한 간격의 숫자 생성.
yy = np.linspace(ymin, ymax, 10) 
X1, X2 = np.meshgrid(xx, yy)

# 4. 각 그리드 포인트에 대한 결정 함수 값 계산
z = np.empty(X1.shape)
for (i, j), val in np.ndenumerate(X1):
    x1 = val
    x2 = X2[i, j]
    # [문법] decision_function: 데이터 포인트에서 결정 경계까지의 거리를 반환함.
    p = model.decision_function([[x1, x2]]) 
    z[i, j] = p[0]

# 5. 결과 시각화 (결정 경계 및 서포트 벡터)
plt.scatter(X[y == -1, 0], X[y == -1, 1], marker='o', label="-1 클래스")
plt.scatter(X[y == +1, 0], X[y == +1, 1], marker='x', label="+1 클래스")

# [문법] plt.contour: 등고선을 그림. levels=[-1, 0, 1]은 마진(±1)과 결정 경계(0)를 의미함.
plt.contour(X1, X2, z, levels=[-1, 0, 1], colors='k', linestyles=['dashed', 'solid', 'dashed'])

# [문법] model.support_vectors_: 학습된 모델에서 서포트 벡터로 선택된 데이터 포인트들을 반환함.
plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=300, alpha=0.3)

# 6. 새로운 테스트 데이터 예측 및 표시 (예측 시 model.predict() 사용 가능)
x_new = [10, 2]
plt.scatter(x_new[0], x_new[1], marker='^', s=100)
plt.text(x_new[0] + 0.03, x_new[1] + 0.08, "테스트 데이터")

plt.xlabel("x1")
plt.ylabel("x2")
plt.legend()
plt.title("SVM 예측 결과")
plt.show()

# 7. 선택된 서포트 벡터 좌표 출력
print("선택된 서포트 벡터 좌표:")
print(model.support_vectors_)
# 선택된 서포트 벡터 좌표:
# [[9.03715314 1.71813465]
#  [9.17124955 3.52485535]]