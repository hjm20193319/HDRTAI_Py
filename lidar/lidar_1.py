import numpy as np
import matplotlib.pyplot as plt

# ---------- 환경/에이전트 설정 ----------

# 시뮬레이션 세계 즉,
# LiDAR 센서가 탐지하는 2D 환경의 공간 경계(지도 크기)를 설정.

WORLD_W, WORLD_H = 20.0, 15.0

# 벽 두께
# 단순히 경계 밖이면 충돌로 처리
# 경계판정이나 시각화 개선 시 활용 가능한 변수

WALL_THICK = 0.5

# 원형 장애물
# (중심 x, 중심 y, 반지름 r)

OBSTACLES = [
    (6.0, 4.0, 1.0),      # (6,4) 위치 반지름 1.0 장애물
    (12.0, 10.0, 1.5),    # (12,10) 위치 반지름 1.5 장애물
    (15.0, 5.0, 1.0),     # (15,5) 위치 반지름 1.0 장애물
]

# 에이전트 초기 상태
# (x, y, 바라보는 각도 rad 단위)

# LiDAR 시뮬레이션의 에이전트
# (센서가 달린 로봇)의 초기 위치와 방향(heading)

agent = dict(
    x=3.0,
    y=3.0,
    theta=np.deg2rad(30)
)  # 30° 방향을 바라봄

# -----------------------------
# LiDAR 파라미터
# -----------------------------

# 레이(광선) 개수
NUM_RAYS = 32

# 시야각 180도
# degree(도)를 radian(라디안)으로 변환

# 삼각함수 등에서 각도를 다룰 때
# radian은 수학 표준 단위
# degree는 사람이 직관적으로 사용하는 단위

# radians = degrees × (π / 180)

FOV = np.deg2rad(180)

# 탐지 최대 거리
MAX_RANGE = 10.0

# 레이 전진 단위 거리
# 세밀할수록 정확도 증가

# 레이가 0.05m씩 전진하며 충돌 여부 검사

STEP = 0.05

# 한 레이가 최대 거리 10.0까지 나아가려면
#
# 10.0 / 0.05
#
# = 200번 충돌 체크 수행


def inside_world(x, y):
    """
    (x,y)가 세계 경계 안에 있는지 검사

    (x,y)가

    0 <= x <= WORLD_W
    0 <= y <= WORLD_H

    범위 안이면 True

    밖이면 벽 충돌로 처리
    """

    return (
        0.0 <= x <= WORLD_W
        and
        0.0 <= y <= WORLD_H
    )


def hit_circle(px, py, cx, cy, r):
    """
    점(px, py)이

    중심(cx, cy)
    반지름 r

    인 원형 장애물 내부에 있는지 검사

    True  -> 충돌
    False -> 비충돌
    """

    return (
        (px - cx) ** 2 +
        (py - cy) ** 2
        <=
        r ** 2
    )


def cast_lidar(
    x,
    y,
    theta,
    num_rays=NUM_RAYS,
    fov=FOV,
    max_range=MAX_RANGE,
    step=STEP
):
    """
    에이전트 (x,y,theta)에서

    시야각 FOV 만큼
    NUM_RAYS 개의 광선을 발사

    각 레이가 처음 충돌한 지점까지의 거리를 구함

    입력
    ----
    x, y
        시작 위치

    theta
        바라보는 방향

    num_rays
        레이 개수

    fov
        시야각

    max_range
        최대 탐지 거리

    step
        레이 전진 거리

    출력
    ----
    dists
        각 레이 충돌 거리

    angles
        각 레이 절대 각도
    """

    # 첫 번째 레이 시작 각도
    # 시야의 왼쪽 끝

    start = theta - fov / 2

    # angles는

    # start
    # ~
    # start + fov

    # 까지 균등 분배

    # 양 끝 포함
    # 좌우 끝 모두 레이 존재

    angles = (
        start +
        np.arange(num_rays)
        *
        (
            fov /
            max(num_rays - 1, 1)
        )
    )

    # 거리 배열 초기화

    dists = np.full(
        num_rays,
        max_range,
        dtype=float
    )

    for i, ang in enumerate(angles):

        dist = 0.0
        hit = False

        # 최대 거리까지 전진

        while dist < max_range:

            # 레이 끝점 좌표

            px = x + np.cos(ang) * dist
            py = y + np.sin(ang) * dist

            # 벽 충돌 검사

            if not inside_world(px, py):

                # 월드 밖이면 벽 충돌

                hit = True
                break

            # 원형 장애물 검사

            for (cx, cy, r) in OBSTACLES:

                if hit_circle(
                    px,
                    py,
                    cx,
                    cy,
                    r
                ):
                    hit = True
                    break

            if hit:
                break

            # 충돌 없으면 한 걸음 전진

            dist += step

        # 충돌 거리 기록

        dists[i] = min(
            dist,
            max_range
        )

    return dists, angles


def plot_world(agent, rays_endpoints=None):
    """
    2D LiDAR 환경 시각화

    입력

    agent
        로봇 상태

    rays_endpoints
        각 레이 시작점과 끝점 좌표
    """

    fig, ax = plt.subplots(
        figsize=(7.5, 5.5)
    )

    ax.set_xlim(0, WORLD_W)
    ax.set_ylim(0, WORLD_H)

    # 가로 세로 비율 유지

    ax.set_aspect(
        'equal',
        adjustable='box'
    )

    ax.set_title("Simple 2D LiDAR")

    # ---------------------
    # 월드 경계
    # ---------------------

    ax.plot(
        [0, WORLD_W, WORLD_W, 0, 0],
        [0, 0, WORLD_H, WORLD_H, 0],
        lw=2
    )

    # ---------------------
    # 장애물
    # ---------------------

    for (cx, cy, r) in OBSTACLES:

        circ = plt.Circle(
            (cx, cy),
            r,
            edgecolor='tab:red',
            facecolor='none',
            lw=2
        )

        ax.add_patch(circ)

    # ---------------------
    # 에이전트
    # ---------------------

    x = agent["x"]
    y = agent["y"]
    th = agent["theta"]

    L = 0.6

    tri = np.array([
        [
            x + np.cos(th) * L,
            y + np.sin(th) * L
        ],
        [
            x + np.cos(th + 2.5) * L / 1.5,
            y + np.sin(th + 2.5) * L / 1.5
        ],
        [
            x + np.cos(th - 2.5) * L / 1.5,
            y + np.sin(th - 2.5) * L / 1.5
        ]
    ])

    ax.fill(
        tri[:, 0],
        tri[:, 1],
        alpha=0.8,
        color='tab:blue',
        label='agent'
    )

    # ---------------------
    # LiDAR 레이 시각화
    # ---------------------

    if rays_endpoints is not None:

        for (
            x0,
            y0,
            x1,
            y1
        ) in rays_endpoints:

            ax.plot(
                [x0, x1],
                [y0, y1],
                lw=1,
                alpha=0.8
            )

    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    # obs
    # 각 레이가 감지한 거리 배열

    # 예)
    # [3.2, 4.7, 6.5 ...]

    obs, angs = cast_lidar(
        agent["x"],
        agent["y"],
        agent["theta"]
    )

    endpoints = []

    for d, a in zip(obs, angs):

        x0 = agent["x"]
        y0 = agent["y"]

        # 충돌 지점 계산

        x1 = x0 + np.cos(a) * d
        y1 = y0 + np.sin(a) * d

        endpoints.append(
            (x0, y0, x1, y1)
        )

    print("LiDAR observation (distances):")
    print(np.round(obs, 2))

    plot_world(
        agent,
        endpoints
    )