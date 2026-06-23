# 리스트 자료 v = [7, 9, 15, 43, 32, 21] 에서 최대값 구하기 - 재귀 호출 사용 

v = [7,9,15,43,32,21]

def find_max(a, n):
    if n == 1:
        return a[0]
    big = find_max(a, n-1)
    if big <= a[n-1]:
        return a[n-1]
    else:
        return big

print(find_max(v, len(v)))

# 다시 고민해보기
# 재귀 함수 복습



    


