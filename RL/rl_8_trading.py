# 주식 트레이딩 - DQN
import math, random
from collections import deque
import numpy as np
import tensorflow as tf
import pandas as pd

# 데이터 준비 (Close 칼럼)
def load_returns(csv_path:str):
    df = pd.read_csv(csv_path)
    close = df['Close'].astype(float).values
    ret = np.zeros_like(close, dtype=np.float32)    # 같은 길이의 수익률 배열 초기화
    ret[1:] = (close[1:] - close[:-1]) / (close[:-1] + 1e-9)    # 일별 수익률 계산 (분모 0 방지용 노이즈 추가)
    return ret


# 환경
class TradingEnv:
    # 매개변수 : 수익률 배열, 관측일, 거래비용
    def __init__(self, returns:np.ndarray, window=20, cost_bps=10.0) -> None:
        assert len(returns) > window + 1, '데이터가 너무 짧아요'

        self.rets_all = returns.astype (np.float32)
        self.window = window    # 관측에 사용할 과거 수익률 개수
        self.cost = cost_bps / 10_000.0     # bps(1 / 100bp) → 실수 비율로 변환
        self.reset()

    @property       # 메소드를 변수처럼 접근 가능 / 객체 변수명.obs_dim 으로 사용 가능
    def obs_dim(self):
        return self.window + 1      # 관측 차원(최근 window 일 수익률 + 현재 포지션)을 반환 
    
    @property
    def n_actions(self):
        return 3       # 행동 공간 크기 반환 (숏:-1 / 현금:0 / 롱:1)

    
    def reset(self):
        self.t = self.window    # t를 window 부터 시작 
        self.pos = 0.0     # 초기 포지션
        return self.obs()   # 현재 관측치 반환
    

    def obs(self):      # 현재 시점의 관측 벡터 생성
        window = self.rets_all[self.t - self.window : self.t]   # 직전 window 일의 수익률 슬라이싱
        return np.concatenate([window, [float(self.pos)]]).astype(np.float32)   # 수익률들 + 현재 포지션 반환
    

    def step(self, action:int):     # 환경 한 step 진행 (행동에 의해 다음 상태/보상/종료)
        new_pos = [-1, 0 ,1][action]    # 행동 인덱스를 실제 포지션 값으로 매핑 (0 → -1, 1 → 0, 2 → 1)
        trade_cost = self.cost * abs(new_pos - self.pos)    # 거래 비용 : 포지션 변화량
        reward = self.pos * self.rets_all[self.t] - trade_cost      # 보상(이전 포지션 * 금일 수익률) - 거래 비용
        self.pos = new_pos      # 포지션 갱신
        self.t += 1     # 시간 단계 갱신
        done = (self.t >= len(self.rets_all))   # 마지막 전 날까지 진행하면 에피소드 종료
        return self._obs(), float(reward), done



#######################################################################################
# Network 구성
def build_qnet_seq(obs_dim, n_actions):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(obs_dim, )),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(n_actions)    # defalt = 'linear'
    ])
    return model


# Replay Buffer : 경험 재생 메모리
class Replay:
    def __init__(self, cap=20000):
        self.buf = deque(maxlen=cap)


    def __len__(self):
        return len(self.buf)
    

    def push(self, *tr):
        self.buf.append(tr)     # (obs, act, r, nobs, done) → (s,a,r,s',done)


    def sample(self, n):    # minibatch sampling
        s = random.sample(self.buf, n)
        s, a, r, n, d = zip(*s)
        return(
            np.array(s, np.float32),    # 상태 배열
            np.array(a, np.float32),    # 행동 배열
            np.array(r, np.float32),    # 보상 배열
            np.array(n, np.float32),    # 다음 상태 배열
            np.array(d, np.float32)     # 종료 배열
        )
    

