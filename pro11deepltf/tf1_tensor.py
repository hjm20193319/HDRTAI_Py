import numpy as np
import tensorflow as tf

print(tf.__version__)  # 설치된 텐서플로의 버전을 확인합니다.

print('즉시 실행 모드 : ', tf.executing_eagerly())  # TF2.0부터는 기본적으로 True이며, 그래프 생성 없이 즉시 연산 결과를 반환합니다.
print('GPU 사용 정보 : ', tf.config.list_physical_devices('GPU'))  # 현재 환경에서 텐서플로가 인식한 GPU 장치 목록을 출력합니다.
print('\n')

print('---------------------------')
# Tensor
# : Tensorflow 에서 데이터를 담는 기본 자료구조
# : 숫자 데이터 저장용 다차원 배열

# ndarray와 유사하지만, Tensorflow 에서 연산에 사용되도록(특화된) 만들어진 객체

print(12, type(12))   # 파이썬 상수로, 파이썬이 직접 계산 [문법] int 타입의 스칼라 값입니다.
print(tf.constant(12))   # 0d 텐서 (0차원) → Scaler [문법] tf.constant()는 변경 불가능한(Immutable) 텐서를 생성합니다.
print(tf.constant([12]))    # 1d 텐서 → Vector [문법] 리스트를 전달하여 1차원 배열 형태의 텐서를 생성합니다.
print(tf.constant([[12]]))  # 2d 텐서 → Matrix [문법] 중첩 리스트를 통해 행렬 형태의 텐서를 생성합니다.
print(tf.constant([[12, 1]])) # 1행 2열의 2차원 텐서입니다.
print('\n')

print(tf.rank(tf.constant([[12, 1]])))  # tf.Tensor(2, shape=(), dtype=int32) [문법] tf.rank는 텐서의 차원(Rank)을 반환합니다.
tf.print(tf.constant(12))   # 12 [문법] tf.print()는 텐서 내부의 실제 값만을 깔끔하게 출력할 때 사용합니다.
print('\n')

# 파이썬 기본함수 print(): 객체 자체를 문자열로 변환 후 출력, 정보(dtype, shape 등) 중심 출력
# Tensorflow 전용 출력 함수 tf.print(): 텐서 실제값을 중심으로 출력

imsi = np.array([1, 2])     # 일반 수치 연산(CPU 연산이 기본, 미분 불가, 값 변경 가능) [문법] 넘파이 배열은 가변(Mutable) 객체입니다.
print(type(imsi))           # <class 'numpy.ndarray'> 
imsi[0] = 10         # 값 변경 가능 [문법] 인덱싱을 통한 직접적인 요소 수정이 가능합니다.
a = tf.constant([1, 2])     # 딥러닝 연산(GPU 연산도 가능, 자동 미분 가능, 값 변경 불가능) [문법] 텐서는 불변(Immutable) 객체입니다.
print(type(a))              # <class 'tensorflow.python.framework.ops.EagerTensor'> 
a = a + 10           # 값 변경 불가능 [문법] 기존 텐서를 수정하는 것이 아니라 연산 결과로 새로운 텐서를 생성하여 'a'에 재할당하는 것입니다.
b = tf.constant([3, 4])

c = a + b   # 텐서 요소값 더하기(열단위 연산)   → 사칙 연산 모두 가능 [문법] Element-wise(요소별) 연산이 수행됩니다.
tf.print(c)

d = tf.constant([3])
e = c + d   # [추천] # tf.add(c, d)를 사용하면 명시적인 텐서 연산임을 나타낼 수 있습니다.
tf.print(e)     # [7, 9] Broadcast 연산 [문법] 크기가 다른 텐서 간의 연산 시 작은 쪽의 크기를 큰 쪽에 맞춰 확장하여 연산합니다.
print('\n')

# 넘파이와 텐서플로 형변환 가능
print(tf.convert_to_tensor(7))  # tf.Tensor(7, shape=(), dtype=int32) [문법] 파이썬 객체나 넘파이 배열을 텐서로 변환합니다.
print(tf.constant(7).numpy())   # 7 [문법] .numpy() 메서드를 호출하여 텐서를 넘파이 배열(또는 스칼라)로 변환합니다.
print('\n')

