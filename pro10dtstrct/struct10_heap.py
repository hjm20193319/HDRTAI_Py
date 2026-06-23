# Heap 힙
# : 모든 노드가 특정한 순서를 유지하며 구성된 완전 이진 트리 형태의 자료 구조

# 내부 구현 없이 Heap 개념 이해하기
import heapq    # 기본이 Min Heap

# Min Heap
heap = []
heapq.heappush(heap, 30)
heapq.heappush(heap, 10)
heapq.heappush(heap, 20)
print('현재 힙 상태 : ', heap)      # 내부적으로 힙 구조가 유지됨
print('\n')

# 최소값 꺼내기
print('가장 작은 값 : ', heapq.heappop(heap))
print('남은 힙 상태 : ', heap)
print('\n')
print('가장 작은 값 : ', heapq.heappop(heap))
print('남은 힙 상태 : ', heap)
print('\n')
# ⇨ 힙의 구조에 맞게 들어가 있게 때문에 정렬하지 않아도 알아서 작은 값이 먼저 나옴

# Max Heap
heap = []
heapq.heappush(heap, -30)       # Max Heap으로 사용하기 위해 (-)를 붙이는 트릭을 사용
heapq.heappush(heap, -10)
heapq.heappush(heap, -20)
print('현재 힙 상태 : ', heap)
print('\n')

# 최대값 꺼내기
print('가장 큰 값 : ', -heapq.heappop(heap))
print('남은 힙 상태 : ', heap)
print('\n')
