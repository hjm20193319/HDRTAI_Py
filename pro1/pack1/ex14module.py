# Module : 소스 코드의 재사용을 가능하게 하며, 소스 코드를 하나의 이름공간으로 구분하고 관리
# 하나의 파일은 하나의 모듈이 된다
# 표준 모듈, 사용자 작성 모듈, 제 3자 모듈(third party)로 구분

# third party module --> site-packages 에 저장 // conda install or pip install

print(print.__module__)         #  print는 builtins 모듈 안에 들어있음 
# 자주 쓰이는 모듈은 이미 import가 되어 있는 상태 

print('\n뭔가를 하다가...외부 모듈 사용하기\n')

import sys          # 표준 모듈이지만 쓰임새 적음 --> import 시켜주면 됨
print(sys.path)     # 모듈명.멤버   sys.py 안에 path 가 있음
a = 2              # 휘발성 메모리, 프로그램이 끝나면 사라짐
if a > 3:
    sys.exit()          # 프로그램 강제 종료(종료 점) , ( )있으니까 실행하는 종류

import math
print(math.pi)

import calendar
calendar.setfirstweekday(6)
calendar.prmonth(2026,2)
del calendar            # 안쓰면 다시 지워줌/이후에 다시 calendar 하면 error

import random       # "C:\Users\hjm20\anaconda3\Lib\random.py"
print(random.random())          # 0 ~ 1 사이의 실수값
print(random.randrange(1, 10))      # 1 ~ 10 사이의 정수값
from random import random, choice, randrange       # from 모듈명 import 멤버 하면 멤버만 바로 사용할 수 있다
from random import *                # 추천 X 메모리 관리에 안좋음
print(random())







print('\nend')





