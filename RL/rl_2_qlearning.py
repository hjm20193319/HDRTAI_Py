# 강화 학습
# 에이전트가 라벨이 없이 직접 행동해보고, 행동에 대한 보상을 받아 어떤 행동이 좋은지 점점 학습해 나감
# < 현재 상태 → 행동 선택 → 보상 확인 → 다음 행동 개선 >    순으로 진행

# 강화 학습은 정답이 아니라 보상으로 배운다
# 순서
# 1) 상태 : 현재 위치
# 2) 행동 : 위/아래/좌/우
# 3) 보상 : 행동 결과에 대한 점수
# 4) Q-table : 상태별 행동 점수표
# 5) Q-learning : Q-table 조금씩 갱신
# 6) Epsilon-Greedy : 탐험과 이용을 조절
# 7) 학습 후 Q-table 에서 가장 큰 행동을 선택 ⇨ 정책(policy)
# 8) 이 구조가 Gymnasium의 step() 구조와 연결됨



#######################################################################################
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# GridWorld 환경 설정
ROWS = 3
COLS = 4

START = (0,0)   # 에이전트 행동 시작 위치
GOAL = (2,3)    # 목표
TRAP = (1,1)    # 함정

actions = {
    0:(-1, 0), # 위
    1:(1, 0),  # 아래
    2:(0, -1), # 좌
    3:(0, 1)   # 우
}

action_names = {
    0:"UP",
    1:"DOWN",
    2:"LEFT",
    3:"RIGHT"
}

num_states = ROWS * COLS    # 상태수는 12
num_actions = len(actions)   # 행동수는 4

Q = np.zeros((num_states, num_actions))
print(Q)

# 하이퍼 파라미터
alpha = 0.1
gamma = 0.9
epsilon = 1.0   # 초기 탐험률
epsilon_decay = 0.995
min_epsilon = 0.1
episodes = 1000
max_steps = 30  # 하나의 에피소드 내에서 최대 이동 가능 횟수

# 위치 정보를 Q-table에서 사용할 상태 번호로 변환 (0,0) → 0, .... (2,3) → 11
def pos_to_state(pos):
    row, col = pos
    return row * COLS + col

def state_to_pos(state):    # 상태 번호를 위치정보로 변환
    row = state // COLS
    col = state % COLS
    return (row, col)




#######################################################################################
# 환경 이동 함수
def step(pos, action):  # 현재 위치에서 행동을 실행하고 결과를 반환하는 함수
    row, col = pos
    dr, dc = actions[action]    # 선택한 행동에 해당하는 행변화량, 열변화량 얻기

    next_row = row + dr     # 이동 후의 행 위치 계산
    next_col = col + dc     # 이동 후의 열 위치 계산

    # GridWorld 경계 밖으로 나가면 제자리, 패널티 부여
    if next_row < 0 or next_row >= ROWS or next_col < 0 or next_col >= COLS:
        next_pos = pos
        reward = -2
        done = False    # 벽에 부딪혔다고 에피소드가 끝나지는 않음
        return next_pos, reward, done
    
    next_pos = (next_row, next_col)

    if next_pos == GOAL:
        reward = 10
        done = True
    elif next_pos == TRAP:
        reward = -10
        done = True
    else:
        reward = -1     # 일반 이동할 때마다 -1 패널티, 짧은 경로를 유도
        done = False
    
    return next_pos, reward, done

print(step((0,0), 3))
print(step((1,0), 3))
print(step((2,2), 3))
# ((0, 1), -1, False)
# ((1, 1), -10, True)
# ((2, 3), 10, True)



#######################################################################################
# Epsilon-Greedy 행동 선택 : 탐험 또는 이용
def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, num_actions-1)     # 탐험
    else:
        return np.argmax(Q[state])                  # 이용 : 현재 상태에서 Q 값이 가장 큰 행동 선택
    
print('선택된 행동은 ', choose_action(0, 1.0)) 

# Q-learning 학습
for episode in range(episodes):
    pos = START
    state = pos_to_state(pos)   # (0,0) → 0

    # 하나의 에피소드 안에서 최대 행동 횟수
    for step_count in range(max_steps):
        # 행동 선택
        action = choose_action(state, epsilon)

        # 행동 실행
        next_pos, reward, done = step(pos, action)
        next_state = pos_to_state(next_pos)     # 다음 위치를 상태번호로 변환

        # 현재 Q값 (벨만 방정식에 적용)
        old_q = Q[state][action]    # 현재 상태(state)에서 선택한 action의 기존 Q값

        # Q-learning target을 계산 (이번 경험으로 계산한  목표 Q 값)
        if done:
            target = reward     # 함정 또는 목표 도착시 미래 Q 값을 보지 않고 현재 보상만 사용
        else:
            next_max = np.max(Q[next_state])    # 다음 상태에서 가능한 행동 중 가장 큰 Q 값
            target = reward + gamma * next_max

        # Q-learning update
        td_error = target - old_q   # 목표값과 기존 Q 값의 차이
        Q[state][action] = old_q + alpha * td_error     # 현재 상태의 가치를 보상과 다음 상태의 가치로 표현

        # 상태 이동
        pos = next_pos      # 현재 위치를 다음 위치로 갱신
        state = next_state  # 현재 상태번호를 다음 상태번호로 갱신

        if done:
            break

    # Epsilon 감소
    epsilon = max(epsilon * epsilon_decay, min_epsilon)       


# 학습 결과 출력
print('학습된 Q-table')
print(np.round(Q, 2))

print('\n각 상태에서 가장 좋은 행동 출력')
for state in range(num_states):
    pos = state_to_pos(state)

    if pos == GOAL:
        print(f'상태 {state} {pos} : 목표지점')
        continue
    elif pos == TRAP:
        print(f'상태 {state} {pos} : 함정')
        continue

    best_action = np.argmax(Q[state])
    print(f'상태 {state} {pos} : {action_names[best_action]}')



#######################################################################################
# 학습된 정책으로 실제 이동 경로 확인
pos = START
path = [pos]    # 시작 위치부터 이동 경로 저장

for i in range(20):
    state = pos_to_state(pos)
    action = np.argmax(Q[state])
    
    next_pos, reward, done = step(pos, action)
    path.append(next_pos)   # 이동한 다음 위치를 경로에 추가

    pos = next_pos

    if done:
        break
    
print('이동 경로 : ', path)
print('\n')

arrow = {
    0:'↑',
    1:'↓',
    2:'←',
    3:'→'
}

for r in range(ROWS):
    for c in range(COLS):
        pos = (r, c)

        if pos == START:
            row_text += 'S'
        elif pos == GOAL:
            row_text += 'G'
        elif pos == TRAP:
            row_text += 'X'
        else:
            state = pos_to_state(pos)
            best_action = np.argmax(Q[state])
            row_text += arrow[best_action]

print(row_text)