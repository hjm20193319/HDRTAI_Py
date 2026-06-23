var1 = "안녕 파이썬"
print(var1)   #이건 주석
"""
여러 줄 
주석
이지롱
"""

# 변수 데이터 변경
var1 = 5;
var1 = 10
print(var1)

# 변수 데이터의 주소 불러오기
var1 = 5.6
print(var1)
var2=var1
print(var1, var2)
var3 = 7
print(var1, var2, var3)
print(id(var1), id(var2), id(var3))   # id는 데이터의 주소를 불러옴
'''
안녕 파이썬
10
5.6
5.6 5.6
5.6 5.6 7
1767903059184 1767903059184 140706191221864
'''

Var3 = 8
print(var3, Var3) # 대소문자를 구분한다

# 주소와 값을 비교 하기 
a = 5
b = a
c = 5
print(a, b, c)
print(a is b, a == b)    # is : 주소 비교 연산, == : 값 비교 연산
print(b is c, b == c)       # 둘다 true로 나옴
aa = [5]
bb = [5]              # 그룹 기억 장소, 요소가 여러개 들어갈 수 있다
print(aa, bb)         
print(aa is bb, aa == bb)       # 요소값이 하나일 경우엔 같은 주소이지만
                                  # 그룹형 기억장소는 값이 같아도 주소가 다르다
'''
5 5 5
True True
True True
[5] [5]
False True
'''

print('------')   # print("------") 랑 똑같음

# 키워드 목록 확인하기
import keyword    # 키워드 목록 확인용 모듈 읽기 , 자주 안쓰는 건 굳이 자동으로 부팅하지 않음
print('예약어 목록:', keyword.kwlist)
'''
예약어 목록: ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 
'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 
 'return', 'try', 'while', 'with', 'yield']
이미 기능이 있는 것들이니까 변수 이름으로 쓰지 않기
'''

# 자료형 type
kbs = 9
print('type(자료형) 확인')
print(isinstance(kbs, int))
print(isinstance(kbs, float))
print(5, type(5))     # 5 <class 'int'>  클래스는 객체
print(5.1, type(5.1))    #   5.1 <class 'float'>
print(3+4j, type(3+4j))     #(3+4j) <class 'complex'>
print(True, type(True))    #  True <class 'bool'>
print('good', type('good'))       #  good <class 'str'>
print((1,), type((1,)))     #   (1,) <class 'tuple'>
print([1], type([1]))      #   [1] <class 'list'>
print({1}, type({1}))      #   1} <class 'set'>
print({'k':1}, type({'k':1}))           #   {'k': 1} <class 'dict'>