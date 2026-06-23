# 연산자
v1 = 3      # 치환 연산자
v1 = v2 = v3 = 5
print(v1, v2, v3)
print('출력1', end = ',')    # 줄 바꿈 대신에 , 로 이어가기
print('출력2')
print('출력3')
'''
5 5 5
출력1,출력2
출력3
'''

v1, v2 = 10, 20
print(v1, v2)       # 데이터 개수가 맞을 때 제대로 출력해줌
'''
데이터를 바꿀때는 임시 저장소를 만들어서 비우고 채우고 바꿔주지만
'''

v2, v1 = v1, v2    # 파이썬은 이렇게 해주면 된다,,,,, 참조형이기 때문에 가능함
print(v1, v2)
print('값 할당 : packing 연산')
v1 = 1,2,3,4,5     # v1 = (1,2,3,4,5) 와 같은 말이다----기억장소가 하나이지만, 그룹을 할당한 것으로 생각하면 됨
v1 = [1,2,3,4,5]
#v1, v2 = [1,2,3,4,5]   error
*v1, v2 = [1,2,3,4,5]     # 제일 끝은 v2가 나머지는 v1이 가짐
print(v1, ' ', v2)          # v2* 는 에러

v1, *v2 = [1,2,3,4,5]
print(v1, ' ', v2)

*v1, v2, v3 = [1,2,3,4,5]     # *v1, *v2, v3 해주면 에러남
print(v1, ' ', v2, ' ', v3)
'''
[1, 2, 3, 4]   5
1   [2, 3, 4, 5]
[1, 2, 3]   4   5
'''

#  print() 함수
print()
print(format(1.5678, '10.3f'))    # 10자리 확보해서 소수점 3자리만출력, 4자리에서 반올림

print('나는 나이가 %d 이다.'%23)    # 문자열  숫자일 때는 %d 문자일때는 %s

print('나는 나이가 %s 이다.'%'스물셋')

print('나는 나이가 %d 이고 이름은 %s이다.'%(23, '홍길동'))

print('나는 나이가 %s 이고 이름은 %s이다.'%(23, '홍길동'))

print('나는 키가 %f이고, 에너지가 %d%%.'%(177.7, 100))   # %를 출력할땐 %%

print('이름은 {0}, 나이는 {1}'.format('한국인', 33))

print('이름은 {}, 나이는 {}'.format('신선해', 33))    # 대응순서임----입력안하면 알아서

print('이름은 {1}, 나이는 {0}'.format(34, '강나루'))    # 순서를 지정해서 들어감 0이 1보다 더 먼저 

abc = 123
print(f"abc의 값은 {abc}임")   # { } 사용하면 변수값이 들어감----제일 많이 쓰는 방법
'''
abc의 값은 123임
'''
# 웹이나 모바일에서 이쁘게 출력되도록 하면 됨, 여기서는 그냥 잘 나오는지 확인만 하면 된다


print('\n\n-------본격적 연산 ---------')  #\n, \b, \t ... \n는 라인 스킵, \b는 뒤로 \t는 탭
print(5 + 3, 5 - 3, 5 * 3, 5 / 3, 5 // 3, 5 % 3, 3 ** 3)
#  8 2 15 1.6666666666666667 1 2 27     /는 실수 나누기  //는 정수형 나누기(몫)   %는 나머지 나누기(나머지만 표시)

print(divmod(5, 3),' ', 5 % 3)   #divmod는 (몫, 나머지) 를 출력
resualt =  3 + 4 * 5 + (2 + 3) / 2
print(resualt)   
# () -> ** -> 단항 -> 산술연산(*,/,//,% -> +,-) -> 관계연산 -> 논리(not - > and -> or) -> 치환(=)


# 비교 연산자
print(5 > 3, 5 ==3, 5 != 3)

# 논리 연산자
print(5 > 3 and 4 < 3, 5 > 3 or 4 < 3, not(5 >=3))

print(True or False and False)
print(True and False or False)

#
print(4 + 5)   # 산술 연산
print('4' + '5')   # 문자열 더하기 연산
print('한' + '국' + '만세')
print('한국' * 5)
'''
한국만세
한국한국한국한국한국
'''

#누적
print('누적')
a = 10
a = a + 1
print(f'a는 {a}')

a += 1 # -= , *= , /= 도 있다 같은 누적 연산, 계산 속도가 위 방법보다 빠름
print(f'a는 {a}')
# print(a--)   # 파이썬은 증감 연산자 없음
print(--a)   # 이건 부호 변경임
print(-a)
print(a * -1)


#print(('1' + '1')+1)   # type error 
print(int('1'+'1')+1)   # int를 걸어주면 문자열이 정수가 됨
print(float('1'+'1')+1)   # 실수 처리
# print((1+1)+'1')   #type error
print(str(1+1)+'1')  # 숫자를 문자 처리 하는 것

print('boolean 처리 : ', bool(True), bool(False))   
print(bool(1), bool(12.3), bool('ok'), bool([12]))
print(bool(0), bool(0.0), bool(''), bool([]), bool(None))   # 데이터 값이 없으면 False
'''
boolean 처리 :  True False
True True True True
False False False False False
'''

# r 선행문자
print('aa\tbb')
print('aa\nbb')
print(r'aa\nbb')  # 순수 데이터로 인식한다
print(r'aa\tbb')
'''
aa      bb
aa
bb
aa\nbb
aa\tbb
'''