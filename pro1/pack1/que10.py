# 1부터 100까지 출력하되 4의 배수, 6의 배수는 건너뛴다. 그 외의 수 중 5의 배수만 출력하고 그들의 합도 출력하라

i = 1
tot = 0

while i <= 100:
    if i % 4 == 0:
        i += 1
        continue
    elif i % 6 == 0:
        i += 1
        continue
    elif i % 5 == 0:
        print(i)
        tot += i
        i += 1
        continue
    else:
        i += 1
        continue

        
print('총합은 : ', tot)

# 다른 사람 풀이
s = 0
for i in range(1,101):
    if i%4 == 0 or i%6 == 0:
        continue
    if i%5 == 0:
        print(i)
        s += i
print(s)

# 강사님 풀이
i = 1
total = 0

while i <= 100:
    if i % 4 == 0 or i % 6 == 0 or i % 5 != 0:
        i += 1
        continue
    print(i)
    total += i
    i += 1
    