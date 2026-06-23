# Flask: 웹 애플리케이션 서버 구축을 위한 마이크로 프레임워크
# render_template: templates 폴더의 HTML 파일을 클라이언트에 반환
# request: 클라이언트의 요청 데이터(파라미터, 바디 등)에 접근
# jsonify: 파이썬 딕셔너리/리스트를 JSON 응답 객체로 변환 (Content-Type: application/json)
from flask import Flask, render_template, request, jsonify
# db.py 모듈에서 정의한 데이터베이스 커넥션 생성 함수 임포트
from db import get_connFunc

app = Flask(__name__) # Flask 애플리케이션 객체 생성 (__name__은 현재 모듈의 이름)

@app.get('/') # 루트 경로에 대한 HTTP GET 요청 라우팅
def home():
    # index.html 파일을 렌더링하여 메인 페이지 표시
    return render_template('index.html')

# 전체 직원 조회
@app.get('/api/jikwon') # 직원 목록 조회를 위한 REST API 엔드포인트
def jikwon_list():
    # JOIN을 사용하여 직원 정보와 부서명을 함께 가져오는 쿼리 (year() 함수로 입사년도만 추출)
    sql = '''
        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, year(jikwonibsail) as ibsayear
        from jikwon
        inner join buser on jikwon.busernum = buser.buserno
        order by jikwonno
    '''
# sql 문은 잘 돌아가는지 검증해주는 것이 좋다

    with get_connFunc() as conn:        # DB 연결 (with문 사용으로 자동 close 처리)
        with conn.cursor() as cur:      # SQL 실행을 위한 커서 객체 생성
            cur.execute(sql)            # 쿼리 실행
            rows = cur.fetchall()       # 모든 결과 행을 리스트(DictCursor 설정에 따라 딕셔너리 리스트)로 가져옴

    # 성공 여부와 데이터를 JSON 형태로 반환
    return jsonify({'ok':True, 'data':rows})

# 직원 1명 조회
@app.get('/api/jikwon/<int:no>') # URL 파라미터 <int:no>를 통해 특정 직원 번호를 정수형으로 전달받음
def jikwon_one(no):
    # 특정 직원 번호(jikwonno)에 해당하는 데이터 필터링
    sql = '''
        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, year(jikwonibsail) as ibsayear
        from jikwon
        inner join buser on jikwon.busernum = buser.buserno
        where jikwonno = %s
    '''

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (no,))     # %s 플레이스홀더에 no 바인딩 (SQL Injection 방지)
            row = cur.fetchone()        # 단일 행 결과 가져오기

    return jsonify({'ok':True, 'data':row})

# 전체 부서 조회
@app.get('/api/buser')
def buser_list():
    # 부서 테이블의 모든 정보를 부서 번호 순으로 조회
    sql = '''
        select *
        from buser order by buserno
    '''

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return jsonify({'ok':True, 'data':rows})

# 특정 부서 직원 조회
@app.get('/api/buser/<int:bno>/jikwon') # 부서 번호(bno)를 경로 변수로 받음
def buser_dept(bno):
    # 특정 부서 번호(busernum)에 소속된 직원들만 조회
    sql = '''
        select jikwonno, jikwonname, jikwonjik, jikwonpay, year(jikwonibsail) as ibsayear
        from jikwon
        where busernum = %s
    '''
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (bno,))
            rows = cur.fetchall()

    return jsonify({'ok':True, 'data':rows})
if __name__ == '__main__':
    # debug=True: 코드 수정 시 서버 자동 재시작 및 상세 에러 메시지 출력
    app.run(debug=True)