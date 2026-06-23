# 연산자와 기초 함수

import tensorflow as tf
import numpy as np

x = tf.constant(7)
y = tf.constant(3)

# cond() : 삼항 연산
result1 = tf.cond(x > y, lambda: tf.add(x, y), lambda: tf.subtract(x, y))   # 조건에 의해서 함수를 실행
tf.print(result1)
print('\n')

# case() : 조건 연산
f1 = lambda: tf.constant(1) # lamda에 의해 1을 반환
f2 = lambda: tf.constant(tf.multiply(2, 3))
result2 = tf.case([(tf.less(x, y), f1)], default=f2)    # if(x < y) return 1 else return 6
print(result2)
print('\n')

# 관계연산
print(tf.equal(1, 2))
print(tf.not_equal(1, 2))
print(tf.less(1, 2))
print(tf.less_equal(1, 2))
print(tf.greater(1, 2))
print(tf.greater_equal(1, 2))
print('\n')

# 논리연산
print(tf.logical_and(True, False))
print(tf.logical_or(True, False))
print(tf.logical_not(True))
print('\n')

# 유일 합집합
kbs = tf.constant([1,2,2,3,2])
val, idx = tf.unique(kbs)   # 유일값과 인덱스를 반환
print('val : ',val)
print('idx : ',idx)
print('\n')

# reduce ~ 함수
ar = [[1., 2.], [3., 4.]]
print(tf.reduce_mean(ar).numpy()) # 평균 : 차원 축소
print(tf.reduce_mean(ar, axis=0).numpy()) # 열 기준
print(tf.reduce_mean(ar, axis=1).numpy()) # 행 기준
print(tf.reduce_max(ar).numpy()) # 최대값
print('\n')

# reshape 함수
t = np.array([[[0, 1, 2], [3, 4, 5]], [[6, 7, 8], [9, 10, 11]]])
print(t.shape)
print(tf.reshape(t, shape=[12]))    # [ 0  1  2  3  4  5  6  7  8  9 10 11]
print(tf.reshape(t, shape=[2, 6]))  # [[ 0  1  2  3  4  5] [ 6  7  8  9 10 11]]
print(tf.reshape(t, shape=[-1, 6])) # 행 개수 자동 결정
print(tf.reshape(t, shape=[2, -1])) # 열 개수 자동 결정
print('\n')

# squeeze 함수
# 차원 축소(열 요소가 1인 배열의 경우 차원 제거)
print(tf.squeeze(t))   # 열 요소가 1이 아니라 차원 축소X  
t2 = np.array([[[0], [3], [6], [9]]])
print(t2.shape) # (1, 4, 1)
print(tf.squeeze(t2))   # shape=(4,)
print('\n')

# expand 함수 : 차원 확대
tarr = tf.constant([[1, 2, 3], [4, 5, 6]])
print(tarr.shape)
sbs = tf.expand_dims(tarr, 0)   # 첫번째 차원을 추가해 확장 - 맨 앞
print(sbs.numpy())
sbs = tf.expand_dims(tarr, 1)   # 두번째 차원을 추가해 확장 - 중간
print(sbs.numpy())
sbs = tf.expand_dims(tarr, 2)   # 세번째 차원을 추가해 확장 - 맨 뒤
print(sbs.numpy())
sbs = tf.expand_dims(tarr, -1)  # 마지막 차원을 추가해 확장
print(sbs.numpy())
print('\n')

# cast 함수 : 자료형 변환
num = tf.constant([1, 2, 3])    # int type
num2 = tf.cast(num, tf.float32)
print(num2, num2.dtype)