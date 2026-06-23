from flask import Flask, render_template, request, redirect, url_for, session

from datetime import timedelta      # 날짜나 시간 더하기 빼기해서 기간 설정하기 유용

app = Flask(__name__)

app.secret_key = 'abcdef123456'

app.permanent_session_lifetime = timedelta(minutes=5)       # 세션 만료 시간 5분 설정 (Default : 30m)

# 원래는 DB에서 불러오는 것
# 실습을 위해서 직접 데이터 작성
products = [
    {'id':1, 'name':'노트북', 'price':3500000},
    {'id':2, 'name':'키보드', 'price':5000},
    {'id':3, 'name':'마우스', 'price':35000},
    {'id':4, 'name':'모니터', 'price':1500000}
]

@app.route('/')
def product_list():
    return render_template('products.html', products=products)

@app.route('/cart')
def show_cart():
    cart = session.get('cart', {})      # 세션에 들어있는 cart정보를 cart변수에 담기 위해서
    total = sum(info['price'] * info['qty'] for info in cart.values())

    return render_template('cart.html', cart=cart, total=total)      # 총 3가지의 cart, 파이썬 변수/세션키/매개변수

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    # print(product_id)
    # 세션 cart가 없으면 빈 dict로 생성
    cart = session.get('cart', {})
    # next(..., None) : 묶음형 자료에서 다음 값 1개를 꺼내는 함수
    # 주문 상품이 product에 기억됨
    product = next((p for p in products if p['id'] == product_id), None)

    if product is None:
        return '상품을 찾을 수 없어요', 404
    
    # 주문 상품이 상품목록에 있으면 장바구니에 추가
    item_name = product['name']

    if item_name in cart:
        cart[item_name]['qty'] += 1     # 카트에 동일 상품이 있는 경우 수량만 증가
    else:
        cart[item_name] = {'price':int(product['price']), 'qty':1}
        # 카트에 최초 상품일 경우 수량 1(qty 요소(key) 생성)

    session['cart'] = cart      # 변수 cart를 세션 'cart' 키에 값으로 저장
    session.permanent = True    # 5분 만료 적용

    return redirect(url_for('show_cart'))   # cart에 저장 후 장바구니보기로 이동

@app.route('/remove/<item_name>')
def remove_to_cart(item_name):
    cart = session.get('cart')      # 내용 읽기

    if item_name in cart:       # 상품 삭제
        del cart[item_name]
    
    session['cart'] = cart      # 나머지 상품 다시 입력
    return redirect(url_for('show_cart'))
    # redirect 클라이언트의 주소창에 입력한 것과 같은 효과 -> 수행

# 장바구니 비우기
@app.route('/clear')
def clear_cart():
    session.pop('cart', None)       # 세션에 여러 개의 key중에서 'cart'라는 키를 삭제
    return redirect(url_for('show_cart'))

if __name__ == '__main__':
    app.run(debug=True)