# with 구문 사용 - 내부적으로 close() 함
# 파일 저장은 이 방식대로 할 것

try:

    #파일 저장
    with open('ftext3.txt', mode = 'w', encoding='utf-8') as fobj1:
        fobj1.write('파이썬에서 문서 저장\n')
        fobj1.write('with구문은\n')
        fobj1.write('명시적으로 close() 할 필요가 없다\n')
    print('저장 완료\n')

    with open('ftext3.txt', mode = 'r', encoding='utf-8') as fobj2:
        print(fobj2.read())

except Exception as e:
    print('err : ',e)

print('\n===================\n')

# 피클링 (일반 객체 및 복합 개체 파일 처리)
import pickle

try:
    dictData = {'tom' :'111-1111', '길동':'222-2222'}
    listData = ['마우스', '키보드']
    tupleData = (dictData, listData)

    with open('hello.dat', mode = 'wb') as fobj3:      # 객체로 저장할 때는 txt 사용하지 않음,,,  wb : 이진 데이터로 저장
        pickle.dump(tupleData, fobj3)           # pickle.dump(대상, 파일 객체)  
        pickle.dump(listData, fobj3)        # 리스트 타입만 저장

    print('특정 객체를 파일로 저장')

    print('피클 객체 읽기')
    with open('hello.dat', mode = 'rb') as fobj4:
        a, b = pickle.load(fobj4)           # pickle.load(파일객체)
        print('a : ', a)
        print('b : ',b)
        c = pickle.load(fobj4)
        print('c : ',c)


except Exception as e:
    print('err : ', e)

