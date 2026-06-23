# 기본 자료형 : int, float, bool, complex
# 묶음 자료형 : str, list, tuple, set, dict


# str : 문자열 묶음 자료형---순서가 있다!!!/ 수정은 불가능
s = 'sequence'
print(s)
print(s, id(s))     # s의 첫 글자 주소를 기억함
print('길이 : ',len(s))
print(s[0], s[2])    # 0번째 부터 시작
print('길이 : ', s.find('e'), s.find('e',3), s.rfind('e'))  # 문자열 관련 함수 / 해당 순서를 찾는 함수
'''
sequence
sequence 140705989360136
길이 :  8
s q
길이 :  1 4 7
'''

# 인덱싱 / 슬라이싱
print(s[5])   # 변수명[순서]  >>>  index라고 부름, 0부터 출발
print(s[2:5])    # 슬라이싱 (범위를 준다면)  2이상 5미만 까지(2,3,4번째)
print(s[:], ' ', s[0:len(s)], s[::1])   # 증가치 1
print(s[0:7:2])  # 증가치, 등차수열 2씩 증가
print(s[-1])   # 뒤에서 부터 찾는 것 뒤에부터 0번째인건 동일
print(s[-1], ' ', s[-4:-1:1])
print(s)
s = 'sequenc'    # 수정이 아니라 변경이다
print(s, id(s))
s = 'bequence'    # str type은 수정이 아니라, 주소가 바뀐 것으로 보아, 다른 값으로 대체하는 것이다
print(s, id(s))
'''
n
que
sequence   sequence sequence
sqec
e
e   enc
sequence
sequenc 2570023799952
bequence 2570023864112
'''


print('-----------'* 10)
# List : 다양한 종류의 자료 묶음형, 순서도 있고 수정도 가능하다, 중복도 가능하다
a = [1,2,3]
print(a,a[0],a[0:2])  # 순서이기 때문에 소수점 X
b = [10,a,10,20.5,True,'문자열']   #  리스트 안에 리스트 들어갈 수 있다 / bool도 들어가고 다 집어넣을 수 있다. 중복이 가능함
print(b)
print(b, ' ', b[1], ' ', b[1][0])   # b의 1번째의 0번째를 출력
'''
[1, 2, 3] 1 [1, 2]
[10, [1, 2, 3], 10, 20.5, True, '문자열']
[10, [1, 2, 3], 10, 20.5, True, '문자열']   [1, 2, 3]   1
'''

print('----------'*10)
family = ['엄마', '아빠', '나', '여동생']
print(id(family))
family.append('남동생')  # 추가 순서 유지
print(id(family))
family.remove('나')     # 삭제
family.insert(0,'할머니')   #  0번째에 삽입
family.extend(['삼촌','고모','조카'])      #  복수개를 추가
family += ['이모']    # 추가
print(family)
print(family.index('아빠'))        #순서
print('엄마' in family, '나' in family)    # 있으면 T, 없으면 F
'''
2570023194048
2570023194048
['할머니', '엄마', '아빠', '여동생', '남동생', '삼촌', '고모', '조카', '이모']
2
True False
'''

#family.remove(2)    #
family.remove('아빠')    # 값에 의한 삭제
del family[2]   # 순서에 의한 삭제,index
print(family)
'''
['할머니', '엄마', '남동생', '삼촌', '고모', '조카', ' 이모']
'''

print('========='*10)

kbs = ['123', '34', '234']
kbs.sort()    # 문자열 정렬
print(kbs)
'''
['123', '234', '34']
'''

mbc = ['123', '34', '234']
#mbc.sort()    # 숫자 정렬
mbc.sort(reverse=True)    # decending sort, 내림차순
print(mbc)
'''
['34', '234', '123']
'''

sbs = [123, 34, 234]
ytn = sorted(sbs)      # sort는 원본이 바뀜 / sorted는 원본 유지, 새로운 기억장소가 받아서 처리
print(sbs)
print(ytn)
print('========='*10)
'''
[123, 34, 234]
[34, 123, 234]
'''

name = ['tom', 'james', 'oscar']
name2 = name     #  주소를 치환한 것
print(name, id(name))
print(name2, id(name2))

import copy       # copy모듈을 불러옴
name3 = copy.deepcopy(name)    #  새로운 객체에 똑같은 데이터를 또 만듦
print(name3, id(name3))    # 그래서 주소가 다름

name[0] = '길동'
print(name)
print(name2)
print(name3)    # name3는 별도의 기억저장소에 저장했기 때문에 영향을 받지 않음

'''
['tom', 'james', 'oscar'] 1560192053312
['tom', 'james', 'oscar'] 1560192053312
['tom', 'james', 'oscar'] 1560192052992
['길동', 'james', 'oscar']
['길동', 'james', 'oscar']
['tom', 'james', 'oscar']
'''

print()

# tuple : 리스트와 유사 / 읽기 전용(수정 불가)
t = (1,2,3,4)
t = 1,2,3,4   # 위와 동일 ()사용하는 것 권장
print(t, type(t))
k = (1)           # tuple이 아니라 int임------
print(k, type(k))      
k = (1,)    # 이건 tuple 임
print(k, type(k))
print(t[0], ' ', t[0:2])
#  t[0] = 77    #type error >>>> 수정 불가이기 때문에  read only
imsi = list(t)     #type 을 바꿔서 변경하면 됨
imsi[0] = 77     # tuple 이 검색 속도가 빠르다
t = tuple(imsi)
print(t)
print()


# set : 순서 없음, 중복 불가능   >>> 중복 데이터를 없앨 때 사용하기 좋음
ss = {1,2,1,3}
print(ss)
ss2 = {3,4}
print(ss.union(ss2))  #합집합
print(ss.intersection(ss2))   # 교집합
print(ss - ss2, ss| ss2, ss&ss2)     # 차집합, 합집합, 교집합
# print(ss[0])  # typeerror  >>>> 순서가 없기 때문에 인덱싱 슬라이싱 불가능
ss.update({6,7})   # 수정은 가능하다
print(ss)
ss.discard(7)    # 값 삭제
ss.discard(7)     #  해당 값 없으면 그냥 넘어감
ss.remove(6)     # 값 삭제
# ss.remove(6)     # 해당 값 없으면 에러
print(ss)


li = ['aa', 'aa', 'bb', 'cc', 'aa']
print(li)
imsi = set(li)    # 중복을 피하고 싶을 때 / 순서가 없어서 순서는 랜덤..?
li = list(imsi)
print(li)
print('\n==================\n\n')

# dict : 사전 자료형 {'키' : 값}  형태
# 방법 1
mydic = dict(k1 = 1, k2 = 'ok', k3 = 123.4)
print(mydic, type(mydic))

# 방법2
dic = {'파이썬':'뱀', '자바':'커피', '인사':'안녕'}
print(dic)    # 입력 순서를 유지함 / 원래는 순서가 없어서 
print(len(dic['자바']))   # 키를 가지고 값을 찾는 것 (순서를 찾는 것 아님)

ff = dic.get('자바')     # 검색하는 다른 방법
print(ff)


# print(dic['커피'])   # 커피라는 키가 없기 때문에
# print(dic[0])    # 인덱싱 불가능, 슬라이싱 불가능
dic['금요일'] = '와우'     # 순서가 없기 때문에 추가 보다는 데이터 추가
print(dic)
del dic['인사']    # 지우기
print(dic)
print(dic.keys())    
print(dic.values())