from pandas import DataFrame, Series, set_option
import numpy as np

set_option('display.max_columns', None)
set_option('display.max_rows', None)
set_option('display.width', None)


# pandas 문제 1)

#   a) 표준정규분포를 따르는 9 X 4 형태의 DataFrame을 생성하시오. 

#      np.random.randn(9, 4)
arr = DataFrame(np.random.randn(9, 4))
print(arr)
print()

#   b) a에서 생성한 DataFrame의 칼럼 이름을 - No1, No2, No3, No4로 지정하시오
arr = DataFrame(np.random.randn(9, 4), columns=['No1', 'No2', 'No3', 'No4'])
print(arr)
# 더 좋은 풀이: arr.columns = ['No1', 'No2', 'No3', 'No4'] (기존 객체의 컬럼명만 변경 시 효율적)
print()

#   c) 각 컬럼의 평균을 구하시오. mean() 함수와 axis 속성 사용
arrmean = arr.mean(axis=0)
print(arrmean)
print()

print('------------------')

# pandas 문제 2)
# a) DataFrame으로 위와 같은 자료를 만드시오. colume(열) name은 numbers, row(행) name은 a~d이고 값은 10~40.
arr = DataFrame(np.arange(10,50,10).reshape(4, 1), index=['a', 'b', 'c', 'd'], columns=['numbers'])
print(arr)
print()

# b) c row의 값을 가져오시오
print(arr.loc['c',:])
print()

# c) a, d row들의 값을 가져오시오.
print(arr.iloc[[0,3], :])
# 더 좋은 풀이: print(arr.loc[['a', 'd']]) (라벨을 알고 있다면 loc이 가독성이 좋음)
print()


# d) numbers의 합을 구하시오.
print(arr.sum(axis=0))
print()
# 원래는 arr.numbers.sum()을 해줘야 한다

# e) numbers의 값들을 각각 제곱하시오. 아래 결과가 나와야 함.
print(arr.mul(arr))
# 더 좋은 풀이: print(arr ** 2) (산술 연산자를 사용하는 것이 더 직관적임)
print()

# f) floats 라는 이름의 칼럼을 추가하시오. 값은 1.5, 2.5, 3.5, 4.5    아래 결과가 나와야 함.
arr = DataFrame(arr, index=['a', 'b', 'c', 'd'], columns=['numbers', 'floats'])
arr['floats']='1.5', '2.5', '3.5', '4.5'
print(arr)
# 더 좋은 풀이: arr['floats'] = [1.5, 2.5, 3.5, 4.5] (기존 df에 바로 컬럼 추가)
print()

# g) names라는 이름의 다음과 같은 칼럼을 위의 결과에 또 추가하시오. Series 클래스 사용.
names = Series(['길동', '오정', '팔계', '오공'], index=['d', 'a','b', 'c'])
print(names)
arr = DataFrame(arr, index=['a', 'b', 'c', 'd'], columns=['numbers', 'floats', 'names'])
print(arr)
arr['names'] = names
print(arr)
print()

print('------------------')

# pandas 문제 3)

# 1) 5 x 3 형태의 랜덤 정수형 DataFrame을 생성하시오. (범위: 1 이상 20 이하, 난수)
arr = DataFrame(np.random.randint(1, 21, 15).reshape(5, 3))
print(arr)
print()

# 2) 생성된 DataFrame의 컬럼 이름을 A, B, C로 설정하고, 행 인덱스를 r1, r2, r3, r4, r5로 설정하시오.
arr.columns = ['A', 'B', 'C']
arr.index = ['r1', 'r2', 'r3', 'r4', 'r5']
print(arr)
print()

# 3) A 컬럼의 값이 10보다 큰 행만 출력하시오.
print(arr[arr['A'] > 10])
print()

# 4) 새로 D라는 컬럼을 추가하여, A와 B의 합을 저장하시오.
d = arr['A'].add(arr['B'])
print(d)
# 더 좋은 풀이: arr['D'] = arr['A'] + arr['B']
arr['D'] = d
print(arr)
print()

# 5) 행 인덱스가 r3인 행을 제거하되, 원본 DataFrame이 실제로 바뀌도록 하시오.
arr.drop('r3', inplace=True)
print(arr)
print()

# 6) 아래와 같은 정보를 가진 새로운 행(r6)을 DataFrame 끝에 추가하시오.
#          A     B    C     D
#     r6   15   10    2   (A+B)
arr.loc['r6'] = [15, 10, 2, 0]
d = arr['A'].add(arr['B'])
arr['D'] = d
# 더 좋은 풀이: arr.loc['r6'] = [15, 10, 2, 15 + 10] (추가 시점에 바로 계산하여 대입)
print(arr)
print()

print('------------------')

# pandas 문제 4)
data = {
    'product': ['Mouse', 'Keyboard', 'Monitor', 'Laptop'],
    'price':   [12000,     25000,      150000,    900000],
    'stock':   [  10,         5,          2,          3 ]
}

# 1) 위 딕셔너리로부터 DataFrame을 생성하시오. 단, 행 인덱스는 p1, p2, p3, p4가 되도록 하시오.
arr = DataFrame(data=data, index=['p1', 'p2', 'p3', 'p4'])
print(arr)
print()

# 2) price와 stock을 이용하여 'total'이라는 새로운 컬럼을 추가하고, 값은 'price x stock'이 되도록 하시오.
tot = arr['price'].mul(arr['stock'])
arr['total'] = tot
# 더 좋은 풀이: arr['total'] = arr['price'] * arr['stock']
print(arr)
print()

# 3) 컬럼 이름을 다음과 같이 변경하시오. 원본 갱신
#    product → 상품명,  price → 가격,  stock → 재고,  total → 총가격
arr.columns = ['상품명', '가격', '재고', '총가격']
print(arr)
# 더 좋은 풀이: arr.rename(columns={'product':'상품명', ...}, inplace=True) (특정 컬럼만 바꿀 때 유용)
print()

# 4) 재고(재고 컬럼)가 3 이하인 행의 정보를 추출하시오.
print(arr[arr['재고'] <= 3])
print()

# 5) 인덱스가 p2인 행을 추출하는 두 가지 방법(loc, iloc)을 코드로 작성하시오.
print(arr.loc['p2'])
print(arr.iloc[1])
print()

# 6) 인덱스가 p3인 행을 삭제한 뒤, 그 결과를 확인하시오. (원본이 실제로 바뀌지 않도록, 즉 drop()의 기본 동작으로)
imsi = arr.drop('p3', axis=0)
print(imsi)
print()

# 7) 위 DataFrame에 아래와 같은 행(p5)을 추가하시오.
#             상품명             가격     재고    총가격
#  p5       USB메모리    15000     10    가격*재고
arr.loc['p5'] = ['USB메모리', 15000, 10, 0]
tot = arr['가격'].mul(arr['재고'])
arr['총가격'] = tot
print(arr)
# 더 좋은 풀이: arr.loc['p5'] = ['USB메모리', 15000, 10, 15000 * 10]
print('------------------')