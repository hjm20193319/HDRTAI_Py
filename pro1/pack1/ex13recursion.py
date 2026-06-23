# 재귀 함수 : 함수가 자기 자신을 호출 - 반복 처리

def countDown(n):
    if n == 0:
        print('완료')
    else:
        print(n, end = ' ')
        countDown(n-1)          # 재귀 처리

countDown(5)

print('end')
print('\n==================================\n')

# 1 부터 n 까지 합

def totFunc(n):
    if n == 0:
        print('탈출')
        return 1
    return n + totFunc(n -1)        # 재귀 처리 >> 함수를 순서대로 호출을 먼저 한 다음 계산이 이루어짐
'''
호출 : totFunc(5) -> 5 + totFunc(4) -> 4 + totFunc(3) -> 3 + totFunc(2) -> 2 + totFunc(1) -> '탈출' , 1
계산 :    16     <-   5+ (4+3+2+1)   <-    4+ (3+2+1)  <-   3+(2+1)    <-   2+1
'''

result = totFunc(5)
print('result : ', result)

print('\nend')
print('\n==================================\n')

# 5 factorial 계승

def factFunc(a):
    if a == 1: return 1
    print(a)
    return a * factFunc(a - 1)

result2 = factFunc(5)           # 계산량이 많아지면 메모리 공간을 많이 차지해서 Error 뜸
print('result2 : ', result2)

# 재귀 함수는 호출이 먼저고 계산은 나중에 한다는걸 기억!!
# 마지막 요소를 제외한 나머지를 계산해주는 방식으로 구하면 될 것 같다
