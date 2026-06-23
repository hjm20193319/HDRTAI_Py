# lotto

import random

class LottoBall:
    def __init__(self, num):
        self.num = num

class LottoMachine:
    def __init__(self):
        self.ballList = []      # set 으로 주게 되면 순서가 없다            # ballList에 볼이 45개가 만들어짐
        for i in range(1, 46):
            self.ballList.append(LottoBall(i))      # 포함 관계  45개의 객체가 포함관계로 들어감

    def selectBalls(self):
        random.shuffle(self.ballList)       # 번호 섞기 랜덤하게
        
        #for a in range(6):                  # 6개 번호 추출
        #    print(self.ballList[a].num, end = ' ')
        
        return self.ballList[0:6]           # 슬라이싱해서 6개만 리턴

class LottoUI:
    def __init__(self):
        self.machine = LottoMachine()           # 포함 관계

    def playLotto(self):
        input('Press Enter key to start Lotto')
        selectedBalls = self.machine.selectBalls()
        for ball in selectedBalls:
            print('%d'%(ball.num))


if __name__ == '__main__':
   # machine = LottoMachine()
   # print(machine.selectBalls())

    #lot = LottoUI()
    #lot.playLotto()

    LottoUI().playLotto()       # 굳이 객체 변수를 안만들고 해도 된다