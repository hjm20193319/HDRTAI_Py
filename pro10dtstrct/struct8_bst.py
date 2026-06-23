# BST (Binary Search Tree) 이진 탐색 트리 → 오름차순 정렬 가능
# : 각 노드 기준으로 left < node < right
# 왼쪽 서브 트리 : 현재 노드보다 작은 값
# 오른쪽 서브 트리 : 현재 노드보다 큰 값
# 입력 순서에 따라 트리 모양이 달라짐
# 이진 트리는 구조만 있으나, BST는 구조 + 정렬 규칙이 있다
# 중위 순회 (왼쪽 → 현재 → 오른쪽 순서로 방문)를 하면 오름차순 정렬됨

# BST 노드 정의
class Node:
    def __init__(self, key):
        self.key = key      # 노드가 저장하는 값
        self.left = None    # 왼쪽 자식 노드 - 더 작은 값들이 저장
        self.right = None   # 오른쪽 자식 노드 - 더 큰 값들이 저장

# BST 삽입
def insert(root, key):
    if root is None:        # 현재 위치가 비워져 있다면
        return Node(key)    # 새로운 노드 생성
    
    if key < root.key:                          # 넣을 값이 현재 노드보다 작으면
        root.left = insert(root.left, key)      # 왼쪽 서브 트리에 재귀적으로 삽입

    elif key > root.key:                        # 넣을 값이 현재 노드보다 크면
        root.right = insert(root.right, key)    # 오른쪽 서브 트리에 재귀적으로 삽입
    return root

# 중위 순회(정렬 결과 생성)
def inorder(root, result):
    if root is None:
        return                      # 더 내려갈 노드가 없다면 함수 탈출
    else:
        inorder(root.left, result)  # 왼쪽 서브 트리 순회 (작은 값들)
        result.append(root.key)      # 현재 노드 값 추가
        inorder(root.right, result) # 오른쪽 서브 트리 순회 (큰 값들)

values = [5, 3, 7, 2, 4, 9]
root = None
for value in values:
    root = insert(root, value)      # BST에 삽입하고 루트(최상단)를 갱신

# BST 정렬 결과
sorted_result = []
inorder(root, sorted_result)
print('정렬 결과 : ', sorted_result)
print('\n')