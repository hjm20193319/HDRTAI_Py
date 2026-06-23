# * numpy의 array() 관련 연습문제 *

# 1) step1 : array 관련 문제

#  정규분포를 따르는 난수를 이용하여 5행 4열 구조의 다차원 배열 객체를 생성하고, 각 행 단위로 합계, 최댓값을 구하시오.

# < 출력 결과 예시>

# 1행 합계   : 0.8621332497162859

# 1행 최댓값 : 0.3422690004932227

# 2행 합계   : -1.5039264306910727

# 2행 최댓값 : 0.44626169669315

# 3행 합계   : 2.2852559938172514

# 3행 최댓값 : 1.5507574553572447
import numpy as np

aa = np.random.randn(5, 4)
print(aa)

for i in range(len(aa)):
    print(f"{i+1}행 합계   : {np.sum(aa[i])}")
    print(f"{i+1}행 최댓값 : {np.max(aa[i])}\n")

print()
# 방법 2
for a in aa.sum(axis=1):
    print(a)


print('====================\n')
# 2) step2 : indexing 관련문제

#  문2-1) 6행 6열의 다차원 zero 행렬 객체를 생성한 후 다음과 같이 indexing 하시오.

#    조건1> 36개의 셀에 1~36까지 정수 채우기

#    조건2> 2번째 행 전체 원소 출력하기 

#               출력 결과 : [ 7.   8.   9.  10.  11.  12.]

#    조건3> 5번째 열 전체 원소 출력하기

#               출력결과 : [ 5. 11. 17. 23. 29. 35.]

#    조건4> 15~29 까지 아래 처럼 출력하기

#               출력결과 : 

#               [[15.  16.  17.]

#               [21.  22.  23]

#               [27.  28.  29.]]
bb = np.zeros((6, 6))
print(bb)

# 조건 1
cnt = 0
for i in range(len(bb)):
    for j in range(len(bb)):
        cnt += 1
        bb[i,j] = cnt
print(bb)
print()

# 조건 2
print(bb[1, :])     # print(bb[1]) 와 같은 결과

# 조건 3
print(bb[:, 4])

# 조건 4
print(bb[2:5, 2:5])     # 2이상 5미만


print('========================')
#  문2-2) 6행 4열의 다차원 zero 행렬 객체를 생성한 후 아래와 같이 처리하시오.

#      조건1> 20~100 사이의 난수 정수를 6개 발생시켜 각 행의 시작열에 난수 정수를 저장하고, 두 번째 열부터는 1씩 증가시켜 원소 저장하기

#      조건2> 첫 번째 행에 1000, 마지막 행에 6000으로 요소값 수정하기

cc = np.zeros((6, 4))
print(cc)

ran = np.random.randint(20, 100, 6)         # 매번 바뀜
print(ran)

ran = list(ran)
for i in range(len(cc)):
    cc[i, 0] = ran[i]       # ran.pop(0) -> 0번째가 튀어나옴
    
    for j in range(3):
        cc[i, j+1] = ran[i] + j+1
print(cc)

# 조건 2
cc[0, :] = 1000
cc[5, :] = 6000
print(cc)

print('=========================')
# 3) step3 : unifunc 관련문제

#   표준정규분포를 따르는 난수를 이용하여 4행 5열 구조의 다차원 배열을 생성한 후

#   아래와 같이 넘파이 내장함수(유니버설 함수)를 이용하여 기술통계량을 구하시오.

#   배열 요소의 누적합을 출력하시오.

dd = np.random.randn(4, 5)
print(dd)
print('기술 통계량')
print('평균 : ', np.mean(dd))
print('합계 : ', np.sum(dd))
print('표준편차 : ', np.std(dd))
print('분산 : ', np.var(dd))
print('최대값 : ', np.max(dd))
print('최소값 : ', np.min(dd))

print('1사분위 수 : ', np.percentile(dd, 25))
print('2사분위 수 : ', np.percentile(dd, 50))
print('3사분위 수 : ', np.percentile(dd, 75))
print('요소 누적 합 : ', np.cumsum(dd))


