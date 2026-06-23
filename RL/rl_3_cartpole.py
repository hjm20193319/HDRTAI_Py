# 강화 학습으로 Cart Pole 버티기
# 목표 : 200개의 step(시간) 단계 동안 Pole 이 넘어지지 않고 유지하기
# 종료 : Pole (수직으로부터 ± 12° 이상으로) 기울어지거나 카트가 환경 밖으로 벗어나거나
#        최대 시간 단계인 200 에 도달한 경우

# !pip install gymnasium[classic_control]


#######################################################################################
'''
상태요소         범위     구간수
카트위치     -2.4~2.4       6
카트속도     -3.0~3.0       12
막대기울기   -0.5~0.5       6
막대각속도   -2.0~2.0       12
'''
#######################################################################################
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle    # patches → 도형 사용할 때
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# 환경 생성
env = gym.make('CartPole-v1')
print(env.observation_space)
# Cart 위치, Cart 속도, Pole 속도, Pole 각속도
print('\n')
print(env.action_space.n)

# Q-table(observation_space) 공간 범위 인위적 실험 공간 생성
obs_space_low = np.array([-2.4, -3.0, -0.5, -2.0])
obs_space_high = np.array([2.4, 3.0, 0.5, 2.0])

# 상태공간 이산화 수준 결정 (각 상태 차원을 몇 개의 구간으로 나눌지 결정)
state_bins = [6, 12, 6, 12]

q_table = np.zeros(state_bins + [env.action_space.n])
print(q_table.shape)
# (6, 12, 6, 12, 2)
# 10368개 state




#######################################################################################
# 연속적인 값(실수)을 몇 개의 고정된 구간(bin)으로 나눠 이산적인(정수) 인덱스로 변환
def discretize_state(state):
    # state(카트위치, 속도, 막대각, 각속도)의 각 요소가 관측값 중 어디에 위치하는지 비율(정규화)로
    ratios = (state - obs_space_low) / (obs_space_high - obs_space_low)
    print('ratios : ', ratios)
    descrete = (ratios * state_bins).astype(int)
    print('descrete : ', descrete)
    return tuple(np.clip(descrete, 0, np.array(state_bins) - 1))

ex_state = np.array([1.0, 0.5, 0.5, -1.0])
print('Q-table index : ', discretize_state(ex_state))



#######################################################################################
# clip : 제한된 범위 내의 수치 얻기
a = np.array([-2, 0 , 3, 7, 10])
result = np.clip(a, 0, 5)
print(result)
# [0 0 3 5 5]



#######################################################################################
# 하이퍼 파라미터 설정
alpha = 0.1
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.999
epsilon_min = 0.05
episodes = 1000

reward_list = []    # 에피소드에서 받은 총 보상 기록
trajectories = []   # 위치 정보 (궤적)를 저장 → 학습 진행 과정을 애니메이션으로 보기 위해서
best_reward = 0    # 지금까지 달성한 최고의 총 보상을 누적



#######################################################################################
# 에피소드 만큼 반복
for ep in range(episodes):
    # 초기화 작업
    obs, _ = env.reset()
    state = discretize_state(obs)
    total_reward = 0
    trajectory = []

    for step in range(200):
        # 행동 선택 → 새로운 상태, 보상, 종료 여부 반환 → Q-table 갱신 → 상태 갱신
        if np.random.random() < epsilon:
            action = env.action_space.sample()  # 무작위 행동 선택 → 탐험
        else:
            action = np.argmax(q_table[state])

        # 주어진 action으로 환경 내에서 실행
        next_obs, reward, terminated, truncated, _ = env.step(action)

        done = terminated or truncated
        next_state = discretize_state(next_obs)     # 실수형을 이산형으로 변환
        best_next_q = np.max(q_table[next_state])   # 다음 상태에서 가장 큰 Q 값 → 미래 가치 계산

        # Q-table 갱신 : MDP 적용 - 벨만 방정식
        q_table[state + (action, )] += alpha * (reward + gamma * best_next_q - q_table[state + (action, )])

        state = next_state
        obs = next_obs  # 시각화를 위한 처리 (원래 상태값도 갱신)
        total_reward += reward
        trajectory.append(obs.copy())   # 애니메이션 용

        if done:
            break
    
    reward_list.append(total_reward)

    # 향상된 보상 출력
    if total_reward > best_reward:
        best_reward = total_reward      # 새로운 보상이 더 큼 → best reward 갱신
        print(f'Episode : {ep} → Reward Improved To {total_reward}')

    # 10 에피소드 마다 위치정보(궤적) 저장
    if ep % 10 == 0:
        trajectories.append(trajectory)
        
    # epsilon 감소
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay



#######################################################################################
# 보상 그래프 시각화
plt.figure(figsize=(10, 4))
plt.plot(reward_list)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Reward per Episode')
plt.grid(True)
plt.tight_layout()
plt.show()



#######################################################################################
# 저장된 궤적 정보로 애니메이션 실행
flat_states = []    # 여러 에피소드의 궤적을 한 줄로 펼쳐 저장

episode_labels = []
episode_numbers = list(range(0, episodes, 10))

# 시각화 목적의 데이터 평탄화 라벨링
for i, traj in enumerate(trajectories):
    flat_states.extend(traj)
    episode_labels.extend([episode_numbers[i]] * len(traj))

frame_count = len(flat_states)

fig, ax = plt.subplots()
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-0.3, 1.5)
ax.set_xlabel('Cart Position')
ax.set_ylabel('Height')
ax.set_title('Cart-Pole Visualization')
ax.grid(True)

# 카트와 막대 표시
cart_width = 0.4
cart_height = 0.2
cart_y = 0.0
cart_rect = Rectangle((0, cart_y), cart_width, cart_height, color='blue')
ax.add_patch(cart_rect)

pole_len = 1.0
line_list = ax.plot([],[], 'r-', lw=4)
pole_line = line_list[0]

episode_text = ax.text(0.05, 1.4, '', transform=ax.transData, fontsize=12, color='black')


def updateFunc(frame):
    x = flat_states[frame][0]   # cart 위치(x축 좌표)
    theta = flat_states[frame][2]   # pole 각도
    ep_num = episode_labels[frame]  # 현재 프레임의 에피소드 번호
    cart_rect.set_xy((x-cart_width/2, cart_y))      # 카트의 가운데를 기준으로 잡기 위해서

    # 막대 끝 좌표
    x_start = x
    y_start = cart_y + cart_height
    x_end = x_start + pole_len * np.sin(theta)
    y_end = y_start + pole_len * np.cos(theta)
    pole_line.set_data([x_start, x_end], [y_start, y_end])

    episode_text.set_text(f'Episode : {ep_num}')
    return cart_rect, pole_line, episode_text    

ani = FuncAnimation(fig, updateFunc, frames=frame_count, interval=50, repeat=False)
plt.close(fig)
# display(HTML(ani.to_jshtml()))    # 주피터 노트북용
# ani.to_jshtml() : 애니메이션을 HTML + Javascript로 변환