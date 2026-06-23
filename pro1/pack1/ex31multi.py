# 클래스의 다중 상속
# : 부모가 복수 

class Tiger:                # Super Class
    data = 'Tiger World'

    def cry(self):
        print('Tiger : grrr')

    def eat(self):
        print('Meat Lover')


class Lion:                 # Super Class
    def cry(self):
        print('Lion errrr')

    def hobby(self):
        print('Sleep... Lazy..')


class Liger1(Tiger, Lion):      # 다중 상속은 순서가 중요!!!
    pass

a1 = Liger1()
print(a1.data)

a1.eat()
a1.hobby()
a1.cry()        # 누구의 것을 가져오는지
# Tiger : grrr 가 출력 ----> 먼저 적은것이 우선순위

print('\n===============\n')

def hobby():
    print('Member of Module, general Func')

class Liger2(Lion, Tiger):
    data = 'Liger Mansea'

    def play(self):
        print('Liger own Method')

    def hobby(self):        # 메소드 오버라이드
        print('Liger likes walk at the park')

    def showData(self):
        self.hobby()  # Liger2
        super().hobby()  # Lion
        hobby()         # Module

        self.eat()      # Liger2 ---> X ----> Lion ----> X -----> Tiger
        super().eat()   # Lion
        
        print(self.data + ' ' + super().data)

a2 = Liger2()
a2.cry()       # Lion cry()
a2.showData()