# 리스트 안에 들어 있는 자료를 오름차순 정렬

# 1) 선택 정렬(Selection sort)
# 선택 정렬: 전체 원소 중 최솟값을 찾아 맨 앞의 원소와 교체하고, 그 다음 위치부터 반복하는 정렬 방식

# 1-1) 이해 위주(메모리 고려X)
# 별도의 결과 리스트를 생성하여 정렬된 값을 채워넣는 방식 (공간 복잡도 증가)
def find_min_idx(a):
    n = len(a)  # 리스트의 전체 요소 개수 파악
    min_idx = 0 # 0번 인덱스를 초기 최솟값 위치로 가정
    for i in range(1, n): # 1번 인덱스부터 끝까지 순회하며 비교
        if a[i] < a[min_idx]: # 현재 요소가 기존 최솟값보다 작다면
            min_idx = i # 최솟값의 위치(인덱스)를 갱신
    return min_idx # 가장 작은 값의 위치 반환

# d = [2, 4, 5, 1, 3]
# print(find_min_idx(d))      # 가장 작은 값의 인덱스를 반환

def select_sort(a):
    result = [] # 정렬된 결과를 담을 빈 리스트 생성
    while a:                        # 원본 리스트 a에 원소가 남아있는 동안 계속 반복 (모든 원소가 없어질때가지 수행)
        min_idx = find_min_idx(a) # 현재 리스트에서 최솟값의 위치를 찾음
        # pop(index): 해당 인덱스의 요소를 리스트에서 제거하며 그 값을 반환
        value = a.pop(min_idx)      # 최솟값(예: 1)을 원본에서 뽑아서 변수에 저장
        result.append(value) # 결과 리스트의 맨 뒤에 추가
    return result                   # 정렬이 완료된 새 리스트 반환 (결국 d와 크기가 같아짐)

d = [2, 4, 5, 1, 3]
print(select_sort(d))
print(d)                            # pop으로 인해 원본 리스트는 비어있게 됨 (리스트를 2개 만듦)
print('\n')

# 1-2) 일반 알고리즘    - O(n**2) 
# 제자리 정렬(In-place sort): 추가 메모리 없이 원본 리스트 내부에서 위치 교환(Swap)만 수행
# 시간 복잡도: 중첩 루프를 사용하므로 데이터 양의 제곱에 비례하는 O(n^2) 성능을 가짐
def select_sort2(a):
    n = len(a) # 리스트의 길이
    # 외부 루프: 정렬되지 않은 부분의 시작 위치를 0부터 n-2까지 이동
    for i in range(0, n-1): 
        min_idx = i # 현재 i번째를 최솟값 위치로 가정
        # 내부 루프: i+1번째부터 끝까지 비교하여 실제 최솟값의 위치를 찾음
        for j in range(i+1, n): 
            if a[j] < a[min_idx]: # 더 작은 값을 발견하면
                min_idx = j # 최솟값 인덱스 갱신
        # 파이썬의 다중 할당(Tuple Unpacking)을 이용한 값 교환(Swap)
        # 별도의 임시 변수(temp) 없이 두 변수의 값을 서로 바꿈
        a[i], a[min_idx] = a[min_idx], a[i]     # 찾은 최솟값을 현재 정렬 기준 위치(i번)로 이동
    return a # 정렬된 원본 리스트 반환

d = [2, 4, 5, 1, 3]
select_sort2(d)
print(d)                                        # 원본 리스트 자체가 정렬됨 (기존 리스트를 사용해서)
print('\n')