# local db 연동 후 DataFrame에 자료 저장
import sqlite3 # 파이썬 내장 라이브러리로 별도 설치 없이 SQLite DB 연동 가능

# if not exists: 테이블이 없을 때만 생성하여 오류 방지
# varchar(가변길이 문자열), real(실수), integer(정수) 타입 정의
sql = 'create table if not exists extab(product varchar(10), maker varchar(10), weight real, price integer)'

# sqlite3.connect(':memory:'): 디스크가 아닌 RAM(메모리)에 임시 DB 생성 (속도가 빠름)
conn = sqlite3.connect(':memory:') 
cur = conn.cursor() # SQL 실행 및 결과 페치를 위한 커서 객체 생성
cur.execute(sql) # 테이블 생성 쿼리 실행
conn.commit() # 변경 사항을 데이터베이스에 물리적으로 반영

# 데이터 삽입을 위한 튜플 리스트 준비
data = [
    ('mouse','samsung', 12.5, 5000),
    ('keyboard','lg',52.5,35000)
    ]
isql = 'insert into extab values(?,?,?,?)'
cur.executemany(isql, data)
data1 = ('pen','abc',5.0,1200)
cur.execute(isql, data1) # 단일 행 삽입
conn.commit()

# 데이터 조회
cursor = conn.execute('select * from extab')
rows = cursor.fetchall() # 모든 레코드를 튜플의 리스트 형태로 가져옴
for a in rows:
    print(a)

#######################
# rows를 DataFrame에 저장
import pandas as pd
# pd.DataFrame(data, columns): 리스트 데이터를 기반으로 컬럼명을 지정하여 데이터프레임 생성
df1 = pd.DataFrame(rows, columns=['product', 'maker', 'weight', 'price'])
print(df1)
print(df1.describe()) # 수치형 데이터(weight, price)의 요약 통계량 출력
print()

#########################
# pandas의 read_ 이용
# pd.read_sql(query, connection): SQL 쿼리 결과를 즉시 DataFrame으로 변환 (가장 효율적)
df2 = pd.read_sql('select * from extab', conn)
print(df2)
print(df2.describe())
# as 건수: SQL 별칭(Alias)을 사용하여 결과 컬럼명 지정
print(pd.read_sql('select count(*) as 건수 from extab', conn))
print()

#########################
# DataFrame의 자료를 테이블에 저장(insert)
data = { # 딕셔너리 구조: Key는 컬럼명, Value는 데이터 리스트
    'product':['연필','볼펜','지우개'],
    'maker':['모나미','모나미','모나미'],
    'weight':[2.3, 3.0, 5.0],
    'price':(1000, 2000, 500)
}
frame = pd.DataFrame(data)
print(frame)
# to_sql: DataFrame을 DB 테이블로 내보내기. if_exists='append'는 기존 데이터 뒤에 추가
frame.to_sql('extab', conn, if_exists='append', index=False)
print('\n')

df3 = pd.read_sql('select * from extab', conn)
print(df3)

# 리소스 해제: 사용이 끝난 커서와 연결 객체를 닫아 메모리 누수 방지
cursor.close()
conn.close()