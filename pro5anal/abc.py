# 통계량 : 데이터의 특징을 하나의 숫자로 요약한 것
# 표본 데이터를 추출해 전체(모집단) 데이터를 짐작 가능
# 평균, 분산, 표준편차 ....

grades = [1, 3, -2, 4]      # 변량

def show_grades(grades):
    for g in grades:
        print(g, end = ' ')

show_grades(grades)

print()

# ======================================
# 직접 계산
# ======================================
def grades_sum(grades):
    tot = 0
    for g in grades:
        tot += g
    return tot

print('합은 ', grades_sum(grades))

# 평균
def grades_avg(grades):
    tot = grades_sum(grades)
    avg = tot / len(grades)
    return avg

print('평균은 ', grades_avg(grades))

# 분산 (편차 제곱의 평균) : 평균값 기준으로 다른 값 들의 흩어진 정도
def grades_var(grades):
    avg = grades_avg(grades)
    sum_of_squared_diffs = 0
    for g in grades:
        sum_of_squared_diffs += (g - avg)**2
    var = sum_of_squared_diffs / len(grades)    # 파이썬은 전체로 나눔
    # var = sum_of_squared_diffs / (len(grades) - 1)    R에서는 전체 -1 로 나눔
    return var

print('분산은 ', grades_var(grades))

# 표준편차 : 분산의 제곱근
def grades_std(grades):
    return grades_var(grades)**0.5

print('표준편차는 ', grades_std(grades))

# ==================================
# numpy 사용
# ==================================
print('\n넘파이 지원 함수 사용')
import numpy
print('합은 ', numpy.sum(grades))      # 합계
print('평균은 ', numpy.mean(grades))    # 평균
print('분산은 ', numpy.var(grades))     # 분산
print('표준편차는 ', numpy.std(grades))  # 표준편차