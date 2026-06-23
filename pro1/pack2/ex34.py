# 파일 처리---읽기, 저장

import os

try:
    print(os.getcwd())      # getcwd -- 읽어오는                    # 상대적인 경로 써주는 법
    f1 = open(os.getcwd() + r'\ftext.txt', encoding='utf-8')        # utf-8 -> 전세계 언어를 읽어올 수 있는
    f2 = open('ftext.txt', mode = 'r', encoding='utf-8')          # 추천하는 방법    # mode = 'r' 은 생략 가능---'r', 'w', 'a', 'b' ----
    print(f1)
    print(f1.read())
    print(f2)
    print(f2.read())

    print('\n')

    # 파일 저장
    f3 = open('ftext2.txt', mode ='w', encoding='utf-8')         # open 먼저 해주고 마무리로 close 를 꼭 해줘야 함
    f3.write('내 친구들\n')
    f3.write('홍길동, 한국인')
    f3.close()
    print('파일 저장 성공')

    # 파일 내용 추가
    f4 = open('ftext2.txt', mode = 'a', encoding = 'utf-8')     # a > append
    f4.write('\n사오정')
    f4.write('\n저팔계')
    f4.write('\n손오공')
    f4.close()
    print('파일 추가 성공')

    f5 = open('ftext2.txt', mode = 'r', encoding='utf-8')
    print(f5.read())
    f5.close
    

except Exception as e:
    print('파일 처리 오류 : ', e)

# file작업 : 데이터베이스, 파일, 네트워크 처리할 때는 try Except는 꼭 써줄 것

print('\n====================\n')

