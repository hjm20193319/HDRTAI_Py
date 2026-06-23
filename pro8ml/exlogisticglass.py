import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression


# 데이터
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/bodycheck.csv', usecols=['게임', 'TV시청', '안경유무'])
print(data.head())

x = data.iloc[:, [0, 1]]
y = data.iloc[:, 2]

# 데이터 구분
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# 모델 생성
model = LogisticRegression(random_state=0).fit(x_train, y_train)

# 분류
pred = model.predict(x_test)
print('예측값 : ', np.around(pred).astype(int))
print('실제값 : ', y_test.values)
print('\n')

# 분류 정확도
print('분류 정확도 : ', accuracy_score(y_test, np.around(pred)))
print('\n')

# 새로운 값으로 분류 예측
new_df = pd.DataFrame()
new_df['게임'] = [input('게임 시간을 입력하시오 : ')]
new_df['TV시청'] = [input('TV시청 시간을 입력하시오 : ')]
print(new_df)
print('\n')

new_pred = model.predict(new_df)
if np.around(new_pred) == 1:
    print('안경을 쓴다')
else:
    print('안경을 쓰지 않는다')