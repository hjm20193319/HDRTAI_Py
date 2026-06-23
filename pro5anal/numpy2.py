# 배열 연산

import numpy as np

x = np.array([[1, 2], [3, 4]])
print(x.dtype)

x = np.array([[1, 2], [3, 4]], dtype=np.float64)
print(x.dtype)

x = np.array([[1, 2], [3, 4]], dtype=np.complex128)
print(x.dtype)


y = np.arange(5, 9)     # 1차원 배열
print(y)

y = np.arange(5, 9).reshape(2, 2)   # 구조 변경 1차원 -> 2차원 배열
print(y, ' ', y.dtype)
y = y.astype(np.float32)            # 타입 변경
print(y, ' ', y.dtype)

print('======================')
x = np.array([[1, 2], [3, 4]], dtype=np.float64)
print(x + y)        # 파이썬 연산자 또는 함수 (속도 느림)
print(np.add(x, y))     # numpy 함수 - universial function (속도 빠름)
print(x-y)
print(np.subtract(x, y))
print(x*y)
print(np.multiply(x, y))
print(x/y)
print(np.divide(x, y))

print(np.sqrt(x))

print('======================')
print('\ndot은 numpy 모듈의 함수나 배열 객체의 인스턴트 매소드로 사용이 가능')
v = np.array([9, 10])
w = np.array([11, 12])

print(v * w)    # 요소별 곱셈 => 9*11 10*12

# 두 벡터의 내적 (행렬 곱)
print(v.dot(w))     # 내적의 결과는 스칼라(크기만) => 9*11 + 10*12
print(np.dot(v, w))    
print(np.dot(x,v))      # x는 2차원이기 때문에 2개의 값이 나옴

print('======================')

# 배열 계산 함수 
print(x)
print(np.mean(x), ' ', np.var(x))
print(np.max(x), ' ', np.min(x))            # 최대값, 최소값 을 리턴
print(np.argmax(x), ' ', np.argmin(x))      # 최대값, 최소값의 인덱스를 리턴

print(np.cumsum(x))     # 누적합
print(np.cumprod(x))    # 누적곱

print('======================')
names1 = np.array(['tom', 'james', 'tom', 'oscar'])
names2 = np.array(['tom', 'page', 'john'])
print(np.unique(names1))    # 중복제거  
print(np.intersect1d(names1, names2))   # 교집합
print(np.intersect1d(names1, names2, assume_unique=True))   # 교집합, 중복허용 옵션
print(np.union1d(names1, names2))       # 합집합

print('======================')
print('전치(Transpose) - 2차원 배열에서 행과 열을 바꿈\n')
print(x)
print(x.T)              # T 속성을 이용한 전치
print(x.transpose())    # transpose() 메소드 사용
print(x.swapaxes(0, 1)) # 축(axis)을 서로 맞바꿈 (0번 축과 1번 축 교환)

print('======================')
print('Broadcasting : 크기가 다른 배열 간의 연산 - 작은 배열을 여러번 반복해 큰 배열과 연산\n')
x = np.arange(1, 10).reshape(3, 3)
y = np.array([1, 0, 1])
print(x)
print(y)        # x 와 y 의 구조가 다름
print(x + y)    # 큰 배열에 맞게 크기 자동 조정

np.savetxt('my.txt', x)     # 배열 file i/o  loadtxt()