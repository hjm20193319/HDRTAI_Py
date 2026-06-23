# 1부터 50까지의 숫자 중 3의 배수는 건너뛰고 나머지 수만 출력하라

i = 1

while i <= 50:
    if i % 3 == 0:
        i += 1
        continue
    else:
        print(i, end = ' ')
        i += 1

# 다른 사람 풀이======for문을 이용한
for i in range(1,51):
    if i%3 == 0:
        continue
    print(i)

# 강사님 풀이
i = 1
while i <= 50:
    if i % 3 == 0:
        i += 1
        continue
    print(i, end = ' ')
    i += 1