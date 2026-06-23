# tf.constant()
# tf.Variable()
# autograph 기능

import tensorflow as tf

node1 = tf.constant(3, dtype=tf.float32)    # 데이터 타입 지정 가능 [문법] tf.constant()는 변경 불가능한 상수를 생성합니다.
node2 = tf.constant(4.0)    # 실수를 주면 알아서 실수가 됨(지정해주는게 좋음) [문법] dtype을 명시하지 않으면 입력값에 따라 자동 추론됩니다.
print(node1)
print(node2)
# tf.Tensor(3.0, shape=(), dtype=float32)
# tf.Tensor(4.0, shape=(), dtype=float32)
print('\n')

adddata = tf.add(node1, node2)
print('adddata : ', adddata)
# adddata :  tf.Tensor(7.0, shape=(), dtype=float32)
print('\n')

node3 = tf.Variable(3, dtype=tf.float32) # [문법] tf.Variable은 학습 가능한 파라미터(Weight, Bias 등)를 저장할 때 사용합니다.
node4 = tf.Variable(4.0) # [문법] 초기값을 기반으로 형태(Shape)와 타입(DType)이 결정됩니다.
print(node3)
print(node4)
# <tf.Variable 'Variable:0' shape=() dtype=float32, numpy=3.0>
# <tf.Variable 'Variable:0' shape=() dtype=float32, numpy=4.0>
print('\n')

imsi1 = tf.add(node3, node4)    # imsi 변수를 tensor 더하기 연산 [문법] Variable 객체도 Tensor 연산 함수에 인자로 전달될 수 있습니다.
print(imsi1)    # tf.Tensor(7.0, shape=(), dtype=float32)
print('\n')

node4.assign_add(node3)     # node4 변수에 더하기 후 치환 [문법] .assign_add()는 기존 메모리 위치에서 값을 누적하여 업데이트합니다.
print(node4)    # <tf.Variable 'Variable:0' shape=() dtype=float32, numpy=7.0>
print('\n')

a = tf.constant(5)
b = tf.constant(10) 
# 조건 처리 → tf.cond(조건, 함수 1, 함수 2)
result = tf.cond(a < b, lambda: tf.add(10, a), lambda:tf.square(a)) # [문법] tf.cond는 텐서플로 그래프 내에서 조건 분기를 실행합니다.
print('result : ', result)      # result :  tf.Tensor(15, shape=(), dtype=int32)
# result = tf.cond(a < b, tf.add(10, a), tf.square(a))
# ↪ Error : 함수를 주지 않으면 안됨
print('\n')

# Autograph 기능
# : 파이썬 코드를 텐서플로 그래프(Graph) 코드(그래프 연산)로 자동 변환

# Tensorflow의 두 가지 실행 방법
# 1) Eager Execution : 파이썬 코드 처럼 즉시 실행(기본)
# 2) Graph Execution : 별도 운영이 가능한 계산 그래프를 만들어 최적화 후 실행(Tensor 처리에 효율적)

@tf.function        # Autograph가 개입함 → Tensorflow 그래프 연산을 함 [문법] @tf.function 데코레이터는 파이썬 함수를 호출 가능한 텐서플로 그래프로 컴파일합니다.
def calcFunc1(a, b):        # 위 tf.cond()를 Autograph 사용한 경우
    if (a < b):
        return tf.add(10, a)
    else:
        return tf.square(a)
result_autograph = calcFunc1(a, b)
print('result_autograph : ', result_autograph)
# result_autograph :  tf.Tensor(15, shape=(), dtype=int32)
print('\n')

# [참고]
# @tf.function 안에서 if, for, while, break, continue, return 등을 사용하면 Autograph가 개입하여 제어 흐름을 텐서 연산으로 변환합니다.

# <반복문 처리>
@tf.function
def culcFunc2(n):
    sum = tf.constant(0)
    for i in tf.range(n + 1): # [문법] tf.range()를 사용하면 그래프 모드에서 효율적인 루프로 변환됩니다.
        sum += i
    return sum

print('sum : ', culcFunc2(10))
# sum :  tf.Tensor(55, shape=(), dtype=int32)
print('\n')


# <1부터 3까지 증가>
imsi = tf.constant(0)
# ↪ 전역변수 처리 해주지 않으면 Error 떨어짐
su = tf.Variable(1)
# ↪ tf 변수는 @tf.function 밖에서 선언해야 함
@tf.function
def culcFunc3():
    # imsi = tf.constant(0)
    global imsi                 # imsi가 local이 아님을 알림 [문법] 함수 외부의 텐서를 수정하기 위해 global 키워드를 사용합니다.
    # su = tf.Variable(1) → Autograph에서는 구조가 고정적이어야 함 [문법] tf.Variable은 함수 내부에서 매번 생성할 수 없으며 외부에서 정의되어야 합니다.
    # su = 1
    for _ in range(3):
        # imsi = imsi + su → 파이썬 연산자를 사용한 것
        imsi = tf.add(imsi, su)    # → Tensorflow 연산자를 사용한 것 ⇨ 권장하는 방법 [추천] 명시적인 tf 연산자 사용은 그래프 최적화에 유리합니다.
    return imsi

print('imsi : ', culcFunc3())
# imsi :  tf.Tensor(3, shape=(), dtype=int32)
print('\n')

# <구구단 3단 출력>
@tf.function
def calcFunc4(dan):
    for i in range(1, 10):
        result = tf.multiply(dan, i)
        # tf.print('{}*{}={:2}'.format(dan, i, result)) → Tensor를 문자열 포맷팅에 직접 넣음 ⇨ 에러 [문법] tf.print는 파이썬 포맷팅과 직접 호환되지 않을 수 있습니다.
        tf.print(dan, '*', i, '=', result) # [문법] tf.print()는 그래프 실행 시점에 텐서의 값을 출력하기 위해 사용합니다.

calcFunc4(3)