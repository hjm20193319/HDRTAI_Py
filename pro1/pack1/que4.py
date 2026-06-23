# -1, 3, -5, 7, -9, 11 ~ 99 까지의 모두에 대한 합을 출력

a = list(range(1,100,2))

i = 0
while i < len(a):
    if i % 2 == 0:
        a[i] = -a[i]
    else:
        a[i] = a[i]
    i += 1

print(sum(a))


# 다른 사람 풀이

i = -1
sum = 0
while abs(i)<=99:
    sum=sum+i
    if i<0:
        i-=2
    else:
        i+=2
    i*=-1
print(sum)
    
# 강사님 풀이
