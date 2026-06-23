# 다항회귀 : 데이터가 비선형 분포인 경우 선형회귀로는 모델링이 어려움
# 다항회귀는 선형회귀의 확장으로, 입력 변수의 다항식 항을 추가하여 모델링하는 방법
# 회귀선이 직선이 아닌 곡선이 됨 - 2차, 3차 ...
# 예시: y = a + b1*x + b2*x^2 + b3*x^3 + ... + bn*x^n
# 다항회귀는 선형회귀보다 유연한 모델링이 가능하지만, 과적합의 위험이 있음
# 다항회귀 모델을 작성할 때는 적절한 다항식의 차수를 선택하는 것이 중요함

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import tensorflow as tf

np.random.seed(7)
tf.random.set_seed(7)

# 가상의 feature와 label 데이터 생성
x = np.linspace(-3, 3, 40).reshape(-1, 1)   # 40개의 데이터를 -3에서 3까지 균등하게 생성
print(x[:3])

# y = x^2 + x + 2 + 노이즈
y = (x[:, 0] ** 2) + x[:, 0] + 2 + np.random.normal(0, 1.5, size=len(x))
print(y[:3])

# 시각화
plt.scatter(x, y, color='blue', label='Data Points')
plt.title('Polynomial Regression Data')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')



# R2 score 계산 함수 작성
def r2_score_np(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)  # 잔차 제곱합
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)  # 총 제곱합
    r2 = 1 - (ss_res / ss_tot)  # R2 score 계산
    return r2



# 비교를 위해 선형 회귀 모델 작성
linear_model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(1,)),
    tf.keras.layers.Dense(1, activation='linear')
])
linear_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.05), loss='mse')
linear_model.fit(x, y, epochs=500, verbose=0)
print('학습 완료')
y_pred_linear = linear_model.predict(x, verbose=0).flatten()



# 다항 회귀 모델 작성 (2차 다항식)
x_poly = np.column_stack(
    (x[:, 0], x[:, 0] ** 2)
).astype(np.float32)  # x와 x^2를 feature로 사용
print(x_poly[:3])

poly_model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(2,)),
    tf.keras.layers.Dense(1, activation='linear')
])
poly_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.05), loss='mse')
poly_model.fit(x_poly, y, epochs=500, verbose=0)
print('학습 완료')
y_pred_poly = poly_model.predict(x_poly, verbose=0).flatten()


# 부드러운 곡선을 그리기 위한 x축 데이터 생성
x_plot = np.linspace(x.min(), x.max(), 300).reshape(-1, 1).astype(np.float32)
y_plot_linear = linear_model.predict(x_plot, verbose=0)



# 예측할 때도 x와 x^2의 값을 함께 넣어야 함 
# (그래프에 그릴 x값-x_plot 도 다항 회귀 모델이 입력 받을 수 있도록 변환)
x_plot_poly = np.column_stack(
    (x_plot[:, 0], 
     x_plot[:, 0] ** 2)
).astype(np.float32)

y_plot_poly = poly_model.predict(x_plot_poly, verbose=0).flatten()



# 성능 계산
r2_linear = r2_score_np(y, y_pred_linear)
r2_poly = r2_score_np(y, y_pred_poly)
print('선형 회귀 모델의 R2 score : ', r2_linear)
print('다항 회귀 모델의 R2 score : ', r2_poly)



# 시각화
plt.figure(figsize=(12, 6))
plt.scatter(x, y, color='blue', label='Data Points')
plt.plot(x_plot, y_plot_linear, color='red', label='Linear Regression')
plt.plot(x_plot, y_plot_poly, color='green', label='Polynomial Regression')
plt.title('Polynomial Regression vs Linear Regression')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.tight_layout()
plt.show()
print('\n')