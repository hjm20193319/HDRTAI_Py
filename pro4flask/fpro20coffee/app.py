from pathlib import Path
from flask import Flask, render_template, request, url_for, redirect
# [개념] Flask: 파이썬 기반의 마이크로 웹 프레임워크로, 가볍고 확장이 용이함
# [개념] render_template: HTML 템플릿 파일을 렌더링하여 클라이언트에 반환
# [개념] request: 클라이언트가 보낸 HTTP 요청 데이터(form, args 등)에 접근하는 객체
from db import insert_survey, fetchall_survey
from analysis import analysis_func, save_barchart_func

# [문법] Path(__file__).resolve(): 현재 실행 중인 스크립트의 절대 경로를 객체로 생성
BASE_DIR = Path(__file__).resolve().parent
IMG_PATH = BASE_DIR / 'static' / 'img' / 'vbar.png'

app = Flask(__name__)

@app.route('/')
def index():
    # [개념] 라우팅(Routing): 특정 URL 주소와 파이썬 함수를 연결하는 과정
    return render_template('index.html')

@app.get('/coffee/survey')
def survey_view():
    return render_template('coffee/coffeesurvey.html')

@app.post('/coffee/surveyprocess')
def survey_process():
    # [문법] request.form.get(): POST 방식으로 전달된 폼 데이터를 읽어옴 (Key가 없으면 None 반환)
    gender = (request.form.get('gender') or '').strip()
    age_raw = (request.form.get('age') or '').strip()
    co_survey = (request.form.get('co_survey') or '').strip()

    # 입력 검증
    # [문법] .isdigit(): 문자열이 숫자로만 구성되어 있는지 확인하는 메소드
    if not gender or not age_raw.isdigit() or not co_survey:
        return redirect(url_for('survey_view'))
    
    age = int(age_raw)

    # db에 자료 저장
    insert_survey(gender, age, co_survey)

    # 조회 및 분석
    rdata = fetchall_survey()
    # [개념] 카이제곱 검정(Chi-square test): 범주형 변수 간의 독립성이나 동질성을 통계적으로 확인
    crossTab, results, df = analysis_func(rdata)

    # 차트 저장
    if not df.empty:
        save_barchart_func(df, IMG_PATH)

    # [추천] : 분석 결과가 많을 경우 세션(session)을 활용하여 데이터를 유지하거나, 
    # 분석 로직을 별도의 비동기 태스크(Celery 등)로 분리하면 웹 서버의 응답 속도를 높일 수 있습니다.
    # [문법] to_html(): Pandas DataFrame/Series 객체를 HTML <table> 태그 문자열로 변환

    return render_template(
        'coffee/result.html',
        crossTab=crossTab.to_html() if not crossTab.empty else '데이터가 없어요',
        results=results,
        df = df.to_html(index=False) if not df.empty else '',
    )


@app.get('/coffee/surveyshow')
def survey_show():
    # 저장 없이 결과만 출력
    # [개념] GET 요청: 서버로부터 정보를 조회할 때 사용하며, 브라우저 주소창에 데이터가 노출됨
    rdata = fetchall_survey()
    crossTab, results, df = analysis_func(rdata)
    
    if not df.empty:
        save_barchart_func(df, IMG_PATH)

    return render_template(
        'coffee/result.html',
        crossTab=crossTab.to_html() if not crossTab.empty else '데이터가 없어요',
        results=results,
        df = df.to_html(index=False) if not df.empty else '',
    )


if __name__ == '__main__':
    # [개념] debug=True: 코드 수정 시 서버 자동 재시작 및 브라우저에 상세 에러 메시지 출력
    app.run(debug=True, host='127.0.0.1', port=5000)