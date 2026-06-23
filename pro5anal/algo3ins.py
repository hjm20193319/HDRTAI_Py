# 리스트 안에 있는 자료를 오름차순 정렬
# 2) 삽입 정렬(insertion sort) : 앞에서부터 하나씩 꺼내서 자기자리 찾아 끼워 넣는 정렬
# - 특징: 이미 정렬된 부분과 비교하여 자신의 위치를 찾아 '삽입'하는 방식
# - 성능: 최선의 경우(이미 정렬된 상태) O(n), 최악의 경우 O(n^2)의 시간 복잡도를 가짐

# 2-1) 이해 위주(메모리 고려X)
# 별도의 결과 리스트(r)를 유지하며 원본 리스트의 값을 하나씩 적절한 위치에 끼워넣는 방식
def find_ins_idx(r, v):
    # 이미 정렬된 리스트 r을 앞에서부터 순회하며 v가 들어갈 위치(인덱스)를 찾음
    for i in range(0, len(r)):
        if v < r[i]:        # 현재 위치의 값보다 삽입하려는 값 v가 작다면
            return i        # 해당 위치(인덱스)를 반환
    return len(r)           # r에 있는 모든 값보다 크다면 리스트의 맨 뒤 인덱스 반환

def ins_sort(a):
    result = []             # 정렬된 값을 담을 새 리스트 생성
    while a:                # 원본 리스트 a에 데이터가 남아있는 동안 반복
        # pop(0): 리스트의 첫 번째 요소를 꺼내고 원본에서는 삭제 (O(n) 연산)
        value = a.pop(0)    
        # 새 리스트에서 value가 들어갈 위치를 찾음
        ins_idx = find_ins_idx(result, value) 
        # list.insert(index, value): 특정 인덱스 위치에 값을 삽입
        result.insert(ins_idx, value) 
    return result           # 최종 정렬된 리스트 반환

d = [2, 4, 5, 1, 3]
print(ins_sort(d))
print('\n')

# 2-2) 일반 알고리즘
# 제자리 정렬(In-place sort): 추가 리스트 없이 원본 리스트 내에서 요소들을 이동시켜 정렬
def ins_sort2(a):
    n = len(a)              # 리스트의 전체 길이
    for i in range(1, n):   # 1번 인덱스부터 시작(삽입할 대상을 선택)
        # 현재 정렬 대상이 되는 값을 key 변수에 복사해둠
        key = a[i]      # i 번째 위치 값을 key에 저장
        # j는 key의 바로 왼쪽(이미 정렬된 부분의 끝) 인덱스
        j = i - 1       # j는 i 바로 왼쪽 위치로 지정
        
        # 비교 대상(a[j])이 key보다 크면, 비교 대상을 오른쪽으로 한 칸 이동
        # j가 0보다 작아지거나 key보다 작거나 같은 값을 만날 때까지 반복
        while j >= 0 and a[j] > key:    
            a[j + 1] = a[j]     # 삽입할 공간이 생기도록 값을 우측으로 밀기
            j -= 1              # 왼쪽으로 이동하며 계속 비교
        # 반복문이 멈춘 지점(j)의 바로 오른쪽(j+1)이 key가 들어갈 적절한 위치
        a[j + 1] = key      # 찾은 삽입 위치에 key를 저장

d = [2, 4, 5, 1, 3]
ins_sort2(d)
print(d)
print('\n')