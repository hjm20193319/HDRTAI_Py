# 문제 2  /// 데이터 나누는 것이 중요

# 데이터 입력 함수
def inputfunc():
    datas = [
        "새우깡,15",
        "감자깡,20",
        "양파깡,10",
        "새우깡,30",
        "감자깡,25",
        "양파깡,40",
        "새우깡,40",
        "감자깡,10",
        "양파깡,35",
        "새우깡,50",
        "감자깡,60",
        "양파깡,20",
    ]
    return datas

def outputFunc(data):            # inputfunc의 datas 값을 받음
    print('상품명 수량 단가 금액')
    print('---------------------')
    data = str(data)            # list 를 문자열로 변환

    import re                   # 추출을 위해 모듈 선언
    num = re.findall(r'\d+', data)      # 수량 추출(숫자를 기준으로)
    snack = re.findall(r'[가-힣]+', data)    # 과자 이름 추출(한글을 기준으로)

    numsh = 0                   # 새우깡 수량의 초기값
    numpo = 0                   # 감자깡 수량의 초기값
    numon = 0                   # 양파깡 수량의 초기값
    totprices = []              # 소계를 계산하기 위한 리스트 초기값

    for i in range(0,len(snack)):       # data를 과자 종류 별로 구분하기 위한 for문
        if snack[i] == '새우깡':
            price = 450
            numsh += int(num[i])        # 과자 별로 수량을 누적해준다(소계)
        elif snack[i] == '감자깡':
            price = 300
            numpo += int(num[i])
        else:
            price = 350
            numon += int(num[i])
        totprice = int(num[i]) * price      # 각 과자의 금액을 구하기 위해

        print(f'{snack[i]:<4} {num[i]:<3} {price:<4} {totprice:<5}')   # 리스트 출력
        
        totprices.append(totprice)          # 소계를 구하기 위한 리스트에 요소 추가
    
    totnum = [numsh, numpo, numon]          # 소계를 작성하기 위해 각 과자별 누적 수량 리스트 



# 소계와 총계 출력을 위한 최종본 함수
    def total(a, b, c):        # a = snack  b = totnum   c = totprices
        totpsh = 0             # 각 과자의 소계액 초기값 지정
        totppo = 0
        totpon = 0
        for i in range(0,len(snack)):
            if a[i] == '새우깡':    # 각 과자별로 소계액 누적
                totpsh += c[i]
            elif a[i] == '감자깡':
                totppo += c[i]
            else:
                totpon += c[i]

        print()
        print('소계')
        print(f'새우깡 : {b[0]}건  소계액 : {totpsh}원')
        print(f'감자깡 : {b[1]}건  소계액 : {totppo}원')
        print(f'양파깡 : {b[2]}건  소계액 : {totpon}원')
        print()
        print('총계')
        print(f'총 건수 : {sum(b)}')
        print(f'총 액 : {sum(c)}원')

    total(snack, totnum, totprices)         # 소계 총계를 위한 함수 호출


outputFunc(inputfunc())


# dict type으로 만들어서 진행해도 좋은 것 같음
# 누적용 리스트도 dict type으로 만들어서