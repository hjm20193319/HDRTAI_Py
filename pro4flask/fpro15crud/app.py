# Flask 웹 프레임워크와 템플릿 렌더링, HTTP 요청 처리, JSON 응답을 위한 모듈 임포트
from flask import Flask, render_template, request, jsonify
# db.py 파일에서 정의한 데이터베이스 연결 함수(커넥션 풀/생성) 임포트
from db import get_connFunc

app = Flask(__name__)

# 기본 경로('/') 접속 시 메인 페이지(index.html)를 사용자에게 반환
@app.get('/')
def home():
    return render_template('index.html')

# 상품 데이터 전체 조회 API (GET 방식)
@app.get('/api/sangdata')
def list_sangdata():
    # 상품 코드(code)를 기준으로 오름차순 정렬하여 모든 컬럼을 가져오는 SQL 쿼리
    sql = 'select code, sang, su, dan from sangdata order by code asc'
    with get_connFunc() as conn:        # DB 연결 객체 생성 (with문 종료 시 자동 close)
        with conn.cursor() as cur:      # SQL 실행을 위한 커서 객체 생성
            cur.execute(sql)            # 쿼리 실행
            rows = cur.fetchall()       # 실행 결과인 모든 행(rows)을 가져옴

    # 성공 여부(ok:True)와 조회된 데이터를 JSON 형태로 클라이언트에 응답
    return jsonify({'ok':True, 'data':rows})

# 새 상품 추가 API (POST 방식) ---- RESTful 설계 원칙 적용
@app.post('/api/sangdata')
def create_sangdata():
    # 클라이언트가 보낸 JSON 데이터를 파이썬 딕셔너리(dict) 형태로 변환하여 가져옴
    data = request.get_json()       
    # print('data : ', data)
    code = int(data['code'])        # 상품 코드 추출 및 정수형 변환 (연산 안할거면 int 안써도 됨)
    sang = data['sang']
    su = int(data['su'])            # 수량 추출 및 정수형 변환
    dan = int(data['dan'])          # 단가 추출 및 정수형 변환

    # 데이터 삽입을 위한 SQL문 (보안을 위해 플레이스홀더 %s 사용)
    isql = 'insert into sangdata(code, sang, su, dan) values(%s, %s, %s, %s)'

    with get_connFunc() as conn:        # DB 연결 (with 사용으로 작업 완료 후 자동으로 close() 호출)
        with conn.cursor() as cur:
            # SQL Injection 방지를 위해 데이터를 튜플(tuple) 형태로 전달하여 실행
            cur.execute(isql, (code, sang, su, dan))        

    return jsonify({'ok':True})

# 특정 상품 정보 수정 API (PUT 방식, URL 파라미터로 code 전달받음)
@app.put('/api/sangdata/<int:code>')
def update_sangdata(code):
    data = request.get_json()       # 수정할 데이터를 JSON에서 추출
    sang = data['sang']
    su = int(data['su'])
    dan = int(data['dan'])
    # 특정 코드를 가진 상품의 이름, 수량, 단가를 변경하는 업데이트 쿼리
    usql = 'update sangdata set sang=%s, su=%s, dan=%s where code=%s'

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            # 쿼리 실행 (영향받은 행의 수가 0이면 False, 1이면 True 이런 방식으로 결과 처리 가능)
            cur.execute(usql, (sang, su, dan, code))  

    return jsonify({'ok':True})

# 상품 삭제 API (DELETE 방식)
@app.delete('/api/sangdata/<int:code>')
def delete_sangdata(code):
    try:    # 예외 처리를 위한 try-except 블록
        dsql = 'delete from sangdata where code=%s'
        with get_connFunc() as conn:
            with conn.cursor() as cur:
                cur.execute(dsql, (code,))
                if cur.rowcount == 0:
                    return jsonify({'ok':False, 'msg':'해당 자료 없음'})
        
        # 삭제 성공 시 응답 (기존 코드의 ok:False 유지하며 주석 추가: 실제로는 True가 논리적으로 맞음)
        return jsonify({'ok':False, 'msg':'삭제 완료'})

    except Exception as err:    # DB 오류 등 예외 발생 시 에러 메시지 반환
        return jsonify({'ok':False, 'msg':str(err)})
    
if __name__ == '__main__':
    # Flask 내장 개발 서버 실행 (debug=True 설정으로 코드 수정 시 자동 재시작 및 에러 추적 활성화)
    app.run(debug=True)