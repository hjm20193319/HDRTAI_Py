# 원격 데이터 베이스 연동 프로그래밍
# MariaDB : driver file 설치 후 사용
# pip install mysqlclient   -> 많이 사용

import MySQLdb      # 사용하는 DB에 맞는 드라이버를 설치후 드라이버에서 제공하는 모듈을 import 해서 사용하면 됨

'''
# 정보 하나라도 잘못 입력하면 ERROR
conn = MySQLdb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '123',
    database = 'test',
    port = 3306)
print(conn)
conn.close()
'''

# sangdata 자료 CRUD
config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '123',
    'database' : 'test',
    'port' : 3306,
    'charset' : 'utf8'
}
# DB 연결 정보를 dict type으로 별도의 객체로 선언

def myFunc():

    try:
        conn = MySQLdb.connect(**config)          # dict type을 선언해줄 때
        cursor = conn.cursor()

        # 자료 추가
        # isql = "insert into sangdata(code, sang, su, dan) values(5, '신상1', 5, 7800)"      # sql문은 전체가 하나의 문자열, 칼럼 데이터 타입만 맞춰주면 됨
        # cursor.execute(isql)    # 트랜잭션 시작
        # conn.commit()           # 트랜잭션 끝, 파이썬은 commit이 수동이다

        '''
        isql = "insert into sangdata values(%s, %s, %s, %s)"        # 문자열 더하기
        sql_data = (6, '신상2', 11, 5000)   # 튜플은 () 빼도 됨
        cursor.execute(isql, sql_data)
        conn.commit()           # 원본 DB 내용 갱신
        '''

        # 자료 수정
        '''
        usql = "update sangdata set sang = %s, su = %s, dan = %s where code = %s"       # PK는 수정대상에서 제외
        sql_data = ('물티슈', 66, 1000, 5)
        cursor.execute(usql, sql_data)
        conn.commit()
        '''
        '''
        usql = "update sangdata set sang = %s, su = %s, dan = %s where code = %s"       # PK는 수정대상에서 제외
        sql_data = ('콜라', 77, 1000, 5)
        cou = cursor.execute(usql, sql_data)             # 삭제 후 반환값 얻기 (0 또는 1)
        print('수정 건수 : ', cou)                  
        conn.commit()
        '''

        # 자료 삭제 __ 여러가지 방법
        code = '6'          
        # dsql = "delete from sangdata where code = " + code      # 문자열 더하기로 SQL완성 비권장 -- secure coding 가이드라인 위배
        # dsql = "delete from sangdata where code = %s"
        # cursor.execute(dsql, (code,))          # 주의 : 하나짜리 튜플을 할때는 (a,) 형태로 써줘야 함
        dsql = "delete from sangdata where code = '{0}'".format(code)
        # cursor.execute(dsql)
        cou = cursor.execute(dsql)          # 삭제 후 반환값 얻기 (0 또는 1 이상)
        if cou != 0:
            print('삭제 성공')
        else:
            print('삭제 실패')              # 이미 6번이 삭제된 후에는 실패 메세지 뜰것임

        conn.commit()


        # 자료 읽기 여러가지 방법(파이썬으로)
        sql = "select code, sang, su, dan from sangdata"
        cursor.execute(sql)
        
        for data in cursor.fetchall():
            # print(data)     # 튜플로 출력
            print('%s %s %s %s' %data)

        print()

        for r in cursor:
            print(r[0], r[1], r[2], r[3])

        print()

        for (코드, 상품, 수량, 단가) in cursor:    # data를 변수에 하나씩 넣어줌 ()는 없어도 됨_가독성을 위해 추가
            print(코드, 상품, 수량, 단가)           # 칼럼명이 아니라 변수명이다


    except Exception as e:
        print('err : ', e)
        conn.rollback()
    finally:
        cursor.close()                               # close 할때 는 역순으로 해준다
        conn.close()
        

if __name__ == "__main__":
    myFunc()