# 우편 정보 파일 자료 읽기
# 키보드에서 입력한 동 이름으로 해당 주소 정보 출력

def zipProcess():
    dongIrum = input('동이름 입력 : ')
    
    # print(dongIrum)
    with open(r'zipcode.txt', mode = 'r', encoding='euc-kr') as f:  # utf-8 아니면   euc-kr      
        line = f.readline()     # 한 행 읽기
        # print(line)   #  135-806 서울    강남구  개포1동 경남아파트 -> 하나의 문자열__개포1동을 뽑아내고 싶음 --> 잘라내야 함

        # lines = line.split('\t')    # 구분자 tab키
        # lines = line.split(chr(9))  # chr(tab에 해당하는 ascii 코드)  위에랑 같은 말
        # print(lines)        # 띄어쓰기를 기준으로 문자열을 자름
        while line:
            lines = line.split(chr(9)) 
            if lines[3].startswith(dongIrum):       # 이 글자로 시작되는
                # print(lines)
                print('우:' + lines[0] + ', ' + lines[1] + ' ' + lines[2] + ' ' + lines[3])

                
            line = f.readline()



if __name__ == '__main__':
    zipProcess()