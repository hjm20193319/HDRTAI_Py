from flask import Flask, render_template_string, request, make_response, redirect, url_for
# render_template_string : 문자열로 작성한 jinja탬플릿을 렌더링 해서HTML으로 반환
# request : 클라이언트의 HTTP REQUEST의 정보를 담는
# make_response : 응답 객체를 직접 만드는, 쿠키 설정할 때 사용
# redirect : 다른 URL로 이동하기
# url_for : route 함수 이름으로 URL을 안전하게 생성하는 함수

app = Flask(__name__)

# Cookie는 브라우저에 저장되는 작은 키-값 데이터이고, 
# 서버가 클라이언트와 연결 상태를 유지하는 것처럼 할 수 있다
# 서버가 설정 -> 브라우저가 저장 -> 다음 요청부터 브라우저가 자동으로 함께 전송

HOME_HTML = '''
<h2>Flask Cookie test</h2>
<form action='/set_cookie' method='post'>
    쿠키 값 : <input type='text' name='name' placeholder='예 : hong'>
    <button type='submit'>쿠키 저장</button>
</form>
<p>
    <a href='/read_cookie'>쿠키 읽기</a>
    <a href='/delete_cookie'>쿠키 삭제</a>
</p>

'''

@app.get('/')
def home():
    return render_template_string(HOME_HTML)

@app.post('/set_cookie')
def set_cookie():
    # 쿠키 저장
    name = request.form.get('name', 'anonymous')

    # 클라이언트에 쿠키를 심으려면 응답 객체가 필요
    # 먼저 'read_cokie페이지로 이동하라' 는 redirect 객체를 만들고
    # 그 응답에 따라 cookie를 추가한 뒤 브라우저에 돌려줌
    resp = make_response(redirect(url_for('read_cookie')))
    # 쿠키 만들기(옵션이 많음)
    resp.set_cookie(                # 브라우저에 쿠키 저장
        key = 'name',        # 쿠키 이름
        value = name,        # 사용자가 입력한 쿠키 값
        max_age=60 * 5,       # 유효 시간 - 5분 뒤 만료
        httponly=True,        # JS에서 document.cookie로 접근 불가
        samesite='Lax',       # CSRF 공격 방지용
    )    

    return resp     # 쿠키가 포함된 응답을 브라우저로 반환
    # 브라우저는 쿠키를 저장하고, redirect 요청에 따라 read_cookie로 다시 요청함


    # url_for(함수) : 함수명을 바로 부름
    # redirect : /read_cookie 페이지로 이동

@app.get('/read_cookie')
def read_cookie():
    # 브라우저가 요청에 실어 보낸 모든 쿠키 중에서 내 서버가 만든 name 쿠키를 꺼냄
    # 없으면 None 반환 : 첫방문, 만료, 삭제
    name = request.cookies.get('name')      # 실제 쿠키 이름은 더 복잡하다(중복 방지)

    # 읽은 쿠키 HTML로 출력하기
    return f'''
        <h3>쿠키 읽기</h3>
        <p>name 쿠키 값 : {name}</p>
        <a href="/">홈페이지</a>
    '''

@app.get('/delete_cookie')
def delete_cookie():
    # 쿠키 삭제 후 홈(/)으로 이동하기 위한 redirect 응답을 생성
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('name')

    return resp


if __name__ == '__main__':
    app.run(debug=True)