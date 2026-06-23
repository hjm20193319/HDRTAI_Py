# 함수 장식자
# 기존 함수 코드를 고치지 않고 함수의 앞/뒤 동작을 추가하기
# 함수를 받아서 기능을 덧붙인 새 함수로 바꿔치기하는 것
# meta 기능이 있다(정보를 가지고 있다)

def make2(fn):
    return lambda:'hello ' + fn()           # fn 은 함수 안녕 뒤에 fn의 실행결과를 더함

def make1(fn):
    return lambda:'nice to meet you ' + fn()

def hello():
    return 'Mr. Hong'

hi = make2(make1(hello))            # make2 는 hi에 주소를 리턴 (lambda:'hello' + fn)의 주소
print(hi())                         # 장식자 없이 할 때 
print()

@make2              # 장식자/////
@make1              # hello2 가 make1에 make1 이 make2 에 전달 된다
def hello2():
    return 'wow'
print(hello2())

print('\n===================\n')

def traceFunc(func):
    def wrapperFunc(a, b):
        r = func(a, b)
        print(f'함수명 : {func.__name__} (a = {a}, b = {b} -> {r})')                  #  .__name__ : 모듈의 이름을 반환
        return r                # 함수 반환값을 반환
    return wrapperFunc          # Closure, 함수 주소 반환

@traceFunc              # addFunc가 traceFunc에 넘어감 
def addFunc(a, b):
    return a + b

print(addFunc(10, 20))

print('\n==================\n')
