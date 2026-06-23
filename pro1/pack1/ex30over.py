# 오버라이딩 : 결제 시스템

class Payment:  # 공통 규칙 선언
    def pay(self, amount):
        print(f'{amount}원 결제 처리')

# Payment의 자식은 결제를 pay()라는 동일 메소드를 이용하기를 기대
# 동일 인터페이스 구사

class CardPayment(Payment):
    # CardPayment 만의 고유멤버....
    # 고유 메소드....있다고 가정 

    def pay(self, amount):              # 메소드 오버라이딩
        print(f'{amount}원 카드 결제 승인 완료함')


class CashClass(Payment):
    # ...

    def pay(self, amount):              # 메소드 오버라이딩
        print(f'{amount}원 현금 결제 완료 - 감사합니다')

# 이름은 pay() 똑같지만, 각 클래스에서 내용 재정의 > 결과 다르게 처리 위해서

payments = [CardPayment(), CashClass()]     # 각 클래스의 객체를 리스트로 만듦

for p in payments:
    p.pay(5000)         # 다형성

'''
5000원 카드 결제 승인 완료함
5000원 현금 결제 완료 - 감사합니다
'''

