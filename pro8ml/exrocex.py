from cProfile import label
from calendar import c

from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 수집
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/advertisement.csv', usecols=['Daily Time Spent on Site', 'Age', 'Area Income', 'Daily Internet Usage', 'Clicked on Ad'])
print(data.head())
print(data.shape)
print('\n')

# 데이터 구분
x = data.iloc[:, :-1]
y = data.iloc[:, -1]
# print(x)
# print(y)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# 데이터의 단위 차이가 있으므로 표준화 진행
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(x_train)
x_train = sc.transform(x_train)
x_test = sc.transform(x_test)
print(x_train[:3])
print(x_test[:3])
print('\n')

# 분류 모델 생성
model = LogisticRegression(random_state=0)
model.fit(x_train, y_train)
y_pred = model.predict(x_train)

# 모델 성능 파악
from sklearn.metrics import confusion_matrix
conf_mat = confusion_matrix(y_train, y_pred)
print(conf_mat)
# [[330   6]
#  [ 13 351]]
print('\n')

tp = conf_mat[0][0]
fn = conf_mat[0][1]
fp = conf_mat[1][0]
tn = conf_mat[1][1]
print(tp, fn, fp, tn)
print('\n')

acc = (tp + tn) / (tp + fn + fp + tn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
specificity = tn / (tn + fp)
fallout = fp / (fp + tn)
f1 = 2 * (precision * recall) / (precision + recall)

print('정확도acc : ', acc)
print('재현율recall : ', recall)
print('정밀도precision : ', precision)
print('specificity : ', specificity)
print('fallout : ', fallout)
print('f1 : ', f1)
print('\n')

from sklearn import metrics
fpr, tpr, thresholds = metrics.roc_curve(y_train, model.decision_function(x_train))
print('fpr : ', fpr)
print('tpr : ', tpr)
print('thresholds : ', thresholds)
print('\n')

plt.plot(fpr, tpr, '-', label='Logistic Regression')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier line(AUC:0.5)')
plt.plot([fallout], [recall], 'ro', ms=6)   # 위앙성률, 재현율 출력
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC Curve')
plt.legend()
plt.show()

# AUC 
print('AUC : ', metrics.auc(fpr, tpr))

# 새로운 데이터로 분류
y_newpred = model.predict(x_test)
print('새로운 예측값 : ', y_newpred[:5])
print('실제값 : ', y_test.values[:5])
print('\n')

# 분류 정확도
from sklearn.metrics import accuracy_score
print('분류 정확도 : ', accuracy_score(y_test, y_newpred))
# 분류 정확도 :  0.9666666666666667
print('\n')

# 분류 오류 개수
print(f'총 개수 : {len(y_test)}, 오류수 : {(y_test != y_newpred).sum()}')
# 총 개수 : 300, 오류수 : 10

# 시각화
import seaborn as sns

# 테스트 데이터의 혼동행렬 생성
test_conf_mat = confusion_matrix(y_test, y_newpred)

plt.figure(figsize=(6, 5))
sns.heatmap(test_conf_mat, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Not Clicked', 'Clicked'], 
            yticklabels=['Not Clicked', 'Clicked'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Test Data Confusion Matrix')
plt.show()