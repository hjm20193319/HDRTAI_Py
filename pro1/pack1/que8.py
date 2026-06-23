# 1 ~ 1000 사이의 소수(1보다 크며 1과 자신의 수 이외에는 나눌 수 없는 수)와 그 갯수를 출력

print('1~1000사이 소수는')
i = 1
num = 0

while i <= 1000:
    if i == 1:
        i += 1
        continue
    elif i ==2:
        print(i)
        i += 1
        num += 1
        continue
    else:
        ii = 2
        while ii < i:
            if i % ii == 0:
                break
            else:
                if ii == i - 1:
                    print(i)
                    num += 1
                ii += 1
                continue
    
    i += 1
print('이고')
print('총 개수는 : ', num)

# 다른 사람 풀이
count = 0
for i in range(2,1001):
    flag = 0
    for j in range(2,i-1):
        if i%j == 0:
            flag = 1
            break
    if flag == 0:
        print(i)
        count += 1
print(count)

# 강사님 풀이
num = 2
count = 0

while num <= 1000:
    i = 2
    is_prime = True
    while i < num:
        if num % i == 0:
            is_prime = False
            break
        i += 1
    if is_prime:
        print(num, end = ' ')
        count += 1
    num += 1
print('개수 : ', count)