'''
문3) 성별 직원 현황 출력 : 성별(남/여) 단위로 직원 수와 평균 급여 출력

성별 직원수 평균급여

남 3 8500

여 2 7800
'''

import MySQLdb

import pickle

# 보안을 위해서 정보를 별도의 파일로 만들어서 사용하기

with open('mydb.dat', mode = 'rb') as obj:          # config 외부 파일에서 읽어오기
    config = pickle.load(obj)


def jikGen():
    try:
        conn = MySQLdb.connect(**config)         
        cursor = conn.cursor()

        sql_gen = """
            select jikwongen as 성별, count(*) as 직원수, avg(jikwonpay) as 평균급여 
            from jikwon group by jikwongen
            having jikwongen is not null
        """

        cursor.execute(sql_gen)
        datas = cursor.fetchall()

        for r in datas:
            print('%s %s %s' %r)


    except Exception as e:
        print('err : ', e)
        # conn.rollback()
    finally:
        cursor.close()                               # close 할때 는 역순으로 해준다
        conn.close()


if __name__ == "__main__":
    jikGen()