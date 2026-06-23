# 기본 골격

import MySQLdb

import pickle

# 보안을 위해서 정보를 별도의 파일로 만들어서 사용하기

'''
# jikwon table이 있는 test DB 정보 (필요한 데이터가 있는 테이블의 DB 정보로 바꿔주면 됨)
config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '123',
    'database' : 'test',
    'port' : 3306,
    'charset' : 'utf8'
}
'''

with open('mydb.dat', mode = 'rb') as obj:          # config 외부 파일에서 읽어오기
    config = pickle.load(obj)

def functionname():
    try:
        conn = MySQLdb.connect(**config)         
        cursor = conn.cursor()



    except Exception as e:
        print('err : ', e)
        conn.rollback()
    finally:
        cursor.close()                               # close 할때 는 역순으로 해준다
        conn.close()




if __name__ == "__main__":
    functionname()