arr = np.array([1, 2])      # ndarray
# tf.add(), tf.subtract(), tf.multiply(), tf.divide() 가능
tfarr = tf.add(arr, 5)      # 텐서 연산을 하면 텐서 타입으로 자동 형변환됨 [문법] 넘파이 배열이 텐서 연산 함수에 들어가면 암시적으로 텐서로 변환됩니다.
print(tfarr)                # tf.Tensor([6 7], shape=(2,), dtype=int64)
print(np.add(tfarr, 2))     # [8 9] ⇨ 배열 연산을 하면 넘파이 타입으로 자동 형변환됨 [문법] 넘파이 함수에 텐서가 들어가면 넘파이 배열로 자동 변환되어 처리됩니다.
print('\n')

# Tensorflow 로 변수 선언 후 사용하기
# tf.Variable() → Tensorflow에서 값이 바뀔 수 있는 텐서를 만들 때 사용.
# 예) weight, bias ...
v1 = tf.Variable(1.0)   # 변수에 값 기억 [문법] tf.Variable은 학습 과정에서 업데이트되는 파라미터를 저장하는 용도입니다.
tf.print('v1 : ', v1)
v2 = tf.Variable(tf.ones((2, )))    # 1로 채워진 변수 [문법] tf.ones()는 모든 요소가 1인 텐서를 생성합니다.
tf.print('v2 : ', v2)
v3 = tf.Variable(tf.zeros((2, )))   # 0으로 채워진 변수 [문법] tf.zeros()는 모든 요소가 0인 텐서를 생성합니다.
tf.print('v3 : ', v3)
# v1 :  1
# v2 :  [1 1]
# v3 :  [0 0]

# Tensor 치환 연산
# - 값 변경
v1.assign(123)  # [문법] .assign() 메서드를 사용하여 Variable의 값을 덮어씁니다.
tf.print('v1 : ', v1)   # v1 :  123
# v1 = 123 ⇨ Error [문법] 파이썬 변수 할당(=)을 사용하면 텐서 객체 자체가 파이썬 상수로 대체되어 텐서의 특성을 잃게 됩니다.
v2.assign([30, 40]) # [문법] 기존 v2의 shape(2,)와 일치하는 리스트를 할당해야 합니다.
tf.print('v2 : ', v2)   # v2 :  [30 40]
print('\n')

aa = tf.Variable(tf.zeros((2,1)))     # 2행 1열에 모두 0을 기억 [문법] 2차원 형태의 변수를 생성합니다.
tf.print('aa : \n', aa)
aa.assign(tf.ones((2,1)))   # 2행 1열에 모두 1을 기억하도록 값 변경 [문법] assign 시에도 shape이 유지되어야 합니다.
tf.print('aa : \n', aa)

# - 더하기 할당(치환) : assign_add
aa.assign_add([[2], [3]]) # [문법] aa = aa + [[2], [3]]과 유사하지만, 메모리 주소를 유지하며 값을 업데이트합니다.
tf.print('aa : \n', aa)     # aa : [[3] [4]]

# - 빼기 할당(치환) : assign_sub
aa.assign_sub([[2], [3]]) # [문법] 기존 값에서 인자로 받은 값을 뺀 후 다시 할당합니다.
tf.print('aa : \n', aa)     # aa : [[1] [1]]

# - 곱하기 나누기는 따로 메서드 없음
aa.assign(aa * [[2], [3]]) # [문법] 연산 결과를 다시 assign()으로 덮어씌우는 방식을 사용합니다.
tf.print('aa : \n', aa)     # aa : [[2] [3]]
aa.assign(aa / [[2], [3]])
tf.print('aa : \n', aa)     # aa : [[1] [1]]
print('\n')

# 난수 처리
print(tf.random.uniform([1], minval=0, maxval=1))   # 균등분포 ([shape], min, max) [문법] 지정된 범위 내에서 모든 값이 나올 확률이 동일하게 난수를 생성합니다.
print(tf.random.normal([3], 0, 1))   # 정규분포 ([shape], 평균, 표준편차) [문법] 평균이 0이고 표준편차가 1인 가우시안 정규분포에서 난수를 생성합니다.
# tf.Tensor([0.8674506], shape=(1,), dtype=float32)
# tf.Tensor([-0.98570293  0.16128401 -0.67076606], shape=(3,), dtype=float32)
print('\n')
print(tf.random.normal([3, 2], mean=0, stddev=1)) # 3행 2열의 행렬 형태로 정규분포 난수를 생성합니다.
# tf.Tensor(
# [[-0.538607   -0.6969211 ]
#  [ 0.2401047   0.54667675]
#  [-1.2590975  -2.4968183 ]], shape=(3, 2), dtype=float32)
print('\n')