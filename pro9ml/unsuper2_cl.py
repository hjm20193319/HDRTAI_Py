# 계층적 군집 분석(Hierarchical Clustering): 개별 데이터 포인트에서 시작하여 유사한 것끼리 결합하여 계층적인 트리 구조를 형성하는 방법
# 학생 10명의 시험 점수 사용

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

students = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']
# [문법] reshape(-1, 1): 1차원 배열을 행의 개수는 자동으로 계산하고 열은 1개인 2차원 배열로 변환
scores = np.array([76,95,65,85,60,92,55,88,83,72]).reshape(-1,1)
print('점수 : ', scores)
print('\n')

# [문법] linkage(data, method='ward'): 워드 연결법(Ward's method)을 사용하여 군집 간의 오차 제곱합의 증가량을 최소화하는 방향으로 병합
linked = linkage(scores, method='ward')

# 시각화 (Dendrogram)
plt.figure(figsize=(10,7))
dendrogram(linked, labels=students)
plt.ylabel('Students score')
plt.xlabel('Students')
plt.ylabel('Distance')
plt.axhline(y=25, color='r', linestyle='--', label='cut at 25')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# [문법] fcluster: 계층적 군집 결과로부터 특정 기준(t)에 따라 평면적인 군집(Flat Cluster)을 형성
# criterion='maxclust': 최대 군집의 개수를 t개로 제한
clusters = fcluster(linked, t=3, criterion='maxclust')
print('학생 자료 군집 결과')
for stu, cluster in zip(students, clusters):
    print(f'{stu} : {cluster}')
print('\n')

# 군집 별로 점수와 학생 이름 확인 (딕셔너리 활용)
cluster_info = {}
for student, cluster, score in zip(students, clusters, scores.flatten()):
    if cluster not in cluster_info:
        cluster_info[cluster] = {'students': [], 'scores': []}
    cluster_info[cluster]['students'].append(student)
    cluster_info[cluster]['scores'].append(score)

print(cluster_info)
print('\n')

# 군집 별 평균 점수와 학생 이름 확인 (분석 결과 출력)
for cluster_id, info in sorted(cluster_info.items()):
    avg_score = np.mean(info['scores'])
    student_list = ', '.join(info['students'])
    print(f'Cluster {cluster_id} : 평균점수 = {avg_score:.2f}, 학생들 = {student_list}')

# 군집별 scatter plot (산점도 시각화)
x_positions = np.arange(len(students))
# [문법] ravel(): 다차원 배열을 1차원 배열로 평평하게(flatten) 펼쳐주는 함수
y_scores = scores.ravel()
colors = {1:'red', 2:'blue', 3:'green'}
plt.figure(figsize=(10,7))
for i, (x, y, cluster) in enumerate(zip(x_positions, y_scores, clusters)):
    plt.scatter(x, y, c=colors[cluster], label=f'Cluster {cluster}')
    plt.annotate(students[i], (x, y+1.5), fontsize=12, ha='center')
plt.xticks(x_positions, students)
plt.xlabel('Students')
plt.ylabel('Students score')
plt.title('Score Cluster')
plt.legend()
plt.grid(True)
plt.tight_layout()
# [추천] plt.show() 대신 plt.savefig('cluster_result.png')를 사용하여 결과를 파일로 저장할 수 있음
plt.show() 
# 성적 그룹 분석, 고객 등급 분류, 사용자 행동 패턴 등을 군집화할 수 있다