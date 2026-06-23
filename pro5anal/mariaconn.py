# MariaDB 연결 정보 dict type을 별도의 파일로 저장

import pickle

config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '123',
    'database' : 'test',
    'port' : 3306,
    'charset' : 'utf8'
}

with open('mydb.dat', mode = 'wb') as obj:      # binary로 저장
    pickle.dump(config, obj)

# mydb.dat 파일로 만들어줌