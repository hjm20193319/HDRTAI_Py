# Queue : FIFO(First-In-First-Out, 선입선출) 구조
# 먼저 들어온 데이터가 가장 먼저 나가는 자료구조 (예: 매표소 줄서기, 프린터 출력 대기열, 프로세스 스케줄링) [개념] 큐(Queue)

# list 대신 deque를 이용해 Queue를 구현 (list.pop(0)은 O(n)이지만 deque.popleft()는 O(1)로 성능상 유리함)
from collections import deque   # [문법] collections.deque: 양방향에서 데이터 삽입/삭제가 가능한 자료구조

# [deque 자료 메소드]
# deque(): 데크 객체 생성
# append(value): 우측(뒤)에 데이터 추가 (Queue의 ENQUEUE 역할)
# appendleft(value): 좌측(앞)에 데이터 추가
# pop(): 우측(뒤)에서 데이터 제거 및 반환
# popleft(): 좌측(앞)에서 데이터 제거 및 반환 (Queue의 DEQUEUE 역할)
# ...

# 놀이 공원 대기 줄
queue = deque()
print('놀이 공원 기구 대기 시작')

# 줄서기
queue.append('철수')    # [문법] append(value): 큐의 맨 뒤에 새로운 요소를 추가함
print('첫번째 줄 서기 : ', list(queue))
queue.append('영희')
print('두번째 줄 서기 : ', list(queue))
queue.append('민수')
print('세번째 줄 서기 : ', list(queue))
print('\n') 

# 놀이 기구 탑승 - FIFO
first_person = queue.popleft()    # [문법] popleft(): 큐의 가장 앞에 있는(가장 먼저 들어온) 요소를 제거하고 반환함
print(first_person, '놀이 기구 탑승')
print('현재 대기줄 : ', list(queue))
print('\n')

# 한 명 더 놀이 기구 탑승 - FIFO    ⇨  중간 데이터 처리 불가 (Queue의 추상 자료형(ADT) 원칙)
first_person = queue.popleft()    # queue에서 제거
print(first_person, '놀이 기구 탑승')
print('현재 대기줄 : ', list(queue))
print('\n')

if queue:   # [문법] if deque: 객체가 비어있지 않으면 True, 비어있으면 False 반환
    print('탑승 예정자 : ', queue[0])   # [문법] queue[0]: 삭제하지 않고 맨 앞의 요소를 확인 (PEEK 역할)
else:
    print('탑승 예정자가 없습니다.')
print('\n')

# [추천] 큐의 크기를 제한하고 싶다면 deque(maxlen=N)을 사용하여 가득 찼을 때 오래된 데이터를 자동으로 삭제하게 할 수 있음
# [추천] 멀티스레드 환경에서는 thread-safe한 queue.Queue 모듈 사용을 권장함

print('----------------------------------')
############################################
# FIFO 구조를 클래스로 구현
############################################

class Queue:
    def __init__(self, iterable = None): # [문법] __init__: 객체 생성 시 호출되는 초기화 메소드
        self._data = deque() # [문법] self._data: 내부 캡슐화를 위해 언더바(_)를 붙여 선언
        if iterable is not None:
            for x in iterable:
                self.enqueue(x)

    def enqueue(self, x):
        self._data.append(x)    # [문법] append(x): 데크의 오른쪽(뒤)에 데이터를 추가함 (Queue의 ENQUEUE)
        return x
    
    def dequeue(self):          # front 요소 제거
        if not self._data: # [문법] if not deque: 비어있는지 확인
            raise IndexError('dequeue from empty queue')
        return self._data.popleft() # [문법] popleft(): 데크의 왼쪽(앞) 데이터를 제거하고 반환함 (Queue의 DEQUEUE)
    
    def front(self):            # Queue에서 맨 앞 요소를 확인하는 메소드 (조회만 함)
        if not self._data:
            raise IndexError('front from empty queue')
        return self._data[0] # [문법] deque[0]: 인덱스를 통해 가장 앞의 요소를 참조 (Queue의 PEEK)
    
    def is_empty(self):
        """큐가 비어있는지 여부를 확인"""
        return not self._data   # [문법] 데이터가 없으면 True, 있으면 False 반환
    
    def __repr__(self):         # [문법] __repr__: 객체를 문자열로 표현할 때 사용되는 특별 메소드
        front_to_back = list(self._data)
        return f'Queue(front → back {front_to_back})' # [추천] f-string을 사용하여 큐의 상태를 직관적으로 표현
    
    def size(self):             # 요소 개수 반환
        return len(self._data) # [문법] len(obj): 저장된 요소의 총 개수를 반환
    
    def clear(self):           # 큐 비우기
        self._data.clear() # [문법] clear(): 데크의 모든 요소를 삭제함
    
def demo1Func():
    imsi1 = Queue()
    imsi2 = Queue([10, 20, 30])
    print('imsi1 : ', imsi1)
    print('imsi2 : ', imsi2)
    print('\n')

    print(imsi2.front())
    print(imsi2.size())
    print(imsi2.clear())
    print(imsi2)
    print('\n')

    q = Queue()
    for item in ['A', 'B', 'C', 'D']:
        q.enqueue(item)
        print(f'enqueue {item} → ', q)
    print('demo1 실행 후 : ', q._data)
    print('\n')

    print('FIFO에 따라 하나씩 추출')
    while not q.is_empty(): # [문법] while: 조건이 참인 동안 반복 수행
        print('dequeue → ', q.dequeue(), '| 현재는 : ', q)
    print('demo1 실행 후(dequeue) : ', q._data)

def demo2Func(jobs, ppm=15):
    q = Queue(jobs)     # 작업들을 큐에 입력
    t_sec = 0.0         # 시뮬레이션 시간 누적
    order = []          # 실제 처리된 문서 저장

    print('프린터로 출력하기')
    while not q.is_empty():
        doc, pages = q.dequeue()
        # 출력 시간 계산 : 페이지수 / 분당 페이지수 * 60
        duration = (pages / ppm) * 60.0 # [문법] /: 부동소수점 나눗셈 연산
        t_sec += duration
        order.append(doc)   # 처리 순서 기록
        print(f'누적 t = {t_sec:6.1f}초 | 출력 : {doc:10s} ({pages} 페이지)')

    print('처리 순서(FIFO) : ', order)    


if __name__ == '__main__':
    demo1Func()
    print('\n')
    print('문서 프린터로 출력 시뮬레이션 - FIFO')
    jobs = [('abc.pdf', 10), ('nice.doc', 30), ('good.txt', 5)]
    demo2Func(jobs, ppm=20)     # 현재 프린터는 1분에 20장 출력이 가능함