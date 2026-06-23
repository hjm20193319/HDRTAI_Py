# 사용자 정의 함수 : 중복되고 반복되는 내용을 하나의 함수로 만들어두고 사용
'''
def 함수명(가인수,,,):
    ....
    return 반환값           # 1개만 반환, return이 없으면 return None

함수명(실인수,,,)           # 함수 호출
'''

def doFunc1():
    print('doFunc1 수행')

def doFunc2(name):
    print('name : ', name)        # return 값이 없으면, return None이라고 쓰거나 안쓰면 된다

def doFunc3(arg1, arg2):
    re = arg1 + arg2
    return re

def doFunc4(a1, a2):     # 홀수면 
    imsi = a1 + a2
    if imsi % 2 == 1:
        return
    else:
        return imsi
    
doFunc1()       # 함수 호출      함수를 수행하시오.
print('함수 주소는 ', doFunc1)             # 주소를 반환함 > 함수의 이름도 변수이기 때문에 참조형...
print('함수 주소는 ', id(doFunc1))          # 
imsi = doFunc1              # 주소를 치환
imsi()
print(doFunc1())                    

print('\n==========================\n')

doFunc2(7)
doFunc2('길동')            # 타입 알아서 결정
# doFunc2('길동', '순신')             # 매개변수가의 개수가 다름 / 아예 안줘도 Error 개수를 맞춰야 한다

print('\n==========================\n')

doFunc3('대한', '민국')                # 수행은 되지만 출력되는 것이 없음//문자 더하기
print(doFunc3('대한', '민국'))          # return 된 대한민국이 출력 됨
print(doFunc3(5, 6))              # 숫자 더하기 
result = doFunc3('5', '6')         # 문자열 더하기
print(result)

print('\n==========================\n')

print(doFunc4(3, 4))
print(doFunc4(2, 4))

print('\n==========================\n')

def triArea(a, b):
    c = a * b / 2
    triAreaPrint(c)     # 함수 안에서 다른 함수 호출


def triAreaPrint(cc):
    print('삼각형의 면적은 ', cc)

triArea(20, 30)

print('\n==========================\n')

def passResult(kor, eng):
    ss = kor + eng
    if ss >= 50:
        return True
    else:
        return False

if passResult(20, 20):
    print('합격') 
else:
    print('불합격')

print('\n==========================\n')

def swapFunc(a, b):
    return b, a             # 값을 두개 리턴하는 것 같이 보이지만, tuple로 리턴하는 것 = return(b, a)

a = 10
b = 20
print(a, ' ', b)
print(swapFunc(a, b))

print('\n==========================\n')

def funcTest():
    print('funcTest 멤버 처리')
    def funcInner():                    # 함수 내부에서 함수 선언
        print('내부 함수')
    funcInner()
funcTest()

print('\n==========================\n')

# if 조건식 안에 함수 사용
def isOdd(para):
    return para % 2 == 1       # 홀수이면 True 반환

mydict = {x:x *  x for x in range(11) if isOdd(x)}
print(mydict)

print('\n==========================\n')

print('변수의 생존 범위(scope rule)\n')
# 변수가 저장되는 이름공간은 변수가 어디서 선언 되었는가에 따라 생존 시간이 다름
# 전역, 지역 변수
# Local > Enclosing function > Global > Built-in 순서로 변수를 찾아감

player = '전국대표'
name = '한국인'      # Golbal 변수   / 현재 모듈 어디서든 호출 가능

def funcSoccer():
    name = '홍길동'                 # local 변수 / 지역 변수 / 현재 함수에서만 호출 가능
    player = '지역대표'
    city = '서울'
    print(f'이름은 {name}, 수준은 {player}')
    print(f'지역은 {city}')

funcSoccer()
print(f'이름은 : {name}, 수준은 : {player}')       # 전역 변수.... 변수 이름은 최대한 다르게 하는 것이 좋다
# print(f'이름은 {name}, 수준은 {player}')    > 지역 변수 이기 때문에 호출 불가
print()

a = 10; b = 20; c = 30
def Foo():
    a = 7                   # 지역 변수
    b = 100
    def Bar():              # Bar 는 Foo 에 종속적, 내부 함수
        global c            # c가 전역변수가 됨 Bar함수의 멤버가 아니라 모듈(파일)의 멤버가 됨
        nonlocal b          # 잘 안씀-----상위 단계인 Foo의 지역변수가 됨
        b = 8               # 지역 변수
        print(f'Bar 수행 후 a:{a}, b:{b}, c:{c}')   
        c = 9               # 전역 변수 c 와 같은 변수가 됨
        b = 200    
    Bar()     
    print(f'Foo 수행 후 a:{a}, b:{b}, c:{c}')       # Foo 영역 안에서부터 찾음___Bar 내부로 들어가지 않는다

Foo()
print(f'함수 수행 후 a:{a}, b:{b}, c:{c}')             # 전역 변수 a,b,c ____ 함수 내부를 찾지 않음 > 모듈 단위에서만 탐색

print('\n=====================\n')

g = 1
print('g : ',g)
def func():
    global g        # g 를 global로 선언해줌
    a = g
    g = 2           #  global g가 없으면 Error : 이 치환에 의해서 g가 지역변수가 됨_____윗줄의 g가 값을 갖지 않는 상태가 됨
    return a

print('func 결과 : ', func())
print('g : ',g)
