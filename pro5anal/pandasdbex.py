# pandas 문제 7)

#  a) MariaDB에 저장된 jikwon, buser, gogek 테이블을 이용하여 아래의 문제에 답하시오.

#      - 사번 이름 부서명 연봉, 직급을 읽어 DataFrame을 작성

#      - DataFrame의 자료를 파일로 저장

#      - 부서명별 연봉의 합, 연봉의 최대/최소값을 출력

#      - 부서명, 직급으로 교차 테이블(빈도표)을 작성(crosstab(부서, 직급))

#      - 직원별 담당 고객자료(고객번호, 고객명, 고객전화)를 출력. 담당 고객이 없으면 "담당 고객  X"으로 표시

#      - 연봉 상위 20% 직원 출력  : quantile()
#      - SQL로 1차 필터링 후 pandas로 분석 

#             - 조건: 연봉 상위 50% (df['연봉'].median() ) 만 가져오기  후 직급별 평균 연봉 출력

#      - 부서명별 연봉의 평균으로 가로 막대 그래프를 작성


#  b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.

#      - pivot_table을 사용하여 성별 연봉의 평균을 출력

#      - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프

#      - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))



#  c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.

#       조건 :  try ~ except MySQLdb.OperationalError as e:      사용

#      사번  직원명  부서명   직급  부서전화  성별

#      ...

#      인원수 : * 명

#     - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
#     - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력


import MySQLdb
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import csv
import seaborn as sns
# pip install sqlalchemy
from sqlalchemy import create_engine
# 1. 엔진 생성 (접속 정보 입력)
# 형식: dialect+driver://username:password@host:port/database
engine = create_engine('mysql+mysqldb://root:123@127.0.0.1:3306/test', encoding='utf-8')
# 엔진 전달
# df = pd.read_sql(sql, con=engine)

with open('mydb.dat', mode = 'rb') as obj:          # config 외부 파일에서 읽어오기
    config = pickle.load(obj)

conn = MySQLdb.connect(**config)
cur = conn.cursor()

sql1 = '''
    select jikwonno, jikwonname, busername, jikwonpay, jikwonjik 
    from jikwon left outer join buser 
    on jikwon.busernum = buser.buserno
'''
df1 = pd.read_sql(sql1, conn, index_col='jikwonno')
print(df1)
print('\n')

# DataFrame을 직접 CSV로 저장하는 것이 더 간단하고 효율적입니다.
# SQL을 재실행하고 csv 모듈을 사용할 필요가 없습니다. (pandas6.py 참고)
# df1.to_csv('jikwon_data.csv', encoding='utf-8-sig')
cur.execute(sql1)
with open('df1_csv', mode='w', encoding='utf-8') as fobj:
    writer = csv.writer(fobj)
    for row in cur:
        writer.writerow(row)

buser_pay = df1.groupby('busername')['jikwonpay'].agg(['sum','max','min'])
print(buser_pay)
print('\n')

print(pd.crosstab(df1['busername'], df1['jikwonjik'], margins=True))
print('\n')

sql2 = '''
    select jikwonno, jikwonname, gogekno, gogekname, gogektel
    from jikwon left outer join gogek
    on jikwon.jikwonno = gogek.gogekdamsano
'''
# np.nan을 바꾸는 데에는 .replace() 대신 .fillna()를 사용하는 것이 의도에 더 명확하게 부합합니다.
# df2 = pd.read_sql(sql2, conn, index_col='jikwonno').fillna('담당 고객 X')
df2 = pd.read_sql(sql2, conn, index_col='jikwonno').replace(np.nan, '담당 고객 X')
print(df2)
print('\n')  

print(df1[df1['jikwonpay'] > df1['jikwonpay'].quantile(0.8)])
print('\n')

df50 = df1[df1['jikwonpay'] > df1['jikwonpay'].median()]
print(df50)
print('\n')

jik_pay50 = df50.groupby('jikwonjik')['jikwonpay'].mean()
print(jik_pay50)
print('\n')

busername_pay = df1.groupby('busername')['jikwonpay'].mean()
print(busername_pay)
print('\n')

# Matplotlib을 직접 사용하는 대신, Pandas의 내장 plot 기능을 사용하면 더 간결하게 코드를 작성할 수 있습니다. (plot2.py 참고)
# busername_pay.plot(kind='barh', title='부서별 연봉 평균')
# plt.barh(busername_pay.index, busername_pay.values)
# plt.show()

###############################################################
dfjikwon = pd.read_sql('select * from jikwon', conn)
jikwon_pivot = dfjikwon.pivot_table(index='jikwongen', values='jikwonpay', aggfunc='mean')
print(jikwon_pivot)
print('\n')

# pivot_table로 생성된 결과 역시 DataFrame이므로, plot 기능을 바로 사용할 수 있습니다.
# jikwon_pivot.plot(kind='bar', title='성별 연봉 평균')

sql = '''
    select jikwonno, busernum, jikwongen, busername 
    from jikwon left outer join buser
    on jikwon.busernum = buser.buserno
'''
dfjikwonbu = pd.read_sql(sql, conn)

ctab = pd.crosstab(dfjikwonbu['busername'],dfjikwonbu['jikwongen'], margins=True)
print(ctab)
print('\n')

##################################################################
try:
    sql = '''
        select jikwonno, jikwonname, busername, jikwonjik, busertel, jikwongen, jikwonpay
        from jikwon left outer join buser
        on jikwon.busernum = buser.buserno
    '''
    df = pd.read_sql(sql, conn)
    # 로그인 확인을 위해 전체 데이터를 불러오는 것은 비효율적입니다.
    # SQL의 WHERE 절을 사용하여 필요한 데이터만 가져오는 것이 훨씬 빠르고 효율적인 방법입니다.
    # sql_login = "SELECT ... FROM jikwon ... WHERE jikwonno=%s AND jikwonname=%s"
    # cur.execute(sql_login, (loginno, loginname))
    # login_data = cur.fetchone() # 데이터가 있으면 로그인 성공, 없으면 실패
    loginno = input('사번을 입력하시오 : ')
    loginname = input('이름을 입력하시오 : ')
    df.columns = ['사번', '이름', '부서', '직급', '부서전화', '성별', '연봉']

    logincheck = df[(df['사번'] == int(loginno)) & (df['이름'] == loginname)]

    if logincheck.empty:
        print('로그인 실패')
    else:
        print('로그인 성공')
        print(df[['사번', '이름', '부서', '직급', '성별']], '\n', '인원수 : ', len(df))
        print('\n')

        sns.boxplot(data=df, x='성별', y='연봉')
        plt.show()

        # 남/여 연봉 분포를 '비교'하려면 histplot의 hue 옵션을 사용하는 것이 더 효과적입니다.
        # 하나의 그래프에서 두 그룹의 분포를 겹쳐서 보여주어 직관적인 비교가 가능합니다. (plot3.py, plot5bike.py 참고)
        # sns.histplot(data=df, x='연봉', hue='성별', kde=True)
        sns.histplot(data=df, x='성별', y='연봉', kde=True)
        plt.show()


except MySQLdb.OperationalError as err:
    print('error : ', err)

cur.close()
conn.close()