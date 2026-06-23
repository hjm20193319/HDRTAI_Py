n, m = map(int, (input('팜플렛 가로 X 세로 : ').split()))
a, b = map(int,(input('부스 소개 가로 X 세로 : ').split()))
while True:
    if a < 0 or a >= n or b < 0 or b >= m:
        print(f'가로의 길이는 0보다 크고 {n}보다 작아야 합니다')
        print(f'세로의 길이는 0보다 크고 {m}보다 작아야 합니다')

        a, b = map(int,(input('부스 소개 가로 X 세로 : ').split()))
        continue
    else:
        break

c, d = map(int, (input('일정표 가로 X 세로 : ').split()))
while True:
    if c < 0 or c >= n or d < 0 or d >= m:
        print(f'가로의 길이는 0보다 크고 {n}보다 작아야 합니다')
        print(f'세로의 길이는 0보다 크고 {m}보다 작아야 합니다')

        a, b = map(int,(input('부스 소개 가로 X 세로 : ').split()))
        continue
    else:
        break


