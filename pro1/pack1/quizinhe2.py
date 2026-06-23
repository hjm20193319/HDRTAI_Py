# 다중 상속 문제

class Animal:       # Super class
    animal = '동물'

    def moveF(self):
        print('이 녀석은 동물')

    def move(self, notice):
        self.notice = notice
        print(f'Notice : "이 동물은 { self.notice } 과 입니다"')









class Dog(Animal):
    name = '개'

    def move(self, notice):
        self.notice = notice

        print(f'Notice : "{self.name}은 { self.notice } 과 입니다"')






class Cat(Animal):
    name = '고양이'

    def move(self, notice):
        self.notice = notice

        print(f'Notice : "{self.name}은 { self.notice } 과 입니다"')





class Wolf(Dog, Cat):
    def wwwolf(self):
        return 0






class Fox(Cat, Dog):
    name = 'fox'

    def foxMethod(self):
        print('Fox,,,ning....')

    def move(self, notice):
        self.notice = notice
        print(f'Notice : "여우는 { self.notice } 과가 아니라 개과 입니다"')


ani = Animal()
dog = Dog()
cat = Cat()
wolf = Wolf()
fox = Fox()

ani.moveF()
ani.move('---')
print()
dog.move('강아지')
dog.moveF()
print()
cat.move('야옹이')
cat.moveF()
print()
wolf.moveF()
print(wolf.name)
print(wolf.animal)
print()
fox.move(cat.name)
fox.foxMethod()
fox.moveF()
print(fox.name)
print(fox.animal)