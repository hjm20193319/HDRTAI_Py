# Closure : Scope에 제약을 받지 않는 변수들을 포함하고 있는 코드블럭이다.
# 내부 함수의 주소를 반환해 함수 밖에서 함수 내의 멤버를 참조하기

def funcTimes(a, b):
    c = a * b
    return c                # 지역 변수
print(funcTimes(2, 3))
# print(c)          # Error

print()
kbs = funcTimes(2, 3)
print(kbs)
kbs = funcTimes
print(kbs)          # 주소를 치환해서 주소 반환
print(kbs(2, 3))        
print(id(kbs), id(funcTimes))       # 두 주소가 같다(치환)
mbc = sbs = kbs             # 모두 같은 함수
del funcTimes               # 함수 삭제(변수삭제)
#print(funcTimes(2, 3))     # 없어졌기 때문에 Error
print(mbc(2, 3))            # mbc sbs kbs에는 주소를 치환 했기 때문에 기능 유지

print('\n===================\n')

print('클로저를 사용하지 않은 경우')
def out():
    count = 0
    def inn():
        nonlocal count              # out에서 선언 된 변수
        count += 1
        return count
    print(inn())
#print(count)  ----> Error
out()
out()


print('\n===================\n')

print('클로저를 사용한 경우')
def outer():
    count = 0
    def inner():
        nonlocal count              # out에서 선언 된 변수
        count += 1
        return count
    return inner                  # ***Closure*** : 실행한 결과가 아니라 주소를 return, 내부함수의 주소를 반환

var1 = outer()          # 내부함수의 주소를 변수에 저장
print('var1 주소 : ', var1)
print(var1())
print(var1())           # 2가 찍힘 ||| 내부 함수의 주소를 함수밖에서 함수의 멤버를 참조함
myvar = var1()
print(myvar)            # 3
print()
var2 = outer()      # 새로운 객체 (inner 함수) 생성  -----동일한 함수에서 꺼냈지만 var1 은 var2와 다른 객체
print(var2())       
print(var2())
print()
print(var1, var2)          # 두 주소가 다름(다른 객체) // 별도로 돌아간다

print('\n===================\n')


print('수량 * 단가 * 세금 한 결과를 출력하는 함수 작성')        # Closure를 사용하여
print()
def outer2(tax):        # tax -> local value
    def inner2(su, dan):
        amount = su * dan * tax
        return amount
    return inner2           # Closure

# 1분기에는 su * dan 에 대한 tax는 0.1 부과
q1 = outer2(0.1)        # q1에는 inner2 의 주소를 기억함
result1 = q1(5, 50000)      # 5개 / 5만원 ---- inner2 를 실행
print('result1 : ', result1)

result2 = q1(2, 10000)
print('result2 : ', result2)
print()

# 2 분기에는 tax 0.05 부과
q2 = outer2(0.05)
result3 = q2(5, 50000)
print('result3 : ', result3)

result4 = q2(2, 10000)
print('result4 : ', result4)            # 함수 외부에서 함수 내부의 변수를 계속해서 사용

print('\n=======================\n')

# 일급 함수 : 함수 안의 함수, 인자로 함수를 전달, 반환값이 함수 // 함수를 값처럼 다룰 수 있으면
print('<일급 함수 알아보기>')

def func1(a, b):
    return a + b

func2 = func1
print(func1(3, 4))
print(func2(3, 4))
print()

def func3(fu):              # 인자로 함수 전달 
    def func4():            # 함수 안의 함수 선언
        print('나는 내부함수야~~')          
    func4()
    return fu               # 반환값이 함수

mbc = func3(func1)          # func1 을 fu에 전달=========mbc는 func1을 전달 받았다
print(mbc(3, 4))            # func1 의 결과가 출력 됨

print('\n===========================\n')

# 축약함수(Lambda function) : 이름이 없는 한 줄짜리 함수
# 형식 : lambda 매개변수들,,, : 반환식   /// 매개변수는 없을 수도 여러개일수도  /// return 없이 결과 반환
print('<축약함수Lambda function 알아보기>')
print()

def hapFunc(x, y):
    return x + y
print(hapFunc(1, 2))

# lambda 로 표현하기

print((lambda x, y : x + y)(1, 2))        # 이름이 없음__형식에만 맞게

gg = lambda x, y : x + y            # 변수로도 받을 수 있다
print(gg(1, 2))

kbs = lambda a, su = 10 : a + su    # 가변 인수일 때, 초기값을 지정할수도 있다
print(kbs(5))
print(kbs(5, 6))

sbs = lambda a, *tu, **di : print(a, tu, di)            # tuple, dict 형도 줄 수 있다 /// argument의 성질은 그대로
sbs(1, 2, 3, var1 = 4, var2 = 5)

li = [lambda a, b : a + b, lambda a, b : a * b]         # list 의 요소가 lambda인 경우
print(li[0](3, 4))
print(li[1](3, 4))

print('\n====================\n')

# 다른 함수에서 lambda 사용하기
# ex ) filter 함수           ----------> 참인 것을 리턴하는 함수
# filter(함수, 반복가능한 객체)

print(list(filter(lambda a : a < 5, range(10))))            # 다른 함수의 매개변수로 함수를 쓸 때, lambda를 쓸 수 있다
print(list(filter(lambda a : a % 2, range(10))))        # 홀수만 출력

print('\n=====================\n')

# 문제 : filter를 이용해 1~100 사이의 정수 중 5의 배수이거나 7의 배수만 출력

fu = filter(lambda a : not(a % 5 and a % 7), range(1,101))   # a % 5 == 0 or a % 7 == 0 이렇게 해도 됨
print(list(fu))