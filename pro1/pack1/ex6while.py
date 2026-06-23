# while 반복문
'''
a = 1
while a <= 5:     # 참이면 수행, 거짓이면 탈출
    print(a)
print('end')     # 무한루프(계속 참이어서)  ,ctrl c 누르면 강제 종료
'''
print('--------'*10)

a = 1      # 초기값을 반드시 줘야 함
while a <= 5:
    print(a, end = ' ')
    a = a + 1      # 변수 값에 변화(거짓으로 만드는)를 주면 된다
else:
    print('수행성공')
print('end')

print('\n===============\n')

# 중첩 while
i = 1
while i <= 3:
    j = 1
    while j <= 4:
        print('i=' + str(i) + '/j=' + str(j))     # 문자열 더하기 // 문자형 변화 후 더하기
        j = j + 1
    i = i + 1
print('end')

print('\n===============\n')

print('1~100 사이의 정수 중 3의 배수의 합')
su = 1; hap = 0   # 두개를 한줄에 ;-------------------초기 변수를 어디에 써주는지도 중요함
while su <= 100:
    # print(su)
    if su % 3 == 0:
    # print(su)
        hap += su    # hap = hap + su   누적 더하기 방법
    su += 1    
print('합은 ',hap)

print('end')

print('\n============\n')

colors = ["빨강", "파랑", "노랑"]
'''
num = 0              이런 방법은 생산성이 떨어짐--요소의 개수가 늘어날수록
print(colors[num])
print(colors[1])
print(colors[2])
'''
num = 0
# while num < 3:
while num < len(colors):    # 요소의 개수가 아무리 늘어나도 상관이 없도록 함
    print(colors[num])          # 요소 개수가 많을 때 방법!!
    num += 1

print('end')

print('\n=============\n')

# 다중 while
print('\n------별찍기-------')          
i = 1   
while i <= 10:          # while 안에 while
    j = 1
    msg = ''
    while j <= i:     # 바깥쪽 변수가 참여하고 있음
        msg  += "*"
        j += 1
    print(msg)
    i += 1

print('end')

print('\n==============\n')
'''
print('if 블럭 내 while 블럭 사용')
import time
sw = input('폭탄 스위치를 누를까요?[n/y]')      # input 입력값은 모두 문자형
# print('sw : ', sw)
if sw == 'Y' or sw == 'y':
    count = 5
    while 1 <= count:
        print('%d초 남았습니다' %count)    # %d 에 해당되는 데이터 맵핑
        time.sleep(1)         # 1초 후 다음 문장 실행하는 함수, delay
        count -= 1
    print('폭발')
elif sw == 'N' or sw == 'n':
    print('작업취소')
else:
    print('y 또는 n 을 누르세요')
print('end')
'''
print('\n====================\n')

print('continue, break')
a = 0
while a < 10:
    a += 1
    if a == 3:
        continue    # 아래 문을 무시하고 while로 이동
    if a == 5:
        continue
    if a == 7:
        break        # while 문 무조건 탈출 (비정상 종료, 조건에 의한 종료가 아님)
    print(a)
else:
    print('정상 종료')
print ('while 수행 후 a 값은 :  %d'%a)

print('end')

# 무한 루프 만들기 / break 만나기 전까지 계속 수행
print('\n===============\n')
print('키보드로 숫자를 입력받아 홀수 짝수 확인하기(무한 반복)')
while True:           # True, 1, 100, -12, 4.5, 'ok' --- 등과 같이 데이터가 있으면 모두 참
    mysu = int(input('확인할 숫자 입력(예:5) : '))          # 키보드로 입력하기 위한 함수 input()
    if mysu == 0:
        print('프로그램 종료')
        break
    elif mysu % 2 == 0:
        print('%d는 짝수'%mysu)
    elif mysu % 2 == 1:
        print('%d는 홀수'%mysu)
        
print('end')