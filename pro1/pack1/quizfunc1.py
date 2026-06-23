# 함수 문제 1번

def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas


years=[]
pluswages = []
finalwages = []

def processfunc(a):
    print('사번  이름  기본급  근무년수  근속수당  공제액    수령액')
    print('---------------------------------------------------------')
    for i in [0,1,2]:
        yeardiff = 2026 - a[i][3]       # 고정된 상수 값을 적을 때는 대문자로 적어준다
        years.append(yeardiff)          # datetime.now().year  >> 현재 연도를 알 수 있다
        if years[i] <= 3:
            pluswage = 150000
        elif years[i] <= 8:
            pluswage = 450000
        else:
            pluswage = 1000000

        pluswages.append(pluswage)
        firstwage = a[i][2] + pluswage

        if firstwage < 2000000:
            minuswage = firstwage * 0.15
        elif firstwage < 3000000:
            minuswage = firstwage * 0.3
        else:
            minuswage = firstwage * 0.5

        finalwage = firstwage - minuswage
        finalwages.append(int(finalwage))

        print(f'{a[i][0]}    {a[i][1]}  {a[i][2]}  {years[i]}     {pluswages[i]:>8} {int(minuswage):>8}    {finalwages[i]:>8}')
    print(f'처리건수 : {len(a)} 건')


    
    

        
    








processfunc(inputfunc())