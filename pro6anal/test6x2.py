# 이원 카이제곱 검정
# [개념] 동질성 검정(Test of Homogeneity): 서로 다른 모집단(집단)에서 추출한 표본들의 범주별 분포가 서로 동일한지 검정함.
# - 독립성 검정과 계산 방식은 동일하나, 연구 설계 단계에서 집단을 미리 나누어 놓았다는 점이 다름.

# 실습 1
# : 교육 방법에 따른 교육생들의 만족도 분석, 동질성 검정
# 독립변수 : 교육 방법 / 종속변수 : 만족도

#####################################
# 가설 수립
#####################################
# [개념] 동질성 검정의 가설
# 귀무가설: 모든 집단의 분포가 동일하다. (차이가 없다)
# 대립가설: 적어도 한 집단의 분포가 다른 집단과 다르다. (차이가 있다)

# 귀무 : 교육 방법에 따른 교육생들의 만족도에 차이가 없다.
# 대립 : 교육 방법에 따른 교육생들의 만족도에 차이가 있다.

import pandas as pd
import scipy.stats as stats

###########################################
# 데이터 수집 - 만족도에 대한 설문 수집 자료
###########################################
# [문법] pd.read_csv: 외부 URL의 CSV 데이터를 읽어와 데이터프레임 생성
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/survey_method.csv')
print(data.head())
print(data['method'].unique())  # 교육 방법 범주 확인: [1 2 3]
print(data['survey'].unique())  # 만족도 범주 확인: [1 2 3 4 5]
print('\n')

# [문법] pd.crosstab(index, columns): 두 범주형 변수의 빈도를 집계하여 교차표(Contingency Table) 생성
ctab = pd.crosstab(index=data['method'], columns=data['survey'])
ctab.index = ['방법1', '방법2', '방법3']
ctab.columns = ['매우만족', '만족', '보통', '불만족', '매우불만족']
print(ctab)     # 관측 빈도(Observed Frequency) 출력
print('\n')

# [추천] : 집단 간의 비율 차이를 시각적으로 확인하려면 ctab.div(ctab.sum(1), axis=0)를 사용하여 
# 행별 비율(백분율)로 변환한 뒤 누적 막대 그래프(Stacked Bar Chart)를 그리는 것이 좋습니다.

# [문법] stats.chi2_contingency(observed): 교차표를 입력받아 카이제곱 통계량, p-value, 자유도, 기대빈도를 반환
chi2, p, dof, expected = stats.chi2_contingency(ctab)
print(f'chi2 : {chi2}, p : {p}, dof : {dof}')
# chi2 : 6.544667820529891, p : 0.5864574374550608, dof : 8
# [개념] 자유도(dof): (행의 수 - 1) * (열의 수 - 1) = (3 - 1) * (5 - 1) = 8

print(f'기대도수 : \n', expected) # [수정] : '기대비율' 보다는 '기대도수(Expected Frequency)'가 통계학적으로 더 정확한 표현입니다.

# 판정
# 유의 수준 0.05 < p-value : 0.586457 이므로, 귀무 가설 채택. 우연히 발생한 자료라고 할 수 있다.
# 결론 : 교육 방법에 따른 교육생들의 만족도에 차이가 없다.

print('-----------------------------------------------------------------')
print('\n')
# 동질성 검정 실습2) 
# 연령대별 sns 이용률의 동질성 검정
# 20대에서 40대까지 연령대별로 서로 조금씩 그 특성이 다른 SNS 서비스들에 대해 
# 이용 현황을 조사한 자료를 바탕으로 연령대별로 홍보 전략을 세우고자 한다.
# 연령대별로 이용 현황이 서로 동일한지 검정해 보도록 하자.

# 귀무가설 : 연령대별 sns 서비스별 이용률 현황은 동일하다
# 대립가설 : 연령대별 sns 서비스별 이용률 현황은 동일하지 않다

####################
# 데이터 수집
####################
data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/snsbyage.csv')
print(data.head())

print(data['age'].unique())     # [1 2 3]
print(data['service'].unique())     # ['F' 'T' 'K' 'C' 'E']

ctab2 = pd.crosstab(index=data['age'], columns=data['service'])
ctab2.index = ['20대', '30대', '40대']
print(ctab2)

chi2, p, dof, expected = stats.chi2_contingency(ctab2)
print(f'chi2 : {chi2}, p : {p}, dof : {dof}')
# chi2 : 102.75202494484225, p : 1.1679064204212775e-18, dof : 8
print(f'expected : \n', expected)
print('전체 건수 : ', len(data))       # 1439

# 판정
# 유의 수준 0.05 > p-value : 0 이므로, 귀무 가설 기각
# 결론 : 연령대별 sns 서비스별 이용률 현황은 동일하지 않다.
print('-----------------------------------')
# [개념] 샘플링(Sampling): 모집단 전체를 조사하기 어려울 때, 통계적 추론을 위해 모집단의 일부를 추출하는 과정
# 여기서는 기존 데이터를 모집단으로 간주하고 500개의 표본을 무작위로 추출하여 검정의 일관성을 확인합니다.

# [문법] data.sample(n, replace, random_state): 
# n: 추출할 표본 개수, replace=True: 복원 추출(이미 뽑힌 데이터를 다시 뽑을 수 있음)
# random_state: 난수 시드 고정으로 실행 시마다 동일한 샘플이 나오도록 보장함
samp_data = data.sample(n=500, replace=True, random_state=1)
print(samp_data.head(), '\n', len(samp_data))
print('\n')

# [문법] pd.crosstab: 샘플링된 데이터를 바탕으로 연령대별 SNS 서비스 이용 빈도표 재구성
ctab_samp = pd.crosstab(index=samp_data['age'], columns=samp_data['service'])
ctab_samp.index = ['20대', '30대', '40대']
print(ctab_samp)
print('\n')

# [개념] 카이제곱 검정의 일관성: 표본의 크기가 충분하다면(n=500), 샘플링된 데이터에서도 모집단의 특성(연령대별 차이)이 유의미하게 나타나야 합니다.
chi2, p, dof, expected = stats.chi2_contingency(ctab_samp)
print(f'chi2 : {chi2}, p : {p}, dof : {dof}')
print(f'기대도수 : \n', expected)
print('전체 건수 : ', len(samp_data))

# 판정: 유의 수준 0.05 > p-value 이므로 귀무가설 기각. 샘플 데이터에서도 연령대별 SNS 이용 현황에 유의미한 차이가 있음이 확인됨.
# [추천] : sns.heatmap(ctab_samp, annot=True, fmt='d', cmap='YlGnBu')를 사용하여 샘플링된 데이터의 분포를 시각화하면 분석 결과의 설득력을 높일 수 있습니다.