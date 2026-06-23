# 다중 선형 회귀 : 자동차 연비 예측
# 조기 종료 코드 추가

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
import seaborn as sns

# 데이터 읽기 (물음표가 있는 노이즈 데이터 결측치 처리)
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/auto-mpg.csv', na_values='?')
print(data.head(2))
print('\n')
print(data.info())
print('\n')

# 결측치 처리
del data['car name']   # 문자열 칼럼 제거
data = data.dropna()   # 결측치가 있는 행 제거
print(data.isna().sum()) # 결측치가 있는 칼럼별로 결측치 개수 출력
print('\n')

# 필요한 칼럼 선택
data.drop(['cylinders', 'acceleration', 'model year', 'origin'], axis=1, inplace=True)
print(data.head(2))
print('\n')




# 시각화를 통해 feature와 label의 상관관계 분석
# sns.pairplot(data[['mpg', 'displacement', 'horsepower', 'weight']], diag_kind='kde')
# plt.show()



# feature와 label 분리 - 라이브러리 사용하지 않고 직접 작성
train_dataset = data.sample(frac=0.7, random_state=123)  # 70%를 학습 데이터로 사용
print(train_dataset.shape)   # (274, 4)
test_dataset = data.drop(train_dataset.index)  # 나머지 30%를 테스트 데이터로 사용
print(test_dataset.shape)    # (118, 4)
print('\n')



# 표준화 : 수식으로 처리 ⇨ (feature - 평균) / 표준편차
train_stat = train_dataset.describe()
train_stat.pop('mpg')   # label 칼럼 제거
print(train_stat)
#  displacement  horsepower     weight
#   196.131387  104.755474     2981.941606

train_stat = train_stat.transpose()   # 행과 열을 바꿔서 출력 → 평균과 표준편차를 추출하기 편리하도록
print(train_stat)

# 표준화 함수 작성
def stdscale_func(x):
    return (x - train_stat['mean']) / train_stat['std']

# feature와 label 분리
st_train_data = stdscale_func(train_dataset)
st_train_data = st_train_data.drop('mpg', axis=1)   # feature에서 label 칼럼 제거

st_test_data = stdscale_func(test_dataset)
st_test_data = st_test_data.drop('mpg', axis=1)   # feature에서 label 칼럼 제거

train_label = train_dataset['mpg']
test_label = test_dataset['mpg']

# 모델 작성
def build_model():
    network = Sequential([
        Input(shape=(3,)),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='linear')
    ])
    opti = tf.keras.optimizers.Adam(learning_rate=0.001)
    network.compile(loss='mse', optimizer=opti, metrics=['mse', 'mae'])
    return network

model = build_model()
print(model.summary())
print('\n')

EPOCHS = 5000

# 조기 종료 콜백 함수 정의
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',  # 모니터링할 지표, 무엇을 기준으로 정할지 결정
    patience=10,    # 개선이 없을 때 기다리는 에포크 수,
    restore_best_weights=True,  # 가장 좋은 모델의 가중치를 복원할지 여부
    # baseline=0.01,  # 개선이 없다고 판단할 기준값 (최소한의 성능)
)

history = model.fit(st_train_data, train_label, batch_size=32, epochs=EPOCHS, verbose=2, validation_split=0.2, callbacks=[early_stop])
print('학습 완료')

df = pd.DataFrame(history.history)
print(df.head(3))
print(df.columns)
print('\n')

# 모델 학습 정보 시각화
def plot_history(df):
    hist = df
    hist['epoch'] = history.epoch
    
    plt.figure(figsize=(8, 14))
    plt.subplot(2, 1, 1)
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mae'], label='Train Error')
    plt.plot(hist['epoch'], hist['val_mae'], label='Val Error')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mse'], label='Train Error')
    plt.plot(hist['epoch'], hist['val_mse'], label='Val Error')
    plt.legend()
    plt.show()

plot_history(df)



# 모델 평가
from sklearn.metrics import r2_score
pred = model.predict(st_test_data, verbose=0)
loss, mse, mae = model.evaluate(st_test_data, test_label, verbose=0)
print('evaluate result - loss : {:.4f}, mse : {:.4f}, mae : {:.4f}'.format(loss, mse, mae))
print('설명력 : ', r2_score(test_label, pred.ravel()))
print('\n')

# 새로운 값으로 예측
new_data = pd.DataFrame({
    'displacement': [300, 400],
    'horsepower': [120, 150],
    'weight': [2000, 4000]
})

new_data_std = stdscale_func(new_data)
new_pred = model.predict(new_data_std, verbose=0).flatten()
print('새로운 데이터 예측값 : ', new_pred)
print('\n')