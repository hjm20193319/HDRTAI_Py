# 스택(Stack): LIFO(Last-In-First-Out, 후입선출) 구조
# 나중에 들어온 데이터가 가장 먼저 나가는 자료구조 (예: 뒤로 가기, 실행 취소, 함수 호출 스택)

# 파이썬의 리스트를 스택처럼 사용하는 것
stack = []

# 놀이공원 입장
# 놀이기구 탈 때의 기록을 남김
stack.append('T-express 탑승')  # [문법] append(value): 리스트의 맨 끝에 데이터를 추가함 (Stack의 PUSH 역할)
print('기록 : ', stack)

stack.append('바이킹 탑승')
print('기록 : ', stack)

stack.append('회전목마 탑승')
print('기록 : ', stack)
print('\n')

# [주의!]
print(stack[2])     # [문법] 리스트[인덱스]: 특정 위치에 직접 접근하는 것은 Stack의 추상 자료형(ADT) 개념에 위배됨
print('\n')

# 가장 최근 기록 삭제
last_action = stack.pop()   # [문법] pop(): 리스트의 마지막 요소를 제거하고 그 값을 반환함 (Stack의 POP 역할)
print('마지막 기록 취소 후 현재1 : ', stack)
print('마지막 기록1 : ', last_action)
print('\n')

last_action = stack.pop()
print('마지막 기록 취소 후 현재2 : ', stack)
print('마지막 기록2 : ', last_action)
print('\n')

# [주의!!] pop(1) → [문법] 인덱스를 지정하여 중간 데이터를 삭제하는 것은 Stack의 LIFO 원칙을 위반하는 것임

print('----------------------------------')
############################################
# LIFO 구조를 클래스로 구현
############################################
class MyStack:
    def __init__(self, iterable = None):
        self._data = []  # [문법] self._data: 관례적으로 내부에서만 사용하는 변수임을 나타내기 위해 언더바(_)를 붙임
        if iterable is not None:
            for x in iterable:
                self.push(x)

    def push(self, x):
        self._data.append(x)
        return x
    
    def pop(self):
        # 맨 위(top) 요소 제거
        if not self._data: # [문법] if not list: 리스트가 비어있는지 확인
            raise IndexError('pop from empty stack')
        return self._data.pop()
    
    def is_empty(self):
        """스택이 비어있는지 여부를 확인"""
        return not self._data   # [문법] 리스트가 비어있으면 True, 데이터가 있으면 False 반환
    
    def __repr__(self): # [문법] __repr__: 객체를 print()하거나 디버깅 시 출력될 문자열 형식을 정의하는 특별 메소드
        top_to_bottom = list(reversed(self._data)) # [문법] reversed(seq): 시퀀스를 역순으로 순회하는 반복자 반환
        return f'Stack(top → bottom {top_to_bottom})' # [추천] f-string을 사용하여 객체의 현재 상태를 직관적으로 표현
    
def demo1Func():
    s = MyStack()
    for item in ['A', 'B', 'C', 'D']:
        s.push(item)
        print(f'push {item} → ', s)
    print('demo1 실행 후 : ', s._data)
    print('\n')
    print('LIFO에 따라 하나씩 추출')
    while not s.is_empty(): # [문법] while: 조건이 참인 동안 반복 수행
        print('pop → ', s.pop(), '| 현재는 : ', s)
    print('demo1 실행 후(pop) : ', s._data)

def demo2Func(text : str) -> str:
    """문자열을 입력받아 스택을 이용해 역순으로 반환"""
    s = MyStack(text) # [문법] 문자열(iterable)을 생성자 인자로 전달
    out = []    # 뒤집힌 문자 기억용
    while not s.is_empty():
        out.append(s.pop())
    return ''.join(out)

if __name__ == '__main__':
    demo1Func()
    print('\n')
    print(demo2Func('Python is good'))
    print(demo2Func('파이썬 만세'))