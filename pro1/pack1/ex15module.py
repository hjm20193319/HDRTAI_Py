# pack1/ex15module - main

# 사용자 정의 모듈 처리하기

print('=========================')

s = 20  # 뭔가를 하다가...
print('\n경로 지정 방법1 : import 모듈명\n')

import pack1.mymod1           # 같은 패키지에 있어도 import 해줘야 한다
print(dir(pack1.mymod1))      # 멤버들이 출력 됨 : python이 만들어주는 기본 + 내가 만든 멤버
# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
#  '__name__', '__package__', '__spec__', 'kbs', 'listHap', 'mbc', 'tot']
print(pack1.mymod1.__file__)
print(pack1.mymod1.__name__)
print()

list1 = [1, 2]
list2 = [3, 4, 5]
pack1.mymod1.listHap(list1, list2)        # 외부 모듈의 멤버를 사용함
print()

if __name__ == '__main__': print('나는 메인 모듈')          # python ~~~.py 해서 실행하는 모듈이 메인이다

print('\n경로 지정 방법2 : fron 모듈명 import 함수명(메소드) 또는 변수\n')

from pack1.mymod1 import kbs
kbs()           # ctrl + space bar 로 멤버 확인?

from pack1.mymod1 import mbc, tot
mbc()
print(tot)

from pack1.mymod1 import *       # * 을 사용해서 mymod1의 모든 멤버 로딩
print('tot : ', tot)

from pack1.mymod1 import mbc as 엠비씨만세별명        # 멤버의 이름을 가독성 좋게 별명을 설정
엠비씨만세별명()

print('\n경로 지정 방법3 : import 하위패키지.모듈명\n')

import pack1.subpack.sbs
pack1.subpack.sbs.sbsManse()
import pack1.subpack.sbs as nickname
nickname.sbsManse()

print('\n경로 지정 방법4 : 현재 package와 동등한 다른 패키지 모듈 읽기')

# import../pack1_other.mym0d2
from pack1_other import mymod2
mymod2.hapFunc(4, 3)        # 실행이 안됨 > 상위 단계로 나가야 함
# (myproject) C:\work\projects\pro1>python -m pack1.ex15module--->확장자 없이 모듈명만
# 경로에서 상위로 나갔기 때문에 pack1 인지 pack1_other인지 구분 해줘야 함

print()
import mymod3
result = mymod3.hapFunc2(4, 3)
print('path가 설정된 곳의 module 읽기 - result : ', result)
