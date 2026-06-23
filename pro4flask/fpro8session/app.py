from flask import Flask, render_template, request, redirect, url_for, session
# session 모듈 추가

# 파이썬 세션(session) : 웹에서 사용자 정보를 서버에 저장하는 기능을 말함
# -> 쿠키를 통해 세선 운영
# 일정 시간 동안 동일 사용자(브라우저)와 일련의 요청을 하나의 상태로 보고,
# 그 상태를 유지시키는 기술
# - 쿠키에 비해 상대적으로 안전함

# 실습 : 사용자가 os를 선택하면 세션에 저장하고 읽기
from datetime import timedelta      # 날짜나 시간 더하기 빼기해서 기간 설정하기 유용
app = Flask(__name__)

# Flask는 세션 사용을 위해 secret_key 설정이 필요
app.secret_key = 'abcdef123456'     # 위조 방지용 비밀키 값
# 참고 키 값 자동생성 : 터미널 창 > python -c "import secrets; print(secrets.token_hex(32))"
# 출력 : 7340e812cf0db5ce8446cbbf31a3f4537c52ea5bcdaa52a0800daa82af0bd452

# 만료 시간 : 활동 중이 아닐 때부터 5초(상대적인 시간)
app.permanent_session_lifetime = timedelta(seconds=5)       # 세션 만료 시간 5초 설정 (Default : 30m)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/setos')
def setos():
    favorite_os = request.args.get('favorite_os')

    if favorite_os:
        session.permanent = True        # 세션 만료 시간 적용
        session['f_os'] = favorite_os       # f_os라는 key로 특정 값 저장(세션에 - 클라이언트와 서버 사이에 연결을 위해서)
        return redirect(url_for('showos'))      # 요청명과 매핑된 함수를  call
    else:
        return render_template('setos.html')

# 결과 보기
@app.route('/showos')
def showos():
    context = {}

    if 'f_os' in session:
        context['f_os'] = session['f_os']       # dict type context(변수)에 세션값을 할당
        context['message'] = f'당신이 선택한 운영체제는 "{session["f_os"]}"'

    else:
        context['f_os'] = None
        context['message'] = '운영체제를 선택하지 않았거나 세션 만료됨'

    return render_template('showos.html', context=context)      # dict type(상황에 맞게) / 묶음형 자료가 넘어가기 때문에 html에서 알맞게 뽑아서 사용해야 한다


if __name__ == '__main__':
    app.run(debug=True)