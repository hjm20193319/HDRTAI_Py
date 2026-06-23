# 1 ~ 100 사이의 정수 중 3의 배수이나 2의 배수가 아닌 수를 출력하고, 
# 합을 출력

a = 1
tot = 0

while a <= 100:
    if a % 3 == 0 and a % 2 != 0:
        print(a, end = ' ')
        tot += a
    a += 1
print()
print('tot : ', tot)

# 다른 사람 풀이
'''
i=0
sum=0               # sum 은 키워드 이기 때문에 사용 안하는 것이 좋다
while i<100:
    i+=1
    if i%2==0:continue
    if i%3==0:continue
    print(i)
    sum=sum+i

else:
    print(sum)
'''

# 강사님 풀이
i = 0
total = 0

while i <= 100:
    if i % 3 == 0 and i % 2 != 0:
        print(i, end = ' ')
        total += i
    i += 1

print(f'합은 {total}')