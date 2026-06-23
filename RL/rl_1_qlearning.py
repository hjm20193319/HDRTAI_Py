# Q - learning 의 구조를 이해하기 : 벨만 방정식 기반의 근사학습
# Q - learning 에서 에이전트는 가장 Q 값이 높은 행동을 선택 → Greedy 한 행동

# 현대 위치(State)에서 어떤 행동(Action)을 취할 것인가? (왼쪽/오른쪽...)

import numpy as np
import random

# 상태 공간 : 에이전트가 있을 수 있는 위치
state_space = [0, 1, 2, 3, 4]

# 행동 공간 : -1 은 왼쪽, 1은 오른쪽 이동을 의미
action_space = [-1, 1]

# Q-table : (행 : 상태, 열 : 행동)
# Q[state][action] : 특정 상태에서 특정 행동을 했을 때의 가치

Q = np.zeros((len(state_space), len(action_space)))
print(Q)
# [[0. 0.]
#  [0. 0.]
#  [0. 0.]
#  [0. 0.]
#  [0. 0.]]



#######################################################################################
# 하이퍼 파라미터 설정
alpha = 0.1     # 학습율 (새롭게 배운 값을 기존 Q 값에 얼마나 반영할지 결정)
gamma = 0.9     # 할인율 (discount factor), 미래 보상을 얼마나 중요하게 볼 것인지를 결정
epsilon = 1.0   # 탐험 확률값
epsilon_decay = 0.99    # epsilon 감소율
epsilon_min = 0.1   # epsilon 최소값
episodes = 500     # 에피소드 수 (전체 학습 횟수)

# 보상 함수 : state = 4 이면 목표에 도달
def get_reward(state):
    return 10 if state == 4 else 0



#######################################################################################
# 학습 시작 : episode 는 하나의 학습 시도
for episode in range(episodes):
    state = 0   # 매 episode마다 0번 위치에서 시작
    for step in range(20):  # step : 한번의 이동, 한 episode 안에서 action은 20번으로 제한
        # 행동 선택
        if random.random() < epsilon:
            action_index = random.randint(0, 1)     # 탐험(Exploration) - Random 하게
        else:
            action_index = np.argmax(Q[state])      # 이용(Exploitation) - Greedy Action

        action = action_space[action_index]     # action_index 를 실제 행동값 (-1, 1)로 변환

        # 다음 상태 계산
        next_state = state + action     # state=2, action=1 ⇨ next_state : 3

        # 상태 공간을 유지
        if next_state < 0 or next_state > 4:
            next_state = state

        # 보상
        reward = get_reward(next_state)

        # Q 값 업데이트
        old_q = Q[state][action_index]

        next_max = np.max(Q[next_state])    # 다음 상태에서 가장 좋은 행동을 했을 때 기대되는 가치

        # Q-learning 갱신 식 - 벨만 방정식(off-policy 방식의 수식)
        #  Q(s,a) ← Q(s,a) + α × [ r + γ × max(Q(s',a')) - Q(s,a) ]
        Q[state][action_index] = old_q + alpha * (reward + gamma * next_max - old_q)

        # 상태 이동
        state = next_state  # 다음 상태를 현재 상태로 변경

        if reward ==10:
            break
    
    # epsilon 감소
    epsilon = max(epsilon * epsilon_decay, epsilon_min)
    # print(epsilon)

print(Q)
# [[ 6.55947559  7.29      ]
#  [ 6.56079767  8.1       ]
#  [ 7.28959826  9.        ]
#  [ 8.09961242 10.        ]
#  [ 0.          0.        ]]