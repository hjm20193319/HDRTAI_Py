# Deque 데큐
# : 양쪽 끝에서 삽입과 삭제가 모두 가능한 자료구조

# 놀이공원 우선 탑승 + 일반 대기 줄

from collections import deque

dq = deque()
print('놀이 공원 기구 대기 시작')

# 일반인은 뒤쪽으로 들어옴 (Queue 처럼)
dq.append('철수')
dq.append('영희')
dq.append('민수')
print('현재 일반 대기줄 : ', list(dq))
print('\n')

# VIP 고객(지수)은 앞쪽으로 들어옴
dq.appendleft('VIP 지수')
print('현재 대기줄 상태 : ', list(dq))
print('\n')

# 놀이 기구 탑승
person = dq.popleft()
print(person, '놀이 기구 탑승')
print('탑승 후 현재 대기줄 : ', list(dq))
print('\n')

# 줄 맨 뒷 사람 줄서기 포기
person = dq.pop()
print(person, '줄서기 포기')
print('포기 후 현재 대기줄 : ', list(dq))
print('\n')

# 양쪽에서 삽입과 삭제가 가능하다!!

# 실시간 로그 분석, 이동 평균 계산 등에 활용 가능 ⇨ 양방향 처리하는 경우