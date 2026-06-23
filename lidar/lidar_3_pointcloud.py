# 자동차가 이동하며 여러 방향으로 레이저를 쏘고 건물 표면 좌표를 수집하여
# 3D 점군(Point Cloud) 생성
# 라이다는 물체를 면으로 보는 것이 아니라, 많은 점좌표(x, y)를 모아 환경을 재구성한다
# 즉, [x, y, z] 이런 점으로 구성할 수 있다

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 도시 환경 정의 : 각 건물은 직 육면체 형태
# (xmin, xmax, ymin, ymax, zmin, zmax)
building = [
    (-20, -10, 10, 20, 0, 20),
    (10, 20, 15, 25, 0, 25),
    (-15, -5, 35, 45, 0, 18),
    (5, 18, 50, 60, 0, 30)
]

car_positions = []  # 자동차 이동 경로

# 자동차가 y축 방향으로 이동 : y=0 ~ y=60 구간을 25개 위치로 나눔
for y in np.linspace(0, 60, 25):
    car_positions.append(np.array([0, y, 2]))   # [차량위치, 현재전진위치, 센서높이]

print('car positions : ', car_positions)

# Lidar 스캔 함수
def simulate_lidar(car_pos):
    points = []     # point cloud 저장 list
    horizontal_angles = np.linspace(-90, 90, 120)  # 수평 방향 스캔 각도 -90 ~ 90
    vertical_angles = np.linspace(-15, 15, 8)      # 수직 방향 스캔 각도 -15 ~ 15
    max_distance = 80   # 최대 측정거리
    # 모든 방향으로 레이저 발사
    for h_deg in horizontal_angles:
        for v_deg in vertical_angles:
            h = np.radians(h_deg)
            v = np.radians(v_deg)

            # 레이저 방향 벡터 계산
            dx = np.cos(v) * np.sin(h)
            dy= np.cos(v) * np.cos(h)
            dz = np.sin(v)

            # 레이저 방향으로 진행
            for d in np.linspace(0, max_distance, 400):
                # 현재 레이저 위치 계산
                x = car_pos[0] + dx * d
                y = car_pos[1] + dy * d
                z = car_pos[2] + dz * d

                hit = False
                # 모든 건물에 대한 충돌 검사
                for b in building:
                    xmin, xmax, ymin, ymax, zmin, zmax = b
                    # 현재 레이저 위치가 건물 내부에 있는지 판단
                    inside = (xmin <= x <= xmax) and (ymin <= y <= ymax) and (zmin <= z <= zmax)

                    if inside:  # 레이저가 건물과 충돌한 경우
                        points.append([x, y, z])
                        hit = True
                        break

                if hit:
                    break

    return points


all_points = []     # point cloud 저장

for pos in car_positions:
    scan_points = simulate_lidar(pos)
    all_points.extend(scan_points)


all_points = np.array(all_points)
print(all_points)


# 시각화 - 3차원
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2], c=all_points[:, 2], marker='o', s=1, cmap='jet')

car_positions_np = np.array(car_positions)

# 자동차 이동 경로 출력
ax.plot(car_positions_np[:, 0], car_positions_np[:, 1], car_positions_np[:, 2], color='black', linestyle='-', linewidth=3, label='Car Path')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Simple Lidar Simulation with Point Cloud')
ax.set_xlim(-30, 30)
ax.set_ylim(0, 70)
ax.set_zlim(0, 20)
ax.legend()
plt.legend()
plt.show()