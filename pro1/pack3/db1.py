# 개인용(local) Data Base : sqlite3 - 파이썬에 기본 모듈로 제공
# https://www.sqlite.org
# 모바일 기기, 임베디드 시스템 주로 사용


import sqlite3
print(sqlite3.sqlite_version)       # 버전 확인 : 3.51.0

# conn = sqlite3.connect('exam.db')       # DB파일 생성
conn = sqlite3.connect(':memory:')      # RAM에만 db 저장 -> 휘발성 -- 실험용으로 쓸때

try:
    cur = conn.cursor();        # sql문 처리를 위한 cursor 객체 생성

    # 테이블 생성
    cur.execute("create table if not exists friends(name text, phone text, addr text)")         # sql문장은 큰 따옴표를 두른다

    # 자료 입력
    cur.execute("insert into friends values('홍길동', '222-2222', '서초1동')")          # 세미콜론 쓰지 않음
    cur.execute("insert into friends values(?, ?, ?)", ('신기해', '333-3333', '역삼2동'))   # 외부에서 받는 데이터지만 지금은 직접 적어줌
    inputdatas = ('신기한', '444-4444', '역삼2동')
    cur.execute("insert into friends values(?, ?, ?)", inputdatas)
    conn.commit()

    # 자료 보기
    cur.execute("select * from friends")        # DB에서 자료를 읽어서 RAM에 올려놓고, cur객체를 이용해서 접근한다
    print(cur.fetchone())       # 한개의 레코드(행) 읽기
    print(cur.fetchall())       # 모든 레코드 읽기
    print()
    cur.execute("select name, addr, phone from friends")        # 원본 칼럼 순서는 중요하지 않음, 읽어오는 순서대로 들어옴
    for r in cur:           
        print(r[0] + ' ' + r[1] + ' ' + r[2])

except Exception as e:
    print('err : ', e)
    conn.rollback()

finally:
    conn.close()        # 작업이 끝나면 반드시 close







