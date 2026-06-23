# 상속

class Person:
    say = "I'm human~~"         # 접근 권한 : public
    nai = '20'
    __msg = 'good'   #  __ 를 이름 앞에 붙이면 다른 클래스에선 사용할 수 없다
    def __init__(self, nai):
        print('Person 생성자')
        self.nai = nai

    def printInfo(self):
        print(f'나이 : {self.nai}, 이야기 : {self.say}')

    def helloMethod(self):
        print('hello : ', self.say, self.nai, self.__msg)

print(Person.say, Person.nai)
# Person.printInfo()

per = Person('25')
per.printInfo()
per.helloMethod()

print('=============')

class Employee(Person):
    subject = '근로자'
    say = '일하는 동물'         # hiding(shadowing) > 부모가 가지고 있는걸 자식이 선언하면 자식은 자식것을 사용 > 부모의 변수를 숨기는 듯한

    def __init__(self):
        print('Employee 생성자')

    def printInfo(self):
        print(f'Employee 클래스의 printInfo 호출됨')        # 부모의 메소드 가져왔지만, 부모 메소드는 숨김 >> 지역이 우선이니까

    def ePrintInfo(self):
        print(self.subject, self.say, self.nai)         # 현재 클래스에서 찾다가 부모로 올라가는 것 >> Local 우선이다
        # print(self.__msg)      >> private member >> Person에서만 유효하다
        self.helloMethod()
        self.printInfo()    # self 때문에 일하는 동물이  출력 됨
        print(super().say)          # self가 아니고 super(). 때문에 바로 부모의 say를 가져옴, 멤버필드, 메소드 모두 해당 >> 바로 위의 클래스 탐색
        super().printInfo()

emp = Employee()
print(emp.subject, emp.nai, emp.say)
emp.ePrintInfo()

print('\n========================\n')

class Worker(Person):       # Employee랑 둘 다 Person 의 자식이지만, 다른 클래스 서로 가져다 주지 못함
    def __init__(self, nai):
        print('Worker 생성자')
        super().__init__(nai)   # 부모 클래스의 생성자 호출 , 요구하는 argument도 넣어줌

    def wPrintInfo(self):
        print('Worker - wPrintinfo 처리')
        # self.printInfo()      # 어차피 없으니까 현재 클래스에서 찾지 말고
        super().printInfo()     # 바로 부모 클래스에서 탐색하기

pro = Worker('30')
print(pro.say, pro.nai)
pro.wPrintInfo()

print('\n====================\n')

class Programmer(Worker):
    def __init__(self, nai):
        print('Programmer 생성자')
        # super().__init__(nai) # bound call
        Worker.__init__(self, nai)  # unbound call

    def pPrintInfo(self):
        print('Programmer - pPrintInfo 처리')

    def wPrintInfo(self):       # 부모 메소드와 동일 메소드 선언 >> 상속에서만 나오는 개념
        print('Programmer에서 overriding')

pro = Programmer(35)
print(pro.say, pro.nai)
pro.pPrintInfo()
pro.wPrintInfo()

print('\n===============\n')
print('타입확인')
a = 3; print(type(a))
print(type(pro))  # >>  Programmer class type
print(Person.__bases__)  # object /  제일 최상위 >. 모든 클래스는 object의 자식
print(Employee.__bases__)       # 부모를 확인하고 싶을 때
print(Worker.__bases__)
print(Programmer.__bases__)
