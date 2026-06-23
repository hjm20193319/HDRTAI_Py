# for 반복문 

for i in [1,2,3,4,5]:      # 묶음형 자료형(list, tuple, set, dict---모두 사용 가능하다)
    print(i, end = ' ')        # 묶음형 자료형을 하나씩 i 에 넘겨짐/자료가 없으면 탈출

print('\nend')             # dict는 성격이 약간 다르다

print('\n================\n')

print('<분산, 표준편차 구하기>')       # 평균, 분산--- 데이터에서 매우 중요
'''
편차 = 변수 - 평균
분산 = 편차 제곱의 합 
표준 편차 = 제곱근 분산
'''
numbers = [3,4,5,6,7]
tot = 0
for a in numbers:
    tot += a
print(f'합은 {tot}, 평균은 {tot / len(numbers)}')      # 합과 평균
avg = tot / len(numbers)
hap = 0
for i in numbers:
    hap += (i - avg) ** 2
print(f'편차 제곱의 합 {hap}')     # 편차제곱의 합
vari = hap / len(numbers)
print(f'분산은 {vari}')             # 분산
print(f'표준편차는 {vari ** 0.5}')             # 표준편차 

print('end')

print('\n=======================\n')
colors = ['r', 'g', 'b']          # set 자료형은 순서대로 안찍힐수도 있다(순서가 없기 때문)
for v in colors:
    print(v, end = ' ')

print('\nend')

print('\n==============\n')

# iter 함수 
print('iter() : 반복 가능한 객체를 하나씩 꺼낼 수 있는 상태로 만들어 주는 함수')
iterator = iter(colors)
for v in iterator:
    print(v, end = ', ')

print()

# enumerate 함수
for idx, d in enumerate(colors):        # 인덱스와 값을 반환해준다
    print(idx, ' ', d)


print('\n=========\n')

# 사전형
print('<사전형 알아보기>')
datas = {'python':'만능언어', 'java':'웹용언어', 'mariadb':'RDBMS'}
for i in datas.items():         # 튜플 타입으로 반환
    # print(i)
    print(i[0], ' ~~ ', i[1])

for k, v in datas.items():     # 데이터를 따로 받아줌
    print(k, '--', v)

for k in datas.keys():          # key만 따로
    print(k, end = ' ')
print()

for v in datas.values():        # value 만 따로
    print(v, end = ' ')

print('end')

print('\n====================\n')

# 다중 for문
print('<다중 for>')
for n in [2,3]:
    print('--{}단--'.format(n))            # print 또다른 방법
    for i in [1,2,3,4,5,6,7,8,9]:
        print('{} * {} = {}'.format(n, i, n * i))

print('end')

print('\n====================\n')

print('continue, break')
nums = [1,2,3,4,5]
for i in nums:
    if i == 2: continue
    if i == 4: break
    print(i, end = ' ')
else:
    print('정상종료')

print('end')

print('\n============\n')

print('<정규 표현식 + for>')
str = '''
옛날 옛적에, 호기심 많은 작은 여우가 숲속을 탐험하고 있었습니다.
어느 날, 반짝이는 별이 나무 사이로 떨어지는 것을 발견했어요. 별
은 마법의 씨앗이었고, 여우는 그것을 심기로 결심했죠.skrrr
며칠 후, 그 자리에는 하늘까지 닿는 아름다운 나무가 자라났습니다. 
나무 꼭대기에는 모든 소원을 이뤄주는 황금 열매가 열렸고, 
여우는 숲의 친구들과 함께 행복한 삶을 살게 되었답니다.
'''
import re           # 정규표현식 모듈
str2 = re.sub(r'[^가-힣\s].,','', str)    # 한글과 공백 이외의 문자는 공백처리
print(str2)
str3 = str2.split(' ')         # 공백을 기준으로 문자열 분리
print(str3)
cou = {}              #set 아니면 dict
for i in str3:
    if i in cou:
        cou[i] += 1            # 같은 단어 있으면 누적
    else:
        cou[i] = 1            # 최초 단어인 경우는 "단어 : 1"
print(cou)

print('-----------')

for test_ss in ['111-1234', '일이삼-일이삼사', '222-1234', '333&1234']:
    if re.match(r'^\d{3}-\d{4}$', test_ss):      # ( )안에 ^ 는 처음, $는 마지막을 나타냄 >> 이문자로 시작해서 이문자로 끝나는
        print(test_ss, ' : 전화번호 맞아요')
    else:
        print(test_ss, ' : 전화번호 아니야')

print('end')

print('\n===================\n')

print('<comprehension : 반복문 + 조건문 + 값 생성을 한 줄로 표현>\n')
a = [1,2,3,4,5,6,7,8,9,10]
li = []
for i in a:
    if i % 2 == 0:
        li.append(i)
print(li)
print(list(i for i in a if i % 2 == 0))              # 위와 같은 결과

datas = [1, 2, 'a', True, 3.0]             # datas = {1, 2, 'a', True, 3.0, 1, 2, 1, 2, 1}   해줘도 결과는 같음 : 중복을 배제하기 때문에
li2 = [i * i for i in datas if type(i) == int]       # 정수만 찾아서 거듭제곱 해줌
print(li2)

id_name = {1: 'tom', 2: 'oscar'}
print(id_name)
name_id = {val:key for key, val in id_name.items()}      # 서로 위치를 바꿔줌
print(name_id)
print()

print([1,2,3])
print(*[1,2,3])        # * : unpack 기능   리스트를 풀어줌
aa = [(1, 2), (3, 4), (5, 6)]        # aa가 튜플임
for a, b in aa:
    print(a + b)
# print([a + b for a, b in aa])
print(*[a + b for a, b in aa], sep = '\n')      # unpack 하고 다음 줄로 내림 

print('end')

print('\n======================\n')

print('<수열 생성 : range>')
print(list(range(1, 6)))             # 이상~~미만, 증가치 1(생략 가능), 반환 타임 리스트
print(tuple(range(1, 6, 2)))         # 증가치 2
print(list(range(-10, -100, -20)))
print(set(range(1, 6)))               # type 걸어줘야 함

for i in range(6):                 # 초기값을 안주면 0부터 : 0부터 6미만까지
    print(i, end = ' ')
print()
for _ in range(6):
    print('반복')

tot = 0
for i in range(1, 11):      # 1부터 10 까지 
    tot += i
print('tot : ', tot)
print('tot : ', sum(range(1, 11)))       # 내장함수 sum 사용---같은 결과

for i in range(1, 10):
    print(f'2 * {i} = {2 * i}')

print('\nend')

print('\n=====================\n')

# 문제1 : 2~9 단 구구단 출력 단은 행 단위 출력
for i in range(2,10):
    print(f'<{i}단>')
    for ii in range(1,10):
        print(f'{i} * {ii} = {i * ii}  ', end = ' ')
    print()
print('end')

# 문제2 : 주사위를 두 번 던져서 나온 숫자들의 합이 4의 배수가 되는 경우만 출력

print('\n=======================\n')

print('주사위 눈의 합이 4의 배수인 경우\n')
d1 = list(range(1,7))          
d2 = list(range(1,7))
for i in d1:
    for ii in d2:
        if (i + ii ) % 4 == 0:
            print(f'({i}, {ii})')
print('end')

print('\n===============================\n')

