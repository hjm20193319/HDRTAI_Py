# pandas 의 DataFrame의 자료를 원격 DB의 테이블에 저장

import pandas as pd
import pymysql
from sqlalchemy import create_engine

# 딕셔너리를 이용한 데이터프레임 생성
data = {
    'code':[10, 11, 12],
    'sang':['사이다', '맥주', '와인'],
    'su':[20, 22, 5],
    'dan':[5000, 3000, 70000]
}

try:
    frame = pd.DataFrame(data)
    print(frame)

    # 엔진 생성 (접속 정보 입력)
    # 형식: dialect+driver://username:password@host:port/database
    engine = create_engine('mysql+pymysql://root:123@127.0.0.1:3306/test')

    # to_sql(): DataFrame을 DB 테이블로 내보내기
    frame.to_sql(name='sangdata', con=engine, if_exists='append', index=False)
    print('저장 완료')
    
    # pd.read_sql(): SQL 쿼리와 connection 객체를 인자로 받아 직접 DataFrame으로 변환
    df = pd.read_sql('select * from sangdata', engine)
    print(df)

except Exception as err:
    print('error : ', err)

'''
.env 파일
DB_USER=root
DB_PASS=123

from dotenv import load_dotenv
load_dotenv()

engine = create_engine(f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@127.0.0.1:3306/test?charset=utf8mb4')
'''