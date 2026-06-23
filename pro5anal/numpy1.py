# numpy의 ndarray는 단순한 배열이라기 보다,
# 벡터 / 행렬 연산도 가능한 다차원 수치 데이터 구조다

import numpy as np

ss = ['tom', 'james', 'oscar', 1, True]     # 파이썬의 리스트는 여러종류의 타입을 넣을 수 있다
print(ss, ' ', type(ss))

ss2 = np.array(ss)
print(ss2, ' ', type(ss2))          # numpy는 모두 동일 타입의 데이터로 구성

li = list(range(1, 10))
print(li)
print(li[0], ' ', id(li[0]))        # 별도의 객체로 기억됨 -> 인덱스의 주소가 모두 다름
print(li * 10)          # li를 10번 반복함 _ 각 요소에 대한 곱 연산이 아님
print('======================')

for i in li:
    print(i * 10, end=' ')
print()

num_arr = np.array(li)
print(num_arr[0], ' ', num_arr[1], ' ',id(num_arr[0]), ' ', id(num_arr[1]))      # 인덱스의 주소가 같음
print(num_arr * 10)         # 10번 반복이 아니라 요소에 10이 곱해짐(for 문 없이도 가능)->계산 속도 빠름
# 벡터화 연산이 가능함

print('======================')
a = np.array([1, 2, 3.5], dtype='float32')
print(a, type(a))  # ndarray는 동일 타입만 취급
# 여러 타입의 자료가 입력되면 상위 타입으로 자동 변환. int -> float -> complex -> str

print('======================')
b = np.array([[1, 2, 3], [4, 5, 6]])
print(b, b.shape, ' ', b[0 ,0], ' ', b[[0]])

print('======================')
c = np.zeros((2,2))     # 0으로 채워진 2x2 배열 생성
print(c)
d = np.ones((2,2))      # 1로 채워진 2x2 배열 생성
print(d)
e = np.eye(3)           # 3x3 단위 행렬(주대각선이 1인 행렬) 생성
print(e)
f = np.full((2,2), 7)   # 지정한 값(7)으로 채워진 2x2 배열 생성
print(f)

print('======================')
# 난수 생성
print(np.random.rand(5))    # 균등 분포
print(np.random.randn(5))       # 정규 분포

print(np.random.randn(2, 3))        # 실행할 때마다 값이 바뀜
np.random.seed(0)
print(np.random.randn(2, 3))        # 실행할 때마다 값이 바뀌지 않음

print('======================')
print(list(range(0,10)))    # 파이썬 기본 range: 0부터 9까지 리스트 생성
print(np.arange(10))        # numpy의 arange: 0부터 9까지 ndarray 생성

print('======================')
# 인덱싱 / 슬라이싱
a = np.array([1, 2, 3, 4, 5])
print(a, ' ', a[1])     # 전체 배열과 1번 인덱스 요소 출력
print(a[1:4])           # 1번부터 3번 인덱스까지 슬라이싱
print(a[1:])            # 1번 인덱스부터 끝까지
print(a[1:5:2])         # 1번부터 4번까지 2개씩 건너뛰며 추출
print(a[:3])            # 처음부터 2번 인덱스까지
print(a[:])             # 전체 요소

print('======================')
b = a                   # 얕은 복사 (주소값 복사)
print(a[0], ' ', b[0])
b[0] = 88               # b를 수정하면 원본 a도 함께 수정됨
print(a[0], ' ', b[0])  # 같은 결과 : 주소를 참조하기 때문
c = np.copy(a)              # 복사본 생성
print(a[0], ' ', c[0])
c[0] = 33               # c를 수정해도 원본 a는 변하지 않음
print(a[0], ' ', c[0])  # 깊은 복사: 실제 값을 별도 메모리에 복사함

print('======================')
