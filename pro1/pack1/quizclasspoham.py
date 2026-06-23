# 커피 머신 코드 작성

# 잔돈 계산 클래스
class CoinIn:
    def __init__(self, coins, cups):       # coins: 투입 금액, cups: 입력 잔 수
        self.coins = coins
        self.cups = cups
        self.change = 0

    def culc(self, coins, cups):
        ACUP = 200
        self.coins = coins
        self.cups = cups
        self.price = ACUP * self.cups    # 주문한 커피의 가격
        if self.price > self.coins:     # 주문 불가
            print('Coins are return to you, Reorder please')
            return 0
        else:   
            self.change = self.coins - self.price
            return self.change          # 거스름돈 반환


class Machine:
    def __init__(self):
        self.cupCount = 1
        self.coins = 0
        self.cups = 0
        self.coinin = CoinIn(self.coins, self.cups)

    def orderFunc(self):
        self.coins = int(input('Insert coin : '))
        if self.coins < 200:
            print('More Money..!!')
            self.orderFunc()
        elif self.coins < 400:      # 무조건 한 잔
            self.showData(1, self.coinin.culc(self.coins, 1))
        else:
            self.cups = int(input('How many cups..? : '))       # 몇 잔 필요한지?
            self.showData(self.cups, self.coinin.culc(self.coins, self.cups))         # 계산 프로그램으로 정보 전달

    def showData(self, cup, change):
        self.cup = cup
        self.change = change
        if self.change > 0:
            print(f'Coffee : {self.cup}cup(s)& Change : {self.change} WON')
        else:
            Machine().orderFunc()
class Start:
    def __init__(self):
        self.startmach = Machine()
        

    def start(self):
        self.startmach.orderFunc()

if __name__ == '__main__':
    Start().start()
