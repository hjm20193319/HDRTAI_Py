# 1 ~ 100 사이의 숫자 중 각 자리 수의 합이 10 이상인 수만 출력

i = 1
sip = (i // 10) + (i % 10)
beak = (i // 100) + ((i - 100) // 10) + (i % 10)
while i <= 100:
    if i < 100:
        if sip >= 10:
            print(f'{i} : {sip}')
    else:
        if beak >= 10:
            print(f'{i} : {beak}')
    i += 1

# 다른 사람 풀이
'''
i=10
while i<=100:
    str_i=str(i)  # 숫자를 문자로 처리
    hap=sum((int(str_i[0]),int(str_i[1])))       # 자릿수를 분리해서 다시 정수처리해서 더해 줌
    if hap>=10:
        print(f'{str_i}일 때 {hap}')
    i+=1

# 강사님 풀이

num = 1
while num <= 100:
    temp = num
    digit_sum = 0       # 자릿수의 합
    
    while temp > 0:
        digit_sum += temp % 10     # 일의 자리 숫자를 더해줌
        temp //= 10         # 정수 나누기 할당자  temp = temp // 10========십의 자리 숫자를 만들어 주고 while문을 통해 더해줌
    if digit_sum >= 10:     # 10이 넘어가면 출력
        print(num, end = ' ')

    num += 1
    '''