# 다항 회귀

# 매출 = 광고비 * W + b

# 매출 = (광고비1 * W1) + (광고비² * W2) + b

# ⇨ 광고비와 매출의 관계가 직선이 아니라 곡선 형태의 자료를 대상

# 다항 회귀에 적합한 데이터 생성 → CSV 파일로 저장 후 읽기 → 산점도
# → Train/Test Split → 선형 모델, 비선형 모델 학습 후 성능 비교

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import tensorflow as tf

np.random.seed(7)
tf.random.set_seed(7)

# 광고비가 증가하면 매출도 증가하나, 어느 정도 이후에는 증가폭이 둔화되는 곡선 데이터
ad_cost = np.linspace(0, 100, 80)       # 광고비 데이터
# sales는 광고비에 따른 매출 데이터를 만드는 부분 → 이차함수
# sales = {광고비² * (-0.06)} + (7.5 * 광고비) + 40 + noise → 인위적으로 수식 작성
sales = (ad_cost ** 2) * (-0.06) + 7.5 * ad_cost + 40 + np.random.normal(0, 25, size=len(ad_cost))

df = pd.DataFrame({'광고비': ad_cost, '매출': sales})
print(df.head())
print('\n')

df.to_csv('ad_sales.csv', index=False, encoding='utf-8-sig')
print('저장 완료')
print('\n')

df = pd.read_csv('ad_sales.csv')
print(df.info())
print('\n')

# 결측치가 있다면 해당 행 삭제
df = df.dropna()
print('데이터 크기 : ', df.shape)
print('\n')

# feature, label 분리
x = df[['광고비']].values.astype(np.float32)
y = df[['매출']].values.astype(np.float32)
print(x[:3])
print(y[:3])
print('\n')

# 산점도
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='blue', alpha=0.7)
plt.xlabel('광고비')
plt.ylabel('매출')
plt.title('광고비와 매출의 관계')
plt.grid(True)
plt.tight_layout()
plt.show()

# train/ test split - sklearn 없이 직접 섞기
indices = np.arange(len(x))
np.random.shuffle(indices)
x = x[indices]
y = y[indices]

train_size = int(0.8 * len(x))
x_train, x_test = x[:train_size], x[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print('x : ', x_train.shape, x_test.shape)
print('y : ', y_train.shape, y_test.shape)
# x :  (64, 1) (16, 1)
# y :  (64, 1) (16, 1)
print('\n')

# Scaling : train 데이터 기준으로 평균과 표준편차 계산 후 표준화
x_mean = x_train.mean(axis=0)
x_std = x_train.std(axis=0)

y_mean = y_train.mean(axis=0)
y_std = y_train.std(axis=0)

# 표준화
x_train_scaled = (x_train - x_mean) / x_std
x_test_scaled = (x_test - x_mean) / x_std

y_train_scaled = (y_train - y_mean) / y_std
y_test_scaled = (y_test - y_mean) / y_std


# 다항 특성 함수 : degree = 2 → [x, x²] 생성
# 스케일링된 입력값을 다항 회귀용 입력 데이터로 변환
def make_poly_features(x_scaled,degree=2):
    features = [x_scaled ** d for d in range(1, degree + 1)]
    return np.concatenate(features, axis=1).astype(np.float32)  # 배열을 열 방향으로 붙임

x_train_poly = make_poly_features(x_train_scaled, degree=2)
x_test_poly = make_poly_features(x_test_scaled, degree=2)
print('선형 회귀 입력 shape : ', x_train_scaled.shape, x_test_scaled.shape)
print('다항 회귀 입력 shape : ', x_train_poly.shape, x_test_poly.shape)
print('\n')


# R2 score 계산 함수 작성
def r2_score_np(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)  # 잔차 제곱합
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)  # 총 제곱합
    r2 = 1 - (ss_res / ss_tot)  # R2 score 계산
    return r2


# 모델 성능 평가 함수
def evaluate_model(name, y_true, y_pred):
    mse = np.mean((y_true - y_pred) ** 2)   # 평균 제곱 오차
    rmse = np.sqrt(mse)
    r2 = r2_score_np(y_true, y_pred)   # R2 score
    print(f'\n[{name}] 모델 성능 평가')
    print('MSE : ', round(mse, 3))
    print('RMSE : ', round(rmse, 3))
    print('R2 score : ', round(r2, 3))
    print('\n')


# 선형 회귀 모델
linear_model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(1,)),
    tf.keras.layers.Dense(1, activation='linear')
])
linear_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mse')
linear_model.fit(x_train_scaled, y_train_scaled, epochs=2000, verbose=0)
print('학습 완료')
y_pred_linear_scaled = linear_model.predict(x_test_scaled, verbose=0)

# 원래 매출 단위로 예측값 복원
y_pred_linear = y_pred_linear_scaled * y_std + y_mean


# 다항 회귀 모델
poly_model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(2,)),
    tf.keras.layers.Dense(1, activation='linear')
])
poly_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mse')
poly_model.fit(x_train_poly, y_train_scaled, epochs=2000, verbose=0)
print('학습 완료')
y_pred_poly_scaled = poly_model.predict(x_test_poly, verbose=0)

# 원래 매출 단위로 예측값 복원
y_pred_poly = y_pred_poly_scaled * y_std + y_mean


# 모델 성능 비교
evaluate_model('선형 회귀', y_test, y_pred_linear)
evaluate_model('다항 회귀(degree=2)', y_test, y_pred_poly)
print('\n')


# 시각화
x_plot = np.linspace(x.min(), x.max(), 300).reshape(-1, 1).astype(np.float32)
x_plot_scaled = (x_plot - x_mean) / x_std   # 표준화
x_plot_poly = make_poly_features(x_plot_scaled, degree=2)   # 다항 특성

y_plot_linear_scaled = linear_model.predict(x_plot_scaled, verbose=0)
y_plot_poly_scaled = poly_model.predict(x_plot_poly, verbose=0)

# 원래 매출 단위로 복원
y_plot_linear = y_plot_linear_scaled * y_std + y_mean
y_plot_poly = y_plot_poly_scaled * y_std + y_mean


plt.figure(figsize=(12, 6))
plt.scatter(x_train, y_train, alpha=0.5, label='Train Data')
plt.scatter(x_test, y_test, alpha=0.9, label='Test Data')
plt.plot(x_plot, y_plot_linear, color='red', label='Linear Regression')
plt.plot(x_plot, y_plot_poly, color='green', label='Polynomial Regression(degree=2)')
plt.xlabel('광고비')
plt.ylabel('매출')
plt.title('광고비와 매출의 관계')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
print('\n')