# 1부터 시작해서 누적합이 처음으로 1000을 넘는 순간의 숫자와 그때의 합을 출력

i = 1
sum = 0
while True:
    sum += i
    if sum <= 1000:
        i += 1
    else:
        print('순간의 숫자 : ', i)
        print('누적 합 : ', sum)
        break

# 다른 사람 풀이
s = 0
i = 1
while s < 1000:
    s += i
    i += 1
print(i-1)
print(s)

