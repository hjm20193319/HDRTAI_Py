#MariaDB(sangdata) + Flask RESTful API + HTML/JS(fetch) 로 전체조회 / 추가 / 수정 / 삭제(CRUD) 처리 


# pip install flask pymysql : Flask 웹 프레임워크와 MariaDB 연동을 위한 라이브러리 설치
from flask import Flask, jsonify, request, render_template
# db.py 모듈에서 정의한 데이터베이스 커넥션 생성 함수 임포트
from db import get_connFunc 

app = Flask(__name__) # Flask 애플리케이션 객체 생성 (__name__은 현재 모듈 이름)

@app.get("/") # 루트 경로에 대한 GET 요청 처리 (메인 페이지)
def home():
    # templates 폴더 내의 index.html 파일을 렌더링하여 클라이언트에 반환
    return render_template("index.html")


# 1) 전체 조회
@app.get("/api/sangdata") # 상품 목록 조회를 위한 REST API 엔드포인트
def list_sangdata():
    # 상품 코드(code) 기준 오름차순 정렬 쿼리
    sql = "SELECT code, sang, su, dan FROM sangdata ORDER BY code"
    with get_connFunc() as conn:        # DB 연결 (with문 사용으로 자동 close 처리)
        with conn.cursor() as cur:      # SQL 실행을 위한 커서 객체 생성
            cur.execute(sql)            # 쿼리 실행
            rows = cur.fetchall()       # 모든 결과 행을 리스트(또는 DictCursor 설정에 따라 딕셔너리 리스트)로 가져옴
    # jsonify: 파이썬 딕셔너리를 JSON 문자열로 변환하고 Content-Type을 application/json으로 설정하여 응답
    return jsonify({"ok": True, "data": rows})   # dict, list 등을 JSON 응답으로 만들어 반환


# 2) 1건 조회(선택)
@app.get("/api/sangdata/<int:code>") # URL 파라미터 <int:code>를 통해 특정 상품 코드 전달받음
def get_one(code: int):
    sql = "SELECT code, sang, su, dan FROM sangdata WHERE code=%s"
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (code, ))
            row = cur.fetchone()
    if not row:
        # 데이터가 없을 경우 404 Not Found 상태 코드와 함께 에러 메시지 반환
        return jsonify({"ok": False, "error": "NOT_FOUND"}), 404
    return jsonify({"ok": True, "data": row})


# 3) 추가 (POST / JSON)
@app.post("/api/sangdata") # 새로운 리소스를 생성할 때 사용하는 POST 메서드
def create_sangdata():
    # request.get_json(): 클라이언트가 보낸 JSON 데이터를 파이썬 딕셔너리로 변환
    # silent=True: JSON 형식이 아닐 때 에러 대신 None 반환, or {}를 통해 빈 딕셔너리 보장
    data = request.get_json(silent=True) or {}

    # 필수값 체크 및 데이터 유효성 검사 (Validation)
    try:
        code = int(data.get("code")) # 상품 코드를 정수형으로 변환 시도
    except Exception:
        return jsonify({"ok": False, "error": "code is required(int)"}), 400

    sang = (data.get("sang") or "").strip()
    if not sang:
        return jsonify({"ok": False, "error": "sang is required"}), 400

    try:
        # 수량(su)과 단가(dan) 추출, 기본값 0 설정 및 정수 변환
        su = int(data.get("su", 0))
        dan = int(data.get("dan", 0))
    except Exception:
        return jsonify({"ok": False, "error": "su/dan must be int"}), 400

    sql = "INSERT INTO sangdata(code, sang, su, dan) VALUES(%s, %s, %s, %s)"
    try:
        with get_connFunc() as conn:
            with conn.cursor() as cur:
                # %s 플레이스홀더를 사용하여 SQL Injection 공격 방지
                cur.execute(sql, (code, sang, su, dan))
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400    # 예: PK 중복(Duplicate entry) 등 DB 제약 조건 위반 시

    return jsonify({"ok": True, "message": "CREATED", "code": code}), 201 # 201: Created 성공 상태 코드


# 4) 수정 (PUT / JSON)
@app.put("/api/sangdata/<int:code>") # 기존 리소스를 전체 수정할 때 사용하는 PUT 메서드
def update_sangdata(code: int):
    data = request.get_json(silent=True) or {}

    sang = (data.get("sang") or "").strip()
    if not sang:
        return jsonify({"ok": False, "error": "sang is required"}), 400

    try:
        su = int(data.get("su", 0))
        dan = int(data.get("dan", 0))
    except Exception:
        return jsonify({"ok": False, "error": "su/dan must be int"}), 400

    sql = "UPDATE sangdata SET sang=%s, su=%s, dan=%s WHERE code=%s"
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (sang, su, dan, code))
            # cur.rowcount: SQL 실행 결과로 영향을 받은 행(row)의 수를 반환
            if cur.rowcount == 0:
                return jsonify({"ok": False, "error": "NOT_FOUND"}), 404

    return jsonify({"ok": True, "message": "UPDATED", "code": code})


# 5) 삭제 (DELETE)
@app.delete("/api/sangdata/<int:code>") # 리소스를 삭제할 때 사용하는 DELETE 메서드
def delete_sangdata(code: int):
    sql = "DELETE FROM sangdata WHERE code=%s"
    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (code,))
            if cur.rowcount == 0:
                # 삭제할 대상이 DB에 존재하지 않는 경우
                return jsonify({"ok": False, "error": "NOT_FOUND"}), 404

    return jsonify({"ok": True, "message": "DELETED", "code": code})


if __name__ == "__main__":
    # debug=True: 코드 수정 시 서버 자동 재시작 및 브라우저에 상세 에러 메시지 출력
    app.run(debug=True, host="127.0.0.1", port=5000)
