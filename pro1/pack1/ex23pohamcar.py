# 여러 개의 부품 객체를 조립해 완성차 생성
# 클래스의 포함 관계 사용    (자원의 재활용) - 객체 중심 프로그램의 핵심
# 다른 클래스를 마치 자신의 멤버처럼 선언하고 사용

from ex23pohamhandle import PohamHandle

class PohamCar:
    turnShowMessage = '정지'

    def __init__(self, ownerName):
        self.ownerName = ownerName
        self.handle = PohamHandle()         # 클래스의 포함관계!!!!!!

    def turnHandle(self, q):            # q가 양수이면 우회전 음수이면 좌회전
        if q > 0:
            self.turnShowMessage = self.handle.rightTurn(q)         # rightTurn 은 PohamHandle의 멤버 > 그걸 handle에 주소 저장했기 때문
        elif q < 0:
            self.turnShowMessage = self.handle.leftTurn(q)
        elif q ==  0:
            self.turnShowMessage = '직진'

if __name__ == '__main__':                  # 가독성을 위해서 작성하는 것이 좋음
    tom = PohamCar('Mr.Tom')
    tom.turnHandle(10)
    print(tom.ownerName + ' 의 회전량은 ' + tom.turnShowMessage + ' ' + str(tom.handle.quantity))

    john = PohamCar('Mr.John')
    john.turnHandle(-20)
    print(john.ownerName + ' 의 회전량은 ' + john.turnShowMessage + ' ' + str(john.handle.quantity))