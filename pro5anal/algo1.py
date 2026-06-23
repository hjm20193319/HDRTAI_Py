# 알고리즘은 특정 문제를 해결하기 위한 명확하고 단계적인 절차나 규칙의 집합 
# 입력값을 받아 유한한 시간 내에 정해진 논리적 순서에 따라 문제를 해결하고 결과물을 도출하는 과정으로, 
# 컴퓨터 프로그래밍 및 일상생활의 문제 해결(예: 요리법)에 모두 적용

# 1부터 n까지 연속한 숫자의 합을 구하는 알고리즘 (반복문 방식)
# 시간 복잡도: O(n) - n의 크기에 비례하여 연산 횟수가 증가함
def sum_n(n):
    s = 0                           # 합계를 저장할 변수 초기화
    for i in range(1, n+1):         # range(시작, 끝+1): 1부터 n까지 반복
        s = s + i                   # 기존 합계에 현재 숫자 i를 더함 (누적합)
    return s                        # 최종 결과 반환

print(sum_n(10))
print(sum_n(100))

# 가우스의 합공식 사용하기 (수학적 접근)
# 시간 복잡도: O(1) - n의 크기와 상관없이 단 한 번의 계산으로 끝남 (효율적)
def sum_n2(n):
    # // 연산자: 나눗셈의 결과에서 소수점 이하를 버리고 정수 몫만 구함 (Floor Division)
    return n * (n + 1) // 2         # 공식: n(n+1)/2

print(sum_n2(10))
print(sum_n2(100))
print('\n')

# 최대값 구하기 알고리즘
# 리스트의 첫 번째 원소를 기준으로 순차적으로 비교하는 방식 (Sequential Search 기반)
d = [17, 92, 33, 58, 7, 32, 42]     # 대상 리스트(Iterable 객체)
def find_max(a):
    n = len(a)                      # 리스트의 전체 요소 개수 파악
    max_v = a[0]                    # 첫 번째 요소를 초기 최대값으로 가정
    for i in range(1, n):           # 두 번째 요소(인덱스 1)부터 마지막까지 비교
        if a[i] > max_v:            # 현재 요소가 기존 최대값보다 크다면
            max_v = a[i]            # 최대값을 현재 요소로 교체 (Update)
    return max_v                    # 루프 종료 후 최종 최대값 반환

print(find_max(d))
print('\n')

# 최대공약수 구하기 알고리즘
# 예) 4, 6 : 4와 6은 2로 모두 나누어 떨어지므로 2(GCD) 
# GCD: Greatest Common Divisor
def gcdFunc(a, b):
    i = min(a, b)                   # 두 수 중 더 작은 값을 시작점으로 설정 (공약수는 작은 수보다 클 수 없음)
    # while True: 무한 루프 구조, 내부에서 return을 만나면 함수가 종료됨
    while True:
        # % 연산자: 나머지 연산. 나머지가 0이면 나누어 떨어진다는 의미
        if a % i == 0 and b % i == 0:
            return i                # 두 수를 동시에 나누어 떨어뜨리는 가장 큰 i를 찾으면 즉시 반환
        i = i - 1                   # 찾지 못했다면 1씩 감소시키며 확인 (Brute-force 방식)

print(gcdFunc(4, 6))
print(gcdFunc(24, 16))
print(gcdFunc(81, 27))
print('\n')

# 최대공약수 구하기 알고리즘 2 - 유클리드 방식
# 유클리드 호제법: a를 b로 나눈 나머지 r에 대해, GCD(a, b) = GCD(b, r)임을 이용
def gcdFunc2(a, b):
    if b == 0:                      # 종료 조건(Base Case): 나머지가 0이 되는 순간의 나누는 수가 GCD
        return a                    # b가 0이 되면 a가 최대공약수임
    # 재귀 호출(Recursive Call): 함수 내부에서 자기 자신을 다시 호출
    return gcdFunc2(b, a % b)       # (나누는 수, 나머지)를 인자로 전달하여 반복 수행

print(gcdFunc2(4, 6))
print(gcdFunc2(24, 16))
print(gcdFunc2(81, 27))
print('\n')