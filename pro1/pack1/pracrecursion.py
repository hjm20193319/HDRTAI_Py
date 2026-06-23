# 재귀 함수 연습 

# 리스트의 합을 구하는 문제
'''
v = [10, 2, 5, 8, 20]

def find_sum(a, n):
    if n == 1:
        return a[0]
    return a[n-1] + find_sum(a, n-1)

print(find_sum(v, len(v)))
print(sum(v))
'''

# 연속된 숫자 출력

print('1~2000 사이 정수를 입력해 : ')