# 추상 클래스 (abstract class)
# 추상 메소드를 가진 클래스
# 이 놈은 인스턴스할 수 없음 > 객체 생성 불가
# 부모 클래스로만 사용 됨

# 다형성을 목적으로 오버라이딩을 강요하기 위해


from abc import *

class AbstractClass(metaclass=ABCMeta):  #추상클래스 ---> 일반 메소드도 가질 수 있다

    @abstractmethod             # 장식자를 걸어 줌 ---> 추상 메소드를 가지고 있으면 추상 클래스가 됨

    def abcMethod(self):     #추상메소드  ---> 자식 메소드들은 반드시 이 메소드를 만들어야 한다
                                # 추상 메소드는 내용을 적지 않는다
        pass

    def normalMethod(self):  #일반메소드  ---> 오버라이딩 선택적으로 해도 됨

        print('추상클래스 내의 일반 메소드')

# parent = AbstractClass()    #에러:추상클래스는 객체 생성 불가

class Child1(AbstractClass):        # 부모가 추상이면 자식도 자동으로 추상이 되고, 반드시 추상 메소드를 오버라이딩 해야한다
    name = '난 Child1'

    def abcMethod(self):            # 오버라이딩 하니까 객체가 생성이 가능하다
        print('부모의 abcMethod 재정의 : 강요 당함ㅠㅠ')

c1 = Child1()
print('name : ', c1.name)
c1.abcMethod()
c1.normalMethod()

class Child2((AbstractClass)):
    def abcMethod(self):
        print('추상 클래스 내의 abcMethod 재정의')

    def normalMethod(self):         # 일반 메소드 재정의__오버라이딩
        print('일반 메소드 내맘대로 변경')

print()

c2 = Child2()
c2.abcMethod()
c2.normalMethod()