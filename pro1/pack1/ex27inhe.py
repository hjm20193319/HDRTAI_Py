# 상속 : 자원의 재활용을 목적으로 특정 클래스의 멤버를 가져다 사용
# 코드 재사용
# 확장성 - 기존 클래스에 새 기능을 추가한 새로운 클래스 생성
# 구조적 설계 - 공통개념은 부모 클래스 / 구체적 내용은 자식 클래스
# 다형성 구사 - 메소드 오버라이딩

class Animal:       # 동물들이 가져야할 공통 속성과 행위 선언
    
    age = 1
    
    def __init__(self):
        print('Animal 생성자')
    
    def move(self):
        print('움직이는 생물')

class Dog(Animal):          # 상속 // 다중 상속도 가능하다
    def __init__(self):
        print('Dog 생성자')

    def my(self):
        print('댕댕이라고 해요')

dog1 = Dog()        # 인스턴스 변수
dog1.my()         # dog1 의 멤버는 my 밖에 없다(상속전)
dog1.move()       # 상속 후에는 Animal class의 move()도 사용 가능하다 > Dog에서 먼저 찾고 Animal로 간다
dog1.age        # 멤버필드도 사용 가능하다
print('age : ', dog1.age)       # 자기꺼인것 처럼 사용이 가능하다

# 자식 > local / 부모 > Global
print()
dog2 = Dog()
dog2.my()
dog2.move()
print()

class Horse(Animal):
    pass
horse1 = Horse()
horse1.move()


