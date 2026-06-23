# 표준편차, 분산의 중요성 : 데이터의 흩어짐 정도(산포도)를 이해하고 시각화하는 실습

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # matplotlib 한글 폰트 깨짐 방지를 위한 라이브러리

# [개념] 재현성을 위해 난수 발생 시드 고정 (동일한 시드값은 항상 동일한 난수 시퀀스를 생성)
np.random.seed(42) 

# 목표 평균 및 표준편차 설정
target_mean = 60
std_dev_small = 10  # 편차가 작은 그룹 (데이터가 평균에 밀집)
std_dev_large = 20  # 편차가 큰 그룹 (데이터가 넓게 퍼짐)

# [문법] np.random.normal(loc, scale, size): 정규분포(가우시안 분포)를 따르는 난수 생성
# loc: 평균, scale: 표준편차, size: 샘플 개수
class1_raw = np.random.normal(loc=target_mean, scale=std_dev_small, size=100)
class2_raw = np.random.normal(target_mean, std_dev_large, 100)

print(class1_raw[:5])
print('\n')

# [개념] 평균 보정(Adjustment): 생성된 난수의 실제 평균이 목표치와 미세하게 다를 수 있으므로 
# (현재값 - 현재평균 + 목표평균) 식을 통해 정확히 목표 평균에 맞춤
class1_adj = class1_raw - np.mean(class1_raw) + target_mean
print(class1_adj[:5])
class2_adj = class2_raw - np.mean(class2_raw) + target_mean
print(class2_adj[:5])
print('\n')

# [문법] np.round(): 반올림 수행, .astype(int): 데이터 타입을 정수형으로 변환
class1 = np.round(class1_adj).astype(int)
class2 = np.round(class2_adj).astype(int)
print(class1[:5])
print(class2[:5])
print('\n')

# [문법] np.clip(배열, 최소값, 최대값): 지정한 범위를 벗어나는 값을 최소/최대값으로 강제 고정
# 시험 점수이므로 10점 미만은 10으로, 100점 초과는 100으로 제한함
class1 = np.clip(np.round(class1_adj), 10, 100).astype(int)
class2 = np.clip(np.round(class2_adj), 10, 100).astype(int)
print(class1[:5])
print(class2[:5])
print('\n')

# [개념] 기술 통계량 계산
# 평균(Mean): 자료의 중심 경향성
# 표준편차(Std): 평균으로부터 떨어진 평균 거리
# 분산(Var): 표준편차의 제곱, 관측값들이 얼마나 퍼져 있는지 나타냄
mean1, mean2 = np.mean(class1), np.mean(class2)
std1, std2 = np.std(class1), np.std(class2)
var1, var2 = np.var(class1), np.var(class2)

print('--- 통계 결과 비교 ---')
print('1반(성적 편차가 작음 - 고른 성적)')
print(f'평균 : {mean1}, 표준편차 : {std1}, 분산 : {var1}')
print('2반(성적 편차가 큼 - 성적 차이가 심함)')
print(f'평균 : {mean2} 표준편차 : {std2}, 분산 : {var2}')

# [문법] pd.DataFrame: 딕셔너리 구조를 활용하여 데이터프레임 생성
df = pd.DataFrame({
    'class':['1반'] * 100 + ['2반'] * 100,
    'score': np.concatenate([class1, class2]) # [문법] np.concatenate: 두 배열을 하나로 합침
})
print(df.head())
# [문법] to_csv: 데이터를 CSV 파일로 저장. encoding='utf-8-sig'는 엑셀 한글 깨짐 방지용
df.to_csv('test1vari.csv', index=False, encoding='utf-8-sig')
print('\n')

# --- 시각화 ---
# [추천] : 산점도에서 x축 값을 미세하게 흔들어주는 'Jittering' 기법을 사용하면 데이터 겹침을 방지하여 분포 확인이 더 용이합니다.
x1 = np.random.normal(1, 0.05, size=100)
x2 = np.random.normal(2, 0.05, size=100)

# 1) 산포도(Scatter Plot): 개별 데이터의 분포를 직접 확인
plt.figure(figsize=(10, 6))
plt.scatter(x1, class1, alpha=0.8, label=f'1반(평균={mean1:.2f}, 표준편차={std1:.2f})')
plt.scatter(x2, class2, alpha=0.8, label=f'2반(평균={mean2:.2f}, 표준편차={std2:.2f})')
# [문법] plt.hlines: 수평선 그리기 (y값, x시작, x끝)
plt.hlines(target_mean, 0.5, 2.5, colors='red', linestyles='dashed', label=f'목표 평균={target_mean}') 
plt.xticks([1, 2], ['1반', '2반'])
plt.ylabel('시험 점수')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 2) 박스 플롯(Boxplot): 사분위수(25%, 50%, 75%)와 이상치를 한눈에 파악
plt.figure(figsize=(8, 5))
plt.boxplot([class1, class2], labels=['1반', '2반'])
plt.ylabel('시험 점수')
plt.grid(True)
plt.tight_layout()
plt.show()

# 3) 히스토그램(Histogram): 도수분포표를 그래프로 나타내어 데이터의 빈도와 밀집도 확인
plt.figure(figsize=(10, 6))
# bins: 구간의 개수, alpha: 투명도
plt.hist(class1, bins=15, alpha=0.6, label='1반', edgecolor='black') 
plt.hist(class2, bins=15, alpha=0.6, label='2반', edgecolor='blue')
# [문법] plt.axvline: 수직선 그리기 (평균선 표시)
plt.axvline(target_mean, color='red', linestyle='dotted', label=f'목표 평균={target_mean}')
plt.xlabel('시험 점수')
plt.ylabel('빈도수')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# 국어 선생님 입장
# 귀무 가설(전통적 주장) : 두 반의 국어 점수의 표준편차(평균)는 차이가 없다

# 누군가가 실험을 통해 데이터 수집 후 두 반의 점수에 대한 통계 계산 후 새로운 주장(의견)
# -> 대립 가설 : 두 반의 국어 점수의 표준편차(평균)는 차이가 있다

# 가설 검정(t-test)을 통해 두 의견의 채택, 기각을 판단할 수 있다