# ROC (Receiver Operating Characteristic) Curve
# : 모든 분류 임계값에서 분류 모델의 성능을 보여주는 그래프
# : x 축이 FPR (1 - 특이도)
# : y 축이 TPR (민감도)
# : 민감도와 특이도의 관계를 표현한 그래프

# ROC Curve는 AUC(Area Under Curve 그래프 아래 면적)를 이용해서 모델의 성능을 평가
# : AUC가 클수록 정확히 분류함을 뜻함
# FPR 위양성률이 변할 때 TPR 민감도가 어떻게 변하는지 알려주는 곡선

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib


x, y = make_classification(
    n_samples=100,           # 전체 데이터 100개
    n_features=2,            # 변수 2개
    n_redundant=0,           # 중복 변수 없음
    random_state=123           # 난수 고정
)
# n_redundant : 독립변수 중 다른 독립변수의 선형 조합으로 
print(x[:3], x.shape)   # (100, 2)
print(y[:3], y.shape)   # (100,)
print('\n')

# 산포도
# plt.scatter(x[:, 0], x[:, 1], c=y)
# plt.show()

model = LogisticRegression()
model.fit(x, y)
y_hat = model.predict(x)
print('y_hat : ', y_hat[:5])
print('real : ', y[:5])
# y_hat :  [0 1 0 1 0]
# real  :  [0 1 1 1 0]
print('\n')

# ROC curve의 판별 경계선 설정용 결정함수 사용
f_value = model.decision_function(x)
print('f_value : ', f_value[:10])
print('\n')

df = pd.DataFrame(np.vstack([f_value, y_hat, y]).T, columns=['f', 'y_hat', 'y'])
print(df.head())

# 모델 성능 파악
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y, y_hat))
print('\n')

acc = (44 + 44) / 100
recall = 44 / (44 + 4)
precision = 44 / (44 + 8)
specificity = 44 / (44 + 8) # 특이도
fallout = 4 / (4 + 44) # FPR 위양성율
f1 = 2 * (precision * recall) / (precision + recall)

print('acc : ', acc)
print('recall : ', recall)      # TPR : 1에 근사하면 좋음
print('precision : ', precision)
print('specificity : ', specificity)
print('fallout : ', fallout)        # FPR : 0에 근사하면 좋음
print('f1 : ', f1)
print('\n')

from sklearn import metrics
acc_score = metrics.accuracy_score(y, y_hat)
print('모델 정확도 : ', acc_score)

cl_rep = metrics.classification_report(y, y_hat)
print(cl_rep)
print('\n')

fpr, tpr, thresholds = metrics.roc_curve(y, model.decision_function(x))
print('fpr : ', fpr)
print('tpr : ', tpr)
print('thresholds : ', thresholds)      # 분류결정 임계값(결정함수 값)
print('\n')

plt.plot(fpr, tpr, 'o-', label='Logistic Regression')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier line(AUC:0.5)')
plt.plot([fallout], [recall], 'ro', ms=6)   # 위앙성률, 재현율 출력
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC Curve')
plt.legend()
plt.show()

# AUC ( Area Under the Curve ) : ROC 커브의 면적
# ㄴ 1에 근사할 수록 좋은 모델
print('AUC : ', metrics.auc(fpr, tpr))
# AUC :  0.9547275641025641 => 매우 성능이 우수한 모델