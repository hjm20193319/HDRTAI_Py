# [개념] 데이터베이스 연동: 파이썬 애플리케이션과 MariaDB/MySQL 간의 데이터 통신을 위한 설정
import os
import pymysql # [문법] pymysql: 순수 파이썬으로 작성된 MySQL 클라이언트 라이브러리

def get_conn():
    # [문법] os.getenv(key, default): 환경 변수에서 설정값을 읽어오며, 없을 경우 기본값(default)을 사용
    # [개념] Connection Pool: 실제 서비스에서는 매번 연결을 생성하기보다 DBUtils 등을 이용한 커넥션 풀 사용을 [추천]합니다.
    return pymysql.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASS', '123'),
        database=os.getenv('DB_NAME', 'coffeedb'),
        charset='utf8',
        # [문법] DictCursor: 결과셋을 튜플이 아닌 파이썬 딕셔너리(Dictionary) 형태로 반환하여 가독성을 높임
        cursorclass=pymysql.cursors.DictCursor,
        # [문법] autocommit=True: insert/update/delete 실행 시 별도의 commit() 호출 없이 즉시 반영
        autocommit=True
    )

def insert_survey(gender:str, age:int, co_survey:str) -> None:
    # [문법] %s: SQL Injection 공격을 방지하기 위한 파라미터 바인딩 플레이스홀더
    sql = '''
        insert into survey(gender, age, co_survey)
        values(%s, %s, %s)
    '''
    conn = get_conn()
    try:
        # [문법] with conn.cursor(): 컨텍스트 매니저를 사용하여 작업 후 커서를 자동으로 닫음
        with conn.cursor() as cur:
            cur.execute(sql, (gender, age, co_survey))
    
    finally:
        # [문법] conn.close(): 사용이 끝난 DB 연결 리소스를 해제하여 메모리 누수 방지
        conn.close()

def fetchall_survey() -> list[dict]:
    # [개념] 데이터 조회: 설문조사 전체 데이터를 일련번호(rnum) 오름차순으로 가져옴
    sql = '''
        select rnum, gender, age, co_survey
        from survey
        order by rnum asc
    '''
    conn = get_conn()

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            # [문법] fetchall(): 실행된 쿼리의 모든 결과 행을 리스트로 반환
            return cur.fetchall()
    
    
    finally:
        conn.close()
