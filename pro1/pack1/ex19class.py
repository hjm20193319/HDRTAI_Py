# oop : 객체 중심(지향) 프로그래밍 가능 - 새로운 타입 생성, 포함, 상속, 다형성 등을 구사
# Class (설계도)로 인스턴스 해서 객체를 생성 (별도의 이름 공간을 갖음)
# 객체는 멤버필드(멤버변수)와 메소드로 구성
# 접근 지정자가 없다. 메소드 오버로딩 없음
# 모듈의 멤버 : 변수, 명령문, 함수, 모듈, 클래스

print('뭔가를 하다가 객체 만들기...\n')

class TestClass:
    aa = 1      # 멤버필드(변수) : 현재 클래스 내에서 전역(global var in this class)

    def __init__(self):   # __init__ : 생성자    / 특별한 메소드  
        print('생성자')           # 초기화 작업이 필요할때 작성, 없어도 상관 없음 > 인터프리터가 만들어 줌

    def __del__(self):              # 콜백 메소드
        print('소멸자')  # 응용 프로그램이 종료되면 자동으로 찍힘, 없어도 에러 안남, 안쓰면 인터프리터가 자동으로 작성해줌

    def printMsg(self):         # 일반 메소드 (일반 함수와 구분하기 위해서 메소드라 부름)
        name = '한국인'         # 반드시 argument가 있어야 한다 > 그게 바로 self 다     # 지역 변수(printMsg 에서만 유효)
        print(name)
# 윗 줄까지는 선언만 한 상태
print(TestClass)        # <class '__main__.TestClass'>  type 자체가 TestClass type 이다

# 객체 생성
test = TestClass()        # TestClass type의 객체를 생성했고, 그 주소를 test가 가지고 있다  ///  객체변수
'''
생성자 : 객체 생성 시 가장 먼저 1회만 호출 - 초기화 담당
소멸자 : 프로그램 종료 시 자동 실행, 마무리 작업
'''
print('test 객체의 멤버 aa : ', test.aa)        # 클래스 내의 멤버를 부르는 방법

# method call
test.printMsg()         # 1. Bound Method call : Auto argument(앞의 객체변수를 입력한 것으로 간주) >> 더 자주 씀
TestClass.printMsg(test)        # 2. UnBound Method call : 객체 변수를 넣어줘야 함 test가 주소를 들고 간다
print(type(1))          # <class 'int'>
print(type(1.0))        # <class 'float'>
print(type(test))       # <class '__main__.TestClass'>    # test가 객체 변수 이기 때문에
print(id(test))         # 1832914219568
print(id(TestClass))    # 1832917410960

#객체를 한 개 더 생성 
test2 = TestClass()
print(id(test2))