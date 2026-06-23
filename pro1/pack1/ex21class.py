# class 추가 설명 // 실제로는 같은 이름 사용하지 말 것

kor = 100       # 모듈의 전역 변수

def abc():
    kor = 0         # 함수 내의 지역 변수
    print('모듈의 멤버 함수')

class My:
    
    kor = 80            # My 멤버 변수(필드)
    
    def abc(self):
        print('My 멤버 메소드')

    def show(self):
        # kor = 77        # show 메소드 안에 있는 지역 변수
        print(kor)          # 지역 변수가 없으면 클래스가 아니라 모듈의 멤버로 넘어 감 >> 100 이 찍힘
        print(self.kor)         # 80이 찍힘
        self.abc()              # 클래스 내의 abc 메소드로 감 > self. 있으니까
        abc()                   # 모듈 내의 abc 함수로 감

my = My()
my.show()   

print('\n==============\n')

print(My.kor)
tom = My()          # tom 이라는 새로운 객체 생성 ---> My class type
print(tom.kor)
tom.kor = 88        # 자기꺼만 해당 됨
print(tom.kor)

oscar = My()        # tom 과는 다른  객체   ----> My class type
print(oscar.kor)