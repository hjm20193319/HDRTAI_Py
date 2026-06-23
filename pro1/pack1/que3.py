# 1 ~ 100 사이의 정수 중 “짝수는 더하고,
# 홀수는 빼서” 최종 결과 출력

# while만 사용하기
i = 1
tot = 0
while i <= 100:
    if i % 2 == 0:
        ii = i
    else:
        ii = -i
    tot += ii
    i += 1
print(tot)


# 다른 사람 풀이
i = 1
sum = 0
while i <= 100:
    if i%2==0:
        sum=sum+i
    else:
        sum=sum-i
    i+=1
print(f'최종결과 = {sum}')