# [개념] SVM(Support Vector Machine) 분류 모델로 이미지 분류
# [개념] 고차원 이미지 데이터를 PCA로 차원 축소한 후 SVM을 적용하여 분류 성능과 속도를 개선하는 실습.
# 세계 정치인들 중 일부 얼굴 사진 데이터 사용

from tkinter import font

from altair import FontWeight
from matplotlib.figure import figaspect
from matplotlib.pylab import rand
from sklearn.datasets import fetch_lfw_people
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sympy import failing_assumptions, im

# 데이터
faces = fetch_lfw_people(min_faces_per_person=60, color=False, resize=0.5) # [문법] fetch_lfw_people: 얼굴 인식용 데이터셋 로드.
# 60 : 한 사람 당 60장 이상의 사진이 있는 자료만 사용
# print(faces)
# print(faces.DESCR)
print(faces.data)
print(faces.data.shape) # (1348, 2914)
print('\n')
print(faces.target)
print(faces.target_names) # [문법] target_names: 분류 대상 인물들의 이름 목록.
print(faces.images.shape) # (1348, 62, 47)
print('\n')

print(faces.images[1])
print(faces.target_names[faces.target[1]])
 # 이미지 1개 시각화
plt.imshow(faces.images[1], cmap='bone') # [문법] imshow: 2차원 배열 데이터를 이미지로 출력.
plt.show()
print('\n')

# [문법] 원본 이미지 15개 시각화
fig, ax = plt.subplots(3, 5)
for i, axi in enumerate(ax.flat):
    axi.imshow(faces.images[i], cmap='bone')
    axi.set(xticks=[], yticks=[], xlabel=faces.target_names[faces.target[i]])
plt.tight_layout()
plt.show()
print('\n')

###########################################################
# [개념] 주성분 분석(PCA)으로 이미지 차원을 축소시켜, 분류 작업을 진행

# 설명력 95% 되는 최소 개수를 얻기
pca = PCA(n_components=0.95) # [문법] n_components=0.95: 전체 분산의 95%를 유지하는 주성분 개수 자동 선택.
x_pca = pca.fit_transform(faces.data)
print(pca.n_components_)    # 184
print('\n')

n = 150 # [개념] 차원수는 분석가가 결과를 보고 판단함
m_pca = PCA(n_components=n, whiten=True, random_state=1)   # whiten=True : 주성분의 스케일이 작아지도록 조정
x_low = m_pca.fit_transform(faces.data)
print('x_low : \n', x_low)   # (1348, 2914)  ->  (1348, n)
print(x_low.shape)  # (1348, 10)

fig, ax = plt.subplots(3, 5, figsize=(10, 6))
for i, axi in enumerate(ax.flat):
    axi.imshow(m_pca.components_[i].reshape(faces.images[0].shape), cmap='bone')
    # faces.images[0].shape : (62, 47)  
    # ->  reshape(faces.images[0].shape) : [2914]->[62, 47]
    axi.axis('off')
    axi.set_title(f'PC {i + 1}')
plt.suptitle('주성분 이미지 Eigenfaces', fontsize=12)
plt.tight_layout() # [문법] tight_layout: 서브플롯 간의 간격을 자동으로 조절.
plt.show()  # 출력 이미지는 실제 얼굴이 아니라 특징 패턴(눈 위치, 코 그림자, 얼굴 윤곽 등등)을 보여줌
print('\n')
# SVM 알고리즘은 실제 얼굴이 아니라 특징 패턴으로 분류 작업을 한다

# 설명력 확인
print(m_pca.explained_variance_ratio_[:10]) # [문법] explained_variance_ratio_: 각 주성분이 설명하는 정보량 비율.
print('누적 설명력 : ', m_pca.explained_variance_ratio_.sum())
# 누적 설명력 :  0.9039658
# n = 100 개로 얼마나 원본 정보를 유지했는지 확인함
print('\n')

# 원본 VS 복원 이미지 비교
x_reconst = m_pca.inverse_transform(x_low) # [문법] inverse_transform: 축소된 데이터를 다시 원래 차원으로 복원.
fig, ax = plt.subplots(2, 5, figsize=(10, 4))
for i in range(5):
    # 원본
    ax[0, i].imshow(faces.images[i], cmap='bone')
    ax[0, i].axis('off')
    ax[0, i].set_title('원본')

    # 복원
    ax[1, i].imshow(x_reconst[i].reshape(faces.images[0].shape), cmap='bone')
    ax[1, i].axis('off')
    ax[1, i].set_title('복원')
plt.suptitle('원본 VS 복원 이미지', fontsize=12)
plt.tight_layout()
plt.show()  # 원본과 복원된 이미지의 기본 특징은 크게 차이가 없다(패턴이 유지됨)
print('\n')

# 분류 모델 생성
svcmodel = SVC(C=1, random_state=1, kernel='rbf', class_weight='balanced') # [추천] 이미지 분류 시 비선형 커널(rbf)과 클래스 불균형 보정(class_weight) 사용 권장.
# PCA 분류기를 하나의 파이프라인으로 묶어 순차적으로 실행
mymodel = make_pipeline(m_pca, svcmodel) # [문법] make_pipeline: PCA와 SVC를 연결하여 하나의 모델처럼 사용.
print(mymodel)
# Pipeline(steps=[('pca', PCA(n_components=100, whiten=True, random_state=0)), ('svc', SVC(C=1, random_state=1))])
print('\n')

# 데이터 분리
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(faces.data, faces.target, test_size=0.3, random_state=1, stratify=faces.target) # [문법] stratify: 클래스 비율 유지 분할.
# stratify=faces.target : 불균형 자료 완화
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)
print('\n')

