'''
문1) jikwon 테이블 자료 출력

키보드로부터 부서번호를 입력받아, 해당 부서에 직원 자료 출력

부서번호 입력 : _______

직원번호 직원명 근무지역 직급

1 홍길동 서울 이사

...

인원 수 :
'''

# 기본적인 흐름과 구조는 알고 있기

import MySQLdb

import pickle



# 보안을 위해서 정보를 별도의 파일로 만들어서 사용하기
'''
# jikwon table이 있는 test DB 정보
config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '123',
    'database' : 'test',
    'port' : 3306,
    'charset' : 'utf8'
}
'''

with open('mydb.dat', mode = 'rb') as obj:
    config = pickle.load(obj)

def chulbal():
    try:
        conn = MySQLdb.connect(**config)         
        cursor = conn.cursor()

        bu_no = input('부서번호 입력 : ')
        # print(bu_no)              # input 내용 점검용
        sql = """
            select jikwonno as 직원번호, jikwonname as 직원명, buserloc as 근무지역, jikwonjik as 직급 
            from jikwon inner join buser on busernum = buserno
            where busernum = {0}
        """.format(bu_no)
        # print(sql)        # SQL문 완성 점검용
        
        cursor.execute(sql)             # 서버에서 RAM으로 로딩, cursor가 RAM에 접근

        datas = cursor.fetchall()
        
        if len(datas) == 0:
            print(bu_no + '번 부서는 없는데..')
            return      # sys.exit(0) : 응용 프로그램 탈출
        
        for jikwonno, jikwonname, buserloc, jikwonjik in datas:             # 가독성을 위한 변수명 설정 --- 칼럼명이 아님
            print(jikwonno, jikwonname, buserloc, jikwonjik)

        print('인원 수 : ' + str(len(datas)) + '명')             # 굳이 SQL문에서 COUNT()안해도 구할 수 있음


    except Exception as e:
        print('err : ', e)
        # conn.rollback()                            # select만 할때는 없어도 됨
    finally:
        cursor.close()                               # close 할때 는 역순으로 해준다
        conn.close()


if __name__ == "__main__":
    chulbal()
