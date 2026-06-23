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