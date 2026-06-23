# 어딘가에서 필요한 부품 핸들 클래스 작성

class PohamHandle:
    quantity = ' '        # 핸들 회전량   >>   클래스 내 생성 될 객체들의 공유 자원__만약에 없었다면 각 객체들의 고유 자원이 되었을 것
    
    
    def leftTurn(self, quentity):
        self.quantity = quentity        # quentity는 지역 변수
        return '좌회전'
    
    def rightTurn(self, quentity):
        self.quantity = quentity
        return '우회전'
    