# 원격 DB 연동 - jikwon 자료를 읽어 DataFrame에 저장

# import MySQLdb
import pymysql  # MySQL/MariaDB와 연동하기 위한 파이썬 라이브러리
import numpy as np  # 수치 계산 및 배열 처리를 위한 라이브러리
import pandas as pd  # 데이터 분석 및 조작을 위한 라이브러리 (DataFrame 사용)
import matplotlib.pyplot as plt  # 데이터 시각화를 위한 기본 라이브러리
import koreanize_matplotlib  # matplotlib 사용 시 한글 폰트 깨짐을 자동으로 해결해주는 라이브러리
import csv  # CSV 파일 읽기 및 쓰기를 위한 내장 모듈

# [환경 설정]
# DB 접속 정보를 딕셔너리 형태로 정의 (언패킹 연산자 **를 사용하여 인자로 전달 가능)
config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True
}

try:
    # pymysql.connect(): 설정 정보를 바탕으로 데이터베이스 연결 객체 생성
    conn = pymysql.connect(**config) 
    # cursor(): SQL 쿼리를 실행하고 결과를 가져오는 포인터 역할을 하는 객체 생성
    cur = conn.cursor() 
    sql = '''
    select jikwonno, jikwonname, busername, jikwonjik, jikwongen,jikwonpay  \
    from jikwon inner join buser on jikwon.busernum = buser.buserno
    '''
    cur.execute(sql)

    # for (jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay) in cur:
    #     print(jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay)
    # print()

# DataFrame 으로 출력
    # cur.fetchall(): 실행된 SQL의 모든 결과 레코드를 튜플의 튜플 형태로 반환
    df1 = pd.DataFrame(cur.fetchall(),
                    columns=['jikwonno', 'jikwonname', 'busername', 'jikwonjik', 'jikwongen', 'jikwonpay'])
    print(df1.head(3)) # 상위 3개의 행만 출력
    print('연봉의 총 합 : ', df1['jikwonpay'].sum())
    print('\n')
    
# csv file i/o
    cur.execute(sql) # 커서를 다시 처음으로 돌리기 위해 재실행

    # open(mode='w'): 쓰기 모드로 파일 열기. encoding='utf-8'은 한글 저장 시 표준 인코딩
    with open('pandasdb2.csv', mode='w', encoding='utf-8') as fobj:
        writer = csv.writer(fobj) # CSV 작성을 위한 writer 객체 생성
        for row in cur:
            writer.writerow(row) # 각 레코드를 CSV 파일의 한 줄로 기록

    # pd.read_csv(): CSV 파일을 읽어 DataFrame 생성. header=None은 첫 줄을 데이터로 인식함
    df2 = pd.read_csv('pandasdb2.csv', header=None, names=['번호', '이름', '부서', '직급', '성별', '연봉'])
    print(df2.head(3))
    print('연봉의 총 합 : ', df2['연봉'].sum())
    print('\n')

# pandas의 sql 처리 함수 이용
    # pd.read_sql(): SQL 쿼리와 connection 객체를 인자로 받아 직접 DataFrame으로 변환 (가장 권장되는 방식)
    df = pd.read_sql(sql, conn)
    df.columns = ['번호', '이름', '부서', '직급', '성별', '연봉'] # 컬럼명 일괄 변경
    print(df.head(3))       #  == print(df[:2]) == print(df[:-28])
    print('연봉의 총 합 : ', df['연봉'].sum()) # 집계 함수 sum() 사용
    print(df['이름'].count(), ' ', len(df))     # 건수 (count()는 유효값 개수, len()은 전체 행 개수)
    print('부서별 인원수 : \n', df['부서'].value_counts()) # value_counts(): 범주형 데이터의 빈도수 계산
    print('연봉 7000 이상\n', df.loc[df['연봉'] >= 7000]) # 불리언 인덱싱을 통한 데이터 필터링
    # 교차표
    # pd.crosstab(index, columns): 두 범주형 변수의 빈도를 표 형태로 나타냄. margins=True는 합계(All) 표시
    ctab = pd.crosstab(df['성별'], df['직급'], margins=True)
    print(ctab)
    print('\n')

# 시각화
    # groupby('컬럼'): 특정 컬럼을 기준으로 그룹화하여 집계 연산 수행
    jik_ypay = df.groupby('직급')['연봉'].mean()     # 직급별 연봉 평균
    print('직급별 연봉 평균 : ', jik_ypay)
    # plt.pie(): 원형 차트 생성
    # explode: 특정 조각을 밖으로 튀어나오게 설정, shadow: 그림자 효과, counterclock: 시계 방향 여부
    plt.pie(jik_ypay, explode=(0.2,0,0,0.3,0), labels=jik_ypay.index, shadow=True, counterclock=False)
    plt.show()

except Exception as err:
    print('error : ', err)

finally:
    cur.close()
    conn.close()