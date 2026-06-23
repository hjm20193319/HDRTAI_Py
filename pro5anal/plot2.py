# 차트 영역 객체 선언시 인터페이스 유형 두 가지
# Matplotlib은 상태 기반(State-based) 방식과 객체 지향(Object-Oriented) 방식 두 가지 인터페이스를 제공함
import numpy as np
import matplotlib.pyplot as plt

# 1) Matplotlib 스타일의 인터페이스
# MATLAB과 유사한 방식으로, plt 함수를 호출하면 현재 활성화된 Figure나 Axes에 명령이 적용됨
x = np.arange(10)
plt.figure()        # 새로운 도화지(Figure) 생성
plt.subplot(2, 1, 1) # 2행 1열 구조의 첫 번째(상단) 서브플롯 생성
plt.plot(x, np.sin(x))
plt.subplot(2, 1, 2) # 2행 1열 구조의 두 번째(하단) 서브플롯 생성
plt.plot(x, np.cos(x))
plt.show()          # 화면 출력 및 메모리 정리

# 2) OOP(객체 지향) 스타일의 인터페이스
# Figure와 Axes 객체를 명시적으로 생성하고 변수에 할당하여 제어하는 방식 (복잡한 레이아웃에 유리)
fig, ax = plt.subplots(nrows=2, ncols=1)
ax[0].plot(x, np.sin(x))    # 첫 번째 축 객체(ax[0])에 그래프 그림
ax[1].plot(x, np.cos(x))    # 두 번째 축 객체(ax[1])에 그래프 그림
plt.show()

print('------------------')

# 차트의 종류 일부 확인
fig = plt.figure()                  # 전체 차트의 틀 생성
ax1 = fig.add_subplot(1, 2, 1)      # 1행 2열 중 첫 번째 영역 추가
ax2 = fig.add_subplot(1, 2, 2)      # 1행 2열 중 두 번째 영역 추가

# 히스토그램
# 데이터의 빈도 분포를 막대 형태로 나타냄. bins는 구간의 개수, alpha는 투명도(0~1)
ax1.hist(np.random.randn(1000), bins=100, color='k', alpha=0.9)

# 꺾은선 그래프
# 연속적인 데이터의 변화를 파악할 때 사용
ax2.plot(np.random.rand(1000))      
plt.show()

# 막대 그래프
# 범주형 데이터의 수치를 비교할 때 사용. 수직 막대가 기본
data = [50, 80, 100, 90, 70]
plt.bar(range(len(data)), data)     # x축 위치와 높이 데이터를 인자로 받음
plt.show()

err = np.random.rand(len(data))     # 오차 막대

# 수평 막대 그래프
# 항목 이름이 길 때 가독성이 좋음
plt.barh(range(len(data)), data, alpha = 0.5)    
plt.show()

# 원 그래프
# 전체에서 각 항목이 차지하는 비율을 시각화. explode는 특정 조각을 돌출시키는 효과
plt.pie(data, colors=['yellow', 'blue', 'red'], explode=(0, 0.2, 0, 0.1, 0,))
plt.title('Pie Chart')
plt.show()

# 박스 플롯 : 전체 데이터의 분포를 확인하기에 효과적. 이상치 확인에 도움
# 중앙값(Q2), 사분위수(Q1, Q3), 최댓값/최솟값(Whisker), 이상치(Outlier)를 한눈에 보여줌
data = [1, 50, 80, 100, 90, 70, 300]
plt.boxplot(data)
plt.show()

# 산점도
# bubble chart : 산점도 차트에 점의 크기를 동적으로 표시
# x, y 좌표 외에 색상(c)과 크기(s)라는 추가 차원의 정보를 표현 가능
n = 30
np.random.seed(0)
x = np.random.rand(n)
y = np.random.rand(n)
color = np.random.rand(n)
sclae = np.pi * (np.random.rand(n) * 15) ** 2
plt.scatter(x, y, c=color, s=sclae)
plt.show()

# 시계열 데이터로 선그래프 
# 시간의 흐름에 따른 데이터의 변화를 관찰
import pandas as pd
fdata = pd.DataFrame(np.random.randn(1000, 4),
                    index=pd.date_range('1/1/2000', periods=1000), # 날짜 인덱스 생성
                    columns=list('ABCD'))
fdata = fdata.cumsum()  # 누적합(Cumulative Sum) 계산: 데이터의 추세를 명확히 함
plt.plot(fdata)
plt.show()

# pandas 의 plot 기능
# DataFrame 객체에서 직접 matplotlib을 호출하여 그래프를 생성하는 편리한 기능
fdata.plot()            # 기본 선 그래프
fdata.plot(kind='bar')  # 막대 그래프 형태로 변경 (데이터가 많으면 가독성이 떨어질 수 있음)
plt.xlabel('time')      # x축 라벨 설정
plt.ylabel('data')      # y축 라벨 설정
plt.show()
print('------------------')