# 클래스 상속 - 다형성 문제

class ElecProduct:
    volume = 0

    def volumeControl(self, volume):
        print('Every Elecproduct First Vol : ', volume)
    


class ElecTv(ElecProduct):
    def volumeControl(self, volume):
        print('TV - Now Vol : ',volume)
        vTv = int(input('Enter Vol : '))
        print(f'Tv Vol Now : {vTv}...')

class ElecRadio(ElecProduct):
    def volumeControl(self, volume):
        print('Radio - Now Vol : ',volume)

elec = ElecProduct()

voltv = ElecTv()
volrd = ElecRadio()

voltv.volumeControl(0)
volrd.volumeControl(0)