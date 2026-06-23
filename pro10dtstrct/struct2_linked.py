# 연결 리스트(Linked List)
# 데이터를 임의의 메모리 공간에 저장하고, 각 데이터가 다음 데이터의 위치(포인터)를 가리키도록 연결한 자료구조
# 삽입과 삭제가 빈번한 경우 선형 리스트보다 효율적임 (O(1) ~ O(n))

# 놀이공원에 줄서기
class Node:
    """데이터와 다음 노드에 대한 참조를 가지는 기본 단위"""
    def __init__(self, name):
        self.name = name    # 데이터 필드: 사람의 이름 저장
        self.next = None    # 링크 필드: 다음 노드의 주소를 가리키는 포인터

# Linked List 관리하는 객체
class LinkedList:
    def __init__(self):
        self.head = None    # [문법] self.head: 리스트의 첫 번째 노드를 가리키는 시작점 (초기값 None)

    # 새로운 Node 추가 (줄 뒤에 다음 사람 추가)
    def append(self, name):
        new_node = Node(name)   # [문법] Node(name): 새로운 노드 객체 생성

        if self.head is None:   # 줄(List)이 비어 있는 경우
            self.head = new_node # 첫 번째 노드로 지정
            return
        
        # 줄의 맨 끝 사람 찾기(이미 노드가 있다면 마지막 노드까지 이동)
        current = self.head
        while current.next:     # [문법] while current.next: 다음 노드가 존재할 때까지 반복 탐색
            current = current.next

        current.next = new_node # 마지막 노드의 next에 새 노드 연결

    def show(self):
        """리스트의 모든 요소를 순서대로 출력"""
        current = self.head
        while current:          # [문법] while current: 현재 노드가 None이 아닐 때까지 순회
            print(current.name, end='→')
            current = current.next
        print('끝')
    
    def __repr__(self):
        # [추천] __repr__ 또는 __str__ 메소드를 구현하면 print(instance) 시 리스트 상태를 더 쉽게 확인할 수 있음
        return "LinkedList Structure"

    # 특정 사람 뒤에 새 사람 끼워 넣기
    # target node를 찾고 → new node 만들고 → 기존 연결 변경
    def insert_after(self, target_name, new_name):
        current = self.head

        while current:
            if current.name == target_name: # 대상 노드를 찾은 경우
                new_node = Node(new_name)
                new_node.next = current.next # 새 노드가 기존의 다음 노드를 가리키게 함
                current.next = new_node      # 기존 노드가 새 노드를 가리키게 함
                return
            current = current.next

    # 특정 사람 삭제
    def remove(self, name):
        # 맨 앞 사람이 나가는 경우
        if self.head and self.head.name == name:
            self.head = self.head.next  # head를 두 번째 노드의 주소로 변경 (첫 노드 제외)
            return

        # 맨 앞 사람이 아닌 경우(첫 노드가 삭제 대상이 아닌 경우)
        current = self.head
        while current.next: # [문법] current.next: 삭제할 노드의 이전 노드에서 다음 노드 존재 여부 확인
            if current.next.name == name:
                current.next = current.next.next # 연결을 끊고 다음다음 노드에 직접 연결
                return
            current = current.next



line = LinkedList()
line.append('철수')
line.append('영희')
line.append('민수')        

print('현재 줄 상태 : ')
line.show()
print('\n')

# 영희 뒤에 지수 삽입
line.insert_after('영희', '지수')
print('새치기 후 현재 줄 상태 : ')
line.show()
print('\n')

# 영희가 줄서기를 포기(삭제)
line.remove('영희')
print('줄에서 빠진 후 현재 줄 상태 : ')
line.show()