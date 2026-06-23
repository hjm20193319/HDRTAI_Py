# 예외처리 : 파일, 네트워크, DB작업, 실행에러 등의 에러 대처

def divide(a, b):
    return a / b

print('이런 저런 작업 진행...')
# c = divide(5, 2)      # 프로그램 정상 실행

# c = divide(5, 0)        # 에러 발생-->프로그램 강제 중단 및 종료
# print(c)

# 예외처리__되도록 적는 것이 좋음
try:
    #c = divide(5, 0)        # 실행문(예외 발생 가능 구문)
    #print(c)

    #aa = [1, 2]
    #print(aa[0])
    #print(aa[3])

    open('c:/work/abc.txt')

except ZeroDivisionError:       # 에러를 처리할 수 있는 예외 종류 관련 클래스
    print('두번째 값은 0을 주면 안됩니다 멍청아')       # 예외 발생 처리 구문

except IndexError as err:       # 별명 지정
    print('참조 범위 오류다 똥멍청아\n', err)     # 오류의 종류를 알고 싶을 때

except Exception as e:          # 에러 처리 클래스의 최상위 클래스 / 모든 에러를 처리 가능
    print('Error : ', e)

finally:            # 무조건 수행 에러 있든 없든
    print('에러 유무에 상관 없이 반드시 수행됨')

'''
Exception 클래스 사용해서 에러 전반적으로 처리하고 에러 종류 확인하기
'''
print('종료')

print('end')