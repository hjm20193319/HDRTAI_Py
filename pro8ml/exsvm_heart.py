from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import koreanize_matplotlib

# 데이터
pd.set_option('display.max_columns', None)
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Heart.csv', index_col=0)
print(df.head(2))
print(df.info())
print('\n')

x = df.drop(['ChestPain', 'Thal', 'AHD'], axis=1)
print(x.head(2))
print('\n')

y = df['AHD']
print(y.head(2))
print('\n')

# feature 정규화
x = x / x.max()
print(x.head(2))
print('\n')

print(np.isnan(x).sum())
print('\n')

x = x.fillna(0)
print(np.isnan(x).sum())
print('\n')


# train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)
print('\n')

# 모델
model = svm.SVC(C=10, kernel='rbf')
model.fit(x_train, y_train)

# 예측
pred = model.predict(x_test)
print('예측값 : ', pred[:10])
print('실제값 : ', np.array(y_test[:10]))
print('맞춘 개수 : ', (pred == y_test).sum())
print('오류수 : ', (pred != y_test).sum())
print('전체 대비 맞춘 비율 : ', sum(y_test == pred) / len(y_test))
print('분류 정확도 : ', metrics.accuracy_score(y_test, pred))
print('\n')

# 교차 검증 모델
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x, y, cv=3)
print('각 3회 교차 검증 정확도 : ', scores)
print('교차 검증 평균 정확도 : ', np.round(scores.mean(), 5))
print('\n')

# 상관관계 분석
yint = y.map({'Yes':1, 'No':0})
corr_matrix = pd.concat([x, yint], axis=1).corr()
print(corr_matrix['AHD'].sort_values(ascending=False))
print('\n')

# 시각화
def scatter_func1(lbl, color):
    b = df.loc[df['AHD'] == lbl]
    plt.scatter(x=b['Oldpeak'], y=b['MaxHR'], c=color, label=lbl)
    plt.legend()

scatter_func1('Yes', 'green')
scatter_func1('No', 'red')
plt.xlabel('ST 분절 하강 정도')
plt.ylabel('최대 심박수')
plt.tight_layout()
plt.show()
print('\n')

##########################################################################
# 새로운 데이터로 예측
new_data_list = [
    [52, 1, "nonanginal", 135, 240, 0, 0, 160, 0, 0.5, 1, 0, "normal"],
    [65, 0, "asymptomatic", 145, 310, 1, 2, 120, 1, 2.2, 2, 2, "reversable"],
    [43, 1, "typical", 120, 215, 0, 1, 175, 0, 0.0, 1, 0, "fixed"],
    [58, 0, "nontypical", 130, 265, 0, 2, 145, 1, 1.4, 2, 1, "normal"],
    [49, 1, "asymptomatic", 150, 230, 0, 0, 130, 0, 3.1, 3, 3, "reversable"]
]

# 컬럼명 설정 (학습 시 사용했던 독립변수 순서와 동일해야 합니다)
columns = ["Age", "Sex", "ChestPain", "RestBP", "Chol", "Fbs", "RestECG", 
        "MaxHR", "ExAng", "Oldpeak", "Slope", "Ca", "Thal"]

# 데이터프레임 생성
new_df = pd.DataFrame(new_data_list, columns=columns)

# 문자열 칼럼 제거
new_df = new_df.drop(['ChestPain', 'Thal'], axis=1)

# feature 정규화
new_df = new_df / new_df.max()

# 예측
new_pred = model.predict(new_df)
print('예측값 : ', new_pred)
print('\n')