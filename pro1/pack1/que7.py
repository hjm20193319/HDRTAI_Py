# 구구단을 출력하되 결과가 30을 넘으면 해당 단 중단하고 다음 단으로 이동

for i in list(range(2,10)):
    print(f'<{i}단>')
    for ii in list(range(1,10)):
        result = i * ii
        while result <= 30:
            print(f'{i} * {ii} = {i * ii}')
            break

# 다른 사람 풀이=========for 문 사용해서 풀이
for i in range(1,10):
    for j in range(1,10):
        if i*j > 30:
            break
        print(f"{i}X{j}={i*j}")

# 강사님 풀이  
dan = 2
while dan <= 9:
    i = 1
    while i <= 9:
        result = dan * i
        if result > 30:
            break
        print(dan, "*", i, '=', result)
        i += 1
    print()
    dan += 1