# Pandas File I/O (입출력) 및 대용량 데이터 처리(Chunk) 연습

import pandas as pd
import numpy as np

# 출력 옵션 설정: 콘솔에서 생략 없이 모든 컬럼과 행을 볼 수 있도록 설정
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 1. CSV 파일 읽기 (기본)
# read_csv(): 쉼표(,)를 기본 구분자로 사용하여 데이터를 읽어 DataFrame 생성
df = pd.read_csv('ex1.csv')     
print(df, type(df))

# 2. read_table() 사용
# read_table(): 탭(\t)을 기본 구분자로 사용하므로, CSV를 읽을 때는 sep=',' 명시 필요
df = pd.read_table('ex1.csv', sep=',')   
print(df)
# skip_blank_lines=True: 파일 내의 빈 줄을 무시하고 읽음
df = pd.read_table('ex1.csv', sep=',', skip_blank_lines=True)   

# 3. 웹상의 데이터 및 옵션 활용
# URL을 직접 전달하여 원격 저장소의 CSV 파일을 읽어올 수 있음
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv')
print(df)

# header=None: 첫 번째 행을 컬럼명으로 쓰지 않고 0, 1, 2... 인덱스로 지정
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv', 
                header=None)
print(df)

# skiprows=n: 처음 n개의 행을 제외하고 읽음
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv', 
                header=None,
                skiprows=1
                )
print(df)

# names: 컬럼 이름을 직접 리스트로 부여
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex2.csv', 
                header=None,
                names=['a', 'b', 'c', 'd', 'e']
                )
print(df)

# sep='\s+': 공백(Space)이 하나 이상인 경우를 구분자로 정규표현식 처리
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/ex3.txt',
                sep='\s+',
                skiprows=[1, 3]
                )
print(df)

# read_fwf(): 고정 길이(Fixed Width) 포맷의 파일을 읽을 때 사용
df = pd.read_fwf('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/data_fwt.txt',
                header=None,
                widths=(10, 3, 5),
                names=('date', 'name', 'price'),
                encoding='utf-8'
                )
print(df)
print(df.iloc[:, 0])
print(df['date'])

print('------------------')

# [개념] Chunk (청크) 처리
# - 대량의 데이터를 한 번에 메모리에 올리지 않고, 지정한 행(Size)만큼 나누어 읽는 방식
# - 장점: 메모리 부족(OOM) 방지, 스트리밍 방식의 순차 처리 가능
# - 단점: I/O 반복 발생으로 전체 로딩 속도는 단일 로딩보다 느릴 수 있음
# - 활용: 데이터 전처리, 부분 통계 계산 등

import time
import os

# 테스트용 대량 데이터 생성 (10,000행)
n_rows = 10000 
data = {
    'id':range(1, n_rows + 1),
    'name':[f'Student_{i}' for i in range(1, n_rows + 1)],
    'score':np.random.randint(50, 101, size=n_rows), # 50~100 사이 난수
    'score2':np.random.randint(50, 101, size=n_rows) # 50~100 사이 난수
}
df = pd.DataFrame(data)
print(df.head())
print(df.tail(3))
print()

# to_csv(): DataFrame을 CSV 파일로 저장
if not os.path.exists('student.csv'):
    df.to_csv('student.csv', index=False)

# csv 파일 읽기 : 전체 한 번에 읽기
start_all = time.time() # 시작 시간 기록
df_all = pd.read_csv('student.csv') # 전체 데이터를 메모리에 로드
average_all = df_all['score'].mean() # score 컬럼 평균 계산
average_all2 = df_all['score2'].mean() # score2 컬럼 평균 계산
end_all = time.time() # 종료 시간 기록

print(f'전체 읽기 처리 결과 - 평균1: {average_all:.2f}, 평균2: {average_all2:.2f}, 소요시간: {end_all - start_all:.7f}초\n')

# csv 파일 읽기 : 청크(chunk) 단위로 읽기
# chunksize 옵션을 주면 TextFileReader 객체(반복자)를 반환함
chunk_size = 1000 
total_score = 0
total_score2 = 0
total_count = 0
start_chunk_total = time.time()

# 반복문을 통해 chunksize만큼의 DataFrame을 순차적으로 처리
for i, chunk in enumerate(pd.read_csv('student.csv', chunksize=chunk_size)):
    start_chunk = time.time()
    # 청크 처리 중 첫번째 학생 정보 출력
    first_student = chunk.iloc[0]
    print(f'청크 {i + 1} 처리 결과 - 각 청크 첫번째 학생 : ID = {first_student["id"]}, 이름 = {first_student["name"]}')
    print(f'청크 {i + 1} 처리 결과 - 점수1 : {first_student["score"]}, 점수2 : {first_student["score2"]}')
    
    # 각 청크의 합계를 누적하여 전체 평균을 구할 준비
    total_score += chunk['score'].sum()
    total_score2 += chunk['score2'].sum()
    total_count += len(chunk) # 현재 청크의 행 수 누적

    end_chunk = time.time()
    elapsed = end_chunk - start_chunk
    print(f'청크 {i + 1} 처리 소요시간: {elapsed:.7f}초\n')     # 청크 단위

time_chunk_total = time.time() - start_chunk_total
average_chunk = total_score / total_count
average_chunk2 = total_score2 / total_count
time_all = end_all - start_all

print(f'전체 학생 수 : {total_count}명, 점수 총합 : {total_score}, 점수2 총합 : {total_score2}, 전체 처리 시간 : {time_all:.7f}초\n')
print(f'청크 단위 처리 결과 - 평균1: {average_chunk:.2f}, 평균2: {average_chunk2:.2f}, 소요시간: {time_chunk_total:.7f}초\n')
print()

# 4. 시각화 (Visualization) - 처리 방식에 따른 성능 비교
import matplotlib.pyplot as plt

# 한글 깨짐 방지를 위한 폰트 설정 (Windows: Malgun Gothic)
plt.rc('font', family='Malgun Gothic')

# 그래프에 표시할 데이터 설정
labels = ['전체', '청크']
times = [time_all, time_chunk_total]
colors = ['skyblue', 'lightcoral']

# 그래프 크기 설정 (가로 6, 세로 4 인치)
plt.figure(figsize=(6, 4)) 

# 막대 그래프(Bar Chart) 생성
bars = plt.bar(labels, times, color=colors)

# 막대 상단에 실제 소요 시간 수치 표시 (텍스트 추가)
for bar, time_val in zip(plt.bar(labels, times, color=colors), times):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{time_val:.7f}', ha='center', va='bottom')

plt.title('청크 처리 시간 비교') # 그래프 제목
plt.ylabel('소요 시간 (초)')     # y축 라벨
plt.grid(linestyle='--')       # 배경 그리드 설정 (점선)
plt.tight_layout()             # 여백 자동 조정
plt.show()                     # 그래프 출력

print('------------------')