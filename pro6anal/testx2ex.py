import pandas as pd
import scipy.stats as stats

# 실습 1
# 카이제곱 문제1) 부모학력 수준이 자녀의 진학여부와 관련이 있는가?를 가설검정하시오

#   예제파일 : cleanDescriptive.csv

#   칼럼 중 level - 부모의 학력수준, pass - 자녀의 대학 진학여부

#   조건 :  level, pass에 대해 NA가 있는 행은 제외한다.

data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/cleanDescriptive.csv')
print(data.head())

# 귀무 : 부모학력 수준이 자녀의 진학여부와 관련이 없다
# 대립 : 부모학력 수준이 자녀의 진학여부와 관련이 있다

# [추천] : df = data[['level', 'pass']].dropna() 처럼 한 줄로 필터링과 결측치 제거를 동시에 할 수 있습니다.
df = pd.DataFrame(data=data[['level', 'pass']])
print(df)

df = df.dropna()
print(df)

# [추천] : pd.crosstab(data['level'], data['pass'])를 사용하면 별도의 DataFrame 복사본(df)을 만들지 않고도 바로 교차표 생성이 가능합니다.
df = pd.crosstab(index=df['level'], columns=df['pass'])
print(df)

chi2, p, dof, expected = stats.chi2_contingency(df)
print(f'chi2 : {chi2}, p : {p}, dof : {dof}')
print(f'기대도수 : \n', expected)

# 판정
# 유의 수준 0.05 < p-value : 0.2507 이므로, 대립 가설 기각, 귀무 가설 채택
# 결론 : 부모학력 수준이 자녀의 진학여부와 관련이 없다.


# 실습 2
# 카이제곱 문제2) 지금껏 A회사의 직급과 연봉은 관련이 없다. 

# 그렇다면 jikwon_jik과 jikwon_pay 간의 관련성 여부를 통계적으로 가설검정하시오.

#   예제파일 : MariaDB의 jikwon table 

#   jikwon_jik   (이사:1, 부장:2, 과장:3, 대리:4, 사원:5)

#   jikwon_pay (1000 ~2999 :1, 3000 ~4999 :2, 5000 ~6999 :3, 7000 ~ :4)

#   조건 : NA가 있는 행은 제외한다.

# 귀무 : A 회사의 직급과 연봉은 관련이 없다
# 대립 : A 회사의 직급과 연봉은 관련이 있다

import MySQLdb
import pickle

with open('mydb.dat', mode = 'rb') as obj:         
    config = pickle.load(obj)

conn = MySQLdb.connect(**config)         
cursor = conn.cursor()

sql = '''
    select jikwonjik, jikwonpay
    from jikwon
'''
df_A = pd.read_sql(sql, conn)
print(df_A)

df_A = df_A.dropna()

print(df_A['jikwonjik'].unique())   # ['이사' '부장' '과장' '대리' '사원']

# [추천] : 반복문(for)을 사용하는 것보다 pandas의 pd.cut()을 사용하면 구간 분할을 훨씬 효율적으로 처리할 수 있습니다.
# bins = [1000, 3000, 5000, 7000, 100000]
# labels = [1, 2, 3, 4]
# df_A['jikwonpay'] = pd.cut(df_A['jikwonpay'], bins=bins, labels=labels, right=False)

for i in range(len(df_A)):
    if df_A['jikwonpay'][i] <= 2999:
        df_A['jikwonpay'][i] = 1
    elif df_A['jikwonpay'][i] <= 4999:
        df_A['jikwonpay'][i] = 2
    elif df_A['jikwonpay'][i] <= 6999:
        df_A['jikwonpay'][i] = 3
    else:
        df_A['jikwonpay'][i] = 4

print(df_A)

df_A = pd.crosstab(index=df_A['jikwonjik'], columns=df_A['jikwonpay'])
print(df_A)

chi2, p, dof, expected = stats.chi2_contingency(df_A)
print(f'chi2 : {chi2}, p : {p}, dof : {dof}')
print(f'기대도수 : \n', expected)

# 판정
# 유의 수준 0.05 > p-value : 0.00019211 이므로, 귀무 가설 기각
# 결론 : A 회사의 직급과 연봉은 관련이 있다.