class DQN:
    def __init__(self, obs_dim, n_actions, lr=3e-4, gamma=0.99, batch=128):
        self.q = build_qnet_seq(obs_dim, n_actions)     # Main Network(Q-network) 생성
        self.tgt = build_qnet_seq(obs_dim, n_actions)    # Target Network 생성
        self.tgt.set_weights(self.q.get_weights())
        self.opt = tf.keras.optimizers.Adam(lr)
        self.gamma, self.batch = gamma, batch
        self.buf = Replay()
        self.loss_fn = tf.keras.losses.Huber()      # mse 보다 이상치에 덜 민감한 Huber 사용 → DQN 에서 많이 사용

        self.eps = 1.0
        self.eps_decay = 0.9995
        self.eps_min = 0.05
        self.n_actions = n_actions


    def act(self, obs):
        if random.random() < self.eps:
            return random.randrange(self.n_actions)     # 무작위 행동 인덱스 반환 / 탐험
        
        qv = self.q(obs[None, :], training=False).numpy()[0]    # Q(s, ) 계산
        return int(np.argmax(qv))   # 이용
    

    def update(self):   # 파라미터 갱신 (Replay Buffer 에서 minibatch sampling)
        if len(self.buf) < self.batch:
            return
        
        s, a, r, ns, d = self.buf.sample(self.batch)
        a_oh = tf.one_hot(a, self.n_actions)    # 행동 인덱스를 One-Hot 벡터로 변환
        with tf.GradientTape() as tape:
            q_sa = tf.reduce_sum(self.q(s) * a_oh, axis=1)      # 내적  Q(s, a)
            q_next = tf.reduce_max(self.tgt(ns), axis=1)    # Target Network로 다음 상태의 최대 Q 얻기
            y = r + (1 - d) * self.gamma * q_next       # 벨만 방정식 적용
            loss = self.loss_fn(y, q_sa)    # 손실 계산 → Huber(y, Q(s,a))
        
        g = tape.gradient(loss, self.q.trainable_variables)    # 기울기 계산
        self.opt.apply_gradients(zip(g, self.q.trainable_variables))    # 파라미터 갱신(경사하강 스텝 적용)
        self.tgt.set_weights(self.q.get_weights())    # Target Network 갱신
        self.eps = max(self.eps * self.eps_decay, self.eps_min)    # eps 감소    


def train_go(csv_path='prices.csv', window=20, cost_bps=10.0, episodes=5):
    rets = load_returns(csv_path)
    # print(rets)
    env = TradingEnv(rets, window, cost_bps)
    agent = DQN(env.obs_dim, env.n_actions)
    equity = []     # 누적 PnL 추적 리스트 (성과 지표용)

    for ep in range(1, episodes + 1):
        obs = env.reset()
        done, ep_pnl = False, 0.0   # ep_pnl : 누적 PnL 초기화
        while not done:
            act = agent.act(obs)
            nobs, r, done = env.step(act)   # 다음 관측, 보상, 종료 받음
            agent.buf.push(obs, act, r, nobs, float(done))
            agent.update()      # Q-network 에서 학습
            ep_pnl += r         # 에피소드 누적 PnL 갱신 (보상의 합)
            equity.append(ep_pnl)
        print(f'ep:{ep} / {episodes} PnL={ep_pnl:.4f}, eps={agent.eps:.3f}')
        
    # 결과 요약
    equity = np.array(equity)
    daily_ret = np.diff(equity, prepend=0.0)    # 일별 PnL 증분 (보상 시퀀스) 추정
    sharp = daily_ret.mean() / (daily_ret.std() + 1e-9) * np.sqrt(252)
    # : 일별 수익률 평균 / 일별 수익률 표준 편차 * sqrt(252)
    #                                                    ↪ 1년 거래일 수 
    print('--- 요약 결과 ---')
    print(f'Final PnL : {equity[-1]:.5f}')
    print(f'Sharp Ratio : {sharp:.3f}')

if __name__ == '__main__':
    train_go(csv_path='prices.csv', window=20, cost_bps=10.0, episodes=5)