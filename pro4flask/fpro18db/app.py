from flask import Flask, render_template, request # Flask: 웹 애플리케이션 프레임워크, render_template: HTML 렌더링, request: 클라이언트 요청 데이터 처리
import pymysql # MySQL/MariaDB 연동을 위한 라이브러리
import pandas as pd # 데이터 분석 및 조작을 위한 라이브러리 (DataFrame 활용)
import numpy as np # 수치 계산 및 배열 처리를 위한 라이브러리
from markupsafe import escape # HTML 이스케이프 처리를 통해 XSS(교차 사이트 스크립팅) 공격 방지

app = Flask(__name__) # Flask 애플리케이션 객체 생성. __name__은 현재 모듈 이름을 의미

# 데이터베이스 접속 정보 설정 (딕셔너리 형태)
# host: 서버 주소, user: 사용자 계정, password: 비밀번호, database: 사용할 스키마, port: 포트번호, charset: 인코딩 설정
db_config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8mb4'
}

# DB 연결 객체를 반환하는 함수
def get_connection():
    return pymysql.connect(**db_config) # **(더블 애스터리스크): 딕셔너리 언패킹을 통해 인자로 전달

@app.route('/') # 루트 경로('/')에 대한 라우팅 설정
def index():
    return render_template('index.html') # templates 폴더의 index.html 파일을 렌더링하여 반환

@app.get('/dbshow') # '/dbshow' 경로에 대한 GET 방식 요청 처리
def dbshow():
    # request.args.get(): URL 파라미터(?dept=값) 추출. strip(): 앞뒤 공백 제거
    dept = request.args.get('dept', '').strip() 

    sql = '''
        -- jikwon(직원) 테이블과 buser(부서) 테이블을 조인하여 필요한 정보 추출
        select j.jikwonno as 직원번호, j.jikwonname as 직원명, b.busername as 부서명, b.busertel as 부서전화, j.jikwonpay as 연봉, j.jikwonjik as 직급
        from jikwon j
        inner join buser b
        on j.busernum = b.buserno
    '''

    params = []
    # 부서명이 입력된 경우 동적으로 WHERE 절 추가
    if dept:
        sql += ' where b.busername like %s' # SQL Injection 방지를 위해 플레이스홀더(%s) 사용
        params.append(f'%{dept}%') # LIKE 연산을 위한 와일드카드(%) 포함

    sql += ' order by j.jikwonno asc' # 직원번호 기준 오름차순 정렬

    # sql 실행
    with get_connection() as conn: # with문을 사용하여 DB 연결 자동 종료(Context Manager)
        with conn.cursor() as cur: # 커서 객체 생성 (SQL 실행 및 결과 페치 담당)
            cur.execute(sql, params) # SQL 쿼리 실행
            rows = cur.fetchall() # 실행 결과의 모든 레코드를 튜플 형태로 가져옴
            cols = [c[0]for c in cur.description] # cur.description: 쿼리 결과의 메타데이터(컬럼명 등) 정보 추출

    # DB에서 가져온 데이터를 Pandas DataFrame으로 변환
    df = pd.DataFrame(rows, columns=cols) 
    # print(df.head(3))

    # 직원정보 html로 전송
    if not df.empty: # 데이터가 존재하는지 확인
        # to_html(): DataFrame을 HTML <table> 태그 문자열로 변환. index=False: 행 번호 제외
        jikwondata = df[['직원번호', '직원명', '부서명', '부서전화', '연봉', '직급']].to_html(index = False)
    else:
        jikwondata = '직원 정보가 없어요'
    # print(jikwondata)


    # 직급별 연봉 통계 분석
    if not df.empty:
        stats_df = (
            df.groupby('직급')['연봉'] # '직급' 컬럼으로 그룹화하여 '연봉' 컬럼 선택
            .agg( # 여러 개의 집계 함수를 동시에 적용
                평균 = 'mean', # 평균 계산
                표준편차 = lambda x:x.std(ddof=0), # 람다 함수를 이용한 모표준편차(ddof=0) 계산
                인원수='count' # 그룹별 데이터 개수 계산
            )
            .round(2) # 소수점 둘째 자리까지 반올림
            .reset_index() # 인덱스로 설정된 '직급'을 일반 컬럼으로 변경
            .sort_values(by='평균', ascending=False) # 평균 연봉 기준 내림차순 정렬

        )
        stats_df['표준편차'] = stats_df['표준편차'].fillna(0) # 결측치(데이터가 1개인 경우 등)를 0으로 채움
        # print(stats_df)
        statsdata = stats_df.to_html(index=False) # 통계 데이터를 HTML 테이블로 변환
        # print(statsdata)
        
    else:
        statsdata = '직원 정보가 없어요'

    return render_template('dbshow.html', dept=escape(dept), jikwondata=jikwondata, statsdata=statsdata)
                                            # XSS 방지





if __name__ == '__main__':
    # debug=True: 코드 수정 시 서버 자동 재시작 및 에러 메시지 상세 출력
    app.run(debug=True) 