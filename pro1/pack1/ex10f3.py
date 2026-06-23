# 매개변수 유형
# 위치 매개변수 : 인수와 순서대로 대응---가장 일반적
# 기본 값 매개변수 : 매개변수에 입력값이 없으면 기본값 사용
# 키워드 매개변수 : 실인수와 가인수를 간 동일 이름으로 대응
# 가변 매개변수 : 인수의 개수가 동적인 경우

def showGugu(start, end = 5):               # 가인수 2개 / 매개변수 / 인자 ======= end 에는 초기값을 줌
    for dan in range(start, end + 1, 1):
        print(str(dan) + '단 출력')
        for i in range(1, 10):
            print(str(dan) + '*' + \
                  str(i) + '=' + str(dan * i), end = ' ')       # 명령문 길게 쓸 때_
        print()

showGugu(2,3)           # 실인수 >> 위치 순서대로 대응하는
print()
showGugu(2)             # 기본값 매개변수 사용하는 것(인수 입력하지 않으면 기본값 사용)
print()
showGugu(start = 7, end = 9)        # 이름은 반드시 맞아야 함(가인수와)
print()
showGugu(end = 9, start = 7)        # 키워드 매개변수 : 순서가 바뀌어도 이름으로 매칭이 되기 때문에 문제없음
print()
showGugu(7, end = 9)                # 키워드 하나만 줘도 가능하다
print()
# showGugu(start=7, 9)              Error : 
# showGugu(end = 9, 7)              Error : 

print('\n===================\n')

print('가변 매개변수')
print()

def func1(*ar):             # 인수의 개수가 정해지지 않았을 때 * 을 붙여주면 된다 : packing 연산 > 여러개의 인자를 tuple로 묶어서 받겠다는 의미
    print(ar)
    for i in ar:            # tuple 자료형을 풀어줌
        print('밥 : ' + i)

func1('김밥', '비빔밥', '볶음밥')       # tuple type으로 출력 됨 (하나의 집단으로)
func1('김밥')                           # 하나일 때는 ('김밥', ) 모양으로 전달 됨  ',' 있는 것 주의
func1('김밥', '비빔밥', '볶음밥', '공기밥')

print('\n===================\n')

def func2(a, *ar):          
# def func2(*ar, a):        ---------->  실행 오류,,type error // 무조건 뒤에 거로
    print(a)
    print(ar)

func2('김밥', '비빔밥')
func2('a','b','c','d')

print('\n===================\n')

def func3(w, h, **other):           # dict 형으로 받겠다는 의미
    print(f'몸무게 : {w}, 키 : {h}')
    print(f'기타 : {other}')

func3(80,180,irum = '신기루', nai = 23)         # {'irum':'신기루} -----> 처음부터 dict 로 주면 Error

print('\n===================\n')

def func4(a, b, *c, **d):
    print(a, b)
    print(c)
    print(d)

func4(1, 2)
func4(1,2,3,4,5)
func4(1,2,3,4,5, kbs = 9, mbc = 11)

print('\n===================\n')

# type hint : 함수의 인자와 반환값에 type을 적어 가독성 향상

def typeFunc(num : int, data : list[str]) -> dict[str, int]:      # type hint > 무엇을 받을것인지 적어주는 것  // only 가독성 // 화살표는 반환값 얘기
    print(num)
    print(data)
    result = {}
    for idx, item in enumerate(data, start=1):          # 인덱스와 자료를 뽑아줌 // 인덱스 1부터 (초기값은 0)
        print(f'idx : {idx}, item : {item}')
        result[item] = idx
    return result

rdata = typeFunc(1.2, ['일','이','삼'])             # 구속력은 없다 >> 다른 type 줘도 된다
print(rdata)