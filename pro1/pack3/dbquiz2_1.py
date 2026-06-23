'''
문2-1) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력

해당 직원이 근무하는 부서 내의 직원 전부를 직급별 오름차순우로 출력. 직급이 같으면 이름별 오름차순한다.

직원번호 입력 : _______

직원명 입력 : _______

직원번호 직원명 부서명 부서전화 직급 성별

1 홍길동 총무부 111-1111 이사 남

...

직원 수 :

이어서 로그인한 해당 직원이 관리하는 고객 자료도 출력한다.

고객번호 고객명 고객전화 나이

1 사오정 555-5555 34

관리 고객 수 :

hint : SQL 문 여러개 사용해서
'''

import MySQLdb

import pickle

with open('mydb.dat', mode = 'rb') as obj:          # config 외부 파일에서 읽어오기
    config = pickle.load(obj)

def jikgoinfo():
    try:
        conn = MySQLdb.connect(**config)         
        cursor = conn.cursor()

        jik_no = input('직원번호 입력 : ')
        jik_name = input('직원명 입력 : ')

        sql_jik = """
            select jikwonno as 직원번호, jikwonname as 직원명, busername as 부서명, busertel as 부서전화, jikwonjik as 직급, jikwongen as 성별
            from jikwon left outer join buser on busernum = buserno 
            where busernum = (select busernum from jikwon where jikwonno = '{0}' and jikwonname = '{1}')
        """.format(jik_no, jik_name)

        sql_gogek = """
            select gogekno as 고객번호, gogekname as 고객명, gogektel as 고객전화 
            from gogek right outer join jikwon on gogekdamsano = jikwonno 
            where jikwonno = '{0}' and jikwonname = '{1}'
        """.format(jik_no, jik_name)

        cursor.execute(sql_jik)
        datas = cursor.fetchall()
        
        cursor.execute(sql_gogek)
        datas2 = cursor.fetchall()

        if len(datas) == 0:
            print('해당 직원은 없는 직원입니다')
            return
        
        for jikwonno, jikwonname, busername, busertel, jikwonjik, jikwongen in datas:
            print(jikwonno, jikwonname, busername, busertel, jikwonjik, jikwongen)

        print('직원수 : ' + str(len(datas)))
        print()

        if len(datas2) == 0:
            print('해당 직원은 관리 고객이 없습니다')
        
        for gogekno, gogekname, gogektel in datas2:
            print(gogekno, gogekname, gogektel)

        print('관리 고객 수 : ' + str(len(datas2)))




    except Exception as e:
        print('err : ', e)
        conn.rollback()
    finally:
        cursor.close()                               # close 할때 는 역순으로 해준다
        conn.close()

if __name__ == "__main__":
    jikgoinfo()