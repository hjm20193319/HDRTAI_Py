# 4) Quick 정렬
# 분할 정복(Divide and Conquer) 알고리즘의 하나로, 평균적으로 매우 빠른 속도(O(n log n))를 가짐
# 하나의 기준점(Pivot)을 중심으로 작은 값과 큰 값을 나눠서 각각 재귀적으로 정렬 후
# 마지막에 합치는(Concatenate) 방식

# g1 : 기준값 보다 작은 그룹
# g2 : 기준값 보다 큰 그룹
# 기준값

# 4-1) 이해 위주
# 리스트 슬라이싱과 추가 메모리(g1, g2)를 사용하여 직관적으로 구현한 방식
def quick_sort(a):
    # 재귀 호출의 종료 조건(Base Case): 리스트 요소가 1개 이하이면 이미 정렬된 상태
    # [개념] 재귀 함수는 반드시 종료 조건이 있어야 무한 루프(Stack Overflow)에 빠지지 않음
    n = len(a)
    if n <= 1:
        return a
    
    # 기준값(편의상 가장 마지막 값을 취함)
    pivot = a[-1]
    g1 = []         # 기준값 보다 작은 그룹
    g2 = []         # 기준값 보다 큰 그룹

    # pivot을 제외한 나머지 요소들을 비교하여 그룹 분리
    for i in range(0, n-1):
        if a[i] < pivot:
            g1.append(a[i])
        else:
            g2.append(a[i])

    # print('g1 : ', g1)
    # print('g2 : ', g2)
    # print('pivot : ', pivot)
    # print('\n')
    
    # [문법] 리스트 더하기(+) 연산자를 사용하여 왼쪽 그룹 + 기준값 + 오른쪽 그룹을 합쳐서 반환
    # [추천] : 파이썬의 리스트 컴프리헨션을 사용하면 더 간결하게 작성 가능합니다.
    # return quick_sort([x for x in a[:-1] if x < pivot]) + [pivot] + quick_sort([x for x in a[:-1] if x >= pivot])
    return quick_sort(g1) + [pivot] + quick_sort(g2)

d = [6, 8, 3, 1, 2, 4, 7, 5]
print("이해 위주 퀵 정렬 결과:", quick_sort(d))
print('\n')

# 4-2) 일반 알고리즘
def quick_sort2_sub(a, start, end):
    if end - start <= 0:    # 종료 조건 : 정렬 대상이 1개 이하
        return
    
    # 기준값(편의상 가장 마지막 값을 취함)
    pivot = a[end]
    i = start   # i는 pivot보다 큰 값을 만났을 때 교체될 위치를 가리키는 포인터
    
    # j를 이용해 start부터 end-1까지 순회
    for j in range(start, end):
        if a[j] <= pivot:
            # [문법] a[i], a[j] = a[j], a[i] : 파이썬의 튜플 언패킹을 이용한 Swap(값 교환)
            a[i], a[j] = a[j], a[i]
            # print(f'{a[i]}, {a[j]}, = {a[j]}, {a[i]}')
            i += 1

    # 마지막에 pivot(a[end])을 자기 자리(i)로 이동
    a[i], a[end] = a[end], a[i]
    # print(f'{a[i]}, {a[end]}, = {a[end]}, {a[i]}')

    quick_sort2_sub(a, start, i-1)  # 기준값 보다 작은 그룹 재귀로 다시 정렬
    quick_sort2_sub(a, i+1, end)    # 기준값 보다 큰 그룹 재귀로 다시 정렬

# 제자리 정렬(In-place sort): 추가적인 리스트 생성 없이 원본 리스트 내에서 위치만 바꿔 메모리 효율적임
def quick_sort2(a):
    quick_sort2_sub(a, 0, len(a)-1)     # (정렬 대상 자료, 시작 인덱스, 끝 인덱스)

d = [6, 8, 3, 1, 2, 4, 7, 5]
quick_sort2(d)
print("일반 알고리즘(In-place) 결과:", d)
print('\n')