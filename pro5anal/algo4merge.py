# 리스트 자료를 오름차순 정렬
# 3) 병합 정렬(Merge Sort) : 분할 정복(Divide and Conquer) 기법을 사용하는 정렬 알고리즘
# - 특징: 리스트를 요소가 1개가 될 때까지 반으로 나눈 뒤(분할), 다시 크기 순으로 합치며(병합) 정렬함
# - 성능: 데이터 분포와 상관없이 항상 O(n log n)의 안정적인 시간 복잡도를 보장함

# 3-1) 이해 위주 
# 리스트 슬라이싱과 pop(0)을 사용하여 직관적으로 구현한 방식
def merge_sort(a):
    n = len(a)

    # 재귀 호출의 종료 조건(Base Case): 리스트 요소가 1개 이하이면 이미 정렬된 상태
    if n <= 1:
        return a
    
    # [문법] // 연산자: 나눗셈의 몫을 정수형으로 구함 (중간 지점 계산)
    mid = n // 2
    # [개념] 함수는 호출될 때마다 독립적인 스택 공간을 가짐. 아래의 g1, g2는 서로 간섭하지 않음
    g1 = merge_sort(a[:mid])    # 왼쪽 부분 분할 (재귀 호출)
    print('g1 : ', g1)
    g2 = merge_sort(a[mid:])    # 오른쪽 부분 분할 (재귀 호출)
    print('g2 : ', g2)

    # 병합 과정: 두 그룹(g1, g2)의 첫 번째 원소를 비교하여 작은 값을 결과 리스트에 추가
    result = []
    # [문법] while g1 and g2: 두 리스트 모두에 요소가 남아있는 동안 반복
    while g1 and g2:
        if g1[0] < g2[0]:
            # [문법] pop(0): 리스트의 첫 번째 요소를 꺼내고 삭제 (O(n) 연산)
            result.append(g1.pop(0)) 
        else:
            result.append(g2.pop(0))
    
    # 한쪽 리스트가 비었을 때 남은 요소들을 결과 리스트에 모두 추가
    while g1:
        result.append(g1.pop(0))
    while g2:
        result.append(g2.pop(0))
    
    return result

d = [6, 8, 3, 1, 2, 4, 7, 5]
print(merge_sort(d))
print('\n')

# 3-2) 일반 알고리즘
# 재귀 호출이 정렬된 리스트를 반환
# 인덱스 포인터(i, j)를 사용하여 pop(0)의 오버헤드를 줄인 방식
# [개념] 원본 리스트는 유지되고 정렬된 결과는 매 단계마다 새로운 리스트에 저장됨
def merge_sort2(a):
    n = len(a)
    # 종료 조건
    if n <= 1:
        return a
    
    # 분할 단계: 리스트 슬라이싱을 이용해 좌우로 나눔
    mid = n // 2
    left = merge_sort2(a[:mid])
    right = merge_sort2(a[mid:])

    result = []
    i = j = 0   # i는 left 리스트의 인덱스, j는 right 리스트의 인덱스

    # 병합 단계: 인덱스를 이동시키며 두 리스트의 값을 비교
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # [문법] 리스트 슬라이싱과 더하기(+): 남은 요소들을 한꺼번에 결과 리스트에 병합
    result += left[i:]
    result += right[j:]

    return result

d = [6, 8, 3, 1, 2, 4, 7, 5]
# [개념] 함수가 호출될 때마다 별도의 메모리 공간(Stack Frame)이 생성되어 데이터를 처리함
sorted_d = merge_sort2(d)
print(sorted_d)
print('\n')

# [추천] : 대량의 데이터를 정렬할 때는 파이썬 내장 함수인 sorted()나 .sort()를 사용하는 것이 가장 빠릅니다. 
# (Timsort 알고리즘을 사용하여 병합 정렬과 삽입 정렬의 장점을 결합함)