# 모듈의 멤버로 나올 수 있는 클래스

class Car:      # 클래스 이름은 대문자로 시작하기로 약속
    handle = 1
    speed = 0

    def __init__(self, name, speed):
        self.name = name                # 현재 객체의 name에게 name(지역변수) 인자값 치환
        self.speed = speed

    def showData(self):
        km = ' 킬로미터'
        msg = '속도 : ' + str(self.speed) + km 
        return msg
    
    def printHandle(self):
        return self.handle                  # 인수가 self 이기 때문에 local의 handle을 먼저 찾고 없으니까 원형의(class)의 handle을 반환해주는 것 > 다이렉트로 가는 것이 아니다
    
print(Car.handle)       # 원형 클래스(prototype)의 멤버 호출
car1 = Car('tom', 10)          # 생성자 호출 후 객체 생성 >> 인스턴스화 했다  ,,,, self는 자동입력
print('car1 객체의 주소 : ',id(car1))
print('car1 : ', car1.name, car1.speed, car1.handle)            # car1 에서 참조한 것 
car1.color = '파랑'                                 # car1 에 color라는 고유 멤버를 추가한 것
print('car1.color : ', car1.color)

car2 = Car('john', 20)          # 생성자 호출 후 다른 객체 생성
print('car2 객체의 주소 : ', id(car2))
print('car2 : ', car2.name, car2.speed, car2.handle)        # car2에서 참조한 것

# print(Car.color, ' ', car2.color)               # 멤버를 찾을 수 없는 에러 // color는 car1 에서만 생성했기 때문에

print(Car, car1, car2)
print(id(Car), id(car1), id(car2))          # 모두 서로 다른 객체들
print(car1.__dict__, car2.__dict__)         # 각각의 멤버를 확인할 수 있는

print('\n========================\n')

print('<메소드>')

print('car1 speed : ', car1.showData())         # showData 를 실행해야하기 때문에 () 붙여 줘야 함
print('car2 speed : ', car2.showData())         # 실제로는 showData(car2) 객체의 주소가 인수로 들어가지만, 인터프리터가 알아서 입력해주는 것이다

print('car1 handle : ', car1.printHandle())
print('car2 handle : ', car2.printHandle())         # handle 이 출력되는 경로 잘 확인하기