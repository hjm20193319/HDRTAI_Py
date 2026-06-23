from abc import*

class Employee(metaclass=ABCMeta):

    def __init__(self, irum, nai):
        self.irum = irum
        self.nai = nai
    
    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def data_print(self):
        pass

    def irumnai_print(self):
        print('이름 : ' + self.irum + ', 나이 : ' + str(self.nai), end = ' ')


class Temporary(Employee):

    def __init__(self, irum, nai, ilsu, ildang):
        self.irum = irum
        self.nai = nai
        self.ilsu = ilsu
        self.ildang = ildang

    def pay(self):      # 월급 용으로 오버라이딩
        self.handal = self.ilsu * self.ildang
        return self.handal
    
    def data_print(self):       # 월급 데이터 출력, 이름나이에서 받아옴
        self.pay()
        self.irumnai_print()
        print(', 월급 : ' + str(self.handal))

class Regular(Employee):

    def __init__(self, irum, nai, salary):
        self.irum = irum
        self.nai = nai
        self.salary = salary

    def pay(self):      # 급여용으로 오버라이딩
        return self.salary
    
    def data_print(self):       # 급여 데이터 출력, 이름나이에서 받아옴
        self.pay()
        self.irumnai_print()
        print(', 급여 : ' + str(self.salary))

class Salesman(Regular):

    def __init__(self, irum, nai, salary, sales, commission):
        self.irum = irum
        self.nai = nai
        self.salary = salary
        self.sales = sales
        self.commission = commission

    def pay(self):      # 수령액용으로 오버라이딩
        self.get = int(self.salary + self.sales * self.commission)
        return self.get
    
    def data_print(self):       # 수령액 데이터 출력, 이름나이에서 받아옴
        self.pay()
        self.irumnai_print()
        print(', 수령액 : ' + str(self.get))

t = Temporary('홍길동', 25, 20, 15000)
t.data_print()
        
r = Regular('한국인', 27, 3500000)
r.data_print()

s = Salesman('손오공', 29, 1200000, 5000000, 0.25)
s.data_print()