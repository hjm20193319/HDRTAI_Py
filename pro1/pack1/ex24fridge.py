# 클래스의 포함 관계 연습 - 냉장고 객체에 음식 객체 담기

class Fridge:
    isopened = False            # 냉장고 문 개폐 여부 확인 변수
    foods = []                  # 음식을 저장할 리스트 

    def open(self):
        self.isopened = True
        print('Open fridge door')

    def close(self):
        self.isopened = False
        print('close fridge door')

    def foodsList(self):            # 냉장고 문이 열린 경우 음식물 확인
        for f in self.foods:
            print(f' - {f.name} {f.expiry_date}')
        print()

    def put(self, thing):
        if self.isopened:
            self.foods.append(thing)
            print(f'put {thing.name} in the fridge')
            self.foodsList()
        else:
            print('Door is closed')


class FoodData:
    def __init__(self, name, expiry_date):
        self.name = name
        self.expiry_date = expiry_date


fObj = Fridge()

apple = FoodData('apple', '2026-08-01')
fObj.put(apple)
fObj.open()
fObj.put(apple)
fObj.close()
print()
cola = FoodData('coke', '2027-11-01')
fObj.open()
fObj.put(cola)
fObj.close()