# 학습 및 예측
mymodel.fit(x_train, y_train) # [문법] fit: 파이프라인을 통해 PCA 변환 후 SVC 학습 수행.
pred = mymodel.predict(x_test) # [문법] predict: 테스트 데이터에 대한 인물 예측.
print('예측값 : ', pred[:10])
print('실제값 : ', y_test[:10])
print('\n')

# 정확도
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
print('정확도 : ', accuracy_score(y_test, pred)) # [문법] accuracy_score: 전체 중 맞춘 비율.
print('\n')
# [추천] GridSearchCV를 사용하여 SVC의 C와 gamma 파라미터를 최적화하면 성능을 더 높일 수 있음.
# 분류 리포트
print('분류 리포트 : \n', classification_report(y_test, pred, target_names=faces.target_names))
print('\n')

# 혼동 행렬
print('혼동 행렬 : \n',confusion_matrix(y_test, pred))
print('\n')

# 분류 결과를 시각화 하기
# 하나만 보기
plt.subplots(1, 1)
plt.imshow(x_test[0].reshape(62, 47), cmap='bone')   # 1차원 -> 2차원으로 변환
plt.show()

# 여러 개 보기
fig, axes = plt.subplots(4, 6)
for i, ax in enumerate(axes.flat):
    ax.imshow(x_test[i].reshape(62, 47), cmap='bone')
    ax.set(xticks=[], yticks=[])
    ax.set_ylabel(faces.target_names[pred[i]].split()[-1], color='black' if pred[i] == y_test[i] else 'red', fontweight='bold')

fig.suptitle('예측 결과', size=14)
plt.tight_layout()
plt.show()
print('\n')

# 오차 행렬 시각화
import seaborn as sns
plt.figure(figsize=(10, 8)) # [문법] heatmap: 혼동 행렬을 색상으로 시각화.
sns.heatmap(confusion_matrix(y_test, pred), annot=True, fmt='d', cmap='Blues', xticklabels=faces.target_names, yticklabels=faces.target_names)
plt.xlabel('예측값')
plt.ylabel('실제값')
plt.title('오차 행렬')
plt.tight_layout()
plt.show()
print('\n')

# PCA 누적 분산 그래프 (왜 n_components=n 인가?)
import numpy as np
plt.plot(np.cumsum(m_pca.explained_variance_ratio_)) # [문법] cumsum: 누적 합계 계산.
plt.xlabel('주성분 개수')
plt.ylabel('누적 설명력')
plt.title('PCA 누적 설명력')
plt.tight_layout()
plt.show()
print('\n')

#############################################################
# [개념] 새로운 이미지를 입력해 분류하기
#############################################################
# 현재 모델의 분류 accuracy : 0.762962962962963

# 실습 1 : 기존 이미지로 테스트 하기
test_img = faces.data[0].reshape(1, -1)
print('test : ', test_img)
test_pred = mymodel.predict(test_img)
print('실습 1 예측 : ', faces.target_names[test_pred[0]])
print('실제값 : ', faces.target_names[faces.target[0]])
print('\n')

# 실습 2 : 새로운 이미지로 테스트 하기
# 단계
# 이미지 읽기 -> 흑백 변환 -> 크기 맞추기(62x47) -> 1차원으로 변환 -> 예측
from PIL import Image # [문법] PIL: 파이썬 이미지 처리 라이브러리.
img = Image.open('bush.jpg')
img.convert('L')    # [문법] convert('L'): 이미지를 그레이스케일(흑백)로 변환.
img = img.resize((47, 62))  # [문법] resize: 이미지 크기 조정. width, height -> PIL은 순서가 반대로 되어 있음
                                                # numpy 이미지는 (height, width) 순서
                                                # 이미지는 라이브러리마다 축 순서가 다르다
img_np = np.array(img)  # numpy 변환
print('img_np : \n', img_np)
# img_np : 
#  [[ 48  44   5 ...  66  66  67]
#  [ 49  27  41 ...  67  66  66]
#  [ 46  26 100 ...  67  67  67]
#  ...
#  [ 54   2   0 ...  26  26  28]
#  [ 20   0   0 ...  25  26  27]
#  [ 20   1   0 ...  24  25  27]]
# 표준화/정규화 가 되어 있지 않은 상태!! (0~255 숫자로 구성)
# >>>>>>>>>> 정규화를 시켜줘야 함
print(img_np.shape) # (62, 47)
print('\n')
img_np = img_np / 255.0   # 학습 데이터와 맞춰주어야 함
print(img_np)
# [[0.18823529 0.17254902 0.01960784 ... 0.25882353 0.25882353 0.2627451 ]
#  [0.19215686 0.10588235 0.16078431 ... 0.2627451  0.25882353 0.25882353]
#  [0.18039216 0.10196078 0.39215686 ... 0.2627451  0.2627451  0.2627451 ]
#  ...
#  [0.21176471 0.00784314 0.         ... 0.10196078 0.10196078 0.10980392]
#  [0.07843137 0.         0.         ... 0.09803922 0.10196078 0.10588235]
#  [0.07843137 0.00392157 0.         ... 0.09411765 0.09803922 0.10588235]]
print('\n')
img_flat = img_np.reshape(1, -1)    # [문법] reshape(1, -1): 2차원 이미지를 모델 입력용 1차원 배열로 변환.
new_pred = mymodel.predict(img_flat)
print('실습 2 예측 : ', faces.target_names[new_pred[0]])
print('\n')

# 시각화 + 예측
plt.imshow(img_np, cmap='bone')
plt.title(f'예측 : {faces.target_names[new_pred[0]]}')
plt.tight_layout()
plt.axis('off')
plt.show()
print('\n')