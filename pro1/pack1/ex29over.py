# 메소드 오버라이딩 ( 재정의 )
# 부모에서 정의된 메소드를 자식이 동일명의 메소드로 내용만 변경해 사용
# 부모 메소드의 기능을 대체하는 새로운 기능
# 목적 : 동작의 구체화 (공통틀은 부모가 / 실제 행동은 자식이)
# polymorphism (다형성) : 같은 메소드이나 객체에 따라 다른 기능을 수행
# 확장, 유지보수에 도움 - 부모 코드는 유지한 채로 자식 코드만 변경

class Parent:
    def printData(self):        
        pass                        # 비워두면, 자식들이 오버라이딩해서 사용하겠다는 뜻_ _ _ 메소드의 이름은 이걸 참고해서 만들면 좋겠다...

class Child1(Parent):
    def abc():
        print('Child1 고유 메소드')

    def printData(self):                    # 메소드 오버라이딩
        a = 5 + 6
        print('Child1 에서 printData 재정의')       

class Child2(Parent):
    def printData(self):                        # 메소드 오버라이딩
        print('Child2 에서 printData override')     
        msg = '부모와 동일 메소드명이나 내용은 다르다'
        print(msg)

# Parent 는 부모로서만 의미가 있음 (현 코드에서)
c1 = Child1()
c1.printData()
print()
c2 = Child2()
c2.printData()

print('\n============\n다형성\n============')
# 다형성을 하는 추천하는 방법
par = Parent()
par = c1
par.printData()
print()
par = c2
par.printData()     # 위와 똑같은 문장이지만 출력 내용은 다르다 >> 다형성(다양한 결과)
print('--------')
# 또 다른 방법
imsi = c1
imsi.printData()
imsi = c2
imsi.printData()            # 같은 방법이지만 다형성을 나타내는 가독성을 위해서 위의 방식 추천
