# 다익스트라 PDF 내용 코드로 구현

import heapq

INF = int(1e9)

# 그래프 (인접 리스트 방식) - (노드번호(인덱스), 비용) 형태로 저장
graph = [   # 노드 1은 0번째, 노드 2는 1번째 ...
    [(1, 2), (2, 5), (3, 1)],   # 1번 노드
    [(0, 2), (2, 3), (3,2)],    # 2번 노드
    [(0, 5), (1, 3), (3, 3), (4, 1), (5, 5)],   # 3번 노드
    [(0, 1), (1, 2), (2, 3), (4, 1)],  # 4번 노드
    [(2, 1), (3, 1), (5, 2)],    # 5번 노드
    [(2, 5), (4, 2)]    # 6번 노드
]

n = 6   # 노드 개수 6개
distance = [INF] * n    # 최단 거리 테이블을 모두 무한으로 초기화

def dijkstraFunc(start):
    pq = []     # 우선 순위 큐(Heap)
    distance[start] = 0
    heapq.heappush(pq, (0, start))      # (거리, 노드) 형태로 큐에 삽입
    
    while pq:
        dist, now = heapq.heappop(pq)

        if distance[now] < dist:
            continue

        for next_node, cost in graph[now]:
            new_cost = dist + cost
            # 만약 새로운 경로가 짧다면최단 거리 갱신
            if new_cost < distance[next_node]:
                distance[next_node] = new_cost  # 갱신
                heapq.heappush(pq, (new_cost, next_node))

dijkstraFunc(0)     # 1번 노드에서 시작 (1번 노드의 인덱스 - 0)

# 각 노드까지의 최단 거리 출력
for i in range(n):
    print(f'{i+1}번 노드까지의 최단 거리 : {distance[i]}')