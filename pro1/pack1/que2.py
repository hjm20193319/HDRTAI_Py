# 2 ~ 5 까지의 구구단 출력

# while 만 사용하기

i = 2
while i <= 5:
    print(f'<{i}단>')
    a = 1
    while a <= 9:
        print(f'{i} * {a} = {i * a}')
        a += 1
    i += 1

# 다른 사람 풀이
i=2
while i<=5:
    j=1
    while j<=9:
        print(f'{i} * {j} = {i*j}', end =' ')
        j+=1
    print()
    i+=1