print('============================')
# Q1) 브로드캐스팅과 조건 연산
# 다음 두 배열이 있을 때,
# a = np.array([[1], [2], [3]])
# b = np.array([10, 20, 30])
# 두 배열을 브로드캐스팅하여 곱한 결과를 출력하시오.
# 그 결과에서 값이 30 이상인 요소만 골라 출력하시오.

a = np.array([[1], [2], [3]])
b = np.array([10, 20, 30])
result = a * b  # 브로드캐스팅을 통한 곱셈 연산 (3x1 배열과 1x3 배열이 만나 3x3 결과 생성)
print(result)   # 연산 결과 출력
resultli = result[result >= 30]  # 불리언 인덱싱을 사용하여 30 이상인 요소만 추출
print(resultli) # 필터링된 결과 출력

print('---------------')
# Q2) 다차원 배열 슬라이싱 및 재배열
#  - 3×4 크기의 배열을 만들고 (reshape 사용),  
#  - 2번째 행 전체 출력
#  - 1번째 열 전체 출력
#  - 배열을 (4, 3) 형태로 reshape
#  - reshape한 배열을 flatten() 함수를 사용하여 1차원 배열로 만들기

aa = np.arange(1, 13)           # 1부터 12까지의 정수 배열 생성
print(aa)
bb = aa.reshape(3, 4)           # 3행 4열로 구조 변경
print(bb)
print(bb[1, :])                 # 2번째 행 전체 출력 (인덱스 1)
print(bb[:, 0])                 # 1번째 열 전체 출력 (인덱스 0)
dd = bb.reshape(4, 3)           # (4, 3) 형태로 다시 reshape
cc = dd.flatten()               # flatten()을 사용하여 1차원 배열로 평탄화, 차원 축소 함수
print(cc)

print('--------------')
# Q3) 1부터 100까지의 수로 구성된 배열에서 3의 배수이면서 5의 배수가 아닌 값만 추출하시오.
# 그런 값들을 모두 제곱한 배열을 만들고 출력하시오.

aa = np.arange(1, 101)
print(aa)
bb = (aa % 3 == 0) & (aa % 5 != 0)
aa = aa[bb]
print(aa)
aas = aa ** 2
print(aas)

print('-----------')
# Q4) 다음과 같은 배열이 있다고 할 때,
# arr = np.array([15, 22, 8, 19, 31, 4])
# 값이 10 이상이면 'High', 그렇지 않으면 'Low'라는 문자열 배열로 변환하시오.
# 값이 20 이상인 요소만 -1로 바꾼 새로운 배열을 만들어 출력하시오. (원본은 유지)
# 힌트: np.where(), np.copy()

aa = np.array([15, 22, 8, 19, 31, 4])

# np.where(조건, 참일때값, 거짓일때값): 조건에 따라 요소를 선택하여 새로운 배열 생성 (삼항 연산자 방식)
labels = np.where(aa >= 10, 'High', 'Low')
print(labels)

bb = np.copy(aa)  # 원본 배열 aa를 보호하기 위해 깊은 복사(Deep Copy) 수행
# 불리언 인덱싱(Boolean Indexing): 조건식(bb >= 20)이 True인 위치의 요소만 선택하여 -1 대입
bb[bb >= 20] = -1
print(bb)

print('-------------------')
# Q5) 정규분포(평균 50, 표준편차 10)를 따르는 난수 1000개를 만들고, 상위 5% 값만 출력하세요.
# 힌트 :  np.random.normal(), np.percentile()

# np.random.normal(loc, scale, size): 평균(loc)이 50이고 표준편차(scale)가 10인 정규분포 난수 1000개 생성
aa = np.random.normal(loc = 50, scale=10, size=1000)
print(aa)

# np.percentile(배열, 백분위수): 데이터의 하위 n% 지점의 값을 반환. 
# 상위 5%를 구하기 위해서는 하위 95% 지점(95 백분위수)을 기준으로 잡아야 함
threshold = np.percentile(aa, 95)
# 불리언 인덱싱: 생성된 난수 배열 aa에서 threshold(95번째 백분위수)보다 큰 값들만 필터링
top5 = aa[aa > threshold]
print('상위 5% 값은 : ', top5)