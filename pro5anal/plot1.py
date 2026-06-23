# matplotlib : 파이썬에서 데이터를 차트나 플롯으로 그려주는 가장 기본적인 시각화(플로팅) 라이브러리
#               MATLAB의 시각화 기능을 모델링하여 그래프 생성을 위한 다양한 함수를 제공
# 시각화의 중요성: 방대한 수치 데이터를 직관적인 그림으로 변환하여 패턴, 추세, 이상치를 쉽게 파악하게 함

import numpy as np
import matplotlib.pyplot as plt

# [환경 설정]
# plt.rc(): 런타임 설정(rc)을 변경. family='Malgun Gothic'은 윈도우의 기본 한글 폰트를 지정함
plt.rc('font', family='Malgun Gothic')      # 한글 깨짐 방지 (폰트 설정)
# axes.unicode_minus: 유니코드 마이너스 기호 사용 여부. False로 설정해야 한글 폰트 사용 시 음수 부호('-')가 깨지지 않음
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지(한글을 사용하면 음수가 깨짐) 

x = ['서울', '인천',' 수원']        # [0, 1, 2]와 같음
# 시각화 데이터 타입:
# x = ('서울', '인천',' 수원')      tuple도 사용 가능
# x = {'서울', '인천',' 수원'}      set 타입은 사용이 불가능 -> 순서가 없어서 인덱싱이 안되기 때문에(only 중복 배제)
y = [5, 3, 7]

plt.xlim([-1,3])
plt.ylim([0,10])

# tick 설정 : 축의 간격(눈금)과 라벨(label)을 인위적으로 표시
# list(range(start, stop, step)): 0부터 10까지 3씩 증가하는 리스트 생성 [0, 3, 6, 9]
plt.yticks(list(range(0, 11, 3)))

plt.plot(x, y)      # 선 그래프 생성 (기본값)
plt.show()      # 생성된 모든 그래프 객체를 화면에 출력하고 메모리에서 비움

data = np.arange(1, 11 ,2)      # [1, 3, 5, 7, 9] 생성
# plt.plot(y): 인자가 하나만 전달되면 해당 데이터를 y축 값으로 간주하고, x축은 0부터 시작하는 인덱스로 자동 설정함
plt.plot(data)      # y축의 데이터로 들어감 
plt.show()          # x축 구간은 자동으로 설정 (0, 1, 2, 3, 4)

data = np.arange(1, 11 ,2)
plt.plot(data)
x = [0,1,2,3,4]
# zip(x, data): 두 리스트의 요소를 하나씩 짝지어 반환 (0,1), (1,3)...
for a, b in zip(x, data):
    # plt.text(x좌표, y좌표, 문자열): 그래프 상의 특정 위치에 텍스트 주석을 추가함
    plt.text(a, b, str(b))      # 차트에 데이터 값(텍스트) 표시
plt.show()

x = np.arange(10)
y = np.sin(x)       # 넘파이의 사인 함수 적용 (벡터 연산)
print(x,y)
plt.plot(x,y)
plt.show()

x = np.arange(10)
y = np.sin(x)
print(x, y)
# 포맷 문자열 'bo--': b(blue, 파란색), o(circle marker, 원형 마커), --(dashed line, 점선 스타일)
# linewidth: 선의 두께, markersize: 마커의 크기 조절
plt.plot(x, y, 'bo--', linewidth=2, markersize=12)
plt.show()

# hold : plt.show()를 호출하기 전까지 여러 번의 plot 명령을 내리면 하나의 Axes에 겹쳐서 그려짐
x = np.arange(0, np.pi * 3, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(10, 5))         # 새로운 Figure 객체 생성 및 전체 크기(너비, 높이) 설정 (단위: 인치)
plt.plot(x, y1, 'r')    # 선그래프 (r: red)
plt.scatter(x, y2)         # 산점도
plt.xlabel('x 축')
plt.ylabel('y 축')
plt.title('sin, cos 그래프')
plt.legend(['sin', 'cos'])
plt.show()

# subplot : 하나의 Figure(도화지)를 여러 개의 격자(Axes)로 나누어 각각 다른 그래프를 그림
# plt.subplot(행의 수, 열의 수, 순서)
plt.subplot(2, 1, 1)
plt.plot(x, y1, 'r')
plt.title('sin 그래프')     # 상단 그래프 제목

plt.subplot(2, 1, 2)
plt.plot(x, y2, 'b')
plt.title('cos 그래프')     # 하단 그래프 제목
plt.show()

print('------------------')
irum = ['a', 'b', 'c', 'd', 'e'] # x축에 사용할 범주형 데이터(이름)
kor = [80, 50, 70, 70, 90]       # y축에 사용할 수치 데이터(국어 점수)
eng = [60, 70, 80, 90, 100]      # y축에 사용할 수치 데이터(영어 점수)

# plt.plot(x, y, format): 'ro-'는 red(빨강), circle marker(원), solid line(실선)을 의미
plt.plot(irum, kor, 'ro-')
# 'bo--'는 blue(파랑), circle marker(원), dashed line(점선)을 의미
plt.plot(irum, eng, 'bo--')

plt.ylim([50,100]) # y축의 표시 범위를 50부터 100까지로 제한 (데이터 집중도 향상)
plt.title('시험 점수') # 그래프의 중앙 상단 제목 설정
plt.xlabel('이름')     # x축 하단 라벨 설정
plt.ylabel('점수')     # y축 좌측 라벨 설정

# plt.legend(): 범례 표시. loc=4는 'lower right'(우측 하단) 위치를 의미함
plt.legend(['국어', '영어'], loc=4)     # loc = 'best'  -> 잘 보일만한 곳에 알아서 표시
plt.grid(True) # 그래프 배경에 격자(Grid)를 표시하여 수치 파악을 용이하게 함

fig = plt.gcf()     # 이미지로 저장할 준비. gcf()는 'Get Current Figure'의 약자로 현재 활성화된 Figure 객체를 반환
plt.show()          # 화면에 그래프 출력 (출력 후에는 내부적으로 Figure가 비워질 수 있음)
fig.savefig('plot1.png') # savefig(): 현재 Figure 객체를 지정한 파일명과 확장자로 로컬 디스크에 저장

from matplotlib.pyplot import imread # imread: 이미지 파일을 수치 데이터(배열)로 읽어오는 함수
img = imread('plot1.png') # 저장된 png 파일을 읽어 numpy 배열 형태로 변환
plt.imshow(img) # imshow(): 수치화된 이미지 데이터를 좌표축 위에 시각화
plt.show()      # 이미지 플롯 출력

print('------------------')
