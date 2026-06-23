# 배열의 행, 열 추가 등등....

import numpy as np

aa = np.eye(3)
print(aa)

bb = np.c_[aa, aa[2]]       # 2열과 동일한 열 추가
print(bb)

cc = np.r_[aa, [aa[2]]]     # 2행과 동일한 행 추가
print(cc)

print('--append, insert, delete--')
a = np.array([1,2,3])
print(a)
# b = no.append(a, [4, 5])
b = np.append(a, [4, 5], axis=0)        # 요소 추가 (1차원 배열이므로 행 기준)
print(b)
c = np.insert(a, 0, [6, 7])             # 0번 인덱스 위치에 요소 삽입
print(c)
d = np.delete(a, 1)                     # 1번 인덱스 요소 삭제
print(d)

print('====================')
aa = np.arange(1, 10).reshape(3, 3)
print(aa)
print(np.insert(aa, 1, 99))         # axis가 없으면 차원이 축소
print(np.insert(aa, 1, 99, axis=0))  # 차원 유지, 행기준
print(np.insert(aa, 1, 99, axis=1))     # 열기준


print('====================')
# 조건 연산 where(조건, 참, 거짓)
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
conditionData = np.array([True, False, True])
result = np.where(conditionData, x, y)  # 조건이 True면 x, False면 y의 요소를 선택
print(result)  # [1 5 3] (첫 번째와 세 번째는 x에서, 두 번째는 y에서 가져옴)

print('====================')
aa = np.where(x >= 2)
print(aa)       # (array([1, 2]), ) -> 조건을 만족하는 요소의 '인덱스'를 튜플 형태로 반환
print(x[aa])    # [2 3]

print('====================')
# 배열 결합
kbs = np.concatenate([x, y])    # 1차원 배열 결합
print(kbs)
# 배열 분할
mbc, sbs = np.split(kbs, 2)     # 1차원 배열 분할
print(mbc)
print(sbs)

print('====================')
a = np.arange(1, 17).reshape(4, 4)
print(a)
# 배열 좌우로 분할 - 반으로 나눠서 분할
x1, x2 = np.hsplit(a, 2)
print(x1)
print(x2)
# 배열 상하로 분할  - 반으로 나눠서 분할
y1, y2 = np.vsplit(a, 2)
print(y1)
print(y2)

print('====================')
print('표본 추출(sampling) - 복원, 비복원\n')
# 표본 추출(Sampling): 전체 데이터에서 일부를 뽑아내는 과정
li = np.array([1, 2, 3, 4, 5, 6, 7])
print(li)

# 1. 복원 추출(Replacement): 뽑았던 것을 다시 넣고 뽑음 (중복 허용)
for _ in range(5):
    # randint(시작, 끝-1)를 이용해 무작위 인덱스를 생성하여 추출
    print(li[np.random.randint(0, len(li))], end=' ')
print()

# 2. 비복원 추출(No Replacement): 한 번 뽑은 것은 다시 뽑지 않음 (중복 불가)
# np.random.choice(배열, 개수) 사용
for _ in range(5):
    print(np.random.choice(li, 1), end=' ') # 1개씩 5번 독립적으로 추출 (여기서는 개별 호출이라 중복 가능성 있음)
print()

# 3. np.random.choice의 replace 옵션 활용
print(np.random.choice(range(1, 46), 6))                # 기본값은 replace=True (복원 추출)
print(np.random.choice(range(1, 46), 6, replace=True))  # 명시적 복원 추출 (중복 허용)
print(np.random.choice(range(1, 46), 6, replace=False)) # 명시적 비복원 추출 (로또 번호처럼 중복 없음)

# 4. 파이썬 기본 random 모듈 사용 (비복원 추출)
import random
print(random.sample(li.tolist(), 5))  # random.sample()은 리스트 타입을 대상으로 비복원 추출 수행

print('====================')