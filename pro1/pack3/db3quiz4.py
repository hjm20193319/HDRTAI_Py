'''
문4)직원별 관리 고객 수 출력 (관리 고객이 없으면 출력에서 제외)

직원번호 직원명 관리 고객 수

1 홍길동 3

2 한송이 1
'''


import MySQLdb

import pickle

# 보안을 위해서 정보를 별도의 파일로 만들어서 사용하기

with open('mydb.dat', mode = 'rb') as obj:          # config 외부 파일에서 읽어오기
    config = pickle.load(obj)

def jik_gogek():
    try:
        conn = MySQLdb.connect(**config)         
        cursor = conn.cursor()

        sql_gogek = """
            select jikwonno as 직원번호, jikwonname as 직원명, count(gogekno) as 관리고객수 
            from jikwon inner join gogek on jikwonno = gogekdamsano 
            group by jikwonname
            order by jikwonno
        """

        cursor.execute(sql_gogek)
        datas = cursor.fetchall()


        for jikwonno, jikwonname, gogekcount in datas:
            print(jikwonno, jikwonname, gogekcount)


        
    except Exception as e:
        print('err : ', e)
        conn.rollback()
    finally:
        cursor.close()                               # close 할때 는 역순으로 해준다
        conn.close()




if __name__ == "__main__":
    jik_gogek()